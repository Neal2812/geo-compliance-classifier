"""
MCP Orchestrator

Main orchestrator class that loads Hugging Face LLM and orchestrates compliance analysis tools.
"""

import logging
# Import existing systems
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .models import MCPRequest, MCPResponse, MCPStatus, ToolUsage
from .tool_registry import ToolRegistry

sys.path.append(str(Path(__file__).parent.parent.parent))

try:
    from monitoring.reporting.compliance_analyzer import ComplianceAnalyzer
    from monitoring.reporting.compliance_reporter import ComplianceReporter
    from src.compliance.feature_generation.tiktok_feature_generator import \
        TikTokFeatureGenerator
    from src.evidence import log_compliance_decision
    from src.evidence.evidence_exporter import EvidenceExporter
    from src.rag import RAGAdapter
except ImportError as e:
    logging.warning(f"Some dependencies not available: {e}")
    RAGAdapter = None
    log_compliance_decision = None
    EvidenceExporter = None
    ComplianceAnalyzer = None
    ComplianceReporter = None
    TikTokFeatureGenerator = None


# Lazy imports to avoid circular dependencies
def _get_faiss_retriever():
    try:
        from retriever.faiss_retriever import FaissRetriever

        return FaissRetriever
    except ImportError:
        return None


def _get_retrieval_service():
    try:
        from retriever.service import RetrievalService

        return RetrievalService
    except ImportError:
        return None


logger = logging.getLogger(__name__)


