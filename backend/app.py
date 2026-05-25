from flask import Flask, jsonify, request
from flask_cors import CORS
from data import SQUADS

app = Flask(__name__)
CORS(app)


@app.route("/api/teams", methods=["GET"])
def get_teams():
    teams = [
        {"id": "MI",   "name": "Mumbai Indians"},
        {"id": "CSK",  "name": "Chennai Super Kings"},
        {"id": "DC",   "name": "Delhi Capitals"},
        {"id": "PBKS", "name": "Punjab Kings"},
        {"id": "KKR",  "name": "Kolkata Knight Riders"},
        {"id": "RCB",  "name": "Royal Challengers Bengaluru"},
        {"id": "SRH",  "name": "Sunrisers Hyderabad"},
        {"id": "RR",   "name": "Rajasthan Royals"},
        {"id": "GT",   "name": "Gujarat Titans"},
        {"id": "LSG",  "name": "Lucknow Super Giants"},
    ]
    return jsonify(teams)


@app.route("/api/squad/<team_id>", methods=["GET"])
def get_squad(team_id):
    squad = SQUADS.get(team_id.upper())
    if not squad:
        return jsonify({"error": "Team not found"}), 404
    return jsonify(squad)


@app.route("/api/analyse", methods=["POST"])
def analyse():
    body = request.get_json()
    team_id = body.get("team", "").upper()
    strategy = body.get("strategy", "balanced")
    selected_names = body.get("players", [])

    squad = SQUADS.get(team_id, [])
    selected = [p for p in squad if p["name"] in selected_names]

    if len(selected) != 11:
        return jsonify({"error": "Exactly 11 players required"}), 400

    messages = []
    roles = {"BAT": 0, "BOWL": 0, "AR": 0, "WK": 0}
    for p in selected:
        roles[p["role"]] = roles.get(p["role"], 0) + 1

    total_bat  = roles["BAT"] + roles["WK"] + roles["AR"]
    total_bowl = roles["BOWL"] + roles["AR"]

    # RCB Easter egg
    if team_id == "RCB":
        virat_in = any(p["name"] == "Virat Kohli" for p in selected)
        if not virat_in:
            messages.append({
                "type": "fun", "icon": "👑",
                "title": "Really? Leaving out the King?",
                "text": "Dropping Virat Kohli from an RCB XI? That's bold. Are you sure about this?"
            })

    # Wicketkeeper
    if roles["WK"] == 0:
        messages.append({"type": "error", "icon": "🧤", "title": "No Wicketkeeper!",
                          "text": "Every XI needs a keeper. Without one, your fielding setup is invalid."})
    elif roles["WK"] > 2:
        messages.append({"type": "warning", "icon": "🧤", "title": "Too many Wicketkeepers",
                          "text": f"You've picked {roles['WK']} keepers — only one can keep. Swap extras for specialists."})

    # Bowlers
    if roles["BOWL"] == 0 and roles["AR"] < 3:
        messages.append({"type": "error", "icon": "🎯", "title": "Critically short on bowlers",
                          "text": "No specialist bowlers and very few all-rounders. You won't complete 20 overs."})
    elif total_bowl < 4:
        messages.append({"type": "error", "icon": "🎯", "title": "Not enough bowlers",
                          "text": f"Only {total_bowl} bowling options. You need at least 4 to cover 20 overs."})
    elif total_bowl == 4:
        messages.append({"type": "warning", "icon": "🎯", "title": "Thin bowling attack",
                          "text": "4 bowling options is tight — one bad day leaves you exposed in the back overs."})
    elif total_bowl >= 7:
        messages.append({"type": "warning", "icon": "🎯", "title": "Too bowling heavy",
                          "text": f"{total_bowl} bowling options is excessive. Your batting will look thin."})

    # Batters
    if total_bat < 5:
        messages.append({"type": "error", "icon": "🏏", "title": "Not enough batters",
                          "text": f"Only {total_bat} batting options. Risk of tail-end collapses."})
    elif roles["BAT"] < 2 and roles["WK"] < 1:
        messages.append({"type": "warning", "icon": "🏏", "title": "Light on specialist batters",
                          "text": "Aim for at least 2–3 pure batters to anchor the innings."})

    # All-rounders
    if roles["AR"] == 0:
        messages.append({"type": "warning", "icon": "⚡", "title": "No all-rounders",
                          "text": "All-rounders give flexibility. Without one, batting and bowling feel very rigid."})
    elif roles["AR"] >= 6:
        messages.append({"type": "warning", "icon": "⚡", "title": "Very all-rounder heavy",
                          "text": f"{roles['AR']} all-rounders may dilute specialist quality in every area."})

    # Strategy checks
    spin_keywords = ["spin", "leg-spin", "off-spin", "left-arm wrist", "chinaman", "mystery"]
    pace_keywords = ["pace", "seam", "swing", "kmph"]

    if strategy == "spin":
        spinners = [p for p in selected if any(k in p["stats"].lower() for k in spin_keywords)]
        if len(spinners) < 2:
            messages.append({"type": "warning", "icon": "🌀", "title": "Spin pitch — add more spinners",
                              "text": f"Only {len(spinners)} spinner(s). Aim for 3–4 on a turning track."})
        else:
            messages.append({"type": "success", "icon": "🌀", "title": f"Good spin coverage ({len(spinners)} spinners)",
                              "text": "Well set for a spin-friendly surface."})

    if strategy == "pace":
        pacers = [p for p in selected if (p["role"] in ["BOWL", "AR"])
                  and any(k in p["stats"].lower() for k in pace_keywords)]
        if len(pacers) < 3:
            messages.append({"type": "warning", "icon": "💨", "title": "Pace pitch — add more pacers",
                              "text": f"Only {len(pacers)} pace option(s). Aim for 3–4 on a seaming track."})
        else:
            messages.append({"type": "success", "icon": "💨", "title": f"Strong pace attack ({len(pacers)} pacers)",
                              "text": "Your pace options suit a quick, bouncy surface well."})

    if strategy == "batting" and roles["BAT"] + roles["WK"] < 5:
        messages.append({"type": "warning", "icon": "🏏", "title": "Batting strategy needs more batters",
                          "text": "For a batting-first approach, aim for 5+ top-order batters/WK."})

    if strategy == "bowling" and total_bowl < 6:
        messages.append({"type": "warning", "icon": "🎯", "title": "Bowling strategy needs more bowlers",
                          "text": "For a bowling-first approach, aim for 6+ bowling options."})

    # Score
    score = 10
    if roles["WK"] == 0:      score -= 4
    if total_bowl < 4:         score -= 3
    elif total_bowl < 5:       score -= 1
    if total_bat < 5:          score -= 2
    if roles["AR"] == 0:       score -= 1
    score = max(0, score)

    if score >= 8:
        overall = {"rating": "strong",   "text": "✅ Strong XI — well balanced squad"}
    elif score >= 5:
        overall = {"rating": "moderate", "text": "⚠️ Moderate XI — some gaps to address"}
    else:
        overall = {"rating": "weak",     "text": "❌ Weak XI — significant issues with this combination"}

    if not messages:
        messages.append({"type": "success", "icon": "🏆", "title": "Excellent balance!",
                          "text": "Your XI covers all bases — great mix of batters, all-rounders, and bowlers."})

    return jsonify({"overall": overall, "messages": messages, "composition": roles})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
