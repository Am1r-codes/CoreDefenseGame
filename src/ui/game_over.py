"""Game over scherm."""

import pygame
from src.ui.menu import GameScreen


class GameOverScreen(GameScreen):
    """Scherm dat verschijnt wanneer het brein is vernietigd."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self._title_font = pygame.font.SysFont(None, 72)
        self._final_score = 0
        self._final_wave = 0

    def set_results(self, score: int, wave: int) -> None:
        """Sla eindresultaten op voor weergave."""
        self._final_score = score
        self._final_wave = wave

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.start_playing()
                elif event.key == pygame.K_ESCAPE:
                    self.game.running = False

    def update(self) -> None:
        pass

    def draw(self) -> None:
        screen = self.game.screen
        width = self.game.width
        height = self.game.height

        screen.fill((20, 20, 30))

        # SYSTEM FAILURE titel
        title = self._title_font.render("SYSTEM FAILURE", True, (255, 60, 60))
        title_rect = title.get_rect(center=(width // 2, height // 3))
        screen.blit(title, title_rect)

        # eindscore
        score_text = self.game.font.render(f"Final Score: {self._final_score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(width // 2, height // 2))
        screen.blit(score_text, score_rect)

        # wave bereikt
        wave_text = self.game.font.render(f"Wave Reached: {self._final_wave}", True, (255, 255, 255))
        wave_rect = wave_text.get_rect(center=(width // 2, height // 2 + 45))
        screen.blit(wave_text, wave_rect)

        # instructies
        restart_text = self.game.font.render("Press R to restart", True, (0, 220, 255))
        restart_rect = restart_text.get_rect(center=(width // 2, height // 2 + 120))
        screen.blit(restart_text, restart_rect)

        quit_text = self.game.font.render("Press ESC to quit", True, (180, 180, 200))
        quit_rect = quit_text.get_rect(center=(width // 2, height // 2 + 160))
        screen.blit(quit_text, quit_rect)
