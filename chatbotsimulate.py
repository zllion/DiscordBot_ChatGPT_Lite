from chatbot import ChatSession


if __name__ == '__main__':
    chat_session = ChatSession()
    user_input = input("Please enter your first prompt\n")
    while chat_session.token_used_total<10000:
        chat_session.chat(user_input)
        user_input = input("Next prompt\n")
