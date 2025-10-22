import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# تحديد المسارات للمجلدات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../templates")
STATIC_DIR = os.path.join(BASE_DIR, "../frontend/static")

# إعداد تطبيق Flask
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

# مفتاح OpenAI من المتغيرات البيئية
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

# 🔹 بوت الشركة المخصص
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"reply": "⚠️ Ingen text skickades."})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Du är ALE Solutions' AI-assistent. "
                        "Du representerar företaget och svarar alltid professionellt på svenska. "
                        "ALE Solutions erbjuder AI-baserade lösningar, automation och smarta bokningssystem. "
                        "När användaren ställer frågor ska du presentera företagets tjänster, hur ni kan hjälpa till, "
                        "och ge ett trevligt, kortfattat svar i marknadsföringsstil. "
                        "Undvik att prata om ämnen utanför företaget."
                    ),
                },
                {"role": "user", "content": message},
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Fel vid anslutning till AI-tjänsten: {str(e)}"})

# 🔹 نقطة الاتصال لاستشارات الموقع
@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.get_json()
    name = data.get("name", "")
    email = data.get("email", "")
    phone = data.get("phone", "")
    message = data.get("message", "")

    reply = (
        f"Tack {name}! Vi har mottagit din förfrågan. "
        "Vårt team kommer att kontakta dig inom kort för en kostnadsfri konsultation. "
        "Hälsningar, ALE Solutions-teamet."
    )
    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
