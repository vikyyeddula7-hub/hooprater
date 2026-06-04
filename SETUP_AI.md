# HoopRater / SmashRater — AI Setup (Free, Local)

All AI features use Ollama — 100% free, runs on your computer, no API key needed.

## One-Time Setup

**1. Install Ollama**
Download from https://ollama.com and run the installer.
Ollama will start automatically in the background after install.

**2. Open Command Prompt and download the AI model (~4GB, one time only):**
```
ollama pull llama3
```

**3. Install the Python library (inside your nba_rater folder):**
```
venv\Scripts\activate
pip install ollama
```

**4. Run the app as normal:**
```
python app.py
```

The AI features will now work — look for the purple 🤖 buttons on player pages
and the chat widget in the bottom-right corner.

---

## Troubleshooting

**"Ollama error" on the website:**
- Make sure the Ollama app is running (check your system tray near the clock)
- If it's not running, open the Ollama app from your Start menu

**Slow responses:**
- llama3 can take 10-30 seconds on older machines — this is normal
- For a faster (but less capable) model, run: ollama pull llama3.2:1b
  Then change "llama3" to "llama3.2:1b" in ai_agent.py

---

## AI Features

| Feature | Where to find it |
|---|---|
| AI Player Analysis | Any NBA or tennis player page → purple "Generate AI Analysis" button |
| Natural Language Search | NBA ratings homepage → AI search bar above the player grid |
| Chat Widget | 🤖 button in bottom-right corner on every page |
| Auto-Update NBA Rosters | Run: python update_rosters.py |
| Auto-Update ATP Rankings | Run: python update_tennis.py |
