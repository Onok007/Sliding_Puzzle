# Sliding Puzzle
# Ondrej Kucera, I. rocnik, kruh 38
# zimni semestr 2024/25
# Programovani NPRG030


import pygame
from tile import Tile
from utils import load_random_image, slice_image, shuffle_puzzle
from settings import *


class Game:
    """Holds the status of the game."""
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Sliding Puzzle")
        self.clock = pygame.time.Clock()

        # Predefined variables, values assigned in reset
        self.image = None   # Image used for the current game
        self.tiles = None   # Tile images
        self.grid = None    # 2D list of numbers
        self.tiles_objs = None  # List of individual tiles
        self.solved = False

        self.reset_game()

    def reset_game(self):
        """Reset the game state to start a new round."""
        self.image = load_random_image()
        self.tiles = slice_image(self.image)
        self.grid = shuffle_puzzle()

        self.tiles_objs = self.create_tiles()
        self.solved = False

    def create_tiles(self):
        """Create Tile objects from the shuffled grid."""
        tiles_objs = []
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                pos = (col * TILE_SIZE, row * TILE_SIZE)
                grid_pos = (row, col)
                index = self.grid[row][col]
                is_empty = index is None
                image = None if is_empty else self.tiles[index]
                tiles_objs.append(Tile(image, pos, grid_pos, is_empty))
        return tiles_objs

    def handle_click(self, pos):
        """Handle user click on a tile."""
        row, col = pos[1] // TILE_SIZE, pos[0] // TILE_SIZE
        empty_tile = next(tile for tile in self.tiles_objs if tile.is_empty)
        empty_row, empty_col = empty_tile.grid_pos

        if abs(row - empty_row) + abs(col - empty_col) == 1:
            # Swap tiles
            clicked_tile = next(tile for tile in self.tiles_objs if tile.grid_pos == (row, col))
            clicked_tile.grid_pos, empty_tile.grid_pos = empty_tile.grid_pos, clicked_tile.grid_pos
            clicked_tile.pos, empty_tile.pos = empty_tile.pos, clicked_tile.pos

            # Check for victory after each move
            if self.check_victory():
                self.solved = True  # Stop further interactions

    def check_victory(self):
        """Check if the tiles are in the correct order."""
        for tile in self.tiles_objs:
            row, col = tile.grid_pos
            expected_index = row * GRID_COLS + col
            if not tile.is_empty and self.tiles.index(tile.image) != expected_index:
                return False
        return True

    def show_victory_popup(self):
        """Display a semi-transparent pop-up when the puzzle is solved."""
        font = pygame.font.Font(None, 60)
        text_surface = font.render("Congratulations!", True, (255, 255, 255))

        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # Black with transparency
        self.screen.blit(overlay, (0, 0))

        # Draw text in the center
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        """Draw the puzzle or victory screen."""
        self.screen.fill(BACKGROUND_COLOR)

        if self.solved:
            # Draw the full image instead of the tiles
            self.screen.blit(self.image, (0, 0))

            # Display victory popup
            self.show_victory_popup()
        else:
            # Draw tiles
            for tile in self.tiles_objs:
                tile.draw(self.screen)

    def run(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
