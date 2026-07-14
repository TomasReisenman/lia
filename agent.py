from typing import Optional

from google.adk.agents.context import Context
from google.adk.agents.llm_agent import Agent
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

from .prompt import ROOT_AGENT_INSTRUCTION
from .sub_agents.wikipedia_agent import wikipedia_agent
from .sub_agents.github_agent import github_agent
from .sub_agents.exercises_agent import exercises_agent
from .sub_agents.corrector_agent import corrector_agent
from .sub_agents.study_advisor_agent import study_advisor_agent
from .sub_agents.url_reader_agent import url_reader_agent

FORBIDDEN_TERMS: list[str] = [
    "hack", "hacking", "crack", "phishing", "malware",
    "ransomware", "keylogger", "exploit", "vulnerabilidad",
    "inyeccion sql", "inyección sql", "sql injection",
]


def block_disallowed_content(
    callback_context: Context, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    last_text = llm_request.contents[-1].parts[0].text if llm_request.contents else ""
    last_text = last_text.lower()
    for term in FORBIDDEN_TERMS:
        if term in last_text:
            callback_context.state["blocked_requests"] = (
                callback_context.state.get("blocked_requests", 0) + 1
            )
            return LlmResponse(
                content=types.Content(
                    parts=[types.Part(text="Lo siento, no puedo ayudar con este tema.")],
                    role="model",
                )
            )
    return None


root_agent = Agent(
    model='gemini-3.1-flash-lite',
    name='root_agent',
    description='Agente principal que delega tareas a agentes especializados',
    instruction=ROOT_AGENT_INSTRUCTION,
    sub_agents=[wikipedia_agent, github_agent, exercises_agent, corrector_agent, study_advisor_agent, url_reader_agent],
    before_model_callback=block_disallowed_content,
)

