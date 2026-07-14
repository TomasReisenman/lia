from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
# from google.adk.tools.mcp_tool import McpToolset, StdioConnectionParams

from mcp import StdioServerParameters

from .prompt import WIKIPEDIA_AGENT_INSTRUCTION

wikipedia_agent = Agent(
    name="wikipedia_agent",
    model='gemini-3.1-flash-lite',
    description="Agente especializado en aprender conceptos usando Wikipedia",
    instruction=WIKIPEDIA_AGENT_INSTRUCTION,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="wikipedia-mcp",
                    args=["--language", "es"],
                ),
            ),
        )
    ],
)
