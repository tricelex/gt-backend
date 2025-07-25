from agents.mcp import MCPServerStdioParams, MCPServerStdio, MCPServerSse, MCPServerStreamableHttp

from app.settings import settings

# Try to create the MCP server with error handling
dataforseo_server = MCPServerStreamableHttp(
    name="data_for_seo",
    params={"url": "https://dataforseo-mcp-worker.tricelex.workers.dev/mcp"},
)

# Alternative configurations (commented out for now)
# dataforseo_server__ = MCPServerStdio(
#     MCPServerStdioParams(
#         command="npx",
#         args=[
#             "-y",
#             "@dataforseo/mcp-server-typescript",
#             "--client-id", settings.dataforseo.client_id,
#             "--client-secret", settings.dataforseo.client_secret,
#             "--base-url", settings.dataforseo.base_url
#         ]
#     ),
#     cache_tools_list=True
# )

# dataforseo_serveree = MCPServerSse(
#     name="data_for_seo", # Tools will be accessed like My_Custom_SSE_Server.some_tool
#     params={
#         "url": "https://dataforseo-mcp-worker.tricelex.workers.dev/http",
#     },
#     cache_tools_list=False,
# )
