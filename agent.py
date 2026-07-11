from google.adk.agents.llm_agent import Agent

from .prompt import ROOT_AGENT_INSTRUCTION
from .sub_agents.wikipedia_agent import wikipedia_agent
from .sub_agents.github_agent import github_agent
from .sub_agents.exercises_agent import exercises_agent
from .sub_agents.corrector_agent import corrector_agent
from .sub_agents.study_advisor_agent import study_advisor_agent
from .sub_agents.url_reader_agent import url_reader_agent

root_agent = Agent(
    model='gemini-3.1-flash-lite',
    name='root_agent',
    description='Agente principal que delega tareas a agentes especializados',
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[wikipedia_agent, github_agent, exercises_agent, corrector_agent, study_advisor_agent,url_reader_agent],
)
