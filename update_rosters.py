#!/usr/bin/env python3
"""
update_rosters.py — Feature 3: Auto-Updating NBA Rosters
---------------------------------------------------------
Run this script (manually or via GitHub Actions cron) to pull the latest
NBA rosters from NBA.com and update teams_data.py automatically.

Usage:
    python update_rosters.py

GitHub Actions: see .github/workflows/update_rosters.yml
Requires: nba_api, pandas
"""

import time
import json
import sys
import os
from datetime import datetime

try:
    from nba_api.stats.endpoints import commonteamroster
    from nba_api.stats.static import teams as nba_teams_static, players as nba_players_static
except ImportError:
    print("ERROR: nba_api not installed. Run: pip install nba_api")
    sys.exit(1)

SEASON = "2025-26"
TEAMS_DATA_PATH = os.path.join(os.path.dirname(__file__), "teams_data.py")

# 2K26 OVR ratings — used to assign ratings to fetched players
NBA_2K26 = {
    "Nikola Jokić":98,"Shai Gilgeous-Alexander":98,"Giannis Antetokounmpo":97,
    "Luka Dončić":95,"Anthony Edwards":95,"Stephen Curry":94,"LeBron James":94,
    "Jayson Tatum":94,"Victor Wembanyama":94,"Kevin Durant":93,"Donovan Mitchell":93,
    "Anthony Davis":93,"Jalen Brunson":93,"Tyrese Haliburton":93,"Kawhi Leonard":92,
    "Cade Cunningham":92,"Joel Embiid":92,"Karl-Anthony Towns":92,"Ja Morant":91,
    "Devin Booker":91,"Jalen Williams":90,"Jaylen Brown":90,"Trae Young":90,
    "Kyrie Irving":90,"Paolo Banchero":89,"Evan Mobley":89,"Pascal Siakam":89,
    "James Harden":89,"Jaren Jackson Jr.":89,"Bam Adebayo":88,"Chet Holmgren":88,
    "Damian Lillard":88,"Domantas Sabonis":87,"Alperen Sengun":87,"LaMelo Ball":87,
    "Darius Garland":87,"Zion Williamson":87,"Ivica Zubac":87,"Derrick White":87,
    "Jimmy Butler III":87,"Amen Thompson":87,"Tyler Herro":86,"Tyrese Maxey":86,
    "Jamal Murray":86,"Franz Wagner":86,"Julius Randle":85,"Zach LaVine":85,
    "De'Aaron Fox":85,"Austin Reaves":85,"DeMar DeRozan":85,"Scottie Barnes":85,
    "OG Anunoby":85,"Kristaps Porziņģis":85,"Lauri Markkanen":84,"Brandon Ingram":84,
    "Mikal Bridges":84,"Rudy Gobert":84,"Norman Powell":84,"Jarrett Allen":84,
    "Jalen Green":83,"Desmond Bane":83,"Myles Turner":83,"Cameron Johnson":83,
    "Dyson Daniels":83,"Coby White":83,"Aaron Gordon":82,"Josh Giddey":82,
    "RJ Barrett":82,"Michael Porter Jr.":82,"Stephon Castle":82,"Brandon Miller":82,
    "Naz Reid":82,"Jalen Duren":82,"Jalen Suggs":82,"Trey Murphy III":82,
    "Cooper Flagg":82,"Isaiah Hartenstein":82,"Jaden McDaniels":82,"Walker Kessler":82,
    "Josh Hart":81,"Luguentz Dort":81,"Herbert Jones":81,"Jrue Holiday":81,
    "Dejounte Murray":81,"Anfernee Simons":81,"Draymond Green":81,"Paul George":81,
    "Onyeka Okongwu":81,"Immanuel Quickley":81,"Andrew Nembhard":81,
    "Jalen Johnson":81,"Alex Sarr":81,"Aaron Nesmith":81,"Shaedon Sharpe":81,
    "Bobby Portis":81,
}

def get_player_ovr(name: str) -> int:
    """Return 2K26 OVR or estimate 74 (solid rotation player)."""
    return NBA_2K26.get(name, 74)

