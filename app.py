# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import json
import os

# Initialize the Flask application
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) for all origins
CORS(app)

# OpenAI API Key (replace this with your actual API key)
OPENAI_API_KEY = ""

# Maximum number of memory exchanges to keep (7 exchanges = 14 messages)
MAX_MEMORY = 7

# Path to the file where chat history will be stored
CHAT_HISTORY_FILE = "chat_history.json"


def load_chat_history():
    """Load the chat history from a JSON file."""
    # Check if the history file exists
    if os.path.exists(CHAT_HISTORY_FILE):
        # If it exists, open the file and load its content
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    # Return an empty dictionary if the file doesn't exist
    return {}


def save_chat_history(history):
    """Save the chat history to a JSON file."""
    # Open the chat history file in write mode and save the current history
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(history, file)


# Route for the root URL ('/')
@app.route('/')
def index():
    # Display a welcome message at the root URL
    return "Welcome to the Chatbot API! Please use the /chat endpoint to interact with the chatbot."


# API endpoint for chat interaction. The API accepts POST requests at '/chat'.
# - URL: http://localhost:5000/chat (when running locally)
# - Method: POST
# - Expected input: A JSON object with `user_id` (string) and `message` (string).
# Example request:
# {
#   "user_id": "user123",
#   "message": "Hello, how are you?"
# }
# The response will include the chatbot's reply and the updated chat history.
@app.route("/chat", methods=["POST"])
def chatbot():
    # Get the JSON data from the incoming request
    data = request.get_json()
    
    # Extract user_id and message from the data
    user_id = data.get("user_id")
    user_message = data.get("message")

    # Check if both user_id and message are provided, else return an error
    if not user_id or not user_message:
        return jsonify({"error": "user_id and message are required"}), 400

    # Load the chat history from the file
    chat_history = load_chat_history()

    # Check if this user has any chat history, if not create an empty list for them
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Append the user's message to their chat history
    chat_history[user_id].append({"role": "user", "content": user_message})

    # Trim the history to keep only the last 7 exchanges (14 messages)
    chat_history[user_id] = chat_history[user_id][-MAX_MEMORY * 2:]

    # Call OpenAI's API to get a response from the chatbot
    try:
        # Initialize the OpenAI client with the API key
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Make the API call to get a response from the chatbot based on the current chat history
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Model to use for chat completion
            messages=chat_history[user_id]  # The chat history for the user
        )

        # Extract the chatbot's reply from the API response
        bot_reply = response.choices[0].message.content

        # Append the bot's reply to the user's chat history
        chat_history[user_id].append({"role": "assistant", "content": bot_reply})

        # Save the updated chat history back to the file
        save_chat_history(chat_history)

        # Return the bot's reply along with the updated chat history in the response
        return jsonify({"reply": bot_reply, "history": chat_history[user_id]})

    except Exception as e:
        # If there's an error, return the error message
        return jsonify({"error": str(e)}), 500


# Start the Flask application when the script is run
if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)
