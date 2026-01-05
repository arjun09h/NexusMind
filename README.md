# NexusMind



Core Features

Real-time Chat Interface: A clean, modern chat window built with HTML, CSS, and JavaScript.

Fact-Checking: Integrates with the Wikipedia API for factual, encyclopedic knowledge.

Conversational AI: Uses a local Ollama model for conversation, creative tasks, and general-purpose questions.

Intelligent Router: The backend "brain" that decides which tool is best for the user's query.

The Team

Frontend Lead: [Ansh Mehra]

Backend Lead: [Arjun Singh]


Tech Stack

Frontend: HTML5, CSS3 (Flexbox), Vanilla JavaScript (ES6+ Fetch)

Backend: Python 3, Flask, Flask-CORS

Tools: 


Project Structure

NexusMind/
│
├── app.py            # Backend Lead: The main Flask server
│
├── backend/
│   └── chatbot.py      # Tools Lead: The "brain" & logic router
│
├── static/
│   ├── styles.css    # Frontend Lead: All app styling
│   └── script.js     # Frontend Lead: All app interactivity
│
└── templates/
    └── index.html    # Frontend Lead: The chat window structure
