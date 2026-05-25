# IPL 2026 — Playing XI Builder

A full-stack web app to build and analyse your IPL 2026 Playing XI.

---

## Project Structure

```
ipl-xi/
├── backend/
│   ├── app.py            ← Flask API
│   ├── data.py           ← All 10 team squads
│   └── requirements.txt  ← Python dependencies
└── frontend/
    └── index.html        ← Complete frontend (single file)
```

---

## Run Locally

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```
The API runs at http://localhost:5000

### 2. Frontend
Just open `frontend/index.html` in your browser. That's it.

---

## Host Online (so your friends can use it too)

### Backend → Render.com (free)

1. Push your project to GitHub
2. Go to https://render.com → New → Web Service
3. Connect your repo, set:
   - **Root directory**: `backend`
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `gunicorn app:app`
4. Deploy — Render gives you a URL like `https://ipl-xi-backend.onrender.com`

### Frontend → Netlify (free)

1. Go to https://netlify.com → Add new site → Deploy manually
2. Drag and drop your `frontend/` folder
3. Before deploying, update the API line in `index.html`:

```js
// Change this line:
const API = "http://localhost:5000/api";

// To your Render backend URL:
const API = "https://ipl-xi-backend.onrender.com/api";
```

4. Netlify gives you a URL like `https://ipl-xi.netlify.app` — share with friends!

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teams` | List all 10 IPL teams |
| GET | `/api/squad/<team_id>` | Get full squad for a team |
| POST | `/api/analyse` | Analyse a selected XI |

### POST /api/analyse — Request body
```json
{
  "team": "RCB",
  "strategy": "balanced",
  "players": ["Virat Kohli", "Rajat Patidar", "...9 more names"]
}
```

---

## Notes
- Free tier on Render may sleep after inactivity — first load can take ~30 seconds to wake up
- To avoid this, upgrade to Render's paid tier ($7/mo) or use Railway.app instead
