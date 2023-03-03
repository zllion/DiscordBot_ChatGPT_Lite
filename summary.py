from newspaper import Article

url = "https://sspai.com/post/78530"
article = Article(url, language='zh')
article.download()
article.parse()
print(article.text)

