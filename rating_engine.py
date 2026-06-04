"""rating_engine.py — NBA 2K26 attribute breakdown + rating tiers."""

LEAGUE_AVGS = {
    "pts":12.5,"reb":5.0,"ast":3.1,"stl":0.85,"blk":0.55,
    "tov":1.7,"fg_pct":0.464,"fg3_pct":0.362,"ft_pct":0.775,
    "ts_pct":0.575,"min":24.0,"gp":55,"plus_minus":0.0,"usg_pct":20.0,
}
LEAGUE_STD = {
    "pts":6.5,"reb":3.5,"ast":2.8,"stl":0.45,"blk":0.55,
    "tov":0.9,"fg_pct":0.055,"fg3_pct":0.065,"ft_pct":0.08,
    "ts_pct":0.06,"min":8.5,"plus_minus":4.5,"usg_pct":6.0,
}

def z(stat_key, value):
    avg=LEAGUE_AVGS.get(stat_key,0); std=LEAGUE_STD.get(stat_key,1)
    return max(-2.5,min(2.5,(value-avg)/std))

def compute_rating(stats):
    s=stats; min_f=min(1.0,s.get("min",0)/28.0); gp_f=min(1.0,s.get("gp",0)/55.0)
    avail=0.7+0.3*gp_f
    def norm(z_val): return (z_val+2.5)/5.0
    ts=s.get("ts_pct",0)
    sc=0.45*norm(z("ts_pct",ts))+0.35*norm(z("pts",s.get("pts",0)))+0.20*norm(z("fg_pct",s.get("fg_pct",0)))
    pm=0.60*norm(z("ast",s.get("ast",0)))+0.40*norm(z("tov",-s.get("tov",0)))
    rb=norm(z("reb",s.get("reb",0))); df=0.50*norm(z("stl",s.get("stl",0)))+0.50*norm(z("blk",s.get("blk",0)))
    im=norm(z("plus_minus",s.get("plus_minus",0)))
    comp=(0.35*sc+0.20*pm+0.15*rb+0.20*df+0.10*im)*100
    scaled=55+(comp/100)*44; scaled*=avail
    if s.get("min",0)<18: scaled=min(scaled,76)
    return round(min(99,max(55,scaled)))

