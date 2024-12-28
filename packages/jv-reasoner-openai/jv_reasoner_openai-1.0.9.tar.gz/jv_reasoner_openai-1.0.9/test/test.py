from jv_reasoner_openai.openai_reasoner import OpenAiReasoner

reasoner = OpenAiReasoner(None)
skills = [
    {'name':'echo', 'description':'repeats user request'},
    {'name':'youtube','description': 'plays a youtube song. Parameters: <songHint>: a search phrase or a hint for a sing to play'}
]
while True:
    request = input('>')
    response = reasoner.selectSkill(skills, [], request)
    print(response)