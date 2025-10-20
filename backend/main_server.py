from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import openai

app = Flask(__name__, static_folder="../frontend")
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key  # الطريقة القديمة المستقرة

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.get_json()
    # هنا ممكن تحفظ البيانات أو تبعت إيميل
    return jsonify({"reply": "Tack! Vi har mottagit din förfrågan."})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
