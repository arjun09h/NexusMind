from flask import Flask, render_template, jsonify, request
from backend import chatbot
from groq import Groq
import sqlite3
import os
from datetime import datetime

# ------------------ App setup ------------------

app = Flask(__name__)
DB_NAME = "chat.db"

# ------------------ Groq client ------------------

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY is not set")

# ------------------ Conversation Memory ------------------

conversation_memory = []
MAX_MEMORY = 6  # last 6 messages (user + assistant)

def add_to_memory(role, content):
    conversation_memory.append({
        "role": role,
        "content": content
    })
    if len(conversation_memory) > MAX_MEMORY:
        conversation_memory.pop(0)

def clear_memory():
    conversation_memory.clear()

# ------------------ Database helpers ------------------

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wiki_cache (
            topic TEXT PRIMARY KEY,
            summary TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

# ------------------ Groq helper ------------------

def ask_groq(memory):
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful conversational assistant. "
                    "Use previous context to answer follow-up questions. "
                    "Resolve pronouns like 'his', 'her', or 'that' from context. "
                    "Answer clearly and concisely."
                )
            }
        ] + memory,
        temperature=0.3
    )

    return response.choices[0].message.content


# ------------------ Routes ------------------

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    # New Wikipedia topic → reset context
    if "wiki" in user_message.lower() or "wikipedia" in user_message.lower():
        clear_memory()

    # Store user message in memory
    add_to_memory("user", user_message)

    # Decide who answers
    if "wiki" in user_message.lower() or "wikipedia" in user_message.lower():
        reply = chatbot.get_reply(user_message)
    else:
        reply = ask_groq(conversation_memory)

    # Store bot reply in memory
    add_to_memory("assistant", reply)

    # Save chat to DB
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO chats (sender, message, timestamp) VALUES (?, ?, ?)",
        ("user", user_message, timestamp)
    )
    cursor.execute(
        "INSERT INTO chats (sender, message, timestamp) VALUES (?, ?, ?)",
        ("bot", reply, timestamp)
    )

    conn.commit()
    conn.close()

    return jsonify({"reply": reply})

# ------------------ App start ------------------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
