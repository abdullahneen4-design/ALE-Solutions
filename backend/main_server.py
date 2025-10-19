from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ OPENAI_API_KEY hittades inte i .env")

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
Du är en AI-assistent för ALE Solutions.
Dina uppgifter:
- Du får ENDAST prata om ALE Solutions och dess tjänster.
- Våra tjänster är:
  1. AI-baserad kundsupport
  2. Automatisering av arbetsflöden
  3. AI-baserade bokningssystem
- Om en användare frågar om något utanför dessa tjänster, svara:
  "Tyvärr, jag kan bara hjälpa till med våra tjänster."
- Var professionell, tydlig och hjälpsam.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Ingen meddelande skickat"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
        )
        answer = response.choices[0].message.content
        return jsonify({"reply": answer})
    except Exception as e:
        print("❌ Exception:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/consultation", methods=["POST"])
def consultation():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    message = data.get("message")

    # في مشروع حقيقي هون ممكن ترسل ايميل أو تحفظ بالـ DB
    print(f"📩 Ny konsultation: {name}, {email}, {phone}, {message}")
    return jsonify({"success": True, "reply": "Tack! Vi kontaktar dig snart."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
