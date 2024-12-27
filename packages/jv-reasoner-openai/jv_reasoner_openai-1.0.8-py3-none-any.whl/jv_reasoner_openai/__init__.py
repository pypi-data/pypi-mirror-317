import code
from jvcore import Reasoner, Communicator
from .openai_reasoner import OpenAiReasoner

def getReasoner(communicator: Communicator) -> Reasoner:
    return OpenAiReasoner(communicator)
