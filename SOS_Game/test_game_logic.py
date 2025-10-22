import unittest
from game_logic import SOSGame, Move, DEFAULT_PLAYERS


class TestSOSGameMore(unittest.TestCase):
    def test_row_win_detected(self):
        """Filling the top row with the same letter should trigger a win and capture the winning combo."""
        game = SOSGame(players=DEFAULT_PLAYERS, board_size=3)
        # Play three "S" moves across the top row
        game.process_move(Move(0, 0, "S"))
        game.process_move(Move(0, 1, "S"))
        game.process_move(Move(0, 2, "S"))

        self.assertTrue(game.has_winner(), "Game should report a winner after full identical row")
        # Winner combo should be the top row coordinates in order [(0,0), (0,1), (0,2)]
        self.assertEqual(game.winner_combo, [(0, 0), (0, 1), (0, 2)])

    def test_reset_game_clears_board_and_state(self):
        """After a win, reset_game() should clear moves, winner flag, and winner combo."""
        game = SOSGame(players=DEFAULT_PLAYERS, board_size=3)
        # Force a quick win
        game.process_move(Move(0, 0, "S"))
        game.process_move(Move(0, 1, "S"))
        game.process_move(Move(0, 2, "S"))
        self.assertTrue(game.has_winner(), "Precondition: there should be a winner before reset")

        # Now reset and verify everything is cleared
        game.reset_game()
        self.assertFalse(game.has_winner(), "Winner flag should be cleared after reset")
        self.assertEqual(game.winner_combo, [], "Winner combo should be cleared after reset")
        # Board should be back to all empty labels
        all_labels = [m.label for row in game._current_moves for m in row]
        self.assertTrue(all(lbl == "" for lbl in all_labels), "All cells should be empty after reset")


if __name__ == "__main__":
    unittest.main()
