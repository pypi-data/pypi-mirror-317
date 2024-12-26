from openai import OpenAI
from jvcore import getConfig, Singleton

class OpenAITool(metaclass=Singleton): #todo 0 a method to continue conversation and start a new converation (singleton vs transient?)
    def __init__(self) -> None:
        accessKey = getConfig().get('openai','accessKey')
        self.__client = OpenAI(api_key=accessKey)
        self.__mesages = []
    
    def completion(self, request: str) -> str:
        result = self.__updateContext(request)
        return result.choices[0].message.content

    def instruct(self, instruction: str) -> bool:
        result = self.__updateContext(instruction + '\nIf you understood the instructions respond with 1 else respond with 0')
        result =  result.choices[0].message.content
        return int(result) == 1

    def __updateContext(self, content: str):
        self.__mesages = [*self.__mesages, 
            {
                "role": "user",
                "content": content
            }
        ]
        return self.__client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages= self.__mesages
        )
