# AI Setup — HoopRater & SmashRater

Uses Groq — 100% free, no credit card, responses in ~1 second.

## Setup (2 minutes)

1. Go to https://console.groq.com and sign up (free, no card needed)
2. Click "API Keys" -> "Create API Key" -> copy the key
3. Open Command Prompt and run:

    set GROQ_API_KEY=your-key-here

4. Run the app as normal:

    venv\Scripts\activate
    python app.py

To make it permanent so you don't have to set it every time:
- Windows Start -> search "Environment Variables"
- New User Variable: Name = GROQ_API_KEY, Value = your key

## Free tier limits
- 30 requests per minute
- 14,400 requests per day
- No cost ever (unless you choose to upgrade)

## Optional fallback
If you have Ollama installed locally, the app will use that
automatically if GROQ_API_KEY is not set.
