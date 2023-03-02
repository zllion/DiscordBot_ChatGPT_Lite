import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
    
class Session():
    def __init__(self) -> None:
        self.system_content = "You are a helpful assistant."
        self.user_content = []
        self.assistant_content = []
        self.token_used_total = 0
    def chat(self,user_input):
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=self.construct_message(user_input)
        )
        token_used =int(response["usage"]["total_tokens"])
        content = response["choices"][0]['message']["content"]
        self.token_used_total += token_used
        # memorize
        self.user_content.append(user_input)
        self.assistant_content.append(content)
        print(content)
        print("session_token:",token_used, "total_token_used:",self.token_used_total)
        return content
    def construct_message(self,user_input):
        messages = [{"role":"system", "content":self.system_content}]
        for u,a in zip(self.user_content,self.assistant_content):
            messages.append({"role": "user", "content": u})
            messages.append({"role": "assistant", "content":a})   
        messages.append({"role": "user", "content": user_input})
        print('messages',len(messages))
        return messages