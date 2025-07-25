from agency_swarm import Agent

from app.DataSEOAgent.tools.data_mcp import dataforseo_server

data_for_seo_agent = Agent(
    name="DataSEOAgent",
    instructions="You are a helpful assistant",
    description="DataForSEO Agent specialized in SEO analysis and data research",
    mcp_servers=[dataforseo_server],
    model="gpt-4o-mini",
)