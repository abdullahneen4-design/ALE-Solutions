from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
import os

# 🧪 تحميل المتغيرات من ملف .env
load_dotenv()

# 🗝️ جلب مفتاح OpenAI من البيئة
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ لم يتم العثور على متغير OPENAI_API_KEY في البيئة.")

# 🧠 إنشاء العميل
client = OpenAI(api_key=api_key)

# 🌐 تهيئة السيرفر
app = Flask(__name__)
CORS(app)

# ✅ راوت بسيط للتجربة
@app.route("/")
def home():
    return "🚀 API is running!"

# 💬 راوت للتعامل مع ChatGPT
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "الرسالة فارغة"}), 400

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": str(e)}), 500

# 🏃 تشغيل محلي (ليس ضروري على Render)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
