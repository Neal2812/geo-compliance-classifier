"""
MCP Tool Registry

Manages registration and execution of compliance analysis tools.
"""

import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from .models import ToolDefinition, ToolUsage

logger = logging.getLogger(__name__)


def tool_executor(timeout_s: int = 30, retries: int = 1):
    """Decorator for tool execution with timeout and retry logic."""

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> ToolUsage:
            start_time = time.time()
            tool_name = func.__name__

            for attempt in range(retries + 1):
                try:
                    # Execute tool with timeout
                    if asyncio.iscoroutinefunction(func):
                        result = await asyncio.wait_for(
                            func(*args, **kwargs), timeout=timeout_s
                        )
                    else:
                        # For sync functions, run in thread pool
                        loop = asyncio.get_event_loop()
                        result = await asyncio.wait_for(
                            loop.run_in_executor(None, func, *args, **kwargs),
                            timeout=timeout_s,
                        )

                    duration_ms = int((time.time() - start_time) * 1000)

                    return ToolUsage(
                        name=tool_name,
                        inputs=kwargs,
                        output=(
                            str(result)[:200] + "..."
                            if len(str(result)) > 200
                            else str(result)
                        ),
                        duration_ms=duration_ms,
                        status="success",
                    )

                except asyncio.TimeoutError:
                    logger.warning(
                        f"Tool {tool_name} timed out after {timeout_s}s (attempt {attempt + 1})"
                    )
                    if attempt == retries:
                        duration_ms = int((time.time() - start_time) * 1000)
                        return ToolUsage(
                            name=tool_name,
                            inputs=kwargs,
                            output="Tool execution timed out",
                            duration_ms=duration_ms,
                            status="timeout",
                            error_message=f"Timeout after {timeout_s}s",
                        )
                    await asyncio.sleep(0.1 * (2**attempt))  # Exponential backoff

                except Exception as e:
                    logger.error(f"Tool {tool_name} failed: {e}")
                    duration_ms = int((time.time() - start_time) * 1000)
                    return ToolUsage(
                        name=tool_name,
                        inputs=kwargs,
                        output=f"Tool execution failed: {str(e)}",
                        duration_ms=duration_ms,
                        status="error",
                        error_message=str(e),
                    )

            # Should never reach here
            return ToolUsage(
                name=tool_name,
                inputs=kwargs,
                output="Tool execution failed after all retries",
                duration_ms=int((time.time() - start_time) * 1000),
                status="error",
                error_message="Failed after all retry attempts",
            )

        return wrapper

    return decorator


