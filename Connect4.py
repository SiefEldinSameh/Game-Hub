import pygame
import sys
import numpy as np
from collections import deque

# Pygame setup
pygame.init()

# Constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE  # extra row for moving disk
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 8)  # Slightly smaller for better visual

# Colors
BLUE = (30, 144, 255)  # Dodger Blue
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 69, 0)     # Red-Orange
YELLOW = (255, 215, 0) # Gold
GRAY = (250, 250, 250) # Light Gray
BOARD_COLOR = (25, 25, 112)  # Midnight Blue

# Screen setup
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 - Enhanced Edition")

# Font setup
try:
    font = pygame.font.SysFont("comicsansms", 40)
    small_font = pygame.font.SysFont("comicsansms", 30)
except:
    font = pygame.font.SysFont("Arial", 40)
    small_font = pygame.font.SysFont("Arial", 30)

# Game board (2D numpy array)
board = np.zeros((ROW_COUNT, COLUMN_COUNT))

# Data Structures
move_history = []  # Stack to track moves for undo functionality
valid_moves = deque(range(COLUMN_COUNT))  # Queue for tracking valid moves

def draw_board(board):
    # Draw background
    screen.fill(BOARD_COLOR)
    
    # Draw header area
    pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARESIZE))
    
    # Draw the grid
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, 
                           (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, 
                             (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS+2)
            
            # Draw pieces
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, 
                                 (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, 
                                 (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, BLACK, 
                                 (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    pygame.display.update()

def draw_turn_indicator(turn):
    pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARESIZE))
    if turn == 0:
        text = small_font.render("Player 1's Turn (RED)", True, RED)
    else:
        text = small_font.render("Player 2's Turn (YELLOW)", True, YELLOW)
    screen.blit(text, (width//2 - text.get_width()//2, SQUARESIZE//2 - text.get_height()//2))
    pygame.display.update()

def draw_win_message(winner):
    pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARESIZE))
    if winner == 1:
        text = font.render("Player 1 (RED) Wins!", True, RED)
    else:
        text = font.render("Player 2 (YELLOW) Wins!", True, YELLOW)
    screen.blit(text, (width//2 - text.get_width()//2, SQUARESIZE//2 - text.get_height()//2))
    
    pygame.display.update()

def draw_draw_message():
    pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARESIZE))
    text = font.render("Game Ended in a Draw!", True, BLUE)
    screen.blit(text, (width//2 - text.get_width()//2, SQUARESIZE//2 - text.get_height()//2))
    again_text = small_font.render("Press R to restart", True, BLACK)
    screen.blit(again_text, (width//2 - again_text.get_width()//2, SQUARESIZE//2 + again_text.get_height()))
    pygame.display.update()

def is_valid_location(board, col):
    return board[0][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT-1, -1, -1):
        if board[r][col] == 0:
            return r
    return -1

def drop_piece_animation(board, row, col, piece):
    # Simple drop animation
    for r in range(0, row+1):
        temp_board = board.copy()
        if r > 0:
            temp_board[r-1][col] = 0
        temp_board[r][col] = piece
        draw_board(temp_board)
        pygame.time.delay(50)
    
    # Ensure final position is correct
    board[row][col] = piece
    draw_board(board)

def check_win(board, row, col, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT-3):
        if board[row][c] == piece and board[row][c+1] == piece and board[row][c+2] == piece and board[row][c+3] == piece:
            return True

    # Check vertical locations
    for r in range(ROW_COUNT-3):
        if board[r][col] == piece and board[r+1][col] == piece and board[r+2][col] == piece and board[r+3][col] == piece:
            return True

    # Check positively sloped diagonals
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for r in range(3, ROW_COUNT):
        for c in range(COLUMN_COUNT-3):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
    return False
def is_board_full(board):
    return np.all(board != 0)

def reset_game():
    global board, move_history, valid_moves
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    move_history = []
    valid_moves = deque(range(COLUMN_COUNT))
    draw_board(board)
    draw_turn_indicator(0)
    return 0  # Return to player 1's turn

def main():
    game_over = False
    turn = 0  # Player 1 starts
    draw_board(board)
    draw_turn_indicator(turn)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    turn = reset_game()
                    game_over = False
                elif event.key == pygame.K_u and not game_over and move_history:  # Undo move
                    col = move_history.pop()
                    for r in range(ROW_COUNT):
                        if board[r][col] != 0:
                            board[r][col] = 0
                            break
                    turn = 1 - turn
                    draw_board(board)
                    draw_turn_indicator(turn)
                    if col not in valid_moves:
                        valid_moves.appendleft(col)
                    game_over = False
            
            if not game_over and event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, GRAY, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()
                
            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARESIZE)
                
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece_animation(board, row, col, turn + 1)
                    move_history.append(col)
                    
                    if check_win(board, row, col, turn + 1):
                        game_over = True
                        draw_win_message(turn + 1)
                    elif is_board_full(board):
                        game_over = True
                        draw_draw_message()
                    else:
                        turn = 1 - turn
                        draw_turn_indicator(turn)
                        
                    # Update valid moves
                    if not is_valid_location(board, col) and col in valid_moves:
                        valid_moves.remove(col)
                
        pygame.display.update()

if __name__ == "__main__":
    main()