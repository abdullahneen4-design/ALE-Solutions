from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import openai

# Initialize Flask app
app = Flask(__name__, template_folder="../templates", static_folder="../frontend/static")
CORS(app)

# Set OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Home route - serve frontend
@app.route("/")
def home():
    return render_template("index.html")

# Chatbot endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}],
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("OpenAI Error:", e)
        reply = "Fel vid anslutning till AI-tjänsten."

    return jsonify({"reply": reply})

# Consultation form endpoint
@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    # هنا ممكن تضيف تخزين البيانات أو إرسال إيميل
    print(f"Konsultation: {name}, {email}, {phone}, {message}")

    return jsonify({"reply": "Tack! Vi kontaktar dig snart."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
