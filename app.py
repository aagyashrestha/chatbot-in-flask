from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai
import json
import os

app = Flask(__name__)
CORS(app)  # Allow frontend requests

# OpenAI API Key
OPENAI_API_KEY = ""

# Max memory (7 exchanges → 14 messages)
MAX_MEMORY = 7

# Storage for chat history (could be replaced with a database)
CHAT_HISTORY_FILE = "chat_history.json"


def load_chat_history():
    """Load chat history from a JSON file"""
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return {}


def save_chat_history(history):
    """Save chat history to a JSON file"""
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(history, file)


@app.route("/")
def chatbot_page():
    return render_template("chat.html")  # Serve the chat UI


@app.route("/chat", methods=["POST"])
def chatbot():
    data = request.get_json()
    user_id = data.get("user_id")
    user_message = data.get("message")

    if not user_id or not user_message:
        return jsonify({"error": "user_id and message are required"}), 400

    # Load chat history
    chat_history = load_chat_history()

    # Fetch or create user chat history
    if user_id not in chat_history:
        chat_history[user_id] = []

    # Append user message
    chat_history[user_id].append({"role": "user", "content": user_message})

    # Trim history to last 7 exchanges (14 messages)
    chat_history[user_id] = chat_history[user_id][-MAX_MEMORY * 2:]

    # Call OpenAI API
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=chat_history[user_id]
    )

    bot_reply = response.choices[0].message.content

    # Append bot response to history
    chat_history[user_id].append({"role": "assistant", "content": bot_reply})

    # Save updated history
    save_chat_history(chat_history)

    return jsonify({"reply": bot_reply, "history": chat_history[user_id]})


if __name__ == "__main__":
    app.run(debug=True)
