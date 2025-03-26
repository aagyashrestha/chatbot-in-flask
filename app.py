# Import necessary libraries
from flask import Flask, request, jsonify  # Flask is a web framework for creating APIs; 'request' handles incoming HTTP requests; 'jsonify' is used to send JSON responses.
from flask_cors import CORS  # CORS is a library to handle Cross-Origin Resource Sharing, allowing different domains to access the API.
import openai  # OpenAI is the library used to interact with GPT-3.5 and send requests to OpenAI’s API.
import json  # JSON module is used to parse and handle JSON data.
import os  # The os module allows interaction with the operating system, such as checking if files exist.

# Initialize the Flask application
app = Flask(__name__)  # Create a new instance of the Flask app, which will handle web requests.

# Enable Cross-Origin Resource Sharing (CORS) for all origins
CORS(app)  # Enable CORS so the app can handle requests from any external domain (useful for front-end applications).

# OpenAI API Key (replace this with your actual API key)
OPENAI_API_KEY = ""  # This key allows us to authenticate with the OpenAI API.

# Maximum number of memory exchanges to keep (7 exchanges = 14 messages)
MAX_MEMORY = 7  # Specifies that the bot will remember the last 7 exchanges (14 messages, user + assistant).

# Path to the file where chat history will be stored
CHAT_HISTORY_FILE = "chat_history.json"  # Path to the file that will store chat history (in JSON format).

# Function to load chat history from the file
def load_chat_history():
    """Load the chat history from a JSON file."""
    # Check if the history file exists
    if os.path.exists(CHAT_HISTORY_FILE):  # If the chat history file exists
        # If it exists, open the file and load its content
        with open(CHAT_HISTORY_FILE, "r") as file:  # Open the file in read mode
            return json.load(file)  # Parse and return the content of the file (which is JSON).
    # Return an empty dictionary if the file doesn't exist
    return {}  # If the file doesn't exist, return an empty dictionary (no chat history).

# Function to save chat history to the file
def save_chat_history(history):
    """Save the chat history to a JSON file."""
    # Open the chat history file in write mode and save the current history
    with open(CHAT_HISTORY_FILE, "w") as file:  # Open the file in write mode
        json.dump(history, file)  # Convert the history to JSON format and save it to the file.

# Route for the root URL ('/')
@app.route('/')
def index():
    # Display a welcome message at the root URL
    return "Welcome to the Chatbot API! Please use the /chat endpoint to interact with the chatbot."  # Basic message when visiting the root URL.

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
@app.route("/chat", methods=["POST"])  # This is the route that handles POST requests at '/chat' endpoint.
def chatbot():
    # Get the JSON data from the incoming request
    data = request.get_json()  # Flask's 'request' object allows us to retrieve the data sent in the POST request as a Python dictionary.
    
    # Extract user_id and message from the data
    user_id = data.get("user_id")  # Get the 'user_id' field from the incoming JSON data
    user_message = data.get("message")  # Get the 'message' field from the incoming JSON data

    # Check if both user_id and message are provided, else return an error
    if not user_id or not user_message:  # Check if either user_id or message is missing in the request
        return jsonify({"error": "user_id and message are required"}), 400  # If any field is missing, send a 400 error with an explanation.

    # Load the chat history from the file
    chat_history = load_chat_history()  # Call the 'load_chat_history' function to retrieve the existing chat history from the file.

    # Check if this user has any chat history, if not create an empty list for them
    if user_id not in chat_history:  # If this user doesn't have chat history (i.e., they are a new user)
        chat_history[user_id] = []  # Create a new empty list to hold this user's conversation history.

    # Append the user's message to their chat history
    chat_history[user_id].append({"role": "user", "content": user_message})  # Add the user's message to the chat history (with 'role' as 'user').

    # Trim the history to keep only the last 7 exchanges (14 messages)
    chat_history[user_id] = chat_history[user_id][-MAX_MEMORY * 2:]  # Ensure that we only keep the last 7 exchanges (14 messages: user + assistant).

    # Call OpenAI's API to get a response from the chatbot
    try:
        # Initialize the OpenAI client with the API key
        client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Create an instance of the OpenAI API client using the API key.

        # Make the API call to get a response from the chatbot based on the current chat history
        response = client.chat.completions.create(  # Use OpenAI's API to get a chat completion response.
            model="gpt-3.5-turbo",  # Use the "gpt-3.5-turbo" model (a version of GPT-3).
            messages=chat_history[user_id]  # Provide the chat history for this user as context for the model.
        )

        # Extract the chatbot's reply from the API response
        bot_reply = response.choices[0].message.content  # The API response contains a list of choices; get the first choice's content (the bot's reply).

        # Append the bot's reply to the user's chat history
        chat_history[user_id].append({"role": "assistant", "content": bot_reply})  # Add the bot's response to the chat history (with 'role' as 'assistant').

        # Save the updated chat history back to the file
        save_chat_history(chat_history)  # Save the updated chat history to the file.

        # Return the bot's reply along with the updated chat history in the response
        return jsonify({"reply": bot_reply, "history": chat_history[user_id]})  # Return the bot's reply and the updated history as a JSON response.

    except Exception as e:  # If there's an error in the OpenAI API request
        # If there's an error, return the error message
        return jsonify({"error": str(e)}), 500  # Return a 500 error with the exception message.

# Start the Flask application when the script is run
if __name__ == "__main__":
    # Run the Flask application in debug mode
    app.run(debug=True)  # Start the Flask app in debug mode, allowing for automatic reloads and easier troubleshooting.
