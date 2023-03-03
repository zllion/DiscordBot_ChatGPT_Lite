import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
    
class Session():
    def __init__(self) -> None:
        with open('system.prompt','r') as f:
            self.system_content = f.read()
        # print(self.system_content)
        self.messages = [{"role":"system", "content":self.system_content}]
        self.token_used_total = 0
        self.current_token = 0

    def chat(self,user_input):
        self.messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = self.messages
        )
        token_used =int(response["usage"]["total_tokens"])
        self.current_token = token_used
        content = response["choices"][0]['message']["content"]
        self.token_used_total += token_used
        # memorize
        self.messages.append({"role": "assistant", "content":content})
        # print(content)
        # print("session_token:",token_used, "total_token_used:",self.token_used_total)
        return content