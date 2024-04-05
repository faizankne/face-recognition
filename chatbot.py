import random

# Dictionary of predefined patterns and responses
responses = {
    "hello": ["Hi!", "Hello!", "Hey!", "Hi there!"],
    "how are you": ["I'm good, thanks!", "I'm doing well, thank you!", "All good, thanks for asking!"],
    "what's your name": ["I am Chatbot!", "People call me Chatbot!", "I go by the name Chatbot!"],
    "bye": ["Goodbye!", "See you later!", "Goodbye! Have a great day!"],
    # Add more patterns and responses as needed
}

def get_response(user_input):
    for pattern, response_list in responses.items():
        if pattern in user_input.lower():
            return random.choice(response_list)
    return "I'm sorry, I don't understand that. Can you please try again?"

def main():
    print("Chatbot: Hi! I am Chatbot. How can I help you today? (type 'bye' to exit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "bye":
            print("Chatbot: Goodbye! Have a great day!")
            break
        response = get_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()
