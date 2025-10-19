import os
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Initialize Flask app
app = Flask(__name__, static_folder="../frontend/static", template_folder="../frontend")

# Serve frontend
@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

# Consultation form endpoint
@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.json
    # ممكن هنا تخزن البيانات أو ترسلها بإيميل
    return jsonify({"reply": "Tack! Vi återkommer snart."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
