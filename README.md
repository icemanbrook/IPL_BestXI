#IPL 2026 — Playing XI Builder

A full-stack web app for cricket fans to build and analyse their ideal Playing 11 for any IPL 2026 team.

**Live Site**: https://playful-churros-63dc77.netlify.app

---

## What it does

- Pick any of the 10 IPL 2026 teams
- Browse the full squad with player roles and stats
- Select your 11 players
- Get instant analysis on your team's balance — bowlers, batters, all-rounders, wicketkeeper
- Strategy modes: Balanced, Batting Heavy, Bowling Heavy, Spin Pitch, Pace Pitch
- Secret easter egg for RCB fans

---

## Tech Stack

| Layer    | Tech |
|----------|------|
| Frontend | HTML, CSS, Vanilla JS |
| Backend  | Python, Flask, Flask-CORS |
| Hosting  | Netlify (frontend) + Render (backend) |

---

## Project Structure

```
ipl-xi/
├── backend/
│   ├── app.py            ← Flask API + analysis logic
│   ├── data.py           ← All 10 IPL 2026 team squads
│   └── requirements.txt
└── frontend/
    └── index.html        ← Complete frontend (single file)
```

---

## Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
API runs at `http://localhost:5000`

### Frontend
Open `frontend/index.html` in your browser. Make sure the API line points to localhost:
```js
const API = "http://localhost:5000/api";
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teams` | Get all 10 IPL teams |
| GET | `/api/squad/<team_id>` | Get squad for a team |
| POST | `/api/analyse` | Analyse a selected XI |

---

## Deployment

- **Backend** → [Render.com](https://render.com) (free tier, Web Service)
- **Frontend** → [Netlify](https://netlify.com) (free tier, drag & drop)

---

## Made by
[@icemanbrook](https://github.com/icemanbrook)
