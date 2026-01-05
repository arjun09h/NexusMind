from flask import Flask, render_template,url_for,jsonify,request
from backend import chatbot
import sqlite3
from datetime import datetime


app = Flask(__name__)
DB_NAME = "chat.db"

# ---------- Database helper ----------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------- Create table ----------
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

# ---------- Routes ----------

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")


@app.route('/chat', methods = ["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    # Get bot reply from backend logic
    reply = chatbot.get_reply(user_message)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Store both messages in SQLite
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

# ---------- App start ----------

if __name__ == "__main__":
    init_db()
    app.run(debug=True)