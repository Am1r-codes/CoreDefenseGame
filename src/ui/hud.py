"""HUD drawing placeholder."""
import pygame

class HUD:

    def __init__(self, width: int, font: pygame.font.Font) -> None:
        self.width = width
        self.font = font

    def draw_enemy_legend(self, screen: pygame.Surface) -> None:
        margin = 20
        box_width = 260
        box_height = 210

        x = self.width - box_width - margin
        y = 20

        # achtergrond
        pygame.draw.rect(screen, (35, 35, 45), (x, y, box_width, box_height), border_radius=10)

        # titel
        title = self.font.render("Enemy Types", True, (255, 255, 255))
        screen.blit(title, (x + 15, y + 10))

        start_y = y + 60          # iest meer ruimte tussen titel en enemys
        row_gap = 30

        # base
        pygame.draw.circle(screen, (80, 150, 255), (x + 20, start_y), 8)
        screen.blit(self.font.render("Corrupted Data", True, (80, 150, 255)), (x + 40, start_y - 10))

        # noise
        pygame.draw.circle(screen, (255, 150, 50), (x + 20, start_y + row_gap), 8)
        screen.blit(self.font.render("Noise", True, (255, 150, 50)), (x + 40, start_y  + row_gap - 10))

        # bias
        pygame.draw.circle(screen, (80, 200, 120), (x + 20, start_y + 2 * row_gap), 8)
        screen.blit(self.font.render("Bias", True, (80, 200, 120)), (x + 40, start_y + 2 * row_gap - 10))

        # hallucination
        pygame.draw.circle(screen, (255, 220, 50), (x + 20, start_y + 3 * row_gap), 8)
        screen.blit(self.font.render("Hallucination", True, (255, 220, 50)), (x + 40, start_y + 3 * row_gap - 10))

        # overfitting
        pygame.draw.circle(screen, (255, 60, 60), (x + 20, start_y + 4 * row_gap), 8)
        screen.blit(self.font.render("Overfitting", True, (255, 60, 60)), (x + 40, start_y + 4 * row_gap - 10))