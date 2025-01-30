# Sliding Puzzle
# Ondrej Kucera, I. rocnik, kruh 38
# zimni semestr 2024/25
# Programovani NPRG030


import pygame
import os
import random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, GRID_ROWS, GRID_COLS, TILE_SIZE


def load_random_image():
    """Load a random image from the specified folder and resize it."""
    file_path = os.path.join(os.path.dirname(__file__), '../assets/')
    images = [os.path.join(file_path, f) for f in os.listdir(file_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        raise FileNotFoundError("No images found in the specified folder.")

    image = pygame.image.load(random.choice(images)).convert()

    # Resize the image to exactly match the grid dimensions
    return pygame.transform.smoothscale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def slice_image(image):
    """Slice the resized image into tiles."""
    tiles = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            x, y = col * TILE_SIZE, row * TILE_SIZE
            tile = image.subsurface((x, y, TILE_SIZE, TILE_SIZE))
            tiles.append(tile)
    return tiles


def shuffle_puzzle():
    """Shuffle the puzzle tiles, leaving the last one empty."""
    grid = [[(row * GRID_COLS + col) for col in range(GRID_COLS)] for row in range(GRID_ROWS)]
    empty_tile = (GRID_ROWS - 1, GRID_COLS - 1)
    grid[empty_tile[0]][empty_tile[1]] = None

    # Simulate sliding movements to shuffle (NEVER SWAP!)
    moves = GRID_ROWS * GRID_COLS * 10
    for _ in range(moves):
        neighbors = get_neighbors(empty_tile)
        target = random.choice(neighbors)
        grid[empty_tile[0]][empty_tile[1]] = grid[target[0]][target[1]]
        grid[target[0]][target[1]] = None
        empty_tile = target

    return grid


def get_neighbors(pos):
    """Get all valid neighbors for the given position."""
    row, col = pos
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = row + dr, col + dc
        if 0 <= nr < GRID_ROWS and 0 <= nc < GRID_COLS:
            neighbors.append((nr, nc))
    return neighbors