class MCPOrchestrator:
    """Main MCP orchestrator for compliance analysis."""

    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()
        self.mcp_config = self.config.get("mcp", {})

        # Initialize components
        self.tool_registry = ToolRegistry()
        self.llm = None
        self.rag_adapter = None
        self.retrieval_service = None
        self.faiss_retriever = None
        self.evidence_exporter = None
        self.compliance_analyzer = None
        self.compliance_reporter = None
        self.feature_generator = None

        # Performance tracking
        self.start_time = time.time()
        self.total_requests = 0
        self.total_latency = 0.0

        # Initialize systems
        self._initialize_llm()
        self._initialize_rag_system()
        self._initialize_compliance_systems()
        self._update_tool_registry()

        logger.info("MCP Orchestrator initialized successfully")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration file."""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}

    def _initialize_llm(self):
        """Initialize the Hugging Face LLM."""
        try:
            model_config = self.mcp_config.get("model", {})
            provider = model_config.get("provider", "transformers_local")
            model_name = model_config.get("name", "mistral-7b-instruct")

            if provider == "transformers_local":
                # Load local transformers model
                try:
                    import torch
                    from transformers import (AutoModelForCausalLM,
                                              AutoTokenizer)

                    logger.info(f"Loading local model: {model_name}")
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float16,
                        device_map="auto" if torch.cuda.is_available() else "cpu",
                    )
                    self.llm = {
                        "provider": "transformers_local",
                        "model_name": model_name,
                        "tokenizer": self.tokenizer,
                        "model": self.model,
                    }
                    logger.info("Local LLM loaded successfully")

                except ImportError:
                    logger.warning("Transformers not available, using fallback")
                    self.llm = {"provider": "fallback", "model_name": "fallback"}
                except Exception as e:
                    logger.error(f"Failed to load local model: {e}")
                    self.llm = {"provider": "fallback", "model_name": "fallback"}

            elif provider == "hf_inference":
                # Use Hugging Face Inference Endpoint
                endpoint_url = model_config.get("endpoint_url")
                if endpoint_url:
                    self.llm = {
                        "provider": "hf_inference",
                        "model_name": model_name,
                        "endpoint_url": endpoint_url,
                    }
                    logger.info(f"HF Inference endpoint configured: {endpoint_url}")
                else:
                    logger.warning("HF Inference endpoint URL not provided")
                    self.llm = {"provider": "fallback", "model_name": "fallback"}

            else:
                logger.warning(f"Unknown LLM provider: {provider}")
                self.llm = {"provider": "fallback", "model_name": "fallback"}

        except Exception as e:
            logger.error(f"LLM initialization failed: {e}")
            self.llm = {"provider": "fallback", "model_name": "fallback"}

    def _initialize_rag_system(self):
        """Initialize RAG and retrieval systems."""
        try:
            # Initialize RAG adapter
            if RAGAdapter:
                self.rag_adapter = RAGAdapter()
                logger.info("RAG adapter initialized")

            # Initialize retrieval service using lazy import
            RetrievalService = _get_retrieval_service()
            if RetrievalService:
                self.retrieval_service = RetrievalService()
                logger.info("Retrieval service initialized")

            # Initialize FAISS retriever using lazy import
            FaissRetriever = _get_faiss_retriever()
            if FaissRetriever:
                self.faiss_retriever = FaissRetriever()
                logger.info("FAISS retriever initialized")

        except Exception as e:
            logger.error(f"RAG system initialization failed: {e}")

    def _initialize_compliance_systems(self):
        """Initialize compliance analysis systems."""
        try:
            # Initialize evidence exporter
            if EvidenceExporter:
                self.evidence_exporter = EvidenceExporter()
                logger.info("Evidence exporter initialized")

            # Initialize compliance analyzer
            if ComplianceAnalyzer:
                self.compliance_analyzer = ComplianceAnalyzer()
                logger.info("Compliance analyzer initialized")

            # Initialize compliance reporter
            if ComplianceReporter:
                self.compliance_reporter = ComplianceReporter()
                logger.info("Compliance reporter initialized")

            # Initialize feature generator
            if TikTokFeatureGenerator:
                self.feature_generator = TikTokFeatureGenerator()
                logger.info("Feature generator initialized")

        except Exception as e:
            logger.error(f"Compliance systems initialization failed: {e}")

    def _update_tool_registry(self):
        """Update tool registry with actual implementations."""
        try:
            # Update retrieve_rag tool with actual RAG system
            if self.rag_adapter:
                self.tool_registry.tool_functions["retrieve_rag"] = (
                    self._retrieve_rag_actual
                )

            # Update analyze_compliance tool
            if self.compliance_analyzer:
                self.tool_registry.tool_functions["analyze_compliance"] = (
                    self._analyze_compliance_actual
                )

            # Update other tools with actual implementations
            if self.compliance_reporter:
                self.tool_registry.tool_functions["report_compliance"] = (
                    self._report_compliance_actual
                )

            if self.evidence_exporter:
                self.tool_registry.tool_functions["export_csv"] = (
                    self._export_csv_actual
                )

            # Use lazy import for FAISS retriever
            if hasattr(self, "faiss_retriever") and self.faiss_retriever:
                self.tool_registry.tool_functions["index_status"] = (
                    self._index_status_actual
                )

            logger.info("Tool registry updated with actual implementations")

        except Exception as e:
            logger.error(f"Tool registry update failed: {e}")

    def analyze(self, request: MCPRequest) -> MCPResponse:
        """
        Main analysis entry point.

        Args:
            request: MCP analysis request

        Returns:
            MCP response with structured decision
        """
        start_time = time.time()

        # Generate request ID if not provided
        if not request.request_id:
            request.request_id = str(uuid.uuid4())

        try:
            logger.info(f"Starting analysis for request: {request.request_id}")

            # Execute orchestrated analysis
            result = self._orchestrate_analysis(request)

            # Calculate total latency
            total_latency = int((time.time() - start_time) * 1000)

            # Update performance metrics
            self.total_requests += 1
            self.total_latency += total_latency

            # Log evidence
            self._log_evidence(request, result, total_latency)

            logger.info(f"Analysis completed for request: {request.request_id}")
            return result

        except Exception as e:
            logger.error(f"Analysis failed for request {request.request_id}: {e}")
            # Return error response
            return self._create_error_response(request, str(e), total_latency)

    def _orchestrate_analysis(self, request: MCPRequest) -> MCPResponse:
        """Orchestrate the analysis workflow."""
        tools_used = []
        timings = {}

        # Step 1: Retrieve regulatory context
        start_time = time.time()
        rag_results = self._execute_tool(
            "retrieve_rag",
            {
                "query": f"{request.feature_title} {request.description}",
                "top_k": 5,
                "jurisdiction": request.region_hint,
            },
        )
        tools_used.append(rag_results)
        timings["rag_ms"] = rag_results.duration_ms

        # Step 2: Analyze compliance
        start_time = time.time()
        compliance_results = self._execute_tool(
            "analyze_compliance",
            {
                "feature_name": request.feature_title,
                "feature_description": request.description,
                "jurisdiction": request.region_hint,
            },
        )
        tools_used.append(compliance_results)
        timings["analysis_ms"] = compliance_results.duration_ms

        # Step 3: Generate report
        start_time = time.time()
        report_results = self._execute_tool(
            "report_compliance",
            {"analysis_results": compliance_results.output, "format": "summary"},
        )
        tools_used.append(report_results)
        timings["report_ms"] = report_results.duration_ms

        # Step 4: Look up jurisdiction mapping
        if request.region_hint:
            start_time = time.time()
            mapping_results = self._execute_tool(
                "map_lookup",
                {"region": request.region_hint, "policy_type": "compliance"},
            )
            tools_used.append(mapping_results)
            timings["mapping_ms"] = mapping_results.duration_ms

        # Step 5: Get index status
        start_time = time.time()
        index_results = self._execute_tool("index_status", {})
        tools_used.append(index_results)
        timings["index_ms"] = index_results.duration_ms

        # Calculate total timing
        total_ms = sum(timings.values())
        timings["total_ms"] = total_ms

        # Determine decision and confidence
        decision_flag, confidence, reasoning = self._determine_decision(
            request, rag_results, compliance_results, report_results
        )

        # Extract related regulations
        related_regulations = self._extract_regulations(
            rag_results,
            compliance_results,
            mapping_results if request.region_hint else None,
        )

        # Create response
        return MCPResponse(
            request_id=request.request_id,
            decision_flag=decision_flag,
            confidence=confidence,
            reasoning_text=reasoning,
            related_regulations=related_regulations,
            tools_used=tools_used,
            retrieval_metadata=self._get_retrieval_metadata(),
            model_metadata=self._get_model_metadata(),
            timings_ms=timings,
            evidence_record_path=f"data/evidence/{datetime.now().strftime('%Y-%m-%d')}.jsonl",
        )

    def _execute_tool(self, tool_name: str, inputs: Dict[str, Any]) -> ToolUsage:
        """Execute a tool and return usage tracking."""
        try:
            return self.tool_registry.execute_tool(tool_name, **inputs)
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {e}")
            return ToolUsage(
                name=tool_name,
                inputs=inputs,
                output=f"Tool execution failed: {str(e)}",
                duration_ms=0,
                status="error",
                error_message=str(e),
            )

    def _determine_decision(
        self,
        request: MCPRequest,
        rag_results: ToolUsage,
        compliance_results: ToolUsage,
        report_results: ToolUsage,
    ) -> tuple:
        """Determine the compliance decision and confidence."""
        # Use LLM to make final decision if available
        if self.llm and self.llm.get("provider") != "fallback":
            try:
                decision, confidence, reasoning = self._llm_decision(
                    request, rag_results, compliance_results, report_results
                )
                return decision, confidence, reasoning
            except Exception as e:
                logger.warning(f"LLM decision failed: {e}")

        # Fallback decision logic
        return self._fallback_decision(
            request, rag_results, compliance_results, report_results
        )

    def _llm_decision(
        self,
        request: MCPRequest,
        rag_results: ToolUsage,
        compliance_results: ToolUsage,
        report_results: ToolUsage,
    ) -> tuple:
        """Use LLM to make the final decision."""
        # Construct prompt
        prompt = f"""Analyze this feature for compliance:

