from google.adk.agents.llm_agent import Agent

from ...tools import search_templates
from .prompt import STUDY_ADVISOR_AGENT_INSTRUCTION

study_advisor_agent = Agent(
    name="study_advisor_agent",
    model='gemini-3.1-flash-lite',
    description="Agente especializado en recomendar temas de estudio en IA/ML usando RAG",
    instruction=STUDY_ADVISOR_AGENT_INSTRUCTION,
    tools=[search_templates],
)
