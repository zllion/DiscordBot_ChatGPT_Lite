import openai
import os
from dotenv import load_dotenv
import datetime
import yaml
import uuid


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
        self.session_id = str(uuid.uuid4())[:8]

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
        print(content)
        print("session_token:",token_used, "total_token_used:",self.token_used_total)
        return content
    
    def _create_folder(self,folder_path):
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"Created folder: {folder_path}")

    def save(self,user):
        folder_path = f'./data/{user.id}'
        self._create_folder(folder_path)
        with open(f'{folder_path}/{self.session_id}.yaml','w') as f:
            yaml.dump({'author':{'name':user.name,'id':user.id},
                       'date':datetime.datetime.now(),
                       'type':'chat',
                       'token':self.current_token,
                       'total_token':self.token_used_total,
                       'messages':self.messages}, f)
        print('Session Saved')
    
    def load(self,user,session_id):
        folder_path = f'./data/{user.id}'
        self._create_folder(folder_path)
        try:
            with open(f'{folder_path}/{session_id}.yaml', 'r') as f:
                data = yaml.load(f, Loader=yaml.FullLoader) 
        except Exception as e:
            print(e)
            return 'Invalid Session id'
        self.session_id = session_id
        self.messages = data['messages']
        self.current_token = data['token']
        self.token_used_total = data['total_token']

        return 'Load Sucess!'
