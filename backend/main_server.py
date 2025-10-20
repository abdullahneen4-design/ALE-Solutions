import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import openai

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../templates")
STATIC_DIR = os.path.join(BASE_DIR, "../frontend/static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

# OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "Fel vid anslutning till AI-tjänsten."})

@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")
    # يمكنك هنا حفظ البيانات أو إرسالها عبر إيميل
    return jsonify({"reply": f"Tack {name}, vi kontaktar dig snart!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
