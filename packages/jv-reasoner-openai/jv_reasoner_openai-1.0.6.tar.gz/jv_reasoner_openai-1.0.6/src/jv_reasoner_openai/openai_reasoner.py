import json
from jvcore import Reasoner, SkillDescription, QueryDescription, ActionParameters, Communicator
from jvopenai import OpenAIConversation

class OpenAiReasoner(Reasoner):
    def __init__(self, communicator: Communicator):
        self.__conversation = OpenAIConversation()
        self.__initialised = False
        self.__communicator = communicator

    def selectSkill(self, skills: list[SkillDescription], queries: list[QueryDescription], utterance: str) -> ActionParameters:
        self.__initialInstruction(skills, queries)
        response = self.__conversation.getResponse(utterance)
        return json.loads(response)
    
    def __initialInstruction(self, skills: list[SkillDescription], queries: list[QueryDescription]) -> str:
        if not self.__initialised:
            instruction = f'''\
You are an assistant of mine. I provide you with commands and queries. Based on my request you should respond with a command I intend to execute. 
If you want to execute a command, you respond with json object and nothing more. json structure should be 
{{"action":"command", "command-name": "<command name>", "parameters": <object with parameters you think are proper>}}
If you want to call a query you respond only with json object with this structure:
{{"action":"query", "query-name": "<query name>", "parameters": <object with parameters you think are proper>}}
If you need additional data to fulfil my request, you can use a query to get information.
commands (name - description):
{[skill.name +' - ' + skill.description for skill in skills]}
queries (name-description):
{[query.name +' - ' + query.description for query in queries]}
if none of the commands match my request respond with json object:
{{"action": "unknown", "request": <users request>}}
\nIf you understood the instructions respond with 1 else respond with 0
'''
            instructionAccepted = self.__conversation.getResponse(instruction) == '0'
            self.__initialised = True
            if not instructionAccepted:
                raise KeyError('Its wrong error and openai doesnt understand me (reasoner)') #this does not make sense, it will always understand