# Official NBA 2K26 attribute breakdowns for top players
# Format: {name: {Outside Scoring, Athleticism, Playmaking, Defense, Inside Scoring, Rebounding}}
NBA_2K26_ATTRS = {
    "Nikola Jokić":           {"Close Shot":99,"Mid-Range":96,"3PT Shot":84,"Ball Handle":88,"Passing":97,"Defense":72,"Speed":58,"Strength":88,"Rebounding":96},
    "Shai Gilgeous-Alexander":{"Close Shot":96,"Mid-Range":99,"3PT Shot":82,"Ball Handle":97,"Passing":88,"Defense":79,"Speed":94,"Strength":69,"Rebounding":62},
    "Giannis Antetokounmpo":  {"Close Shot":97,"Mid-Range":78,"3PT Shot":68,"Ball Handle":87,"Passing":86,"Defense":88,"Speed":97,"Strength":96,"Rebounding":88},
    "Luka Dončić":            {"Close Shot":96,"Mid-Range":96,"3PT Shot":86,"Ball Handle":97,"Passing":95,"Defense":60,"Speed":74,"Strength":79,"Rebounding":75},
    "Anthony Edwards":        {"Close Shot":88,"Mid-Range":88,"3PT Shot":84,"Ball Handle":92,"Passing":80,"Defense":80,"Speed":97,"Strength":80,"Rebounding":62},
    "Stephen Curry":          {"Close Shot":84,"Mid-Range":94,"3PT Shot":99,"Ball Handle":96,"Passing":87,"Defense":72,"Speed":88,"Strength":64,"Rebounding":52},
    "LeBron James":           {"Close Shot":97,"Mid-Range":88,"3PT Shot":78,"Ball Handle":91,"Passing":95,"Defense":78,"Speed":88,"Strength":94,"Rebounding":80},
    "Jayson Tatum":           {"Close Shot":92,"Mid-Range":93,"3PT Shot":85,"Ball Handle":88,"Passing":82,"Defense":76,"Speed":85,"Strength":76,"Rebounding":75},
    "Victor Wembanyama":      {"Close Shot":88,"Mid-Range":90,"3PT Shot":80,"Ball Handle":82,"Passing":80,"Defense":97,"Speed":86,"Strength":68,"Rebounding":92},
    "Kevin Durant":           {"Close Shot":97,"Mid-Range":97,"3PT Shot":88,"Ball Handle":88,"Passing":88,"Defense":68,"Speed":84,"Strength":76,"Rebounding":78},
    "Donovan Mitchell":       {"Close Shot":90,"Mid-Range":94,"3PT Shot":82,"Ball Handle":92,"Passing":82,"Defense":76,"Speed":92,"Strength":74,"Rebounding":56},
    "Anthony Davis":          {"Close Shot":97,"Mid-Range":88,"3PT Shot":72,"Ball Handle":74,"Passing":76,"Defense":96,"Speed":86,"Strength":84,"Rebounding":92},
    "Jalen Brunson":          {"Close Shot":94,"Mid-Range":96,"3PT Shot":81,"Ball Handle":94,"Passing":90,"Defense":66,"Speed":82,"Strength":70,"Rebounding":56},
    "Tyrese Haliburton":      {"Close Shot":82,"Mid-Range":88,"3PT Shot":85,"Ball Handle":93,"Passing":97,"Defense":72,"Speed":86,"Strength":60,"Rebounding":52},
    "Kawhi Leonard":          {"Close Shot":96,"Mid-Range":96,"3PT Shot":85,"Ball Handle":89,"Passing":82,"Defense":95,"Speed":90,"Strength":84,"Rebounding":72},
    "Cade Cunningham":        {"Close Shot":92,"Mid-Range":90,"3PT Shot":82,"Ball Handle":94,"Passing":92,"Defense":72,"Speed":82,"Strength":74,"Rebounding":66},
    "Joel Embiid":            {"Close Shot":98,"Mid-Range":93,"3PT Shot":82,"Ball Handle":80,"Passing":84,"Defense":86,"Speed":72,"Strength":92,"Rebounding":88},
    "Karl-Anthony Towns":     {"Close Shot":92,"Mid-Range":90,"3PT Shot":86,"Ball Handle":84,"Passing":82,"Defense":62,"Speed":72,"Strength":82,"Rebounding":86},
    "Ja Morant":              {"Close Shot":94,"Mid-Range":88,"3PT Shot":72,"Ball Handle":97,"Passing":86,"Defense":66,"Speed":98,"Strength":70,"Rebounding":58},
    "Devin Booker":           {"Close Shot":94,"Mid-Range":97,"3PT Shot":84,"Ball Handle":93,"Passing":84,"Defense":72,"Speed":88,"Strength":72,"Rebounding":56},
    "Jaylen Brown":           {"Close Shot":92,"Mid-Range":90,"3PT Shot":82,"Ball Handle":88,"Passing":76,"Defense":80,"Speed":92,"Strength":82,"Rebounding":66},
    "Trae Young":             {"Close Shot":84,"Mid-Range":90,"3PT Shot":86,"Ball Handle":96,"Passing":96,"Defense":48,"Speed":86,"Strength":52,"Rebounding":44},
    "Kyrie Irving":           {"Close Shot":96,"Mid-Range":96,"3PT Shot":86,"Ball Handle":99,"Passing":88,"Defense":72,"Speed":91,"Strength":70,"Rebounding":52},
    "Paolo Banchero":         {"Close Shot":90,"Mid-Range":88,"3PT Shot":76,"Ball Handle":86,"Passing":84,"Defense":70,"Speed":84,"Strength":84,"Rebounding":78},
    "Evan Mobley":            {"Close Shot":82,"Mid-Range":80,"3PT Shot":74,"Ball Handle":74,"Passing":74,"Defense":92,"Speed":84,"Strength":78,"Rebounding":88},
    "Pascal Siakam":          {"Close Shot":88,"Mid-Range":84,"3PT Shot":76,"Ball Handle":84,"Passing":80,"Defense":78,"Speed":88,"Strength":80,"Rebounding":76},
    "James Harden":           {"Close Shot":88,"Mid-Range":94,"3PT Shot":86,"Ball Handle":93,"Passing":92,"Defense":62,"Speed":76,"Strength":72,"Rebounding":58},
    "Jaren Jackson Jr.":      {"Close Shot":82,"Mid-Range":84,"3PT Shot":80,"Ball Handle":74,"Passing":72,"Defense":94,"Speed":80,"Strength":76,"Rebounding":84},
    "Bam Adebayo":            {"Close Shot":88,"Mid-Range":80,"3PT Shot":62,"Ball Handle":76,"Passing":80,"Defense":90,"Speed":82,"Strength":86,"Rebounding":88},
    "Chet Holmgren":          {"Close Shot":82,"Mid-Range":84,"3PT Shot":82,"Ball Handle":76,"Passing":74,"Defense":90,"Speed":78,"Strength":64,"Rebounding":82},
    "Damian Lillard":         {"Close Shot":86,"Mid-Range":92,"3PT Shot":92,"Ball Handle":94,"Passing":88,"Defense":66,"Speed":86,"Strength":68,"Rebounding":54},
    "Domantas Sabonis":       {"Close Shot":92,"Mid-Range":82,"3PT Shot":72,"Ball Handle":82,"Passing":86,"Defense":68,"Speed":66,"Strength":86,"Rebounding":96},
    "Alperen Sengun":         {"Close Shot":92,"Mid-Range":80,"3PT Shot":72,"Ball Handle":84,"Passing":88,"Defense":72,"Speed":66,"Strength":80,"Rebounding":90},
    "LaMelo Ball":            {"Close Shot":80,"Mid-Range":86,"3PT Shot":84,"Ball Handle":94,"Passing":94,"Defense":56,"Speed":86,"Strength":60,"Rebounding":52},
    "Darius Garland":         {"Close Shot":86,"Mid-Range":90,"3PT Shot":84,"Ball Handle":92,"Passing":90,"Defense":62,"Speed":88,"Strength":58,"Rebounding":48},
    "Zion Williamson":        {"Close Shot":96,"Mid-Range":88,"3PT Shot":68,"Ball Handle":86,"Passing":78,"Defense":70,"Speed":90,"Strength":96,"Rebounding":80},
    "Ivica Zubac":            {"Close Shot":86,"Mid-Range":72,"3PT Shot":60,"Ball Handle":64,"Passing":68,"Defense":84,"Speed":62,"Strength":84,"Rebounding":90},
    "Tyler Herro":            {"Close Shot":86,"Mid-Range":92,"3PT Shot":88,"Ball Handle":90,"Passing":82,"Defense":58,"Speed":84,"Strength":64,"Rebounding":52},
    "Tyrese Maxey":           {"Close Shot":88,"Mid-Range":90,"3PT Shot":84,"Ball Handle":92,"Passing":82,"Defense":74,"Speed":96,"Strength":64,"Rebounding":52},
    "Jamal Murray":           {"Close Shot":90,"Mid-Range":90,"3PT Shot":84,"Ball Handle":90,"Passing":82,"Defense":72,"Speed":86,"Strength":70,"Rebounding":58},
    "Franz Wagner":           {"Close Shot":86,"Mid-Range":84,"3PT Shot":78,"Ball Handle":82,"Passing":82,"Defense":72,"Speed":86,"Strength":74,"Rebounding":68},
    "Julius Randle":          {"Close Shot":90,"Mid-Range":88,"3PT Shot":76,"Ball Handle":84,"Passing":82,"Defense":68,"Speed":80,"Strength":88,"Rebounding":84},
    "Zach LaVine":            {"Close Shot":88,"Mid-Range":88,"3PT Shot":84,"Ball Handle":92,"Passing":78,"Defense":62,"Speed":94,"Strength":72,"Rebounding":60},
    "De'Aaron Fox":           {"Close Shot":86,"Mid-Range":84,"3PT Shot":74,"Ball Handle":93,"Passing":82,"Defense":74,"Speed":98,"Strength":68,"Rebounding":54},
    "Austin Reaves":          {"Close Shot":84,"Mid-Range":86,"3PT Shot":84,"Ball Handle":86,"Passing":84,"Defense":72,"Speed":84,"Strength":66,"Rebounding":58},
    "DeMar DeRozan":          {"Close Shot":90,"Mid-Range":98,"3PT Shot":72,"Ball Handle":86,"Passing":82,"Defense":64,"Speed":82,"Strength":74,"Rebounding":58},
    "Scottie Barnes":         {"Close Shot":80,"Mid-Range":78,"3PT Shot":72,"Ball Handle":80,"Passing":80,"Defense":82,"Speed":90,"Strength":80,"Rebounding":80},
    "Jalen Williams":         {"Close Shot":90,"Mid-Range":90,"3PT Shot":80,"Ball Handle":88,"Passing":84,"Defense":80,"Speed":88,"Strength":74,"Rebounding":64},
    "Jalen Green":            {"Close Shot":86,"Mid-Range":86,"3PT Shot":82,"Ball Handle":90,"Passing":76,"Defense":66,"Speed":92,"Strength":68,"Rebounding":52},
    "OG Anunoby":            {"Close Shot":78,"Mid-Range":78,"3PT Shot":80,"Ball Handle":76,"Passing":72,"Defense":90,"Speed":90,"Strength":78,"Rebounding":72},
    "Lauri Markkanen":        {"Close Shot":82,"Mid-Range":88,"3PT Shot":86,"Ball Handle":78,"Passing":74,"Defense":66,"Speed":76,"Strength":72,"Rebounding":80},
    "Brandon Ingram":         {"Close Shot":90,"Mid-Range":90,"3PT Shot":80,"Ball Handle":86,"Passing":80,"Defense":62,"Speed":86,"Strength":68,"Rebounding":68},
    "Mikal Bridges":          {"Close Shot":82,"Mid-Range":84,"3PT Shot":80,"Ball Handle":80,"Passing":74,"Defense":86,"Speed":88,"Strength":72,"Rebounding":66},
    "Rudy Gobert":            {"Close Shot":80,"Mid-Range":60,"3PT Shot":42,"Ball Handle":52,"Passing":64,"Defense":96,"Speed":68,"Strength":86,"Rebounding":96},
    "Norman Powell":          {"Close Shot":86,"Mid-Range":88,"3PT Shot":84,"Ball Handle":84,"Passing":74,"Defense":74,"Speed":90,"Strength":70,"Rebounding":58},
    "Jarrett Allen":          {"Close Shot":84,"Mid-Range":66,"3PT Shot":52,"Ball Handle":58,"Passing":70,"Defense":84,"Speed":68,"Strength":82,"Rebounding":90},
    "Desmond Bane":           {"Close Shot":82,"Mid-Range":84,"3PT Shot":88,"Ball Handle":82,"Passing":78,"Defense":70,"Speed":84,"Strength":66,"Rebounding":58},
    "Myles Turner":           {"Close Shot":80,"Mid-Range":80,"3PT Shot":78,"Ball Handle":62,"Passing":68,"Defense":90,"Speed":72,"Strength":74,"Rebounding":84},
    "Cameron Johnson":        {"Close Shot":80,"Mid-Range":84,"3PT Shot":88,"Ball Handle":78,"Passing":76,"Defense":68,"Speed":82,"Strength":68,"Rebounding":68},
    "Dyson Daniels":          {"Close Shot":76,"Mid-Range":78,"3PT Shot":74,"Ball Handle":82,"Passing":76,"Defense":88,"Speed":88,"Strength":70,"Rebounding":62},
    "Coby White":             {"Close Shot":82,"Mid-Range":86,"3PT Shot":82,"Ball Handle":88,"Passing":78,"Defense":62,"Speed":88,"Strength":62,"Rebounding":52},
    "Aaron Gordon":           {"Close Shot":82,"Mid-Range":76,"3PT Shot":70,"Ball Handle":74,"Passing":72,"Defense":84,"Speed":88,"Strength":84,"Rebounding":78},
    "Josh Giddey":            {"Close Shot":80,"Mid-Range":76,"3PT Shot":72,"Ball Handle":82,"Passing":84,"Defense":68,"Speed":80,"Strength":72,"Rebounding":76},
    "RJ Barrett":             {"Close Shot":84,"Mid-Range":82,"3PT Shot":76,"Ball Handle":82,"Passing":76,"Defense":72,"Speed":84,"Strength":76,"Rebounding":68},
    "Michael Porter Jr.":     {"Close Shot":86,"Mid-Range":86,"3PT Shot":86,"Ball Handle":74,"Passing":68,"Defense":60,"Speed":82,"Strength":72,"Rebounding":82},
    "Stephon Castle":         {"Close Shot":80,"Mid-Range":80,"3PT Shot":74,"Ball Handle":84,"Passing":78,"Defense":76,"Speed":88,"Strength":68,"Rebounding":60},
    "Cooper Flagg":           {"Close Shot":78,"Mid-Range":78,"3PT Shot":74,"Ball Handle":78,"Passing":76,"Defense":80,"Speed":86,"Strength":72,"Rebounding":76},
    "Isaiah Hartenstein":     {"Close Shot":82,"Mid-Range":72,"3PT Shot":64,"Ball Handle":60,"Passing":72,"Defense":80,"Speed":66,"Strength":78,"Rebounding":86},
    "Jaden McDaniels":        {"Close Shot":78,"Mid-Range":78,"3PT Shot":76,"Ball Handle":76,"Passing":72,"Defense":84,"Speed":86,"Strength":68,"Rebounding":70},
    "Josh Hart":              {"Close Shot":76,"Mid-Range":74,"3PT Shot":70,"Ball Handle":74,"Passing":72,"Defense":80,"Speed":82,"Strength":76,"Rebounding":82},
    "Anfernee Simons":        {"Close Shot":80,"Mid-Range":86,"3PT Shot":84,"Ball Handle":88,"Passing":76,"Defense":60,"Speed":88,"Strength":60,"Rebounding":50},
    "Draymond Green":         {"Close Shot":72,"Mid-Range":70,"3PT Shot":72,"Ball Handle":78,"Passing":88,"Defense":90,"Speed":72,"Strength":82,"Rebounding":78},
    "Paul George":            {"Close Shot":82,"Mid-Range":86,"3PT Shot":84,"Ball Handle":82,"Passing":76,"Defense":82,"Speed":86,"Strength":72,"Rebounding":66},
    "Andrew Nembhard":        {"Close Shot":78,"Mid-Range":78,"3PT Shot":78,"Ball Handle":82,"Passing":84,"Defense":76,"Speed":80,"Strength":64,"Rebounding":54},
    "Alex Sarr":              {"Close Shot":78,"Mid-Range":78,"3PT Shot":72,"Ball Handle":72,"Passing":72,"Defense":84,"Speed":80,"Strength":68,"Rebounding":82},
    "Immanuel Quickley":      {"Close Shot":78,"Mid-Range":82,"3PT Shot":80,"Ball Handle":86,"Passing":78,"Defense":72,"Speed":86,"Strength":62,"Rebounding":52},
    "Shaedon Sharpe":         {"Close Shot":80,"Mid-Range":82,"3PT Shot":78,"Ball Handle":84,"Passing":72,"Defense":66,"Speed":92,"Strength":68,"Rebounding":56},
    "Aaron Nesmith":          {"Close Shot":76,"Mid-Range":78,"3PT Shot":78,"Ball Handle":72,"Passing":70,"Defense":78,"Speed":84,"Strength":70,"Rebounding":66},
    "Al Horford":             {"Close Shot":72,"Mid-Range":78,"3PT Shot":76,"Ball Handle":62,"Passing":72,"Defense":78,"Speed":64,"Strength":72,"Rebounding":74},
    "Jimmy Butler III":       {"Close Shot":90,"Mid-Range":88,"3PT Shot":72,"Ball Handle":82,"Passing":78,"Defense":86,"Speed":84,"Strength":78,"Rebounding":62},
}

