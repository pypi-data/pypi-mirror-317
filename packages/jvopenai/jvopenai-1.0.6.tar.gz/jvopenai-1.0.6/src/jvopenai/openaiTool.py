from openai import OpenAI
from jvcore import getConfig, Singleton

class OpenAIConversation():
    def __init__(self) -> None:
        accessKey = getConfig().get('openai','accessKey')
        self.__client = OpenAI(api_key=accessKey)
        self.__messages = []
    
    def getResponse(self, request: str) -> str:
        result = self.__getCompletion(request)
        return result.choices[0].message.content

    def __getCompletion(self, content: str):
        self.__messages = [*self.__messages, 
            {
                "role": "user",
                "content": content
            }
        ]
        return self.__client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages= self.__messages
        )
