"""Game over screen shown when the brain core is destroyed."""

import pygame
from src.ui.menu import GameScreen
from src.settings import BG_COLOR, COLOR_CYAN, COLOR_SUBTITLE, COLOR_WHITE, COLOR_GAME_OVER, FONT_SIZE_GAME_OVER


class GameOverScreen(GameScreen):
    """Screen displayed when the brain's health reaches zero.

    Shows the final score, wave reached, and options to restart
    or quit. Pressing R resets and restarts, Esc exits the game.
    """

    def __init__(self, game) -> None:
        """Create the game over screen with a large title font.

        Args:
            game: Reference to the parent Game object.
        """
        super().__init__(game)
        self._title_font = pygame.font.SysFont(None, FONT_SIZE_GAME_OVER)
        self._final_score = 0
        self._final_wave = 0

    def set_results(self, score: int, wave: int) -> None:
        """Store the final results to display on the game over screen.

        Args:
            score: The player's final score.
            wave: The wave number reached before game over.
        """
        self._final_score = score
        self._final_wave = wave

    def handle_events(self) -> None:
        """Process game over input events.

        Handles window close, R key to restart, and Esc to quit.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.start_playing()
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self) -> None:
        """No update logic needed for the static game over screen."""
        pass

    def draw(self) -> None:
        """Render the game over screen with results and instructions."""
        screen = self.game.screen
        width = self.game.width
        height = self.game.height

        screen.fill(BG_COLOR)

        # SYSTEM FAILURE titel
        title = self._title_font.render("SYSTEM FAILURE", True, COLOR_GAME_OVER)
        title_rect = title.get_rect(center=(width // 2, height // 3))
        screen.blit(title, title_rect)

        # eindscore
        score_text = self.game.font.render(f"Final Score: {self._final_score}", True, COLOR_WHITE)
        score_rect = score_text.get_rect(center=(width // 2, height // 2))
        screen.blit(score_text, score_rect)

        # wave bereikt
        wave_text = self.game.font.render(f"Wave Reached: {self._final_wave}", True, COLOR_WHITE)
        wave_rect = wave_text.get_rect(center=(width // 2, height // 2 + 45))
        screen.blit(wave_text, wave_rect)

        # instructies
        restart_text = self.game.font.render("Press R to restart", True, COLOR_CYAN)
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 120))
        screen.blit(restart_text, restart_rect)

        quit_text = self.game.font.render("Press ESC to quit", True, COLOR_SUBTITLE)
        quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 160))
        screen.blit(quit_text, quit_rect)
