#!/usr/bin/env python3
"""
Start the MCP Server Bridge service for testing.
"""

import logging

import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    print("🚀 Starting MCP Server Bridge...")
    print("Service will be available at: http://localhost:8000")
    print("MCP endpoints:")
    print("  - POST /mcp/analyze")
    print("  - GET  /mcp/tools")
    print("  - GET  /mcp/status")
    print("  - GET  /docs (OpenAPI documentation)")
    print("\nPress Ctrl+C to stop the service")

    try:
        uvicorn.run(
            "retriever.service:app",
            host="0.0.0.0",
            port=8000,
            reload=False,
            log_level="info",
        )
    except KeyboardInterrupt:
        print("\n🛑 Service stopped by user")
    except Exception as e:
        print(f"❌ Failed to start service: {e}")
        exit(1)
