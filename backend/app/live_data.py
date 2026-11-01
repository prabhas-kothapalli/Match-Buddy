"""Normalize current-match records without inventing scorecard detail."""
from typing import Any
import re

def overs_to_legal_balls(value: Any) -> int:
    """Provider overs use cricket notation: 14.3 is 14 overs and 3 balls."""
    whole, _, fraction = str(value or "0").partition(".")
    try:
        completed, balls = int(whole), int((fraction or "0")[:1])
    except (ValueError, TypeError):
        return 0
    if completed < 0 or not 0 <= balls <= 5:
        return 0
    return completed * 6 + balls

def normalize_match(raw: dict[str, Any]) -> dict[str, Any] | None:
    teams = raw.get("teams") or []
    if len(teams) < 2:
        return None
    home, away = str(teams[0]), str(teams[1])
    innings: list[dict[str, Any]] = []
    for row in raw.get("score") or []:
        if not isinstance(row, dict):
            continue
        label = str(row.get("inning") or "")
        batting_team = next((team for team in teams if str(team).lower() in label.lower()), "")
        runs, wickets, overs = row.get("r", row.get("runs")), row.get("w", row.get("wickets")), row.get("o", row.get("overs"))
        if runs is None or wickets is None or overs is None:
            continue
        over_text = str(overs)
        innings.append({"team":batting_team or label or "Unknown team", "runs":int(runs), "wickets":int(wickets), "overs":over_text,"legal_balls":overs_to_legal_balls(over_text)})
    if not innings:
        return None
    started, ended = raw.get("matchStarted"), raw.get("matchEnded")
    status = str(raw.get("status") or "In progress")
    if started is False or ended is True or re.search(r"\b(won by|drawn|abandoned|no result|match tied|completed)\b", status, re.I):
        return None
    current, prior = innings[-1], innings[-2] if len(innings)>1 else None
    match_type = str(raw.get("matchType") or "Cricket").lower()
    limited = match_type in ("t20","t20i","odi","one day")
    if started is None and not raw.get("live"):
        return None
    if prior and limited:
        target = prior["runs"]+1
    else:
        target = None
    runs_required = max(0,target-current["runs"]) if target is not None else None
    balls_limit = 120 if match_type in ("t20","t20i") else 300 if match_type in ("odi","one day") else None
    balls_remaining = max(0,balls_limit-current["legal_balls"]) if balls_limit is not None else None
    crr = round(current["runs"]*6/current["legal_balls"],2) if current["legal_balls"] else None
    rrr = None
    if runs_required is not None and balls_remaining is not None:
        rrr = round(runs_required*6/balls_remaining,2) if balls_remaining else (0.0 if runs_required==0 else None)
    batting_team=current["team"]
    bowling_team=away if batting_team.lower()==home.lower() else home if batting_team.lower()==away.lower() else ""
    name=str(raw.get("name") or f"{home} vs {away}")
    return {"id":str(raw.get("id") or ""),"name":name,"home":home,"away":away,
        "homeCode":"".join(part[0] for part in home.split() if part)[:3].upper(),
        "awayCode":"".join(part[0] for part in away.split() if part)[:3].upper(),
        "format":match_type.upper(),"competition":str(raw.get("series") or raw.get("seriesName") or raw.get("matchType") or "Cricket"),
        "venue":str(raw.get("venue") or "Venue not provided"),"status":status,
        "dateTimeGMT":str(raw.get("dateTimeGMT") or raw.get("date") or ""),"battingTeam":batting_team,
        "bowlingTeam":bowling_team,"innings":innings,"runs":current["runs"],"wickets":current["wickets"],
        "overs":current["overs"],"legalBalls":current["legal_balls"],"target":target,"runsRequired":runs_required,
        "ballsRemaining":balls_remaining,"currentRunRate":crr,"requiredRunRate":rrr,"summary":status,"live":True,
        "tossWinner":raw.get("tossWinner"),"tossChoice":raw.get("tossChoice")}
