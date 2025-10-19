from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"reply": "No message provided."})

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

# Consultation form endpoint
@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    # ممكن تحط هنا منطق تخزين البيانات أو إرسال إيميل
    print(f"Consultation request from {name} ({email}, {phone}): {message}")

    return jsonify({"reply": "Tack för din förfrågan! Vi återkommer snart."})

# Serve frontend
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
