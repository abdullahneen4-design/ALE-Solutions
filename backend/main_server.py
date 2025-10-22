import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# تحديد المسارات بشكل ثابت وواضح
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../frontend/templates")
STATIC_DIR = os.path.join(BASE_DIR, "../frontend/static")

# إعداد Flask
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

# تهيئة عميل OpenAI
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# مسار البوت (لتوافق مع JavaScript الحالي)
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    
    if not message:
        return jsonify({"reply": "⚠️ Ingen text skickades."})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": message}]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Fel vid anslutning till AI-tjänsten: {str(e)}"})

# نموذج الاستشارة (form)
@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    if not all([name, email, phone, message]):
        return jsonify({"reply": "⚠️ Vänligen fyll i alla fält."})

    # رسالة افتراضية بعد إرسال الاستشارة
    return jsonify({"reply": f"Tack {name}! Vi kontaktar dig snart på {email}."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
