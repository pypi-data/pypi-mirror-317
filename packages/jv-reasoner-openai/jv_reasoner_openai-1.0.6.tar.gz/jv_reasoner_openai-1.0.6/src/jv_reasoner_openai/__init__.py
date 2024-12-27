import code
from jvcore import Reasoner, Communicator
from .openai_reasoner import OpenAiReasoner

def getReasoner(communicator: Communicator) -> Reasoner:
    return OpenAiReasoner(communicator)

def test(communicator: Communicator = None):
    reasoner = OpenAiReasoner(communicator)
    print('Reasoner is available under reasoner variable')
    code.interact(local=locals())
