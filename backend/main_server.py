import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import openai

# المسارات للمجلدات
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "../templates")
STATIC_DIR = os.path.join(BASE_DIR, "../frontend/static")

# إنشاء تطبيق Flask مع تحديد مسارات القوالب والستاتيك
app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

# مفتاح OpenAI من المتغيرات البيئية
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question")
    
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # على Render يجب استخدام port من env
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
