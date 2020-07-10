import numpy as np
import random
import math

class UI :
    def __init__(self,service,valid):
        self.__service = service
        self.ROW_COUNT = 6
        self.COLUMN_COUNT = 7
        self.PLAYER = 0
        self.AI = 1
        self.EMPTY = 0
        self.PLAYER_PIECE = 1
        self.AI_PIECE = 2
        self.__valid = valid

    def get_board(self):
        return self.__service.get_board()

    def print_board(self,board):
        print(np.flip(board,0))

    def drop_piece(self,board,row,col,piece):
        self.__service.drop_piece(board,row,col,piece)

    def is_valid_location(self,board, col):
        return self.__service.is_valid_location(board,col)

    def get_next_open_row(self,board,col):
        return self.__service.get_next_open_row(board,col)

    def winning_move(self,board,piece):
        return self.__service.winning_move(board,piece)

    def evaluate_window(self,window,piece):
        return self.__service.evaluate_window(window,piece)

    def score_position(self,board,piece):
        return self.__service.score_position(board,piece)

    def is_terminal_node(self,board):
        return self.__service.is_terminal_node(board)

    def minimax(self,board,depth,alpha,beta,maximizingPlayer):
        col,val = self.__service.minimax(board,depth,alpha,beta,maximizingPlayer)
        return col,val

    def get_valid_locations(self,board):
        l = []
        l = self.__service.get_valid_locations(board)
        return l

    def pick_best_move(self,board,piece):
        return self.__service.pick_best_move(board,piece)

    def run(self):
        game_over = False
        board = self.__service.get_board()
        turn = random.randint(self.PLAYER, self.AI)
        while not game_over :
            if turn == self.PLAYER:
                col = int(input("Make your selection(0-6): "))
                try :
                    self.__valid.check_valid_input(col)
                    if self.is_valid_location(board, col):
                        row = self.get_next_open_row(board, col)
                        self.drop_piece(board, row, col, self.PLAYER_PIECE)

                        if self.winning_move(board, self.PLAYER_PIECE):
                            print("You Won!!!")
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        self.print_board(board)
                except Exception as ex:
                    print(str(ex))




            if turn == self.AI and not game_over:

                # col = random.randint(0, COLUMN_COUNT-1)
                # col = pick_best_move(board, AI_PIECE)
                col, minimax_score = self.minimax(board, 5, -math.inf, math.inf, True)

                if self.is_valid_location(board, col):
                    # pygame.time.wait(500)
                    row = self.get_next_open_row(board, col)
                    self.drop_piece(board, row, col, self.AI_PIECE)

                    if self.winning_move(board, self.AI_PIECE):
                        print("You Lost!!")
                        game_over = True

                    self.print_board(board)

                    turn += 1
                    turn = turn % 2

            if game_over:
                return
