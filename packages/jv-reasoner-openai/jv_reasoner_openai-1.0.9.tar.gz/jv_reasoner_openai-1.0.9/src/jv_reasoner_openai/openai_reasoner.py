import json
from jvcore import Reasoner, ActionDescription, ActionParameters, Communicator, ActionType
from jvopenai import OpenAIConversation


def _instruction(skillsAndQueries: dict[str, ActionDescription]) -> str:
    return \
f'''You are an assistant of mine. I provide you with commands and queries. Based on my request you should respond with a command I intend to execute. 
If you want to execute a command, you respond with json object and nothing more. json structure should be 
{{"action":"command", "command-name": "<command name>", "parameters": <object with parameters you think are proper>}}
If you want to call a query you respond only with json object with this structure:
{{"action":"query", "query-name": "<query name>", "parameters": <object with parameters you think are proper>}}
If you need additional data to fulfil my request, you can use a query to get information.
the only command available commands are (name - description):
{__actions(ActionType.Command, skillsAndQueries)}
you cannot call commands that are not from this list
the only available queries are (name-description):
{__actions(ActionType.Query, skillsAndQueries)}
you cannot call queries that are not on this list
if none of the commands match my request respond with a word "none"
\nIf you understood the instructions respond with 1 else respond with 0
'''

class OpenAiReasoner(Reasoner):
    def __init__(self, communicator: Communicator):
        self.__conversation = OpenAIConversation()
        self.__initialised = False
        self.__communicator = communicator

    def selectSkill(self, skillsAndQueries: dict[str, ActionDescription], utterance: str) -> ActionParameters | None:
        self.__initialInstruction(skillsAndQueries)
        response = self.__conversation.getResponse(utterance)
        print(response) #debug
        return json.loads(response) if response != 'none' else None
    
    def __initialInstruction(self, skillsAndQueries: dict[str, ActionDescription]) -> str:
        if not self.__initialised:
            instructions = _instruction(skillsAndQueries)
            print(instructions) #debug
            instructionAccepted = self.__conversation.getResponse(instructions) == '1'
            print(instructionAccepted) #debug
            self.__initialised = True
            if not instructionAccepted:
                raise KeyError('Its wrong error and openai doesnt understand me (reasoner)') #this does not make sense, it will always understand

def __actions(type: ActionType, skillsAndQueries: dict[str, ActionDescription]) -> str:
    return '\n'.join([skillName +' - ' + description['description'] for skillName, description in skillsAndQueries.items() if description['type'] == ActionType.Command])