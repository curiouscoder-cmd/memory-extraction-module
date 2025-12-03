from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# get api keys from environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyBJj5A31sKpnS8dJt2WdGG_7IAVpAlRRDo")

def call_llm(prompt):
    """simple function to call llm api (tries gemini first, then openai)"""
    
    # try gemini first
    if GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
            data = {
                "contents": [{"parts": [{"text": prompt}]}]
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            else:
                print(f"Gemini failed: {response.status_code} {response.text}")
        except Exception as e:
            print(f"Gemini failed: {e}")
    
    # fallback to openai
    if OPENAI_API_KEY:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
    
    return None


@app.route("/extract_memory", methods=["POST"])
def extract_memory():
    """takes 30 messages and extracts memory info"""
    data = request.json
    messages = data.get("messages", [])
    
    if not messages:
        return jsonify({"error": "no messages provided"}), 400
    
    # build the prompt
    messages_text = "\n".join([f"- {msg}" for msg in messages])
    
    prompt = f"""Analyze these user messages and extract:
1. User preferences (things they like/dislike)
2. Emotional patterns (how they usually feel)
3. Important facts about them

Messages:
{messages_text}

Return your response as JSON with this format:
{{
    "preferences": ["preference 1", "preference 2"],
    "emotional_patterns": ["pattern 1", "pattern 2"],
    "facts": ["fact 1", "fact 2"]
}}

Only return the JSON, nothing else."""

    result = call_llm(prompt)
    
    if result:
        # try to parse the json
        import json
        try:
            parsed = json.loads(result)
            return jsonify(parsed)
        except:
            return jsonify({"raw_response": result})
    else:
        return jsonify({"error": "failed to get response from llm"}), 500


@app.route("/apply_personality", methods=["POST"])
def apply_personality():
    """transforms a message based on chosen tone"""
    data = request.json
    message = data.get("message", "")
    tone = data.get("tone", "calm mentor")
    
    if not message:
        return jsonify({"error": "no message provided"}), 400
    
    # tone descriptions
    tones = {
        "calm mentor": "a calm, wise mentor who gives thoughtful advice",
        "witty friend": "a witty, funny friend who uses humor and casual language",
        "therapist": "a compassionate therapist who validates feelings and asks reflective questions"
    }
    
    tone_desc = tones.get(tone, tones["calm mentor"])
    
    # first get a basic response
    basic_prompt = f"Respond to this message briefly: {message}"
    basic_response = call_llm(basic_prompt)
    
    # now transform it with personality
    transform_prompt = f"""Take this response and rewrite it as {tone_desc}.

Original response: {basic_response}

Rewrite it in that style. Only return the rewritten response, nothing else."""

    transformed = call_llm(transform_prompt)
    
    return jsonify({
        "original_message": message,
        "before": basic_response,
        "after": transformed,
        "tone": tone
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
