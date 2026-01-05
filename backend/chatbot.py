def get_reply(user_message):
    responses = {
        "hi": "Hello! How can I help you?",
        "how are you?": "I'm doing great 😊",
        "what is your name?":"I'm ChatBot, your virtual assistant.",
        "bye": "Goodbye! Have a nice day!"
    }

    return responses.get(user_message.lower(), "I don't understand that.")
