"""Heads-up display for in-game information."""
import pygame
from src.settings import (
    ENEMY_BASE_COLOR, NOISE_COLOR, BIAS_COLOR, HALLUCINATION_COLOR, OVERFITTING_COLOR,
    COLOR_WHITE, COLOR_COMBO,
    HUD_MARGIN, HUD_LEGEND_WIDTH, HUD_LEGEND_HEIGHT, HUD_LEGEND_COLOR, HUD_ROW_GAP,
    HUD_WAVE_POS, HUD_SCORE_POS, HUD_COMBO_POS,
)

class HUD:
    """Renders HUD elements like the enemy legend, wave counter, and score.

    All draw methods are called independently from the game loop,
    allowing selective rendering depending on the active game state.
    """

    def __init__(self, width: int, font: pygame.font.Font) -> None:
        """Create a HUD instance for the given screen width.

        Args:
            width: Width of the game window in pixels.
            font: Default font used for all HUD text rendering.
        """
        self.width = width
        self.font = font

    def draw_enemy_legend(self, screen: pygame.Surface) -> None:
        """Draw the enemy type legend box in the top-right corner.

        Shows all five enemy types with their color indicators and names.

        Args:
            screen: Pygame surface to draw on.
        """
        x = self.width - HUD_LEGEND_WIDTH - HUD_MARGIN
        y = HUD_MARGIN

        # achtergrond
        pygame.draw.rect(screen, HUD_LEGEND_COLOR, (x, y, HUD_LEGEND_WIDTH, HUD_LEGEND_HEIGHT), border_radius=10)

        # titel
        title = self.font.render("Enemy Types", True, COLOR_WHITE)
        screen.blit(title, (x + 15, y + 10))

        start_y = y + 60          # iest meer ruimte tussen titel en enemys

        # base
        pygame.draw.circle(screen, ENEMY_BASE_COLOR, (x + 20, start_y), 8)
        screen.blit(self.font.render("Corrupted Data", True, ENEMY_BASE_COLOR), (x + 40, start_y - 10))

        # noise
        pygame.draw.circle(screen, NOISE_COLOR, (x + 20, start_y + HUD_ROW_GAP), 8)
        screen.blit(self.font.render("Noise", True, NOISE_COLOR), (x + 40, start_y + HUD_ROW_GAP - 10))

        # bias
        pygame.draw.circle(screen, BIAS_COLOR, (x + 20, start_y + 2 * HUD_ROW_GAP), 8)
        screen.blit(self.font.render("Bias", True, BIAS_COLOR), (x + 40, start_y + 2 * HUD_ROW_GAP - 10))

        # hallucination
        pygame.draw.circle(screen, HALLUCINATION_COLOR, (x + 20, start_y + 3 * HUD_ROW_GAP), 8)
        screen.blit(self.font.render("Hallucination", True, HALLUCINATION_COLOR), (x + 40, start_y + 3 * HUD_ROW_GAP - 10))

        # overfitting
        pygame.draw.circle(screen, OVERFITTING_COLOR, (x + 20, start_y + 4 * HUD_ROW_GAP), 8)
        screen.blit(self.font.render("Overfitting", True, OVERFITTING_COLOR), (x + 40, start_y + 4 * HUD_ROW_GAP - 10))

    def draw_wave_counter(self, screen: pygame.Surface, wave_number: int) -> None:
        """Draw the current wave number on the HUD.

        Args:
            screen: Pygame surface to draw on.
            wave_number: Current wave number to display.
        """
        wave_text = self.font.render(f"Wave: {wave_number}", True, COLOR_WHITE)
        screen.blit(wave_text, HUD_WAVE_POS)

    def draw_score(self, screen: pygame.Surface, score: int, combo: int) -> None:
        """Draw the score and combo multiplier on the HUD.

        The combo multiplier is only shown when it exceeds 1x.

        Args:
            screen: Pygame surface to draw on.
            score: Current player score to display.
            combo: Current combo multiplier value.
        """
        score_text = self.font.render(f"Score: {score}", True, COLOR_WHITE)
        screen.blit(score_text, HUD_SCORE_POS)

        if combo > 1:
            combo_text = self.font.render(f"Combo: x{combo}", True, COLOR_COMBO)
            screen.blit(combo_text, HUD_COMBO_POS)
