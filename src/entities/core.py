"""Brain core entity that the player must defend."""
import pygame
from src.settings import BRAIN_HEALTH, BRAIN_RADIUS, BRAIN_LINE_COLOR, BRAIN_BASE_RGB, HUD_HEALTH_POS, COLOR_WHITE

class Brain:
    """The central AI brain core that enemies try to destroy.

    Displays a stylized brain shape with dynamic coloring based on
    remaining health. Changes its status name as health decreases.
    """

    def __init__(self, x: int, y: int) -> None:
        """Create a brain core at the given position.

        Args:
            x: Horizontal center position in pixels.
            y: Vertical center position in pixels.
        """
        self.x = x
        self.y = y
        self.health = BRAIN_HEALTH
        self.max_health = BRAIN_HEALTH
        self.radius = BRAIN_RADIUS

    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the brain core with health-based color and status name.

        The brain color shifts from pink toward red as health decreases.
        A status name is displayed above the brain that changes at
        health thresholds (75%, 50%, 25%).

        Args:
            screen: Pygame surface to draw on.
            font: Font used to render the status name.
        """
        line_color = BRAIN_LINE_COLOR

        health_ratio = max(0, self.health / self.max_health)          # naam verandert hoe minder punten er zijn
        if health_ratio > 0.75:
            name = "Stable Model"
        elif health_ratio > 0.5:
            name = "Unreliable Model"
        elif health_ratio > 0.25:
            name = "Corrupted Model"
        else:
            name = "Failing System"

        base_red, base_green, base_blue = BRAIN_BASE_RGB              # roder worden naarmate score minder wordt

        red = min(255, int(base_red + (1 - health_ratio) * 80))
        green = int(base_green * health_ratio)
        blue = int(base_blue * health_ratio)

        color = (red, green, blue)

        # Titel boven het brein
        title_text = font.render(name, True, color)
        text_rect = title_text.get_rect(center=(self.x, self.y - 95))
        screen.blit(title_text, text_rect)

        # Centrale hoofdvorm
        pygame.draw.ellipse(
            screen,
            color,
            (self.x - 60, self.y - 40, 120, 80),
        )

        # Linker bobbels
        pygame.draw.circle(screen, color, (self.x - 40, self.y - 20), 25)
        pygame.draw.circle(screen, color, (self.x - 50, self.y + 10), 22)
        pygame.draw.circle(screen, color, (self.x - 20, self.y + 20), 24)
        pygame.draw.circle(screen, color, (self.x - 20, self.y - 30), 20)

        # Rechter bobbels
        pygame.draw.circle(screen, color, (self.x + 40, self.y - 20), 25)
        pygame.draw.circle(screen, color, (self.x + 50, self.y + 10), 22)
        pygame.draw.circle(screen, color, (self.x + 20, self.y + 20), 24)
        pygame.draw.circle(screen, color, (self.x + 20, self.y - 30), 20)

        # Middenlijn
        pygame.draw.line(
            screen,
            line_color,
            (self.x, self.y - 35),
            (self.x, self.y + 35),
            3,
        )

        # Extra details
        pygame.draw.arc(screen, line_color, (self.x - 48, self.y - 20, 30, 25), 0.4, 2.6, 2)
        pygame.draw.arc(screen, line_color, (self.x - 35, self.y + 0, 28, 22), 0.3, 2.7, 2)
        pygame.draw.arc(screen, line_color, (self.x + 18, self.y - 20, 30, 25), 0.5, 2.7, 2)
        pygame.draw.arc(screen, line_color, (self.x + 5, self.y + 0, 28, 22), 0.4, 2.8, 2)

    def draw_health(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the brain's current health value on the HUD.

        Args:
            screen: Pygame surface to draw on.
            font: Font used to render the health text.
        """
        health_text = font.render(f"Health: {self.health}", True, COLOR_WHITE)
        screen.blit(health_text, HUD_HEALTH_POS)
