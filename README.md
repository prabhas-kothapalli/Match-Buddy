# Match Buddy

**Catch up and understand cricket, instantly.** Match Buddy is a live-cricket companion for finding matches in play, understanding the score, and asking questions about cricket or the selected match.

The app combines a React and TypeScript frontend with a FastAPI backend. Live scores come from CricketData, and optional Gemini integration powers open-ended answers from the backend.

## What you can do

- Browse and search matches currently marked as in play by the live provider.
- Open a Match Centre with the current score, innings totals, match status, and available chase calculations.
- Ask Buddy about cricket rules, tactics, terminology, formats, statistics, and the selected live match.
- Get a quick match catch-up based on the facts available in the score feed.
- Choose Beginner, Casual, Regular, or Expert answer styles.
- Use the responsive interface on desktop and mobile.

## How live data and answers work

Match Buddy requests current matches from CricketData's `currentMatches` endpoint. It calculates cricket overs as legal balls (for example, `14.3` means 14 overs and 3 balls) and derives run rates or chase details when the feed includes the needed information. Results are cached by the backend for 15 minutes, and the interface also offers manual refresh.

Ask Buddy uses Gemini when `GEMINI_API_KEY` is configured. The backend sends Gemini the user's question, recent chat context, and the selected match data. If Gemini is unavailable or no key is configured, the app uses its built-in cricket guide. Match Buddy does not invent missing live facts: the current-matches feed may not provide ball-by-ball events, player scorecards, or confirmed lineups, so answers call out those limits.

## Run locally

### Requirements

- Node.js 20 or newer
- Python 3.10 or newer
- A CricketData API key for live matches
- A Gemini API key is optional

### 1. Configure the backend

From the project root, create your local environment file and install the Python dependencies:

```bash
cp .env.example .env
```

Add your provider credentials to `.env`:

```env
CRICKETDATA_API_KEY=your_cricketdata_key
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-3.5-flash-lite
FRONTEND_ORIGIN=http://localhost:5173
```

`GEMINI_API_KEY` is optional. Keep keys in `.env` on the backend; do not put them in frontend variables such as `VITE_GEMINI_API_KEY`.

Install backend dependencies and start FastAPI in a terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8000
```

### 2. Start the frontend

In a second terminal, from the project root:

```bash
npm install
npm run dev
```

Open the local URL printed by Vite (usually `http://localhost:5173`). The FastAPI backend must also be running at `http://localhost:8000`. If Vite selects another port, set `FRONTEND_ORIGIN` in `.env` to that frontend origin and restart the backend.

## Configuration

| Variable | Required | Description | Default |
| --- | --- | --- | --- |
| `CRICKETDATA_API_KEY` | For live data | Server-side key for CricketData's current-matches API | Not set |
| `GEMINI_API_KEY` | No | Server-side key for Gemini-powered Ask Buddy answers | Built-in cricket guide is used |
| `GEMINI_MODEL` | No | Gemini model name | `gemini-3.5-flash-lite` |
| `FRONTEND_ORIGIN` | No | Frontend origin allowed by the backend's CORS policy | `http://localhost:5173` |
| `VITE_API_URL` | No | FastAPI base URL used by the frontend | `http://localhost:8000` |

`VITE_API_URL` is for the backend URL only. Provider credentials must remain server-side.

## API

The FastAPI service exposes:

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/api/health` | Check backend health and whether the live provider is configured. |
| `GET` | `/api/live-matches` | Fetch the current in-play match list. |
| `GET` | `/api/live-matches/{match_id}` | Fetch a match from the current live list. |
| `POST` | `/api/ask` | Ask a question about cricket and a selected live match. |

Example Ask Buddy request:

```json
{
  "question": "What does this score mean?",
  "match_id": "match-id-from-the-live-list",
  "experience_level": "Casual",
  "history": []
}
```

Interactive API documentation is available at `http://localhost:8000/docs` while the backend is running.

## Project structure

```text
.
├── backend/
│   ├── app/
│   │   ├── main.py        # FastAPI routes, provider access, and Ask Buddy
│   │   ├── live_data.py   # Live match normalization and score calculations
│   │   └── cricket.py     # Cricket scoring arithmetic
│   └── tests/             # Backend unit tests
├── src/
│   ├── App.tsx            # React app and page components
│   ├── data.ts            # Frontend types and cricket helpers
│   ├── intelligence.ts    # Built-in answer fallback
│   └── style.css          # App styles
├── .env.example           # Environment variable template
└── README.md
```

## Build and tests

Build the frontend:

```bash
npm run build
```

Run the backend unit tests:

```bash
PYTHONPATH=backend python3 -m unittest discover -s backend/tests -v
```

## Current limitations

- Live match coverage and freshness depend on the CricketData plan, API availability, and the provider's response.
- If CricketData reports no matches in play, the app shows an empty state; it does not substitute demo fixtures.
- The current-matches endpoint may omit ball-by-ball commentary, batter and bowler scorecards, or confirmed playing XIs.
- Match-specific answers can only verify facts included in the live feed. General cricket answers can still use Gemini or the built-in guide.
- The project does not include user accounts, persistent chat storage, or a production database.

## Security

`.env` is excluded from Git by `.gitignore`. Never commit API keys. If a key is exposed, revoke it with its provider and replace it in your local `.env`.
