
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env (for local dev)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=env_path)

# Check if API key is loaded
api_key = os.getenv("OPENROUTER_API_KEY")
if api_key:
    print("✅ API key loaded. Starts with:", api_key[:5], "...")
else:
    print("❌ API key NOT found. Check your environment settings.")

app = Flask(__name__)
CORS(app)  # Optional: allow frontend access

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Crisis detection
    crisis_keywords = [
        "suicide", "kill myself", "end my life",
        "harm myself", "cut myself", "want to die"
    ]
    if any(keyword in user_input.lower() for keyword in crisis_keywords):
        return jsonify({
            "response": (
                "⚠️ I'm really sorry you're feeling this way. You're not alone. "
                "Please talk to someone immediately. In India, you can call the iCall helpline at 9152987821. "
                "If you're in another country, contact a local mental health or crisis helpline."
            )
        })

    # Compose messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are a supportive, calming, and emotionally intelligent mental health support assistant. "
                "You listen with compassion and validate the user's feelings without judgment. "
                "Use natural, comforting language, like a kind friend or supportive counselor — not robotic. "
                "Speak in short, clear paragraphs. Pause with gentle encouragements. "
                "Always remind the user they are not alone, and help is available. "
                "Avoid medical advice. Instead, offer helpful coping strategies, emotional support, and suggest professional help when appropriate. "
                "Be especially gentle when the user expresses distress, fear, sadness, or overwhelm. "
                "Use soft language like: 'That sounds really tough...', 'I hear you...', 'You're doing the best you can, and that's enough.'"
            )
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model":"google/gemini-pro",
        "messages": messages
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        bot_reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        bot_reply = f"⚠️ API Error: {str(e)}"

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


