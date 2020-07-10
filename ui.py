import numpy as np
import random
import pygame
import sys
import math

class UI :
    def __init__(self,service):
        self.__service = service
        self.BLUE = (0,0,255)
        self.BLACK = (0,0,0)
        self.RED = (255, 0 ,0 )
        self.YELLOW = (255,255,0)
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
        self.size = (self.width, self.height)
        self.RADIUS = int(self.SQUARESIZE / 2 - 5)
        self.screen = pygame.display.set_mode(self.size)


    def get_board(self):
        return self.__service.get_board()

    def print_board(self,board):
        print(np.flip(board,0))

    def draw_board(self,board):
        for c in range(self.COLUMN_COUNT) :
            for r in range(self.ROW_COUNT) :
                pygame.draw.rect(self.screen,self.BLUE,(c*self.SQUARESIZE,r*self.SQUARESIZE+self.SQUARESIZE,self.SQUARESIZE,self.SQUARESIZE))
                pygame.draw.circle(self.screen,self.BLACK,(int(c*self.SQUARESIZE+self.SQUARESIZE/2),int(r*self.SQUARESIZE+self.SQUARESIZE+self.SQUARESIZE/2)),self.RADIUS)

        for c in range(self.COLUMN_COUNT) :
            for r in range(self.ROW_COUNT) :
                if board[r][c] == self.PLAYER_PIECE :
                    pygame.draw.circle(self.screen,self.RED,(int(c*self.SQUARESIZE +self.SQUARESIZE/2),self.height - int(r*self.SQUARESIZE +self.SQUARESIZE/2)),self.RADIUS)
                elif board[r][c] == self.AI_PIECE :
                    pygame.draw.circle(self.screen,self.YELLOW,(int(c*self.SQUARESIZE+self.SQUARESIZE/2),self.height - int(r*self.SQUARESIZE+self.SQUARESIZE/2)),self.RADIUS)

        pygame.display.update()

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
        pygame.init()
        board = self.__service.get_board()
        self.draw_board(board)
        pygame.display.update()
        myfont = pygame.font.SysFont("monospace", 75)
        turn = random.randint(self.PLAYER, self.AI)
        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                    posx = event.pos[0]
                    if turn == self.PLAYER:
                        pygame.draw.circle(self.screen, self.RED, (posx, int(self.SQUARESIZE / 2)), self.RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SQUARESIZE))
                    # print(event.pos)
                    # Ask for Player 1 Input
                    if turn == self.PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx / self.SQUARESIZE))

                        if self.is_valid_location(board, col):
                            row = self.get_next_open_row(board, col)
                            self.drop_piece(board, row, col, self.PLAYER_PIECE)

                            if self.winning_move(board, self.PLAYER_PIECE):
                                label = myfont.render("You Won!!", 1, RED)
                                screen.blit(label, (40, 10))
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            self.print_board(board)
                            self.draw_board(board)

            # # Ask for Player 2 Input
            if turn == self.AI and not game_over:

                # col = random.randint(0, COLUMN_COUNT-1)
                # col = pick_best_move(board, AI_PIECE)
                col, minimax_score = self.minimax(board, 5, -math.inf, math.inf, True)

                if self.is_valid_location(board, col):
                    # pygame.time.wait(500)
                    row = self.get_next_open_row(board, col)
                    self.drop_piece(board, row, col, self.AI_PIECE)

                    if self.winning_move(board, self.AI_PIECE):
                        label = myfont.render("You Lost!!", 1, self.YELLOW)
                        self.screen.blit(label, (40, 10))
                        game_over = True

                    self.print_board(board)
                    self.draw_board(board)

                    turn += 1
                    turn = turn % 2

            if game_over:
                pygame.time.wait(3000)

