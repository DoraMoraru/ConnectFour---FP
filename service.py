import numpy as np
import random
import pygame
import sys
import math

class Service :
    def __init__(self,repo):
        self.__repo = repo
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.PLAYER = 0
        self.AI = 1
        self.EMPTY = 0
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.WINDOW_LENGTH = 4
        self.SQUARESIZE = 100
        self.width = self.COLUMN_COUNT * self.SQUARESIZE
        self.height = (self.ROW_COUNT + 1) * self.SQUARESIZE
        self.size = (self.width,self.height)
        self.RADIUS = int(self.SQUARESIZE/2 - 5)

    def get_board(self):
        return self.__repo.get_board()


    def is_valid_location(self,board, col):
    #this function checks if next location is good and it's not out of the matrix
        return board[self.ROW_COUNT - 1][col] == 0

    def get_next_open_row(self,board,col):
    #this function returns the next row that is available to be filled
        for r in range(self.ROW_COUNT) :
            if board[r][col] == 0 :
                return r

    def winning_move(self, board, piece):
        #check horizontal locations for win
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        #check vertical locations for win
        for c in range(self.COLUMN_COUNT):
            for r in range(self.ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        #check positively sloped diaganols
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(self.ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        #check negatively sloped diaganols
        for c in range(self.COLUMN_COUNT - 3):
            for r in range(3, self.ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

    def evaluate_window(self,window, piece):
    #this functions calculate the points according to the number of the pieces of the same colour
        score = 0
        opp_piece = self.PLAYER_PIECE
        if piece == self.PLAYER_PIECE:
            opp_piece = self.AI_PIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4

        return score

    def score_position(self,board, piece):
    #this function calculates the score of the next move
        score = 0
        #score center column
        center_array = [int(i) for i in list(board[:, self.COLUMN_COUNT // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        #score Horizontal
        for r in range(self.ROW_COUNT):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.COLUMN_COUNT - 3):
                window = row_array[c:c + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        #score Vertical
        for c in range(self.COLUMN_COUNT):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.ROW_COUNT - 3):
                window = col_array[r:r + self.WINDOW_LENGTH]
                score += self.evaluate_window(window, piece)

        #score posiive sloped diagonal
        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        for r in range(self.ROW_COUNT - 3):
            for c in range(self.COLUMN_COUNT - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINDOW_LENGTH)]
                score += self.evaluate_window(window, piece)

        return score

    def drop_piece(self,board,row,col,piece):
    # this function updates the matrix that containes the balls of the two players
        self.__repo.drop_piece(board,row,col,piece)

    def is_terminal_node(self,board):
    #this function checks if the next move is one that will end the game by winning
        return self.winning_move(board,self.PLAYER_PIECE) or self.winning_move(board,self.AI_PIECE) or len(self.get_valid_locations(board)) == 0

    def minimax(self,board, depth, alpha, beta, maximizingPlayer):
    #this recursive function is a mathematical algorithm that calculates and returns the best next move that the computer can make in order to win
        valid_locations = self.get_valid_locations(board)
        is_terminal = self.is_terminal_node(board)
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winning_move(board,self.AI_PIECE):
                    return (None, 100000000000000)
                elif self.winning_move(board,self.PLAYER_PIECE):
                    return (None, -10000000000000)
                else:
                # game is over, no more valid moves
                    return (None, 0)
            else:
            # depth is zero
                return (None, self.score_position(board,self.AI_PIECE))
        if maximizingPlayer:
            value = -math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board,col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.AI_PIECE)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, False)[1]
                if new_score > value:
                    value = new_score
                    column = col
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return column, value

        else:
        # minimizing player
            value = math.inf
            column = random.choice(valid_locations)
            for col in valid_locations:
                row = self.get_next_open_row(board,col)
                b_copy = board.copy()
                self.drop_piece(b_copy, row, col, self.PLAYER_PIECE)
                new_score = self.minimax(b_copy, depth - 1, alpha, beta, True)[1]
                if new_score < value:
                    value = new_score
                    column = col
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return column, value

    def get_valid_locations(self,board):
    #this function gets the columns that are still available to be filled
        valid_locations = []
        for col in range(self.COLUMN_COUNT):
            if self.is_valid_location(board, col):
                valid_locations.append(col)
        return valid_locations #the list that containts the columns

    def pick_best_move(self,board, piece):
    #this functions chooses the next best move calling other functions and returns the best coloumn
        valid_locations = self.get_valid_locations(board)
        best_score = -10000
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = self.get_next_open_row(board, col)
            temp_board = board.copy()
            self.drop_piece(temp_board, row, col, piece)
            score = self.score_position(temp_board, piece)
            if score > best_score:
                best_score = score
                best_col = col

        return best_col

