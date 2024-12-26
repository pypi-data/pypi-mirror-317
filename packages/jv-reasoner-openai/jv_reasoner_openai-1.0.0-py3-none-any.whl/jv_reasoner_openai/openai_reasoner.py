import json
from jvcore import Reasoner, SkillDescription, QueryDescription, ActionParameters
from jvopenai import OpenAITool

class OpenaiReasoner(Reasoner):
    def __init__(self):
        self._openai = OpenAITool()

    def selectSkill(self, skills: list[SkillDescription], queries: list[QueryDescription], utterance: str) -> ActionParameters:
        response = self._openai.completion(self.__getPrompt(skills, utterance))
        return json.loads(response)
    
    def __getPrompt(self, skills: list[SkillDescription], utterance: str) -> str:
        return f'''\
Here is a list of commands together with their descriptions:
{[skill.name +' - ' + skill.description for skill in skills]}
Please answer with the command I want to run based on my request
My request: "{utterance}"
your answer should be in json format:
{{"commandName\": \"<commandName>\",\"parameters\": {{}}}}
'''