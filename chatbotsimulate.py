from chatbot import Session


if __name__ == '__main__':
    user_input = input("Please enter your first prompt\n")
    chat_session = Session()
    while chat_session.token_used_total<10000:
        chat_session.chat(user_input)
        user_input = input("Next prompt\n")
