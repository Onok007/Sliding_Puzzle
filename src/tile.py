# Sliding Puzzle
# Ondrej Kucera, I. rocnik, kruh 38
# zimni semestr 2024/25
# Programovani NPRG030


import pygame
from settings import TILE_SIZE, EMPTY_TILE_COLOR


class Tile:
    """Represents an individual tile in the grid."""
    def __init__(self, image, pos, grid_pos, is_empty=False):
        self.image = image
        self.pos = pos          # Screen position (x, y)
        self.grid_pos = grid_pos  # Grid position (row, col)
        self.is_empty = is_empty

    def draw(self, screen):
        if self.is_empty:
            pygame.draw.rect(screen, EMPTY_TILE_COLOR, (*self.pos, TILE_SIZE, TILE_SIZE))
        else:
            screen.blit(self.image, self.pos)
