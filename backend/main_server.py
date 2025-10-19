from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai

# تحميل ملف .env
load_dotenv()

# مفتاح OpenAI من البيئة
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ لم يتم العثور على OPENAI_API_KEY في البيئة")

# تعيين المفتاح للمكتبة
openai.api_key = api_key

# تهيئة السيرفر
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "🚀 Backend is running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")

        if not message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ]
        )

        reply = response.choices[0].message["content"]
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
