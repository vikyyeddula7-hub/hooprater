import math, os
from flask import Flask, render_template, request, jsonify
import rating_engine
from rating_engine import compute_rating, get_rating_breakdown, rating_tier
from data_fetcher import fetch_player_stats, search_players, get_season_leaders, _resolve_ovr
from colleges import get_college
from tennis_data import ATP_PLAYERS, ATP_BY_RANK

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "hooprater-dev-2026")

TEAM_COLORS = {
    "Atlanta Hawks":"#E03A3E","Boston Celtics":"#007A33","Brooklyn Nets":"#000000",
    "Charlotte Hornets":"#1D1160","Chicago Bulls":"#CE1141","Cleveland Cavaliers":"#860038",
    "Dallas Mavericks":"#00538C","Denver Nuggets":"#0E2240","Detroit Pistons":"#C8102E",
    "Golden State Warriors":"#1D428A","Houston Rockets":"#CE1141","Indiana Pacers":"#002D62",
    "Los Angeles Clippers":"#C8102E","Los Angeles Lakers":"#552583","Memphis Grizzlies":"#5D76A9",
    "Miami Heat":"#98002E","Milwaukee Bucks":"#00471B","Minnesota Timberwolves":"#0C2340",
    "New Orleans Pelicans":"#0C2340","New York Knicks":"#006BB6","Oklahoma City Thunder":"#007AC1",
    "Orlando Magic":"#0077C0","Philadelphia 76ers":"#006BB6","Phoenix Suns":"#1D1160",
    "Portland Trail Blazers":"#E03A3E","Sacramento Kings":"#5A2D81","San Antonio Spurs":"#C4CED4",
    "Toronto Raptors":"#CE1141","Utah Jazz":"#002B5C","Washington Wizards":"#002B5C",
}

@app.context_processor
def inject_globals():
    return {"rating_engine": rating_engine}

@app.template_global()
def team_color(n): return TEAM_COLORS.get(n,"#e8523a")

@app.template_global()
def context_note(value, stat_key, invert=False):
    from rating_engine import LEAGUE_AVGS, z as zscore
    avg = LEAGUE_AVGS.get(stat_key)
    if avg is None: return "–"
    zv = zscore(stat_key, value)
    if invert: zv = -zv
    if zv>=2.0: return "Elite"
    elif zv>=1.2: return "Above avg"
    elif zv>=0.3: return "Solid"
    elif zv>=-0.3: return f"Avg (~{avg:.1f})"
    elif zv>=-1.2: return "Below avg"
    else: return "Well below avg"

@app.template_global()
def bar_color(val):
    if val>=90: return "#FFD700"
    elif val>=80: return "#4FC3F7"
    elif val>=70: return "#81C784"
    elif val>=60: return "#FFA726"
    else: return "#EF5350"

def ai_available(): return True

# ── Basketball routes ─────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", leaders=get_season_leaders(), ai_available=ai_available())

@app.route("/player/<int:player_id>")
def player_detail(player_id):
    stats = fetch_player_stats(player_id)
    if not stats: return "Player not found", 404
    rating = _resolve_ovr(stats["name"], stats)
    breakdown = get_rating_breakdown(stats, stats.get("name"))
    college = get_college(stats["name"])
    return render_template("player.html", stats=stats, rating=rating,
                           breakdown=breakdown, college=college, ai_available=ai_available())

@app.route("/teams")
def teams():
    from teams_data import get_all_teams
    return render_template("teams.html", teams=get_all_teams())

@app.route("/compare")
def compare():
    return render_template("compare.html")

@app.route("/api/search")
def api_search():
    q = request.args.get("q","").strip()
    if len(q)<2: return jsonify([])
    return jsonify(search_players(q))

@app.route("/api/player/<int:player_id>")
def api_player(player_id):
    stats = fetch_player_stats(player_id)
    if not stats: return jsonify({"error":"Not found"}),404
    rating = _resolve_ovr(stats["name"],stats)
    return jsonify({"stats":stats,"rating":rating,
                    "breakdown":get_rating_breakdown(stats,stats.get("name")),
                    "tier":rating_tier(rating)})

# ── AI routes ─────────────────────────────────────────────────────────────────
@app.route("/api/ai/analyze_player/<int:player_id>")
def ai_analyze_player(player_id):
    stats = fetch_player_stats(player_id)
    if not stats: return jsonify({"error":"Player not found"}),404
    rating = _resolve_ovr(stats["name"], stats)
    college = get_college(stats["name"])
    try:
        from ai_agent import analyze_player
        return jsonify({"analysis": analyze_player(stats, rating, college), "player": stats["name"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai/nl_search")
def ai_nl_search():
    query = request.args.get("q","").strip()
    if not query: return jsonify({"results":[], "query":""})
    try:
        from ai_agent import parse_nl_search
        results = parse_nl_search(query, get_season_leaders())
        return jsonify({"results": results, "query": query, "count": len(results)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai/chat", methods=["POST"])
def ai_chat():
    data = request.get_json()
    messages = data.get("messages", [])
    if not messages: return jsonify({"error":"No messages"}), 400
    try:
        from ai_agent import chat_with_agent, build_app_context
        from teams_data import get_all_teams
        ctx = build_app_context(get_season_leaders(), get_all_teams(), ATP_PLAYERS)
        return jsonify({"reply": chat_with_agent(messages, ctx)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/ai/analyze_tennis/<int:rank>")
def ai_analyze_tennis(rank):
    player = ATP_BY_RANK.get(rank)
    if not player: return jsonify({"error":"Player not found"}),404
    try:
        from ai_agent import analyze_tennis_player
        return jsonify({"analysis": analyze_tennis_player(player), "player": player["name"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Tennis routes ─────────────────────────────────────────────────────────────
@app.route("/tennis")
def tennis_index():
    return render_template("tennis_index.html", players=ATP_PLAYERS, ai_available=ai_available())

@app.route("/tennis/player/<int:rank>")
def tennis_player(rank):
    player = ATP_BY_RANK.get(rank)
    if not player: return "Player not found",404
    return render_template("tennis_player.html", player=player, ai_available=ai_available())

@app.route("/tennis/rankings")
def tennis_rankings():
    return render_template("tennis_rankings.html", players=ATP_PLAYERS)

@app.route("/tennis/compare")
def tennis_compare():
    return render_template("tennis_compare.html")

@app.route("/tennis/api/search")
def tennis_api_search():
    q = request.args.get("q","").strip().lower()
    if len(q)<2: return jsonify([])
    return jsonify([{"rank":p["rank"],"name":p["name"],"country":p["country"],"flag":p["flag"]}
                    for p in ATP_PLAYERS if q in p["name"].lower()][:10])

@app.route("/tennis/api/player/<int:rank>")
def tennis_api_player(rank):
    p = ATP_BY_RANK.get(rank)
    if not p: return jsonify({"error":"Not found"}),404
    return jsonify(p)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
