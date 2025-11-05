import unittest
from game_logic import SOSGame, Move, DEFAULT_PLAYERS


def triple_same_cells(a, b):
    """Order-agnostic equality for a 3-cell SOS triple."""
    return set(a) == set(b)


class TestSOSSimpleMode(unittest.TestCase):
    def setUp(self):
        self.game = SOSGame(players=DEFAULT_PLAYERS, board_size=3, mode="simple")

    def test_simple_horizontal_sos_wins(self):
        # S O S across top row → immediate win
        self.game.process_move(Move(0, 0, "S"))
        self.assertFalse(self.game.has_winner(), "No winner after first S")
        self.game.process_move(Move(0, 1, "O"))
        self.assertFalse(self.game.has_winner(), "No winner after S,O")
        self.game.process_move(Move(0, 2, "S"))

        self.assertTrue(self.game.has_winner(), "Simple mode should win on first SOS")
        self.assertTrue(len(self.game.last_new_sos) >= 1)
        # Accept either orientation of the triple
        self.assertTrue(
            any(triple_same_cells(t, [(0, 0), (0, 1), (0, 2)]) for t in self.game.last_new_sos)
        )
        # Winner label should match current player at the moment of scoring
        self.assertEqual(self.game.winner_label, self.game.current_player.label)

    def test_simple_diagonal_sos_wins(self):
        # Build \ diagonal: (0,0) S, (1,1) O, (2,2) S
        self.game.process_move(Move(0, 0, "S"))
        self.game.process_move(Move(1, 1, "O"))
        self.game.process_move(Move(2, 2, "S"))

        self.assertTrue(self.game.has_winner())
        self.assertTrue(
            any(triple_same_cells(t, [(0, 0), (1, 1), (2, 2)]) for t in self.game.last_new_sos)
        )

    def test_simple_tie_full_board_no_sos(self):
        # Fill a 3x3 board with no SOS anywhere
        # Layout:
        # S S O
        # O S S
        # O O S
        moves = [
            (0, 0, "S"), (0, 1, "S"), (0, 2, "O"),
            (1, 0, "O"), (1, 1, "S"), (1, 2, "S"),
            (2, 0, "O"), (2, 1, "O"), (2, 2, "S"),
        ]
        for r, c, ch in moves:
            self.game.process_move(Move(r, c, ch))

        self.assertFalse(self.game.has_winner())
        self.assertTrue(self.game.is_tied(), "Full board with no SOS should be a tie")


class TestSOSGeneralMode(unittest.TestCase):
    def setUp(self):
        self.game = SOSGame(players=DEFAULT_PLAYERS, board_size=3, mode="general")

    def test_general_scoring_does_not_end_game(self):
        # Make a horizontal SOS on row 0: S O S
        # Game should continue; current player's score increments by 1.
        current = self.game.current_player.label

        self.game.process_move(Move(0, 0, "S"))
        self.game.process_move(Move(0, 1, "O"))
        self.game.process_move(Move(0, 2, "S"))

        self.assertFalse(self.game.is_over(), "General mode should not end after first SOS")
        self.assertEqual(self.game.scores[current], 1, "Scoring player should get +1")

    def test_general_multiple_sos_counts(self):
        # Create a scenario where one move forms two SOS (if possible).
        # Bottom row: S O S, and also use the same 'O' as middle for another direction.
        # For simplicity, ensure at least one SOS then add a second distinct SOS later.
        # First SOS:
        scorer = self.game.current_player.label
        self.game.process_move(Move(0, 0, "S"))
        self.game.process_move(Move(0, 1, "O"))
        self.game.process_move(Move(0, 2, "S"))
        self.assertEqual(self.game.scores[scorer], 1)

        # Second SOS for same player (e.g., diagonal):
        # Toggle to the other player and back to original to keep test simple and deterministic.
        self.game.toggle_player()
        self.game.toggle_player()
        # Diagonal: (0,0) S already; place O at (1,1) and S at (2,2)
        self.game.process_move(Move(1, 1, "O"))
        self.game.process_move(Move(2, 2, "S"))

        self.assertGreaterEqual(self.game.scores[scorer], 2, "Should be able to score multiple SOS over time")

    def test_general_game_over_on_full_board_and_winner(self):
        # Fill the board ensuring at least one SOS has been scored by someone.
        # Start by scoring one SOS for the current player.
        starter = self.game.current_player.label
        self.game.process_move(Move(0, 0, "S"))
        self.game.process_move(Move(0, 1, "O"))
        self.game.process_move(Move(0, 2, "S"))
        self.assertEqual(self.game.scores[starter], 1)

        # Fill remaining cells (arbitrary, avoiding invalid moves)
        for r in range(3):
            for c in range(3):
                if self.game._current_moves[r][c].label == "":
                    # Fill with something valid; alternate letters so we don't accidentally block input
                    self.game.process_move(Move(r, c, "S"))

        self.assertTrue(self.game.is_over(), "General mode should end when the board is full")
        # Either a winner exists (higher score) or tie if equal scores
        scores = self.game.scores
        top = max(scores.values())
        second = sorted(scores.values(), reverse=True)[1] if len(scores) >= 2 else 0
        if top == second:
            self.assertTrue(self.game.is_tied())
            self.assertFalse(self.game.has_winner())
        else:
            self.assertTrue(self.game.has_winner())
            self.assertEqual(self.game.winner_label, max(scores, key=lambda k: scores[k]))

    def test_invalid_move_rejected(self):
        # Place once, then try to place again on same cell.
        self.assertTrue(self.game.is_valid_move(Move(1, 1, "S")))
        self.game.process_move(Move(1, 1, "S"))
        self.assertFalse(self.game.is_valid_move(Move(1, 1, "O")), "Second move on same cell must be invalid")


if __name__ == "__main__":
    unittest.main()
