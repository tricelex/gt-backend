from agents.mcp import MCPServerSse

dataforseo_server = MCPServerSse(
    name="data_for_seo",
    params={
        "url": "https://dataforseo-mcp-worker.tricelex.workers.dev/sse"
    },
    client_session_timeout_seconds=20
)
