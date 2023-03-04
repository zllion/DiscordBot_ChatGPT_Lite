from chatbot import SummarySession
# Load the web page content using requests

if __name__ == '__main__':
    summary_session = SummarySession()
    url = input("Please input url\n")
    summary_session.summarize(url)