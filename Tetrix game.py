import pygame
import random

# Initialize pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Define the block shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Define the block colors
COLORS = [CYAN, YELLOW, PURPLE, GREEN, RED, ORANGE, BLUE]

# Define the block size and grid
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Define the initial position and shape of the falling block
start_x = GRID_WIDTH // 2
start_y = 0
current_shape = random.choice(SHAPES)
current_color = random.choice(COLORS)

# Define the game clock
clock = pygame.time.Clock()

# Initialize game variables
score = 0
game_over = False

def draw_grid():
    for x in range(GRID_WIDTH):
        pygame.draw.line(win, WHITE, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
    for y in range(GRID_HEIGHT):
        pygame.draw.line(win, WHITE, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))

def draw_block(x, y, color):
    pygame.draw.rect(win, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def check_collision(x, y, shape):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col] and (y + row >= GRID_HEIGHT or x + col < 0 or x + col >= GRID_WIDTH or grid[y + row][x + col] != BLACK):
                return True
    return False

def merge_block(x, y, shape, color):
    for row in range(len(shape)):
        for col in range(len(shape[row])):
            if shape[row][col]:
                grid[y + row][x + col] = color

def clear_rows():
    global score
    full_rows = []
    for row in range(GRID_HEIGHT):
        if all(grid[row]):
            full_rows.append(row)
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK] * GRID_WIDTH)
        score += 10 * GRID_WIDTH

def draw_score():
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    win.blit(text, (20, 20))

def draw_game_over():
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(text, text_rect)

# Game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(start_x - 1, start_y, current_shape):
                    start_x -= 1
            elif event.key == pygame.K_RIGHT:
                if not check_collision(start_x + 1, start_y, current_shape):
                    start_x += 1
            elif event.key == pygame.K_DOWN:
                if not check_collision(start_x, start_y + 1, current_shape):
                    start_y += 1
            elif event.key == pygame.K_SPACE:
                rotated_shape = list(zip(*reversed(current_shape)))
                if not check_collision(start_x, start_y, rotated_shape):
                    current_shape = rotated_shape

    if not check_collision(start_x, start_y + 1, current_shape):
        start_y += 1
    else:
        merge_block(start_x, start_y, current_shape, current_color)
        clear_rows()
        start_x = GRID_WIDTH // 2
        start_y = 0
        current_shape = random.choice(SHAPES)
        current_color = random.choice(COLORS)
        if check_collision(start_x, start_y, current_shape):
            game_over = True

    # Clear the screen
    win.fill(BLACK)

    # Draw the grid
    draw_grid()

    # Draw the falling block
    for row in range(len(current_shape)):
        for col in range(len(current_shape[row])):
            if current_shape[row][col]:
                draw_block(start_x + col, start_y + row, current_color)

    # Draw the placed blocks
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            if grid[row][col] != BLACK:
                draw_block(col, row, grid[row][col])

    # Draw the score
    draw_score()

    # Check for game over
    if game_over:
        draw_game_over()

    # Update the display
    pygame.display.flip()

    # Set the FPS
    clock.tick(10)

# Quit the game
pygame.quit()