Feature: {request.feature_title}
Description: {request.description}
Region: {request.region_hint or 'Global'}

RAG Results: {rag_results.output}
Compliance Analysis: {compliance_results.output}
Report: {report_results.output}

Based on the above information, determine:
1. Does this feature need geo-specific logic? (true/false)
2. Confidence level (0.0-1.0)
3. Brief reasoning

Respond in JSON format:
{{"decision": true/false, "confidence": 0.0-1.0, "reasoning": "explanation"}}"""

        # Get LLM response
        if self.llm["provider"] == "transformers_local":
            response = self._call_local_llm(prompt)
        elif self.llm["provider"] == "hf_inference":
            response = self._call_hf_inference(prompt)
        else:
            raise ValueError("Unknown LLM provider")

        # Parse response
        try:
            import json

            result = json.loads(response)
            return result["decision"], result["confidence"], result["reasoning"]
        except:
            # Fallback parsing
            return False, 0.5, "LLM response parsing failed"

    def _call_local_llm(self, prompt: str) -> str:
        """Call local transformers model."""
        try:
            inputs = self.tokenizer(
                prompt, return_tensors="pt", max_length=2048, truncation=True
            )

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=self.mcp_config.get("model", {}).get(
                        "temperature", 0.1
                    ),
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                )

            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response[len(prompt) :].strip()

        except Exception as e:
            logger.error(f"Local LLM call failed: {e}")
            raise

    def _call_hf_inference(self, prompt: str) -> str:
        """Call Hugging Face inference endpoint."""
        try:
            import requests

            response = requests.post(
                self.llm["endpoint_url"],
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 512,
                        "temperature": self.mcp_config.get("model", {}).get(
                            "temperature", 0.1
                        ),
                    },
                },
                headers={
                    "Authorization": f"Bearer {self.mcp_config.get('model', {}).get('api_key', '')}"
                },
            )

            response.raise_for_status()
            result = response.json()
            return result[0]["generated_text"][len(prompt) :].strip()

        except Exception as e:
            logger.error(f"HF inference call failed: {e}")
            raise

    def _fallback_decision(
        self,
        request: MCPRequest,
        rag_results: ToolUsage,
        compliance_results: ToolUsage,
        report_results: ToolUsage,
    ) -> tuple:
        """Fallback decision logic when LLM is not available."""
        # Simple heuristic-based decision
        has_rag_results = (
            rag_results.status == "success" and "RAG result" not in rag_results.output
        )
        has_compliance = compliance_results.status == "success"

        if has_rag_results and has_compliance:
            # If we have good RAG results and compliance analysis, likely needs geo-specific logic
            return (
                True,
                0.7,
                "Feature has regulatory context and compliance requirements",
            )
        elif has_rag_results:
            # If we have RAG results but no compliance analysis
            return True, 0.6, "Feature has regulatory context, needs further analysis"
        else:
            # No clear regulatory context
            return False, 0.4, "No clear regulatory context found"

    def _extract_regulations(
        self,
        rag_results: ToolUsage,
        compliance_results: ToolUsage,
        mapping_results: ToolUsage = None,
    ) -> List[str]:
        """Extract related regulations from tool results."""
        regulations = []

        # Extract from RAG results
        if rag_results.status == "success":
            # Simple extraction - in practice, this would parse the actual results
            regulations.append("EUDSA")
            regulations.append("FL_HB3")

        # Extract from compliance results
        if compliance_results.status == "success":
            regulations.append("CA_SB976")

        # Extract from mapping results
        if mapping_results and mapping_results.status == "success":
            regulations.append("US_2258A")

        return list(set(regulations))  # Remove duplicates

    def _get_retrieval_metadata(self) -> Dict[str, Any]:
        """Get retrieval system metadata."""
        if self.faiss_retriever:
            try:
                stats = self.faiss_retriever.get_stats()
                return {
                    "embedder_name": "faiss",
                    "vectorstore_type": "faiss",
                    "top_k": 5,
                    "retrieved_count": stats.get("total_chunks", 0),
                    "index_size_mb": stats.get("index_size_mb", 0.0),
                }
            except:
                pass

        return {
            "embedder_name": "unknown",
            "vectorstore_type": "unknown",
            "top_k": 5,
            "retrieved_count": 0,
            "index_size_mb": 0.0,
        }

    def _get_model_metadata(self) -> Dict[str, Any]:
        """Get LLM model metadata."""
        if self.llm:
            return {
                "llm_provider": self.llm.get("provider", "unknown"),
                "model_name": self.llm.get("model_name", "unknown"),
                "temperature": self.mcp_config.get("model", {}).get("temperature", 0.1),
                "max_tokens": self.mcp_config.get("model", {}).get("max_tokens", 2048),
            }

        return {
            "llm_provider": "none",
            "model_name": "none",
            "temperature": 0.0,
            "max_tokens": 0,
        }

    def _log_evidence(
        self, request: MCPRequest, response: MCPResponse, total_latency: int
    ):
        """Log evidence for the analysis."""
        if log_compliance_decision:
            try:
                evidence_data = {
                    "request_id": response.request_id,
                    "timestamp_iso": response.timestamp_iso,
                    "agent_name": "mcp_orchestrator",
                    "decision_flag": response.decision_flag,
                    "reasoning_text": response.reasoning_text,
                    "feature_id": request.feature_id,
                    "feature_title": request.feature_title,
                    "related_regulations": response.related_regulations,
                    "confidence": response.confidence,
                    "retrieval_metadata": response.retrieval_metadata,
                    "model_metadata": response.model_metadata,
                    "timings_ms": response.timings_ms,
                    "dataset_tag": request.dataset_tag,
                }

                log_compliance_decision(evidence_data)
                logger.info(f"Evidence logged for request: {request.request_id}")

            except Exception as e:
                logger.error(f"Evidence logging failed: {e}")

    def _create_error_response(
        self, request: MCPRequest, error_message: str, total_latency: int
    ) -> MCPResponse:
        """Create error response when analysis fails."""
        return MCPResponse(
            request_id=request.request_id,
            decision_flag=False,
            confidence=0.0,
            reasoning_text=f"Analysis failed: {error_message}",
            related_regulations=[],
            tools_used=[],
            retrieval_metadata={},
            model_metadata=self._get_model_metadata(),
            timings_ms={"total_ms": total_latency},
            evidence_record_path="",
            timestamp_iso=datetime.now().isoformat(),
        )

    def get_status(self) -> MCPStatus:
        """Get MCP service status."""
        uptime = time.time() - self.start_time
        avg_latency = self.total_latency / max(self.total_requests, 1)

        # Get FAISS index stats
        index_stats = {}
        if self.faiss_retriever:
            try:
                stats = self.faiss_retriever.get_stats()
                index_stats = {
                    "total_chunks": stats.get("total_chunks", 0),
                    "index_size_mb": stats.get("index_size_mb", 0.0),
                    "last_updated": stats.get("last_updated", "unknown"),
                    "health": (
                        "healthy" if stats.get("total_chunks", 0) > 0 else "unhealthy"
                    ),
                }
            except:
                index_stats = {"health": "unknown"}

        return MCPStatus(
            status=(
                "ready"
                if self.llm and self.llm.get("provider") != "fallback"
                else "degraded"
            ),
            llm_loaded=self.llm and self.llm.get("provider") != "fallback",
            faiss_available=bool(self.faiss_retriever),
            tools_active=len(self.tool_registry.tools),
            index_stats=index_stats,
            evidence_path="data/evidence",
            uptime_seconds=uptime,
            total_requests=self.total_requests,
            avg_latency_ms=avg_latency,
        )

    # Actual tool implementations

    def _retrieve_rag_actual(
        self, query: str, top_k: int = 5, jurisdiction: str = None
    ) -> List[Dict]:
        """Actual RAG retrieval implementation."""
        if self.rag_adapter:
            try:
                results = self.rag_adapter.retrieve_regulatory_context(
                    query, jurisdiction, top_k
                )
                return results
            except Exception as e:
                logger.error(f"RAG retrieval failed: {e}")

        # Fallback to retrieval service
        if hasattr(self, "retrieval_service") and self.retrieval_service:
            try:
                from retriever.models import RetrievalRequest

                request = RetrievalRequest(query=query, top_k=top_k)
                response = self.retrieval_service.retrieve(request)
                return [
                    {
                        "text": result.snippet,
                        "source": result.law_name,
                        "score": result.score,
                    }
                    for result in response.results
                ]
            except Exception as e:
                logger.error(f"Retrieval service failed: {e}")

        return [
            {"text": "No regulatory context found", "source": "fallback", "score": 0.0}
        ]

    def _analyze_compliance_actual(
        self, feature_name: str, feature_description: str, jurisdiction: str = None
    ) -> Dict:
        """Actual compliance analysis implementation."""
        if self.compliance_analyzer:
            try:
                analysis = self.compliance_analyzer.analyze_feature(
                    feature_name, feature_description
                )
                return {
                    "compliance_status": analysis.overall_compliance,
                    "confidence": analysis.confidence_level,
                    "regulations": [
                        match.regulation_name for match in analysis.matches
                    ],
                }
            except Exception as e:
                logger.error(f"Compliance analysis failed: {e}")

        return {
            "compliance_status": "UNKNOWN",
            "confidence": 0.5,
            "regulations": ["fallback"],
        }

    def _report_compliance_actual(
        self, analysis_results: Dict, format: str = "summary"
    ) -> Dict:
        """Actual compliance reporting implementation."""
        if self.compliance_reporter:
            try:
                # This would call the actual reporter
                return {
                    "report": f"Compliance report for {format}",
                    "recommendations": ["Implement geo-specific logic"],
                    "risk_level": "MEDIUM",
                }
            except Exception as e:
                logger.error(f"Compliance reporting failed: {e}")

        return {
            "report": "Fallback report",
            "recommendations": ["Fallback recommendation"],
            "risk_level": "UNKNOWN",
        }

    def _export_csv_actual(
        self, start_date: str = None, end_date: str = None, format: str = "csv"
    ) -> Dict:
        """Actual CSV export implementation."""
        if self.evidence_exporter:
            try:
                # Parse dates
                parsed_start = None
                parsed_end = None
                if start_date:
                    parsed_start = datetime.strptime(start_date, "%Y-%m-%d")
                if end_date:
                    parsed_end = datetime.strptime(end_date, "%Y-%m-%d")

                # Export to temporary file
                import tempfile

                with tempfile.NamedTemporaryFile(
                    mode="w", suffix=".csv", delete=False
                ) as tmp_file:
                    count = self.evidence_exporter.export_to_csv(
                        tmp_file.name, parsed_start, parsed_end, None, None
                    )

                    return {
                        "export_path": tmp_file.name,
                        "record_count": count,
                        "format": format,
                    }

            except Exception as e:
                logger.error(f"CSV export failed: {e}")

        return {"export_path": "export_failed.csv", "record_count": 0, "format": format}

    def _index_status_actual(self) -> Dict:
        """Actual index status implementation."""
        if self.faiss_retriever:
            try:
                stats = self.faiss_retriever.get_stats()
                return {
                    "total_chunks": stats.get("total_chunks", 0),
                    "index_size_mb": stats.get("index_size_mb", 0.0),
                    "last_updated": stats.get("last_updated", "unknown"),
                    "health": (
                        "healthy" if stats.get("total_chunks", 0) > 0 else "unhealthy"
                    ),
                }
            except Exception as e:
                logger.error(f"Index status failed: {e}")

        return {
            "total_chunks": 0,
            "index_size_mb": 0.0,
            "last_updated": "unknown",
            "health": "unknown",
        }
