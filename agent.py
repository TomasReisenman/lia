from google.adk.agents.llm_agent import Agent

from .prompt import ROOT_AGENT_INSTRUCTION
from .sub_agents.wikipedia_agent import wikipedia_agent

root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='root_agent',
    description='Agente principal que delega investigación de conceptos al agente de Wikipedia',
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[wikipedia_agent],
)
