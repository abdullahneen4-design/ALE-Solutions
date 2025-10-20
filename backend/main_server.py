import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Use the new OpenAI client
from openai import OpenAI
client = OpenAI(api_key=api_key)

app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend/templates")
CORS(app)

# Route for the homepage
@app.route("/")
def index():
    return render_template("index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    # Call OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}],
            max_tokens=150
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

# Consultation form endpoint
@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.json
    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    message = data.get("message", "")

    # هنا ممكن تحط منطق حفظ البيانات أو إرسال إيميل
    reply = f"Tack {name}! Vi har mottagit ditt meddelande."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
