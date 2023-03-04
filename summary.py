# from newspaper import Article

url = "https://www.wikiwand.com/en/Hooded_pitohui"


import requests
from bs4 import BeautifulSoup

# Load the web page content using requests
response = requests.get(url)
html_content = response.content

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the <article> tag
article = soup.find('article')

# Extract all text under the <article> tag
article_text = article.get_text()
# Print the extracted text
import re
import jieba
from langdetect import detect

def split_article(text, snippet_size=2000, overlap=200):
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


if __name__ == '__main__':
    for i in split_article(article_text,snippet_size=500,overlap=50):
        print(i)
        print('---------------------')


