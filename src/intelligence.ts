import type { ChatTurn, Experience, LiveMatch } from './data';

const matchSummary = (match: LiveMatch) => {
  const rate = match.currentRunRate ? ` The scoring rate is ${match.currentRunRate} runs per over.` : '';
  if (match.target === null) {
    return `${match.battingTeam || 'The batting side'} are ${match.runs}/${match.wickets} after ${match.overs} overs.${rate} The feed has not provided a target.`;
  }
  return `${match.battingTeam} are ${match.runs}/${match.wickets} after ${match.overs} overs, chasing ${match.target}; ${match.runsRequired} runs are needed from ${match.ballsRemaining} balls.${rate}`;
};

export function answerLiveQuestion(question: string, match: LiveMatch, level: Experience, history: ChatTurn[] = []): string {
  const q = question.toLowerCase();
  const simple = level === 'Beginner';

  if (/\b(lbw|leg before wicket)\b/.test(q)) {
    return 'LBW means leg before wicket. The umpire checks where the ball pitched, where it hit the batter, whether the batter offered a shot, and whether it would have hit the stumps. There are specific exceptions and conditions, so the exact decision depends on all of those details. I can explain the rule, but this live feed does not show whether an LBW appeal happened in this match.';
  }
  if (/\b(drs|review|upstairs|third umpire)\b/.test(q)) {
    return 'A DRS review lets a team challenge certain on-field decisions, subject to that competition’s rules. The third umpire may use replays, ball tracking, or edge detection; the evidence and the law decide whether the call changes. A review being requested does not tell us its result, and this feed does not include review events.';
  }
  if (/\b(power.?play|fielding restriction)\b/.test(q)) {
    return 'A powerplay is a limited-overs period when the fielding side has restrictions on how many players can stand outside the inner circle. The exact overs and limits depend on the format and competition. It encourages attacking batting early and affects field placement. Test cricket has no powerplay.';
  }
  if (/\b(wide|no.?ball|free hit|illegal delivery)\b/.test(q)) {
    return 'A wide or no-ball gives the batting side at least one extra and must be bowled again, so it does not count as one of the six legal balls in an over. A no-ball can bring a free hit in many limited-overs competitions, with dismissal restrictions set by the playing conditions. A wide is judged by whether the batter could reasonably play a normal stroke.';
  }
  if (/\b(follow.?on|declaration|declare|draw|test match|test cricket)\b/.test(q)) {
    return 'In Test cricket, each team can bat up to twice. The follow-on is an option for the team with a sufficiently large first-innings lead; the required margin depends on match length and playing conditions. A captain can declare an innings closed to give the other side time to bat. A Test may end in a win, tie, or draw if time expires without a result.';
  }
  if (/\b(strike rate|batting average|economy rate|bowling average|dot ball|maiden)\b/.test(q)) {
    return 'A batter’s strike rate is runs per 100 balls; batting average is runs divided by the number of times they were out. A bowler’s economy is runs conceded per over, and bowling average is runs conceded per wicket. A dot ball scores no runs to the batter; a maiden is an over with no runs charged to the bowler. Tell me which one you’re looking at and I can explain it with an example.';
  }
  if (/\b(boundary|four|six|run out|stumped|caught|bowled|dismiss|wicket|duck|extras|partnership)\b/.test(q)) {
    return 'A boundary is four if the ball reaches the rope after bouncing, or six if it clears the rope without bouncing. A wicket is a batter’s dismissal; common ways include bowled, caught, run out, stumped, and LBW. Extras are runs not credited to a batter, such as wides and no-balls. A partnership is the runs added while two batters are together. Ask about one of these and I can go deeper.';
  }
  if (/\b(format|t20|twenty.?20|odi|one.?day|innings|overs per side|how long)\b/.test(q)) {
    return 'The main international formats are Test cricket, ODIs, and T20 Internationals. Tests can last up to five days and each side may bat twice; ODIs are usually 50 overs per side, and T20s are 20 overs per side. Domestic competitions can use different lengths and playing conditions.';
  }
  if (/\b(required run rate|asking rate|run rate|rate climbing|rate going up|rate changed|rate matter|why.*rate)\b/.test(q)) {
    if (match.requiredRunRate === null || match.runsRequired === null || match.ballsRemaining === null) {
      return `A required rate applies only when a target is set. ${matchSummary(match)}`;
    }
    return `${match.battingTeam} need ${match.runsRequired} runs from ${match.ballsRemaining} balls, so the required rate is ${match.requiredRunRate} per over. ${simple ? 'That is the pace they need from now on. ' : ''}It rises when balls are used without enough runs and falls after productive scoring.`;
  }
  if (/\b(score|runs|wickets|overs|current situation|target|chase)\b/.test(q)) return matchSummary(match);
  if (/\b(batter|batsman|player|bowler|bowling|lineup|playing xi|who is batting)\b/.test(q)) {
    return `The provider's current-match feed does not include a player scorecard or confirmed playing XI for ${match.name}. I can explain what a batting or bowling figure means, but I cannot verify the player names or numbers from this feed.`;
  }
  if (/\b(what happened|what did i miss|turning point|last wicket|latest event|last ball|last over)\b/.test(q)) {
    return `This provider feed gives innings totals but no ball-by-ball events, so I can't confirm a specific wicket or turning point. ${matchSummary(match)}`;
  }
  if (/\b(who.*ahead|who.*winning|in control|momentum|pressure|favourite|favorite)\b/.test(q)) {
    return `${matchSummary(match)} The feed does not include recent deliveries or player details, so any momentum call would be an interpretation rather than a confirmed fact.`;
  }
  if (/\b(over|overs|legal ball)\b/.test(q)) {
    return `An over is six legal balls. Wides and no-balls add runs but are bowled again, so they do not count toward those six. ${match.name} is currently at ${match.overs} overs in the feed.`;
  }

  const userTurns = history.filter(turn => turn.role === 'user');
  const previous = userTurns[userTurns.length - 1]?.text;
  if (previous && /^(why|how|what about|and|then|which|who|that|it|they|them|more|explain that)\b/i.test(question.trim())) {
    return `About your question on “${previous}”: ${matchSummary(match)} I can also explain the cricket rule or statistic behind it. The feed does not include a full event log.`;
  }

  return `I can help with cricket rules, formats, tactics, statistics, and this match. ${matchSummary(match)} I can't verify player or ball-by-ball details that the feed does not contain. For a general cricket question, ask it directly and I’ll explain the concept.`;
}
