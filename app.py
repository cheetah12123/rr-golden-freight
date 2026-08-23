import os
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from knowledge import COMPANY_DATA

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", "sk-your-actual-api-key-here"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_ai():
    user_query = request.json.get('query', '').strip()
    if not user_query:
        return jsonify({"reply": "Please enter a valid question regarding our dispatch services."})
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are the official AI Dispatch Specialist for R AND R GOLDEN FREIGHT. Answer using this knowledge base: {COMPANY_DATA}."},
                {"role": "user", "content": user_query}
            ],
            temperature=0.3
        )
        return jsonify({"reply": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"reply": "AI service is initializing. Contact Zane Davis (+92 308 5294566) or Christian David (+92 309 7981886) directly via WhatsApp."})

if __name__ == '__main__':
    app.run(debug=True)