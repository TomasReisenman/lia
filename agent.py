from google.adk.agents.llm_agent import Agent

from .prompt import ROOT_AGENT_INSTRUCTION
from .sub_agents.wikipedia_agent import wikipedia_agent
from .sub_agents.github_agent import github_agent

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='Agente principal que delega tareas a agentes especializados',
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[wikipedia_agent, github_agent],
)
