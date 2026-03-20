"""Energy core entity placeholder."""
import pygame
import copy

class Brain: 
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.health = 20
        self.max_health = copy.deepcopy(self.health)
        self.radius = 60
    
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the brain core on the screen."""
        brain_color = (255, 100, 180)
        line_color = (230, 210, 255)

        health_ratio = self.health / self.max_health                # naam verandert hoe minder punten er zijn 
        if health_ratio > 0.75:
            name = "Stable Model"
        elif health_ratio > 0.5:
            name = "Unreliable Model"
        elif health_ratio > 0.25:
            name = "Corrupted Model"
        else:
            name = "Failing System"

        base_red = 200                                          # roder worden naarmate score minder wordt
        base_green = 120
        base_blue = 150

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
        health_text = font.render(f"Health: {self.health}", True, (255, 255, 255))
        screen.blit(health_text, (20, 30))