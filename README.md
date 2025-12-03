# AI Companion - Memory Extraction & Personality Engine

A simple web app that extracts user memories from chat messages and applies different personality tones to AI responses.

⚠️ Deployment Note

This project is hosted on Render’s free tier.
If the backend has been idle for a while, Render puts the server to sleep.
When it wakes up, the first request may take 20–30 seconds to load.
After the initial spin-up, everything works normally.

A background uptime monitor keeps the service warm, but occasional delays are still expected on the free tier.

## What it does

1. **Memory Extraction** - Give it 30 chat messages and it pulls out:
   - User preferences (likes/dislikes)
   - Emotional patterns
   - Important facts

2. **Personality Engine** - Takes a message and transforms the AI response based on tone:
   - Calm Mentor
   - Witty Friend
   - Therapist

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
export OPENAI_API_KEY="your-api-key-here"
python app.py
```

Server runs on http://localhost:5000

### Frontend

Just open `frontend/index.html` in your browser. Or use a simple server:

```bash
cd frontend
python -m http.server 8080
```

Then go to http://localhost:8080

## API Endpoints

### POST /extract_memory

Request:
```json
{
  "messages": ["message 1", "message 2", "..."]
}
```

Response:
```json
{
  "preferences": ["..."],
  "emotional_patterns": ["..."],
  "facts": ["..."]
}
```

### POST /apply_personality

Request:
```json
{
  "message": "I'm feeling stressed",
  "tone": "calm mentor"
}
```

Response:
```json
{
  "original_message": "...",
  "before": "basic response",
  "after": "response with personality",
  "tone": "calm mentor"
}
```

## Deployment

### Render (Backend)

1. Push to GitHub
2. Create new Web Service on Render
3. Set root directory to `backend`
4. Add environment variable `OPENAI_API_KEY`
5. Start command: `gunicorn app:app`

### Vercel/Netlify (Frontend)

1. Set root directory to `frontend`
2. Deploy as static site
3. Update `API_URL` in index.html to point to your backend

## Tech Stack

- Backend: Flask (Python)
- Frontend: Plain HTML/CSS/JS
- LLM: OpenAI GPT-3.5

## Notes

- You need an OpenAI API key to run this
- The app doesn't store any data
- Keep your API key secret!
