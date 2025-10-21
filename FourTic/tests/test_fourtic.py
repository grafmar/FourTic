import unittest
from src.FourTic import reset_game, check_winner, handle_click

class TestFourTic(unittest.TestCase):

    def setUp(self):
        reset_game()

    def test_initial_board(self):
        board = game_board
        self.assertEqual(board, [[["" for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM)] for _ in range(DIM))

    def test_player_move(self):
        handle_click((15, 15), CELL_SIZE_CURRENT)  # Simulate a click
        self.assertEqual(game_board[0][0][0][0], "X")  # Check if the first move is recorded

    def test_winner_detection(self):
        # Simulate a winning condition
        game_board[0][0][0][0] = "X"
        game_board[0][0][1][0] = "X"
        game_board[0][0][2][0] = "X"
        game_board[0][0][3][0] = "X"
        winner = check_winner()
        self.assertEqual(winner, "X")

    def test_tie_condition(self):
        # Fill the board to create a tie
        for w in range(DIM):
            for z in range(DIM):
                for y in range(DIM):
                    for x in range(DIM):
                        game_board[w][z][y][x] = "X" if (w + z + y + x) % 2 == 0 else "O"
        winner = check_winner()
        self.assertEqual(winner, "Tie")

if __name__ == '__main__':
    unittest.main()