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
        self.button_rect = None     # Restart button rectangle

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
        if any(tile.is_moving() for tile in self.tiles_objs):
            return

        row, col = pos[1] // TILE_SIZE, pos[0] // TILE_SIZE
        empty_tile = next(tile for tile in self.tiles_objs if tile.is_empty)
        empty_row, empty_col = empty_tile.grid_pos

        if abs(row - empty_row) + abs(col - empty_col) == 1:
            # Swap tiles
            clicked_tile = next(tile for tile in self.tiles_objs if tile.grid_pos == (row, col))
            clicked_tile.grid_pos, empty_tile.grid_pos = empty_tile.grid_pos, clicked_tile.grid_pos

            # Set target positions for animation
            clicked_tile.target_x, clicked_tile.target_y = empty_tile.x, empty_tile.y
            empty_tile.target_x, empty_tile.target_y = clicked_tile.x, clicked_tile.y

            # Check for victory after each move
            if self.check_victory():
                self.solved = True  # Stop further interactions
                self.fade_in_full_image()

    def check_victory(self):
        """Check if the tiles are in the correct order."""
        for tile in self.tiles_objs:
            row, col = tile.grid_pos
            expected_index = row * GRID_COLS + col
            if not tile.is_empty and self.tiles.index(tile.image) != expected_index:
                return False
        return True

    def fade_in_full_image(self, duration=2000):
        """Fades in the full image over the given duration (in milliseconds)."""
        fade_surface = self.image.copy()
        alpha = 0
        start_time = pygame.time.get_ticks()

        while alpha < 255:
            elapsed = pygame.time.get_ticks() - start_time
            alpha = min(255, int((elapsed / duration) * 255))
            fade_surface.set_alpha(alpha)

            self.screen.fill((0, 0, 0))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

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

        # Draw restart button
        self.draw_restart_button()

    def draw_restart_button(self):
        """Draw a restart button on the screen."""
        button_color = (100, 200, 100)
        text_color = (255, 255, 255)
        font = pygame.font.Font(None, 40)

        self.button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(self.screen, button_color, self.button_rect, border_radius=10)

        text = font.render("Restart", True, text_color)
        text_rect = text.get_rect(center=self.button_rect.center)
        self.screen.blit(text, text_rect)

    def handle_restart_click(self, event):
        """Check if the restart button is clicked and reset the game."""
        if self.button_rect.collidepoint(event.pos):
            self.reset_game()

    def draw(self):
        """Draw the puzzle or victory screen."""
        self.screen.fill(BACKGROUND_COLOR)

        if self.solved:
            self.screen.blit(self.image, (0, 0))
            self.show_victory_popup()
        else:
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
                    if self.solved:
                        self.handle_restart_click(event)
                    else:
                        self.handle_click(event.pos)

            for tile in self.tiles_objs:
                tile.update()

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()