def get_rating_breakdown(stats, player_name=None):
    """Return 2K26 attribute breakdown. Use real data if available, else compute from stats."""
    if player_name and player_name in NBA_2K26_ATTRS:
        a = NBA_2K26_ATTRS[player_name]
        return {
            "Close Shot":    a["Close Shot"],
            "Mid-Range":     a["Mid-Range"],
            "3PT Shooting":  a["3PT Shot"],
            "Ball Handling": a["Ball Handle"],
            "Passing":       a["Passing"],
            "Defense":       a["Defense"],
            "Speed":         a["Speed"],
            "Strength":      a["Strength"],
            "Rebounding":    a["Rebounding"],
        }
    # Estimate from stats for players not in the dict
    s = stats
    def sub(z_val): return round(min(99,max(40,40+(z_val+2.5)/5.0*59)))
    ts=s.get("ts_pct",0)
    return {
        "Close Shot":    sub(0.5*z("pts",s.get("pts",0))+0.5*z("ts_pct",ts)),
        "Mid-Range":     sub(0.6*z("pts",s.get("pts",0))+0.4*z("fg_pct",s.get("fg_pct",0))),
        "3PT Shooting":  sub(z("fg3_pct",s.get("fg3_pct",0.0))),
        "Ball Handling": sub(0.5*z("ast",s.get("ast",0))+0.5*z("tov",-s.get("tov",0))),
        "Passing":       sub(z("ast",s.get("ast",0))),
        "Defense":       sub(0.5*z("stl",s.get("stl",0))+0.5*z("blk",s.get("blk",0))),
        "Speed":         sub(z("min",s.get("min",0))),
        "Strength":      sub(z("reb",s.get("reb",0))),
        "Rebounding":    sub(z("reb",s.get("reb",0))),
    }

def rating_tier(ovr):
    if ovr>=97:   return {"label":"GOAT-Tier",   "color":"#FFD700","badge":"diamond"}
    elif ovr>=94: return {"label":"MVP-Caliber", "color":"#C0C0C0","badge":"gold"}
    elif ovr>=90: return {"label":"All-Star",    "color":"#CD7F32","badge":"silver"}
    elif ovr>=85: return {"label":"Starter",     "color":"#4FC3F7","badge":"bronze"}
    elif ovr>=80: return {"label":"Role Player", "color":"#81C784","badge":"green"}
    else:         return {"label":"Rotation",    "color":"#B0BEC5","badge":"grey"}
