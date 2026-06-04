"""
ai_agent.py — Uses Ollama with llama3.2:1b (fastest local model).
Falls back to llama3 if 1b not available.
Short, focused prompts for speed.
"""
import ollama

FAST_MODEL = "llama3.2:1b"
FALLBACK_MODEL = "llama3"

def _get_model():
    try:
        models = [m.model for m in ollama.list().models]
        if any(FAST_MODEL in m for m in models):
            return FAST_MODEL
        return FALLBACK_MODEL
    except:
        return FALLBACK_MODEL

def _chat(prompt: str) -> str:
    try:
        r = ollama.chat(model=_get_model(),
                        messages=[{"role":"user","content":prompt}],
                        options={"num_predict":300, "temperature":0.7})
        return r["message"]["content"]
    except Exception as e:
        raise RuntimeError(f"Ollama error: {e}. Make sure Ollama is running (check system tray).")

def analyze_player(stats: dict, rating: int, college: str) -> str:
    return _chat(
        f"NBA analyst: 3 short paragraphs on {stats['name']} ({stats['team']}, {stats['position']}, {rating} OVR). "
        f"Stats: {stats['pts']:.1f}pts {stats['reb']:.1f}reb {stats['ast']:.1f}ast {stats['stl']:.1f}stl "
        f"{stats['blk']:.1f}blk {stats['fg_pct']*100:.0f}%FG {stats['fg3_pct']*100:.0f}%3PT "
        f"{stats['ts_pct']*100:.0f}%TS {stats['plus_minus']:+.1f}+/-. College: {college}. "
        f"Cover: strengths/weaknesses, is the {rating} OVR fair, bold prediction. Be direct."
    )

def parse_nl_search(query: str, all_players: list) -> list:
    import json, re
    summary = "\n".join([
        f"{p['name']}|{p['team']}|{p['position']}|OVR:{p['ovr']}|"
        f"PTS:{p['pts']:.1f}|REB:{p['reb']:.1f}|AST:{p['ast']:.1f}|"
        f"STL:{p['stl']:.1f}|BLK:{p['blk']:.1f}|FG:{p['fg_pct']*100:.0f}%|"
        f"3PT:{p['fg3_pct']*100:.0f}%|TS:{p['ts_pct']*100:.0f}%"
        for p in all_players
    ])
    text = _chat(
        f'Basketball filter. Query: "{query}"\nPlayers:\n{summary}\n'
        f'Return ONLY a JSON array of matching player names. Example: ["Player One"]\n'
        f'Rules: "best defenders"=high STL+BLK, "25+ points"=PTS>=25, "PG"=Point Guard, "efficient"=high TS%\n'
        f'Output ONLY the JSON array, nothing else.'
    ).strip()
    m = re.search(r'\[.*?\]', text, re.DOTALL)
    if m:
        try:
            names = json.loads(m.group(0))
            name_set = set(names)
            return [p for p in all_players if p["name"] in name_set]
        except: pass
    return []

def chat_with_agent(messages: list, app_context: dict) -> str:
    ctx = f"""HoopRater & SmashRater AI. Answer questions about NBA and ATP tennis.
NBA top players: {app_context.get('nba_summary','')}
Top teams: {app_context.get('teams_summary','')}
ATP top 10: {app_context.get('tennis_summary','')}
Be concise (2-3 sentences). Use real numbers."""
    enriched = list(messages)
    if enriched and enriched[0]["role"]=="user":
        enriched[0]={"role":"user","content":ctx+"\n\n"+enriched[0]["content"]}
    r = ollama.chat(model=_get_model(), messages=enriched,
                    options={"num_predict":200, "temperature":0.7})
    return r["message"]["content"]

def build_app_context(nba_leaders, teams, tennis_players):
    return {
        "nba_summary": " | ".join([f"{p['name']}({p['team']})OVR:{p['ovr']}" for p in nba_leaders[:15]]),
        "teams_summary": " | ".join([f"{t['name']}:{t['ovr']}" for t in teams[:10]]),
        "tennis_summary": " | ".join([f"#{p['rank']}{p['name']}{p['grand_slams']}GS" for p in tennis_players[:10]]),
    }

def analyze_tennis_player(player: dict) -> str:
    return _chat(
        f"Tennis analyst: 3 short paragraphs on {player['name']} (#{player['rank']} ATP, "
        f"{player['grand_slams']} Grand Slams, {player['points']} pts, age {player['age']}, "
        f"career high #{player['career_high']}). Cover: game style, is {player['rating']} SmashRater fair, "
        f"2026 prediction. Be direct and concise."
    )
