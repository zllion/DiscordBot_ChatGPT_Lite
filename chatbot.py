import openai
import os
from dotenv import load_dotenv
import datetime
import yaml
import uuid
import re
import requests
from bs4 import BeautifulSoup
import jieba
from langdetect import detect

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def is_url(input_string):
    url_pattern = re.compile(r'^https?://\S+$')
    return url_pattern.match(input_string) is not None

def split_article(text, snippet_size=1500, overlap=100):
    # split the text into words
    lang = detect(text)
    ## TODO: improve tokenization
    if lang == 'en':
        words = re.findall(r'\b\w+\b', text)
    elif lang == 'zh-cn' or lang == 'zh-tw':
        words = jieba.lcut(text)
    # split the words into snippets of the desired size
    snippets = []
    i = 0
    while i < len(words)-overlap:
        s = words[i:i+snippet_size]
        if lang == 'en':
            snippets.append(' '.join(s))
        elif lang == 'zh-cn' or lang == 'zh-tw':
            snippets.append(''.join(s))
        i += snippet_size-overlap
    return snippets

def get_article_from_url(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    article = soup.find('article')
    return article.get_text()

class Session():
    def __init__(self) -> None:
        self.token_used_total = 0
        self.current_token = 0
        self.session_id = str(uuid.uuid4())[:8]
    
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
        with open(f'{folder_path}/{session_id}.yaml', 'r') as f:
            data = yaml.load(f, Loader=yaml.FullLoader) 
        self.session_id = session_id
        self.messages = data['messages']
        self.current_token = data['token']
        self.token_used_total = data['total_token']

class ChatSession(Session):
    def __init__(self) -> None:
        super().__init__()
        with open('chat.prompt','r') as f:
            self.system_content = f.read()
        self.messages = [{"role":"system", "content":self.system_content}]

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
    
class SummarySession(Session):
    def __init__(self) -> None:
        super().__init__()
        with open('summary.prompt','r') as f:
            self.system_content = f.read()
        self.messages = [{"role":"system", "content":self.system_content}]
        self.summary = []
    def _summarize(self,text):
        self.messages.append({"role": "user", "content": text})
        working_messages = [{"role":"system", "content":self.system_content}]
        working_messages.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = working_messages
        )
        token_used =int(response["usage"]["total_tokens"])
        self.current_token = token_used
        content = response["choices"][0]['message']["content"]
        self.token_used_total += token_used
        self.messages.append({"role": "assistant", "content":content})
        self.summary.append(content)
        print(content)
        print("session_token:",token_used, "total_token_used:",self.token_used_total)
        return content
    
    def summarize(self,t):
        if is_url(t):
            text = get_article_from_url(t)
        else:
            text = t
        snippets = split_article(text)
        for s in snippets:
            self._summarize(s)
        return '\n'.join(self.summary)