class ToolRegistry:
    """Registry for MCP compliance analysis tools."""

    def __init__(self):
        self.tools: Dict[str, ToolDefinition] = {}
        self.tool_functions: Dict[str, Callable] = {}
        self._register_default_tools()

    def _register_default_tools(self):
        """Register the 9 default tool categories."""
        # 1. retrieve_rag - FAISS + RAG retrieval
        self.register_tool(
            name="retrieve_rag",
            description="Retrieve regulatory context using FAISS vector search and RAG",
            input_schema={
                "query": {"type": "string", "description": "Search query"},
                "top_k": {
                    "type": "integer",
                    "description": "Number of results",
                    "default": 5,
                },
                "jurisdiction": {
                    "type": "string",
                    "description": "Jurisdiction filter",
                    "optional": True,
                },
            },
            output_schema={
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string"},
                        "source": {"type": "string"},
                        "score": {"type": "number"},
                    },
                },
            },
            function=self._retrieve_rag_tool,
            timeout_s=30,
            retries=1,
        )

        # 2. analyze_compliance - Compliance analysis
        self.register_tool(
            name="analyze_compliance",
            description="Analyze feature compliance against regulatory requirements",
            input_schema={
                "feature_name": {"type": "string", "description": "Feature name"},
                "feature_description": {
                    "type": "string",
                    "description": "Feature description",
                },
                "jurisdiction": {
                    "type": "string",
                    "description": "Jurisdiction",
                    "optional": True,
                },
            },
            output_schema={
                "type": "object",
                "properties": {
                    "compliance_status": {"type": "string"},
                    "confidence": {"type": "number"},
                    "regulations": {"type": "array", "items": {"type": "string"}},
                },
            },
            function=self._analyze_compliance_tool,
            timeout_s=45,
            retries=1,
        )

        # 3. report_compliance - Compliance reporting
        self.register_tool(
            name="report_compliance",
            description="Generate compliance report and recommendations",
            input_schema={
                "analysis_results": {
                    "type": "object",
                    "description": "Compliance analysis results",
                },
                "format": {
                    "type": "string",
                    "description": "Report format",
                    "default": "summary",
                },
            },
            output_schema={
                "type": "object",
                "properties": {
                    "report": {"type": "string"},
                    "recommendations": {"type": "array", "items": {"type": "string"}},
                    "risk_level": {"type": "string"},
                },
            },
            function=self._report_compliance_tool,
            timeout_s=30,
            retries=1,
        )

        # 4. map_lookup - Jurisdiction and policy mapping
        self.register_tool(
            name="map_lookup",
            description="Look up jurisdiction-specific policies and regulations",
            input_schema={
                "region": {"type": "string", "description": "Geographic region"},
                "policy_type": {
                    "type": "string",
                    "description": "Type of policy to look up",
                },
            },
            output_schema={
                "type": "object",
                "properties": {
                    "jurisdiction": {"type": "string"},
                    "policies": {"type": "array", "items": {"type": "string"}},
                    "requirements": {"type": "array", "items": {"type": "string"}},
                },
            },
            function=self._map_lookup_tool,
            timeout_s=20,
            retries=1,
        )

        # 5. evidence_log - Evidence logging
        self.register_tool(
            name="evidence_log",
            description="Log compliance decision evidence",
            input_schema={
                "decision_data": {
                    "type": "object",
                    "description": "Decision data to log",
                }
            },
            output_schema={
                "type": "object",
                "properties": {
                    "evidence_id": {"type": "string"},
                    "logged_at": {"type": "string"},
                    "status": {"type": "string"},
                },
            },
            function=self._evidence_log_tool,
            timeout_s=15,
            retries=1,
        )

        # 6. export_csv - CSV export
        self.register_tool(
            name="export_csv",
            description="Export evidence data to CSV format",
            input_schema={
                "start_date": {
                    "type": "string",
                    "description": "Start date (YYYY-MM-DD)",
                    "optional": True,
                },
                "end_date": {
                    "type": "string",
                    "description": "End date (YYYY-MM-DD)",
                    "optional": True,
                },
                "format": {
                    "type": "string",
                    "description": "Export format",
                    "default": "csv",
                },
            },
            output_schema={
                "type": "object",
                "properties": {
                    "export_path": {"type": "string"},
                    "record_count": {"type": "integer"},
                    "format": {"type": "string"},
                },
            },
            function=self._export_csv_tool,
            timeout_s=60,
            retries=1,
        )

        # 7. index_status - FAISS index status
        self.register_tool(
            name="index_status",
            description="Get FAISS index statistics and health status",
            input_schema={},
            output_schema={
                "type": "object",
                "properties": {
                    "total_chunks": {"type": "integer"},
                    "index_size_mb": {"type": "number"},
                    "last_updated": {"type": "string"},
                    "health": {"type": "string"},
                },
            },
            function=self._index_status_tool,
            timeout_s=10,
            retries=1,
        )

        # 8. glossary_lookup - Glossary and terminology
        self.register_tool(
            name="glossary_lookup",
            description="Look up regulatory terms and definitions",
            input_schema={
                "term": {"type": "string", "description": "Term to look up"},
                "regulation": {
                    "type": "string",
                    "description": "Regulation context",
                    "optional": True,
                },
            },
            output_schema={
                "type": "object",
                "properties": {
                    "term": {"type": "string"},
                    "definition": {"type": "string"},
                    "regulation": {"type": "string"},
                    "examples": {"type": "array", "items": {"type": "string"}},
                },
            },
            function=self._glossary_lookup_tool,
            timeout_s=20,
            retries=1,
        )

        # 9. feature_generate - Feature generation
        self.register_tool(
            name="feature_generate",
            description="Generate synthetic features for testing",
            input_schema={
                "feature_type": {
                    "type": "string",
                    "description": "Type of feature to generate",
                },
                "count": {
                    "type": "integer",
                    "description": "Number of features",
                    "default": 1,
                },
            },
            output_schema={
                "type": "object",
                "properties": {
                    "features": {"type": "array", "items": {"type": "object"}},
                    "generated_count": {"type": "integer"},
                },
            },
            function=self._feature_generate_tool,
            timeout_s=30,
            retries=1,
        )

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict,
        output_schema: Dict,
        function: Callable,
        timeout_s: int = 30,
        retries: int = 1,
    ):
        """Register a tool in the registry."""
        self.tools[name] = ToolDefinition(
            name=name,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            timeout_s=timeout_s,
            retries=retries,
        )
        self.tool_functions[name] = function
        logger.info(f"Registered tool: {name}")

    def get_tool(self, name: str) -> Optional[ToolDefinition]:
        """Get tool definition by name."""
        return self.tools.get(name)

    def list_tools(self) -> List[ToolDefinition]:
        """List all registered tools."""
        return list(self.tools.values())

    def execute_tool(self, name: str, **kwargs) -> ToolUsage:
        """Execute a tool by name."""
        if name not in self.tool_functions:
            raise ValueError(f"Tool '{name}' not found")

        tool_func = self.tool_functions[name]
        tool_def = self.tools[name]

        # Apply timeout and retry decorator
        decorated_func = tool_executor(tool_def.timeout_s, tool_def.retries)(tool_func)

        # Execute tool
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Create new event loop for sync execution
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(decorated_func, **kwargs)
                return future.result()
        else:
            return loop.run_until_complete(decorated_func(**kwargs))

    # Tool implementations (placeholder implementations)

    def _retrieve_rag_tool(
        self, query: str, top_k: int = 5, jurisdiction: str = None
    ) -> List[Dict]:
        """Retrieve regulatory context using RAG."""
        # This will be implemented by the orchestrator with actual RAG system
        return [
            {"text": f"RAG result for: {query}", "source": "placeholder", "score": 0.8}
        ]

    def _analyze_compliance_tool(
        self, feature_name: str, feature_description: str, jurisdiction: str = None
    ) -> Dict:
        """Analyze feature compliance."""
        return {
            "compliance_status": "UNKNOWN",
            "confidence": 0.5,
            "regulations": ["placeholder"],
        }

    def _report_compliance_tool(
        self, analysis_results: Dict, format: str = "summary"
    ) -> Dict:
        """Generate compliance report."""
        return {
            "report": "Placeholder report",
            "recommendations": ["Placeholder recommendation"],
            "risk_level": "MEDIUM",
        }

    def _map_lookup_tool(self, region: str, policy_type: str) -> Dict:
        """Look up jurisdiction policies."""
        return {
            "jurisdiction": region,
            "policies": ["placeholder policy"],
            "requirements": ["placeholder requirement"],
        }

    def _evidence_log_tool(self, decision_data: Dict) -> Dict:
        """Log evidence."""
        return {
            "evidence_id": "placeholder_id",
            "logged_at": "2025-01-01T00:00:00Z",
            "status": "logged",
        }

    def _export_csv_tool(
        self, start_date: str = None, end_date: str = None, format: str = "csv"
    ) -> Dict:
        """Export to CSV."""
        return {"export_path": "placeholder.csv", "record_count": 0, "format": format}

    def _index_status_tool(self) -> Dict:
        """Get index status."""
        return {
            "total_chunks": 0,
            "index_size_mb": 0.0,
            "last_updated": "2025-01-01T00:00:00Z",
            "health": "unknown",
        }

    def _glossary_lookup_tool(self, term: str, regulation: str = None) -> Dict:
        """Look up glossary terms."""
        return {
            "term": term,
            "definition": "Placeholder definition",
            "regulation": regulation or "general",
            "examples": ["Placeholder example"],
        }

    def _feature_generate_tool(self, feature_type: str, count: int = 1) -> Dict:
        """Generate features."""
        return {
            "features": [
                {"type": feature_type, "id": f"placeholder_{i}"} for i in range(count)
            ],
            "generated_count": count,
        }
