#!/usr/bin/env python3
"""
update_tennis.py — Feature 5: Live ATP Rankings Sync
------------------------------------------------------
Fetches current ATP singles rankings from the Tennis Abstract API
(tennisabstract.com) and updates tennis_data.py automatically.

Usage:
    python update_tennis.py

GitHub Actions: see .github/workflows/update_tennis.yml
"""

import requests
import json
import re
import sys
import os
import time
from datetime import datetime

TENNIS_DATA_PATH = os.path.join(os.path.dirname(__file__), "tennis_data.py")

COUNTRY_FLAGS = {
    "Italy":"🇮🇹","Spain":"🇪🇸","Germany":"🇩🇪","Serbia":"🇷🇸","USA":"🇺🇸",
    "Canada":"🇨🇦","Australia":"🇦🇺","Russia":"🇷🇺","Norway":"🇳🇴","Kazakhstan":"🇰🇿",
    "Czech Republic":"🇨🇿","France":"🇫🇷","Denmark":"🇩🇰","Greece":"🇬🇷","Great Britain":"🇬🇧",
    "Croatia":"🇭🇷","Argentina":"🇦🇷","Brazil":"🇧🇷","Netherlands":"🇳🇱","Chile":"🇨🇱",
    "Belgium":"🇧🇪","Switzerland":"🇨🇭","Austria":"🇦🇹","Hungary":"🇭🇺","Peru":"🇵🇪",
    "Portugal":"🇵🇹","Poland":"🇵🇱","Monaco":"🇲🇨","Japan":"🇯🇵","India":"🇮🇳",
    "Paraguay":"🇵🇾","Hong Kong":"🇭🇰","Slovakia":"🇸🇰","Georgia":"🇬🇪","Sweden":"🇸🇪",
    "Bolivia":"🇧🇴","Moldova":"🇲🇩","China":"🇨🇳","Chinese Taipei":"🇹🇼","Turkey":"🇹🇷",
    "Finland":"🇫🇮","Bulgaria":"🇧🇬","Romania":"🇷🇴","Ukraine":"🇺🇦","Belarus":"🇧🇾",
    "South Africa":"🇿🇦","New Zealand":"🇳🇿","Colombia":"🇨🇴","Ecuador":"🇪🇨",
}

# Known Grand Slam winners (updated manually when new Slams are won)
GRAND_SLAM_TITLES = {
    "Novak Djokovic": 24,
    "Carlos Alcaraz": 4,
    "Jannik Sinner": 3,
    "Alexander Zverev": 1,
    "Daniil Medvedev": 1,
    "Dominic Thiem": 1,
    "Stan Wawrinka": 3,
    "Marin Čilić": 1,
}

def fetch_atp_rankings_live(limit: int = 150) -> list:
    """
    Fetch ATP rankings from Tennis Abstract's public data.
    Falls back to scraping if API unavailable.
    """
    # Try Tennis Abstract rankings CSV (public, updated weekly)
    url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_rankings_current.csv"
    try:
        print("  Trying Tennis Abstract (Jeff Sackmann's dataset)...")
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            lines = resp.text.strip().split("\n")
            players = []
            for line in lines[1:limit+1]:  # skip header
                parts = line.strip().split(",")
                if len(parts) >= 4:
                    try:
                        rank = int(parts[0])
                        points = int(parts[2]) if parts[2].isdigit() else 0
                        player_id = parts[1]
                        players.append({
                            "rank": rank,
                            "points": points,
                            "id": player_id,
                        })
                    except:
                        continue
            if players:
                print(f"  ✓ Got {len(players)} rankings from Tennis Abstract")
                return players
    except Exception as e:
        print(f"  ✗ Tennis Abstract failed: {e}")

    # Try ATP Tour API endpoint
    try:
        print("  Trying ATP Tour API...")
        url2 = "https://www.atptour.com/en/rankings/singles?rankDate=&rankRange=1-150&countryCode=&"
        headers = {"User-Agent": "Mozilla/5.0 (compatible; HoopRater/1.0)"}
        resp = requests.get(url2, timeout=10, headers=headers)
        if resp.status_code == 200 and "rankingTableBody" in resp.text:
            # Parse HTML table
            rows = re.findall(r'<tr[^>]*class="[^"]*tbodies[^"]*"[^>]*>(.*?)</tr>', resp.text, re.DOTALL)
            players = []
            for i, row in enumerate(rows[:limit]):
                rank_m = re.search(r'<td[^>]*class="[^"]*rank-cell[^"]*"[^>]*>(\d+)', row)
                name_m = re.search(r'<span[^>]*class="[^"]*player-cell-name[^"]*"[^>]*>([^<]+)<', row)
                pts_m  = re.search(r'<td[^>]*class="[^"]*points-cell[^"]*"[^>]*>([\d,]+)', row)
                if rank_m and name_m:
                    players.append({
                        "rank": int(rank_m.group(1)),
                        "name": name_m.group(1).strip(),
                        "points": int(pts_m.group(1).replace(",","")) if pts_m else 0,
                    })
            if players:
                print(f"  ✓ Got {len(players)} rankings from ATP Tour")
                return players
    except Exception as e:
        print(f"  ✗ ATP Tour failed: {e}")

    print("  ⚠ All sources failed — rankings not updated")
    return []

