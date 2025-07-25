from agency_swarm import Agent
from agents import HostedMCPTool

from app.DataSEOAgent.tools.data_mcp import dataforseo_server

# Only include the MCP server if it's available
mcp_servers = [dataforseo_server] if dataforseo_server is not None else []

data_for_seo_agent = Agent(
    name="DataSEOAgent",
    instructions="You are a helpful assistant",
    description="DataForSEO Agent specialized in SEO analysis and data research",
    # mcp_servers=mcp_servers, # <- local mcp server
    # tools=[
    #     HostedMCPTool(      # <- public mcp server (requires ngrok)
    #         tool_config={
    #             "type": "mcp",
    #             "server_label": "mcp-tools-server",
    #             # server_url must be accessible from the internet (not locally)
    #             "server_url": "https://dataforseo-mcp-worker.tricelex.workers.dev/", # <- update this with your ngrok url
    #             "require_approval": "never",
    #         }
    #     ),
    # ],
)

