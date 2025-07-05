from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

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

    # Chat messages with assistant context
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



    try:
        # Connect to OpenRouter
        client = openai.OpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1"
        )

        # Generate assistant reply
        response = client.chat.completions.create(
            model="mistralai/mixtral-8x7b-instruct",  # You can also use: mistralai/mixtral-8x7b-instruct
            messages=messages
        )
        bot_reply = response.choices[0].message.content

    except Exception as e:
        print("OpenRouter Error:", e)
        bot_reply = "Sorry, I'm having trouble responding right now. Please try again later."

    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

