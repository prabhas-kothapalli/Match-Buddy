# Match Buddy

**Catch up and understand, instantly.** Match Buddy now lists only matches returned as in progress by the connected live cricket provider. It does not ship or display simulated fixtures.

## Connect live scores

Match Buddy uses CricketData’s `currentMatches` API. Get a free API key at [cricketdata.org](https://cricketdata.org/), then add it to a root `.env` file:

```env
CRICKETDATA_API_KEY=your_key_here
```

Restart the backend after adding the key. The key is read only by FastAPI and is never included in browser code. Without it, the app shows setup instructions and no fixture cards. If the provider reports no matches in play, the app shows an empty state rather than upcoming games or sample scores.

The provider’s current-matches endpoint returns match status and innings totals. Match Buddy calculates legal-ball counts, current run rate, and chase requirements when the feed contains the needed innings and target. The feed may not include the active batter, bowling card, or ball-by-ball events; the app says when those details are unavailable instead of inventing them. Live list refresh runs every 15 minutes, with a manual refresh button. The backend caches the provider response for 15 minutes to stay within the provider’s stated free current-match quota.

## Run locally

Requirements: Node.js 20+ and Python 3.10+.

```bash
npm install
npm run dev
```

In another terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
cp .env.example .env
# Add CRICKETDATA_API_KEY to .env
uvicorn app.main:app --app-dir backend --reload --port 8000
```

Open the Vite URL printed in the first terminal. If port 5173 is busy, Vite may select the next available port.

## Ask Buddy AI (optional)

The live-feed contextual fallback works without an AI key. For Gemini-powered responses, also set:

```env
GEMINI_API_KEY=your_key_here
GEMINI_MODEL=gemini-3.5-flash-lite
```

Gemini receives the selected live-match context, question, and recent chat turns. Its instructions prohibit inventing events or player statistics missing from the provider response. Keep the key in the backend `.env`; do not use a `VITE_` variable.

## Product features

- Home, live match discovery, live Match Centre, Ask Buddy, experience preferences, and settings.
- Live match filtering/search; scorecards use the latest provider innings totals.
- Match-specific live Q&A for score, target, run rate, over notation, cricket laws, and follow-up questions.
- Three-part “What Did I Miss?” based only on feed facts, with missing event details called out.
- Beginner, Casual, Regular, and Expert explanation styles saved in browser storage.
- Cricket arithmetic represents overs as legal balls internally (`14.3` means 87 balls).
- Responsive layouts, keyboard focus states, and reduced-motion support.

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `CRICKETDATA_API_KEY` | Server-side live cricket provider key | unset; live feed is not configured |
| `GEMINI_API_KEY` | Optional server-side Gemini key for open-ended answers | unset; built-in cricket guide |
| `GEMINI_MODEL` | Gemini model name | `gemini-3.5-flash-lite` |
| `FRONTEND_ORIGIN` | CORS origin | `http://localhost:5173` |

Optional `VITE_API_URL` can point the frontend to a deployed FastAPI base URL. Do not put CricketData or Gemini secrets in a `VITE_` variable.

## API endpoints

- `GET /api/health` — service and provider configuration status.
- `GET /api/live-matches` — current in-play matches from CricketData.
- `GET /api/live-matches/{match_id}` — a current live match.
- `POST /api/ask` — match-context Q&A.

## Verification

```bash
npm run build
PYTHONPATH=backend python3 -m unittest discover -s backend/tests -v
```

## Current limits

The live feed must be configured with a provider key before live match cards and Q&A can load. CricketData controls match coverage and the details included in its current-matches response. This integration does not claim to provide ball-by-ball commentary, confirmed lineups, or full player scorecards when the selected feed response omits them. Authentication, stored conversations, and a production database are not included.
