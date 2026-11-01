import unittest
from app.live_data import normalize_match, overs_to_legal_balls

class LiveProviderNormalizationTest(unittest.TestCase):
    def test_overs_are_converted_as_cricket_not_decimal(self):
        self.assertEqual(overs_to_legal_balls("14.3"), 87)
        self.assertEqual(overs_to_legal_balls("19.5"), 119)
        self.assertEqual(overs_to_legal_balls("20"), 120)

    def test_live_chase_uses_real_innings_and_calculates_target(self):
        record = {"id":"live-123","name":"North vs South","teams":["North","South"],"matchType":"t20",
            "matchStarted":True,"matchEnded":False,"status":"South need 12 runs in 9 balls",
            "score":[{"r":160,"w":7,"o":20,"inning":"North Inning 1"},
                     {"r":149,"w":5,"o":18.3,"inning":"South Inning 1"}]}
        match = normalize_match(record)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertEqual(match["battingTeam"], "South")
        self.assertEqual(match["target"], 161)
        self.assertEqual(match["runsRequired"], 12)
        self.assertEqual(match["legalBalls"], 111)
        self.assertEqual(match["ballsRemaining"], 9)
        self.assertEqual(match["requiredRunRate"], 8.0)

    def test_first_innings_does_not_invent_a_target(self):
        record = {"id":"live-1","teams":["North","South"],"matchType":"odi","matchStarted":True,
            "score":[{"r":84,"w":2,"o":16.4,"inning":"North Inning 1"}]}
        match = normalize_match(record)
        self.assertIsNotNone(match)
        assert match is not None
        self.assertIsNone(match["target"])
        self.assertEqual(match["legalBalls"], 100)

    def test_finished_matches_are_not_listed_as_live(self):
        record = {"teams":["North","South"],"matchStarted":True,"matchEnded":True,
            "score":[{"r":100,"w":5,"o":20,"inning":"North Inning 1"}]}
        self.assertIsNone(normalize_match(record))

if __name__ == "__main__":
    unittest.main()
