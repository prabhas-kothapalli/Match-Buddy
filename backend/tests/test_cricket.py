import unittest
from app.cricket import Innings, balls_remaining, chase_state, current_run_rate, overs_text, required_run_rate

class CricketCalculationsTest(unittest.TestCase):
    def test_cricket_overs_use_legal_balls(self):
        self.assertEqual(overs_text(87), "14.3")
        self.assertEqual(overs_text(119), "19.5")

    def test_chase_at_fourteen_overs(self):
        state = chase_state(Innings(112, 3, 84, 181))
        self.assertEqual(state["overs"], "14.0")
        self.assertEqual(state["runs_required"], 69)
        self.assertEqual(state["balls_remaining"], 36)
        self.assertEqual(state["required_run_rate"], 11.5)
        self.assertEqual(state["wickets_remaining"], 7)

    def test_chase_at_nineteen_overs(self):
        state = chase_state(Innings(168, 5, 114, 175))
        self.assertEqual(state["overs"], "19.0")
        self.assertEqual(state["runs_required"], 7)
        self.assertEqual(state["balls_remaining"], 6)
        self.assertEqual(state["required_run_rate"], 7.0)

    def test_empty_innings_and_completed_chase(self):
        self.assertIsNone(current_run_rate(0, 0))
        self.assertEqual(required_run_rate(0, 0), 0.0)
        self.assertIsNone(required_run_rate(1, 0))
        self.assertEqual(balls_remaining(120), 0)

    def test_invalid_values_are_rejected(self):
        with self.assertRaises(ValueError):
            overs_text(-1)
        with self.assertRaises(ValueError):
            balls_remaining(121)
        with self.assertRaises(ValueError):
            chase_state(Innings(10, 11, 6, 15))

if __name__ == "__main__":
    unittest.main()
