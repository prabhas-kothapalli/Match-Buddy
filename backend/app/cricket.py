"""Cricket arithmetic uses legal balls internally; 14.3 means 87 balls."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Innings:
    runs: int
    wickets: int
    legal_balls: int
    target: int | None = None

def overs_text(legal_balls: int) -> str:
    if legal_balls < 0:
        raise ValueError("legal_balls cannot be negative")
    return f"{legal_balls // 6}.{legal_balls % 6}"

def current_run_rate(runs: int, legal_balls: int) -> float | None:
    if runs < 0 or legal_balls < 0:
        raise ValueError("runs and legal_balls cannot be negative")
    return round(runs * 6 / legal_balls, 2) if legal_balls else None

def balls_remaining(legal_balls: int, innings_limit: int = 120) -> int:
    if not 0 <= legal_balls <= innings_limit:
        raise ValueError("legal balls must be within innings limit")
    return innings_limit - legal_balls

def required_run_rate(runs_required: int, legal_balls_left: int) -> float | None:
    if runs_required < 0 or legal_balls_left < 0:
        raise ValueError("runs and balls cannot be negative")
    return round(runs_required * 6 / legal_balls_left, 2) if legal_balls_left else (0.0 if runs_required == 0 else None)

def chase_state(innings: Innings, innings_limit: int = 120) -> dict:
    if innings.runs < 0 or not 0 <= innings.wickets <= 10:
        raise ValueError("invalid innings score")
    left = balls_remaining(innings.legal_balls, innings_limit)
    needed = max(0, (innings.target or 0) - innings.runs)
    return {"overs": overs_text(innings.legal_balls), "balls_remaining": left,
            "runs_required": needed, "wickets_remaining": 10 - innings.wickets,
            "current_run_rate": current_run_rate(innings.runs, innings.legal_balls),
            "required_run_rate": required_run_rate(needed, left)}
