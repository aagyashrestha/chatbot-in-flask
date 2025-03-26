# Chatbot API using Flask & OpenAI

This is a simple chatbot API built using Flask that integrates with OpenAI's GPT-3.5-turbo model to provide conversational responses. The chatbot maintains user-specific conversation history and supports context retention.


## Features

- Uses OpenAI's GPT-3.5-turbo model to generate responses.

- Stores user-specific conversation history.

- Supports Cross-Origin Resource Sharing (CORS) for external access.

- Limits memory to the last 7 exchanges (14 messages total).

- Simple REST API with JSON-based communication.


## Installation & Setup

### 1. Clone the Repository

```bash

git clone https://github.com/your-username/chatbot-api.git

cd chatbot-api

```

### 2. Create a Virtual Environment (Optional)

```bash

python -m venv venv

source venv/bin/activate   # On macOS/Linux

venv\Scripts\activate      # On Windows

```

### 3. Install Dependencies

```bash

pip install -r requirements.txt

```

### 4. Set Up Environment Variables

Replace `<your-api-key>` with your actual OpenAI API key.

```bash

export OPENAI_API_KEY="<your-api-key>"   # macOS/Linux

set OPENAI_API_KEY="<your-api-key>"      # Windows

```

Alternatively, update the `OPENAI_API_KEY` variable in `app.py`.

### 5. Run the Flask Application

```bash

python app.py

```

By default, the API will be available at:

📌 [http://localhost:5000/](http://localhost:5000/)


## API Endpoints

### 1. Welcome Route

**GET /**

Displays a welcome message.

**Response:**

```json

"Welcome to the Chatbot API! Please use the /chat endpoint to interact with the chatbot."

```

### 2. Chatbot Interaction

**POST /chat**

Processes user messages and returns chatbot responses.

**Request Body:**

```json

{

  "user_id": "user123",

  "message": "Hello, how are you?"

}

```

**Response Example:**

```json

{

  "reply": "I'm just a chatbot, but I'm here to help!",

  "history": [

    {"role": "user", "content": "Hello, how are you?"},

    {"role": "assistant", "content": "I'm just a chatbot, but I'm here to help!"}

  ]

}

```


## Project Structure

```bash

/chatbot-api

│── app.py                 # Main Flask app

│── chat_history.json      # Stores user chat history

│── requirements.txt       # Dependencies

│── README.md              # Project documentation

```


## Dependencies

- Flask

- Flask-CORS

- OpenAI

- JSON

- OS

Install them using:

```bash

pip install -r requirements.txt

```


## Security Considerations

- Never expose your OpenAI API key in public repositories.

- Use environment variables to store sensitive information.

- Limit request rates to prevent excessive API usage.


## Future Improvements

- Add authentication to restrict access.

- Implement a database for persistent chat storage.

- Deploy on a cloud server for scalability.

