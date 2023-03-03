from chatbot import SummarySession
from newspaper import Article

if __name__ == '__main__':
    summary_session = SummarySession()
    url = input("Please input url\n")
    article = Article(url, language='zh')
    article.download()
    article.parse()
    print(article.text)
    summary_session._summarize(article.text)