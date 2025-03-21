from flask import Flask, request, jsonify
import openai
import os
import markdown
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # New OpenAI client

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.json
    tos_text = data.get("text", "")[:8000]

    prompt = f"""
You are a legal assistant. Summarize the key points of this Terms of Service and list any red flags.

Text:
{tos_text}
"""

    response = client.chat.completions.create(  # NEW OpenAI API format
        model="gpt-4-turbo",
        messages=[{"role": "system", "content": "You are a legal expert summarizing Terms of Service."},
                  {"role": "user", "content": prompt}],
        temperature=0.2
    )

    full_text = response.choices[0].message.content  # Correct way to extract response

    # Cleanly separate summary and red flags
    summary, red_flags = full_text.split("Red Flags:") if "Red Flags:" in full_text else (full_text, "None found.")

    return jsonify({
        "summary": markdown.markdown(summary.strip()),  # Convert Markdown to HTML
        "redFlags": markdown.markdown(red_flags.strip())
    })

@app.route('/')
def hello():
    return "TOS Summarizer is live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)), debug=True)
