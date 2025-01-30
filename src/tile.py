# Sliding Puzzle
# Ondrej Kucera, I. rocnik, kruh 38
# zimni semestr 2024/25
# Programovani NPRG030


import pygame
from settings import TILE_SIZE


class Tile:
    """Represents an individual tile in the grid."""
    def __init__(self, image, pos, grid_pos, is_empty=False):
        self.image = image
        self.x, self.y = pos  # Current pixel position
        self.target_x, self.target_y = pos  # Where it should move
        self.grid_pos = grid_pos  # Grid position (row, col)
        self.is_empty = is_empty
        self.speed = 10  # Pixels per frame

    def is_moving(self):
        """Check if the tile is still moving."""
        return (self.x, self.y) != (self.target_x, self.target_y)

    def update(self):
        """Move tile towards its target position smoothly."""
        # if self.is_moving():
        if abs(self.x - self.target_x) < self.speed:
            self.x = self.target_x  # Snap to target
        else:
            self.x += self.speed if self.x < self.target_x else -self.speed

        if abs(self.y - self.target_y) < self.speed:
            self.y = self.target_y  # Snap to target
        else:
            self.y += self.speed if self.y < self.target_y else -self.speed

    def draw(self, screen):
        if not self.is_empty:
            screen.blit(self.image, (self.x, self.y))
