import os
from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

# Flask setup
app = Flask(
    __name__,
    static_folder="../frontend/static",  # مجلد JS/CSS
    template_folder="../Templates"       # مجلد HTML
)
CORS(app)

# OpenAI client
client = OpenAI(api_key=api_key)

# Serve frontend HTML
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return render_template("HTML.index")  # ملف HTML الرئيسي

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": message}]
    )
    reply = response.choices[0].message.content
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
    return jsonify({"reply": f"Tack {name}, vi har mottagit ditt meddelande!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
