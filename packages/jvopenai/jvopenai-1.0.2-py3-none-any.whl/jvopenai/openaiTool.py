from openai import OpenAI
from jvcore import getConfig

class OpenAITool: #todo 0 a method to continue conversation and start a new converation (singleton vs transient?)
    def __init__(self) -> None:
        accessKey = getConfig().get('openai','accessKey')
        self.__client = OpenAI(api_key=accessKey)
    
    def completion(self, request: str) -> str:
        result = self.__client.chat.completions.create(
            model="gpt-3.5-turbo", 
            messages=[
                {
                    "role": "user",
                    "content": request
                }
            ]
        )
        return result.choices[0].message.content
