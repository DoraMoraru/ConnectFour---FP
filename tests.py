import unittest
import math
import numpy as np
from service import Service
from repos import Repo
class ServiceTests(unittest.TestCase):
    def test_get_next_open_row(self):
        board = np.zeros((6, 7))
        board[0][0] = 1
        ob = Service(Repo())
        r = ob.get_next_open_row(board,0)
        self.assertEqual(r, 1)

    def test_winning_move(self):
        board = np.zeros((6,7))
        board[0][0] = 1
        board[0][1] = 1
        board[0][2] = 1
        board[0][3] = 1
        ob = Service(Repo())
        self.assertEqual(ob.winning_move(board,1),True)

    def test_score_position(self):
        board = np.zeros((6,7))
        board[0][0] = 1
        board[0][1] = 1
        board[0][2] = 1
        board[0][3] = 1
        ob = Service(Repo())
        self.assertEqual(ob.score_position(board, 1), 110)

    def test_is_valid_location(self):
        board = np.zeros((6, 7))
        board[0][0] = 1
        col = 0
        ob = Service(Repo())
        self.assertEqual(ob.is_valid_location(board,col),True)

    def test_is_terminal_node(self):
        board = np.zeros((6, 7))
        board[0][0] = 1
        board[0][1] = 1
        board[0][2] = 1
        board[0][3] = 1
        ob = Service(Repo())
        self.assertEqual(ob.is_terminal_node(board), True)

    def test_minimax(self):
        board = np.zeros((6, 7))
        board[0][0] = 2
        board[0][1] = 2
        board[0][2] = 2
        board[0][3] = 2
        ob = Service(Repo())
        self.assertEqual(ob.minimax(board,0,-math.inf, math.inf, True), (None, 100000000000000))

    def test_get_valid_locations(self):
        board = np.zeros((6, 7))
        board[0][0] = 2
        ob = Service(Repo())
        self.assertEqual(ob.get_valid_locations(board), [0,1,2,3,4,5,6])

    def test_drop_piece(self):
        board = np.zeros((6,7))
        row = 0
        col = 0
        piece = 1
        ob = Service(Repo())
        ob.drop_piece(board,row,col,piece)
        self.assertEqual(board[0][0], 1)

    def test_pick_best_move(self):
        board = np.zeros((6, 7))
        board[0][0] = 2
        board[0][1] = 2
        board[0][2] = 2
        AI = 2
        ob = Service(Repo())
        self.assertEqual(ob.pick_best_move(board,AI), 3)


class RepoTests(unittest.TestCase):
    def test_drop_piece(self):
        board = np.zeros((6, 7))
        row = 0
        col = 0
        piece = 1
        ob = Repo()
        ob.drop_piece(board, row, col, piece)
        self.assertEqual(board[0][0], 1)


if __name__ == '__main__':
    unittest.main()
