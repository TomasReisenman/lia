from google.adk.agents.llm_agent import Agent

from ...tools import fetch_url, save_summary
from .prompt import URL_READER_AGENT_INSTRUCTION

url_reader_agent = Agent(
    name="url_reader_agent",
    model='gemini-3.1-flash-lite',
    mode='task',
    description="Agente especializado en leer URLs y resumir su contenido",
    instruction=URL_READER_AGENT_INSTRUCTION,
    tools=[fetch_url, save_summary],
)
