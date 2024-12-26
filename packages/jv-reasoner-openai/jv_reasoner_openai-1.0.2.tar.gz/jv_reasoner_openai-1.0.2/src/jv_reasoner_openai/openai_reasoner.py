import json
from jvcore import Reasoner, SkillDescription, QueryDescription, ActionParameters
from jvopenai import OpenAITool

class OpenAiReasoner(Reasoner):
    def __init__(self):
        self._openai = OpenAITool()

    def selectSkill(self, skills: list[SkillDescription], queries: list[QueryDescription], utterance: str) -> ActionParameters:
        isOk = self._openai.instruct(self.__getInitialInstruction(skills, queries))
        print('is ok', isOk)
        response = self._openai.completion(utterance)
        return json.loads(response)
    
    def __getInitialInstruction(self, skills: list[SkillDescription], queries: list[QueryDescription]) -> str:
        return f'''\
You are an assistant of mine. I provide you with commands and queries. Based on my request you should respond with a command I intend to execute. 
If you want to execute a command, you respond with json object and nothing more. json structure should be 
{{"command-name": "<command name>", "parameters": <object with parameters you think are proper>}}
If you want to call a query you respond only with json object with this structure:
{{"query-name": "<query name>", "parameters": <object with parameters you think are proper>}}
If you need additional data to fulfil my request, you can use a query to get information.
commands (name - description):
{[skill.name +' - ' + skill.description for skill in skills]}
queries (name-description):
{[query.name +' - ' + query.description for query in queries]}
'''