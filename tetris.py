import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Tetromino shapes and colors
# Source: https://github.com/mithyB/mithyb.github.io/tree/40b2b7bb01c009781d9f2933f42f6286c199c54b/resources/projects/tetris/js/script.js
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]  # L
]

SHAPE_COLORS = [CYAN, YELLOW, MAGENTA, GREEN, RED, BLUE, ORANGE]

# Create the game board
board = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_board():
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, board[y][x], (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def draw_tetromino(shape, color, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, ((off_x + x) * GRID_SIZE, (off_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, WHITE, ((off_x + x) * GRID_SIZE, (off_y + y) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

def rotate(shape):
    return [ [ shape[y][x] for y in range(len(shape)) ] for x in range(len(shape[0]) - 1, -1, -1) ]

def valid_move(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT:
                    return False
                if board[y + off_y][x + off_x] != BLACK:
                    return False
    return True

def handle_input():
    global current_tetromino, current_color, current_offset
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_offset = (current_offset[0] - 1, current_offset[1])
                if valid_move(current_tetromino, new_offset):
                    current_offset = new_offset
            elif event.key == pygame.K_RIGHT:
                new_offset = (current_offset[0] + 1, current_offset[1])
                if valid_move(current_tetromino, new_offset):
                    current_offset = new_offset
            elif event.key == pygame.K_DOWN:
                new_offset = (current_offset[0], current_offset[1] + 1)
                if valid_move(current_tetromino, new_offset):
                    current_offset = new_offset
            elif event.key == pygame.K_UP:
                new_tetromino = rotate(current_tetromino)
                if valid_move(new_tetromino, current_offset):
                    current_tetromino = new_tetromino
    return True

def clear_lines():
    global board
    new_board = [row for row in board if any(cell == BLACK for cell in row)]
    lines_cleared = GRID_HEIGHT - len(new_board)
    new_board = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(lines_cleared)] + new_board
    board = new_board

def place_tetromino(shape, color, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = color

def new_tetromino():
    global current_tetromino, current_color, current_offset
    current_tetromino = random.choice(SHAPES)
    current_color = random.choice(SHAPE_COLORS)
    current_offset = (GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0)
    if not valid_move(current_tetromino, current_offset):
        return False
    return True

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Main game loop
current_tetromino = random.choice(SHAPES)
current_color = random.choice(SHAPE_COLORS)
current_offset = (GRID_WIDTH // 2 - len(current_tetromino[0]) // 2, 0)

running = True
while running:
    screen.fill(BLACK)
    draw_board()
    draw_tetromino(current_tetromino, current_color, current_offset)
    pygame.display.flip()
    running = handle_input()
    if not valid_move(current_tetromino, (current_offset[0], current_offset[1] + 1)):
        place_tetromino(current_tetromino, current_color, current_offset)
        clear_lines()
        if not new_tetromino():
            running = False
    else:
        current_offset = (current_offset[0], current_offset[1] + 1)
    pygame.time.delay(500)

pygame.quit()