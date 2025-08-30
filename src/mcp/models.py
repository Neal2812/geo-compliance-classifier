"""
MCP Data Models

Pydantic models for MCP request/response schemas and tool usage tracking.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class MCPRequest(BaseModel):
    """MCP analysis request model."""

    request_id: Optional[str] = Field(
        None, description="Request ID (generated if not provided)"
    )
    feature_id: str = Field(..., description="Unique feature identifier")
    feature_title: str = Field(..., description="Feature title/name")
    description: str = Field(..., description="Feature description")
    artifacts: Optional[List[str]] = Field(None, description="PRD/TRD references")
    region_hint: Optional[str] = Field(None, description="Geographic region hint")
    dataset_tag: Optional[str] = Field(None, description="Dataset tag for grouping")


class ToolUsage(BaseModel):
    """Tool usage tracking model."""

    name: str = Field(..., description="Tool name")
    inputs: Dict[str, Any] = Field(..., description="Tool input parameters")
    output: str = Field(..., description="Short tool output summary")
    duration_ms: int = Field(..., description="Tool execution time in milliseconds")
    status: str = Field(
        ..., description="Tool execution status (success/error/timeout)"
    )
    error_message: Optional[str] = Field(None, description="Error message if failed")


class MCPResponse(BaseModel):
    """MCP analysis response model."""

    request_id: str = Field(..., description="Request ID")
    decision_flag: bool = Field(
        ..., description="Compliance decision (needs_geo_specific_logic)"
    )
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    reasoning_text: str = Field(..., description="Detailed reasoning for decision")
    related_regulations: List[str] = Field(
        ..., description="List of related regulations"
    )
    tools_used: List[ToolUsage] = Field(..., description="Ordered list of tools used")
    retrieval_metadata: Dict[str, Any] = Field(
        ..., description="Retrieval system metadata"
    )
    model_metadata: Dict[str, Any] = Field(..., description="LLM model metadata")
    timings_ms: Dict[str, int] = Field(
        ..., description="Timing breakdown in milliseconds"
    )
    evidence_record_path: str = Field(
        ..., description="Evidence JSONL record reference"
    )
    timestamp_iso: str = Field(default_factory=lambda: datetime.now().isoformat())


class ToolDefinition(BaseModel):
    """Tool definition for registry."""

    name: str = Field(..., description="Tool name")
    description: str = Field(..., description="Tool description")
    input_schema: Dict[str, Any] = Field(..., description="Input parameter schema")
    output_schema: Dict[str, Any] = Field(..., description="Output schema")
    timeout_s: int = Field(30, description="Tool timeout in seconds")
    retries: int = Field(1, description="Number of retry attempts")
    idempotent: bool = Field(True, description="Whether tool is idempotent")


class MCPStatus(BaseModel):
    """MCP service status model."""

    status: str = Field(..., description="Service status")
    llm_loaded: bool = Field(..., description="Whether LLM is loaded")
    faiss_available: bool = Field(..., description="Whether FAISS index is available")
    tools_active: int = Field(..., description="Number of active tools")
    index_stats: Dict[str, Any] = Field(..., description="FAISS index statistics")
    evidence_path: str = Field(..., description="Evidence storage path")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    total_requests: int = Field(..., description="Total requests processed")
    avg_latency_ms: float = Field(..., description="Average request latency")
