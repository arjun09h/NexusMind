import wikipedia
import sqlite3
from datetime import datetime


DB_NAME = "chat.db"

CONTROL_WORDS = {
    "tell", "me", "please", "can", "you", "could",
    "from", "about", "on", "regarding",
    "wiki", "wikipedia",
    "what", "is", "are", "was", "were",
    "give", "explain", "information", "details",
    "something", "some", "the", "a", "an"
}

def get_db_connection():
    return sqlite3.connect(DB_NAME)

def extract_topic(message: str) -> str:
    words = message.lower().split()

    topic_words = [word for word in words if word not in CONTROL_WORDS]

    return " ".join(topic_words)

def get_cached_summary(topic: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT summary FROM wiki_cache WHERE topic = ?",
        (topic,)
    )
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_to_cache(topic: str, summary: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO wiki_cache (topic, summary, timestamp) VALUES (?, ?, ?)",
        (topic, summary, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()  



def get_reply(user_message: str) -> str:
    message_lower = user_message.lower()

    # -------- Wikipedia mode --------
    if "wiki" in message_lower or "wikipedia" in message_lower:
        topic = extract_topic(user_message).strip().lower()

        if not topic:
            return "Please tell me what you want to search on Wikipedia."
        
        cached = get_cached_summary(topic)
        if cached:
            return cached
        try:
            summary = wikipedia.summary(topic, sentences=3)
            save_to_cache(topic, summary)
            return summary

        except wikipedia.exceptions.DisambiguationError:
            return f"The topic '{topic}' is too broad. Please be more specific."

        except wikipedia.exceptions.PageError:
            return f"I couldn't find anything on Wikipedia for '{topic}'."

        except Exception:
            return "Something went wrong while searching Wikipedia."

    # -------- Default responses --------
    responses = {
        "hi": "Hello! How can I help you?",
        "how are you?": "I'm doing great 😊",
        "what is your name?": "I'm ChatBot, your virtual assistant.",
        "bye": "Goodbye! Have a nice day!"
    }

    return responses.get(message_lower, "I don't understand that.")
