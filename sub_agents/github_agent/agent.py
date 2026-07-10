import os

from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

from .prompt import GITHUB_AGENT_INSTRUCTION

token = os.environ.get("GH_TOKEN")
if not token:
    raise ValueError("GH_TOKEN not found in environment variables")

github_agent = Agent(
    name="github_agent",
    model='gemini-2.5-flash',
    description="Agente especializado en buscar repositorios en GitHub",
    instruction=GITHUB_AGENT_INSTRUCTION,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={
                    "Authorization": f"Bearer {token}",
                    "X-MCP-Toolsets": "repos,issues,pull_requests",
                    "X-MCP-Readonly": "true",
                },
            ),
        )
    ],
)