def fetch_all_rosters() -> dict:
    """Fetch all 30 team rosters from NBA.com."""
    all_teams = nba_teams_static.get_teams()
    all_nba_players = nba_players_static.get_players()
    id_to_name = {p["id"]: p["full_name"] for p in all_nba_players}
    
    rosters = {}
    failed = []
    
    for team in all_teams:
        tid = team["id"]
        tname = team["full_name"]
        try:
            print(f"  Fetching {tname}...", end=" ", flush=True)
            r = commonteamroster.CommonTeamRoster(team_id=tid, season=SEASON)
            df = r.get_data_frames()[0]
            
            players = []
            for _, row in df.iterrows():
                pid = int(row["PLAYER_ID"])
                name = row["PLAYER"]
                pos = str(row.get("POSITION", "F")).strip() or "F"
                # Normalize position
                if "/" in pos:
                    pos = pos.split("/")[0]
                ovr = get_player_ovr(name)
                players.append({"name": name, "pos": pos, "ovr": ovr, "id": pid})
            
            rosters[tname] = players
            print(f"✓ ({len(players)} players)")
            time.sleep(0.8)
            
        except Exception as e:
            print(f"✗ ERROR: {e}")
            failed.append(tname)
            time.sleep(2)
    
    if failed:
        print(f"\nFailed teams: {failed}")
    
    return rosters

def generate_teams_data(rosters: dict) -> str:
    """Generate the TEAM_ROSTERS section of teams_data.py."""
    lines = ["\nTEAM_ROSTERS = {\n"]
    
    for team, players in rosters.items():
        lines.append(f'\n"{team}": [\n')
        for p in sorted(players, key=lambda x: x["ovr"], reverse=True):
            lines.append(
                f'    {{"name":{repr(p["name"])},"pos":{repr(p["pos"])},'
                f'"ovr":{p["ovr"]},"id":{p["id"]}}},\n'
            )
        lines.append("],\n")
    
    lines.append("}\n")
    return "".join(lines)

def update_teams_data_file(rosters: dict):
    """Write updated TEAM_ROSTERS into teams_data.py."""
    import re
    
    with open(TEAMS_DATA_PATH, "r") as f:
        src = f.read()
    
    new_rosters_block = generate_teams_data(rosters)
    
    # Replace existing TEAM_ROSTERS block
    new_src = re.sub(
        r'\nTEAM_ROSTERS = \{.*?\n\}',
        new_rosters_block.rstrip("\n"),
        src,
        flags=re.DOTALL
    )
    
    # Add last-updated comment
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    new_src = re.sub(
        r'# Last updated:.*\n',
        f'# Last updated: {timestamp}\n',
        new_src
    )
    if "# Last updated:" not in new_src:
        new_src = f'# Last updated: {timestamp}\n' + new_src
    
    with open(TEAMS_DATA_PATH, "w") as f:
        f.write(new_src)
    
    print(f"\n✅ teams_data.py updated ({timestamp})")

def check_for_changes(new_rosters: dict) -> bool:
    """Return True if rosters differ from current teams_data.py."""
    try:
        import importlib.util, sys
        if "teams_data" in sys.modules:
            del sys.modules["teams_data"]
        spec = importlib.util.spec_from_file_location("teams_data", TEAMS_DATA_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        current = mod.TEAM_ROSTERS
        
        for team, players in new_rosters.items():
            current_names = {p["name"] for p in current.get(team, [])}
            new_names = {p["name"] for p in players}
            if current_names != new_names:
                added = new_names - current_names
                removed = current_names - new_names
                if added: print(f"  {team}: added {added}")
                if removed: print(f"  {team}: removed {removed}")
                return True
        return False
    except Exception as e:
        print(f"Could not compare: {e}")
        return True  # Assume changed if we can't compare

if __name__ == "__main__":
    print(f"🏀 NBA Roster Update Agent — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"Season: {SEASON}\n")
    
    print("Fetching rosters from NBA.com...")
    rosters = fetch_all_rosters()
    
    if not rosters:
        print("❌ No rosters fetched. Exiting.")
        sys.exit(1)
    
    print(f"\nChecking for changes...")
    changed = check_for_changes(rosters)
    
    if changed:
        print("Changes detected. Updating teams_data.py...")
        update_teams_data_file(rosters)
    else:
        print("✅ No roster changes detected. teams_data.py is up to date.")
    
    print(f"\nDone! {len(rosters)} teams processed.")
