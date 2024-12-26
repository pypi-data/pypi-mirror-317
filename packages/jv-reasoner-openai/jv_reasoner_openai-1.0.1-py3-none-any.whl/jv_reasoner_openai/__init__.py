from jvcore import Reasoner
from .openai_reasoner import OpenAiReasoner

def getReasoner() -> Reasoner:
    return OpenAiReasoner()
