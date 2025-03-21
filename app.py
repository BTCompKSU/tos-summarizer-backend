from flask import Flask, request, jsonify
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Corrected OpenAI client setup

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    tos_text = data.get("text", "")[:8000]

    prompt = f"""
You are a legal assistant. Summarize the key points of this Terms of Service and list any red flags.

Text:
{tos_text}
"""

    response = client.chat.completions.create(  # Corrected OpenAI v1.x syntax
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    full_text = response.choices[0].message.content  # Corrected response format

    split = full_text.split("Red Flags:")
    summary = split[0].strip()
    red_flags = split[1].strip() if len(split) > 1 else "None found."

    return jsonify({
        "summary": summary,
        "redFlags": red_flags
    })

@app.route('/')
def hello():
    return "TOS Summarizer is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
