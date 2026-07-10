from google.adk.agents.llm_agent import Agent

from ...tools import search_templates, save_exercise_data
from .prompt import EXERCISES_AGENT_INSTRUCTION

exercises_agent = Agent(
    name="exercises_agent",
    model='gemini-3.1-flash-lite',
    description="Agente especializado en crear ejercicios educativos usando templates",
    instruction=EXERCISES_AGENT_INSTRUCTION,
    tools=[search_templates, save_exercise_data],
)
