import numpy as np
import random
import pygame
import sys
import math

class Repo :
    def __init__(self):
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.board = np.zeros((self.ROW_COUNT, self.COLUMN_COUNT))

    def drop_piece(self,board,row,col,piece):
    #this function updates the matrix that containes the balls of the two players
        board[row][col] = piece

    def get_board(self):
    #this function returns the matrix
        return self.board
