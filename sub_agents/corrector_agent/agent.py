from google.adk.agents.llm_agent import Agent

from ...tools import get_exercise_data
from .prompt import CORRECTOR_AGENT_INSTRUCTION

corrector_agent = Agent(
    name="corrector_agent",
    model='gemini-3.1-flash-lite',
    description="Agente especializado en corregir respuestas de ejercicios",
    instruction=CORRECTOR_AGENT_INSTRUCTION,
    tools=[get_exercise_data],
)