def fetch_player_details(players_raw: list) -> list:
    """
    Enrich raw ranking data with player details from Jeff Sackmann's dataset.
    """
    players_url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master/atp_players.csv"
    player_lookup = {}
    try:
        resp = requests.get(players_url, timeout=10)
        if resp.status_code == 200:
            for line in resp.text.strip().split("\n")[1:]:
                parts = line.strip().split(",")
                if len(parts) >= 5:
                    pid = parts[0]
                    first = parts[1]
                    last = parts[2]
                    hand = parts[3] if parts[3] in ("L","R") else "R"
                    birth = parts[4][:4] if len(parts[4]) >= 4 else "1995"
                    country = parts[5] if len(parts) > 5 else "Unknown"
                    age = max(18, 2026 - int(birth)) if birth.isdigit() else 26
                    player_lookup[pid] = {
                        "full_name": f"{first} {last}".strip(),
                        "hand": hand,
                        "age": age,
                        "country_code": country,
                    }
    except Exception as e:
        print(f"  Player details fetch failed: {e}")
    return player_lookup

# Country code → full name mapping
COUNTRY_CODE_MAP = {
    "ITA":"Italy","ESP":"Spain","GER":"Germany","SRB":"Serbia","USA":"USA",
    "CAN":"Canada","AUS":"Australia","RUS":"Russia","NOR":"Norway","KAZ":"Kazakhstan",
    "CZE":"Czech Republic","FRA":"France","DEN":"Denmark","GRE":"Greece","GBR":"Great Britain",
    "CRO":"Croatia","ARG":"Argentina","BRA":"Brazil","NED":"Netherlands","CHI":"Chile",
    "BEL":"Belgium","SUI":"Switzerland","AUT":"Austria","HUN":"Hungary","PER":"Peru",
    "POR":"Portugal","POL":"Poland","MON":"Monaco","JPN":"Japan","IND":"India",
    "PAR":"Paraguay","HKG":"Hong Kong","SVK":"Slovakia","GEO":"Georgia","SWE":"Sweden",
    "BOL":"Bolivia","MDA":"Moldova","CHN":"China","TPE":"Chinese Taipei","TUR":"Turkey",
}

def update_tennis_data(new_players: list, timestamp: str):
    """Regenerate the _RAW list in tennis_data.py."""
    with open(TENNIS_DATA_PATH, "r") as f:
        src = f.read()

    # Build new _RAW list
    raw_lines = ["_RAW = [\n    # rank, name, country, points, age, hand, grand_slams, career_high, turned_pro\n"]
    for p in new_players[:150]:
        gs = GRAND_SLAM_TITLES.get(p["name"], 0)
        raw_lines.append(
            f"    ({p['rank']}, {repr(p['name'])}, {repr(p['country'])}, "
            f"{p['points']}, {p['age']}, {repr(p['hand'])}, "
            f"{gs}, {p.get('career_high', p['rank'])}, {p.get('turned_pro', 2015)}),\n"
        )
    raw_lines.append("]\n")
    new_raw = "".join(raw_lines)

    # Replace existing _RAW block
    new_src = re.sub(r'_RAW = \[.*?\n\]', new_raw.strip(), src, flags=re.DOTALL)
    
    # Update last-updated comment
    new_src = re.sub(r'# ATP Last updated:.*\n', f'# ATP Last updated: {timestamp}\n', new_src)
    if "# ATP Last updated:" not in new_src:
        new_src = f'# ATP Last updated: {timestamp}\n' + new_src

    with open(TENNIS_DATA_PATH, "w") as f:
        f.write(new_src)

    print(f"✅ tennis_data.py updated ({timestamp})")

if __name__ == "__main__":
    print(f"🎾 ATP Rankings Update Agent — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}\n")

    print("Fetching ATP rankings...")
    raw_rankings = fetch_atp_rankings_live(150)

    if not raw_rankings:
        print("❌ Could not fetch live rankings. Keeping existing data.")
        sys.exit(0)  # Don't fail — just keep existing data

    print("\nFetching player details...")
    player_lookup = fetch_player_details(raw_rankings)

    # Enrich ranking data
    enriched = []
    for r in raw_rankings:
        pid = r.get("id", "")
        detail = player_lookup.get(pid, {})
        name = r.get("name") or detail.get("full_name", f"Player #{r['rank']}")
        country_code = detail.get("country_code", "")
        country = COUNTRY_CODE_MAP.get(country_code, country_code or "Unknown")
        hand = detail.get("hand", "R")
        age = detail.get("age", 26)
        turned_pro = max(2000, 2026 - max(1, age - 17))

        enriched.append({
            "rank": r["rank"],
            "name": name,
            "country": country,
            "points": r["points"],
            "age": age,
            "hand": hand,
            "turned_pro": turned_pro,
            "career_high": r["rank"],  # approximation for new data
            "flag": COUNTRY_FLAGS.get(country, "🎾"),
        })

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    print(f"\nTop 5 updated rankings:")
    for p in enriched[:5]:
        print(f"  #{p['rank']} {p['name']} ({p['country']}) — {p['points']} pts")

    print("\nUpdating tennis_data.py...")
    update_tennis_data(enriched, timestamp)
    print(f"\nDone! {len(enriched)} players updated.")
