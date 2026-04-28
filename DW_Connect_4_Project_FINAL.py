import pygame
import sys
import numpy as np
import math


BLUE = (0,0,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

X_COUNT = 6
Y_COUNT = 7


def create_board():
    board = np.zeros((X_COUNT, Y_COUNT)) 
    return board

def drop_piece(board, row, select, piece):
    board[row][select] = piece

def is_valid_location(board, select):
    return board[X_COUNT - 1][select] == 0

def get_next_open_row(board, select):
    for r in range(X_COUNT):
        if board[r][select] == 0:
            return r
            
def print_board(board): 
   print(np.flip(board, 0))

def winning_move(board, piece):
    for c in range(Y_COUNT - 3):
        for n in range(X_COUNT):
            if board[n][c] == piece and board[n][c+1] == piece and board[n][c+2] == piece and board[n][c+3] == piece: 
                return True    

    for c in range(Y_COUNT):
        for n in range(X_COUNT - 3):
            if board[n][c] == piece and board[n+1][c] == piece and board[n+2][c] == piece and board[n+3][c] == piece: 
                return True 

    for c in range(Y_COUNT - 3):
        for n in range(X_COUNT - 3):
            if board[n][c] == piece and board[n+1][c+1] == piece and board[n+2][c+2] == piece and board[n+3][c+3] == piece: 
                return True 

    for c in range(Y_COUNT - 3):
        for n in range(3, X_COUNT):
            if board[n][c] == piece and board[n-1][c+1] == piece and board[n-2][c+2] == piece and board[n-3][c+3] == piece: 
                return True
    return False
            
def draw_board(board):
   for c in range(Y_COUNT):
       for n in range(X_COUNT):
           pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, n*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
           pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(n*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
   for c in range(Y_COUNT):
        for n in range(X_COUNT):
            if board[n][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(n*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[n][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height - int(n*SQUARESIZE+SQUARESIZE/2)), RADIUS)

   pygame.display.update()

   

board = create_board() 
print_board(board)
game_over = False
player_turn = 0 

pygame.init()

SQUARESIZE = 100 

width = Y_COUNT * SQUARESIZE
height = (X_COUNT+1) * SQUARESIZE

game_size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(game_size)
draw_board(board)
pygame.display.update()

font = pygame.font.SysFont("Aerial", 100)

while not game_over:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if player_turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
        pygame.display.update() 

        if event.type == pygame.MOUSEBUTTONDOWN:
            #print(event.pos)
            
            # Ask for Player 1 Input
            if player_turn == 0:
                posx = event.pos[0]
                select = int(math.floor(posx/SQUARESIZE)) 

                if is_valid_location(board, select):
                    row = get_next_open_row(board, select)
                    drop_piece(board, row, select, 1)

                if winning_move(board, 1):
                    label = font.render("PLAYER 1 WINS!!", 2, RED)
                    screen.blit(label, (40,10 ))
                    game_over = True   
                    screen.blit(label, (40, 10))
                    pygame.display.update()
                
                print(select)
                print(type(select))

            # Ask for Player 2 Input
            else:
                posx = event.pos[0]
                select = int(math.floor(posx/SQUARESIZE)) 
            

                if is_valid_location(board, select):
                    row = get_next_open_row(board, select)
                    drop_piece(board, row, select, 2)

                if winning_move(board, 2):
                    label = font.render("PLAYER 2 WINS!!", 2, YELLOW)
                    screen.blit(label, (40,10 ))
                    game_over = True   

            print_board(board)
            draw_board(board)

            player_turn += 1
            player_turn = player_turn % 2

            if game_over:
                pygame.time.wait(3000)
