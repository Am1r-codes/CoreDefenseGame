"""Base projectile met gedeeld gedrag, subclasses voor wapentypes."""

import pygame
import math


class ProjectileBase:
    """Basiskogel --> rechte lijn, standaard snelheid en schade."""

    def __init__(self, x: float, y: float, target_x: float, target_y: float,
                 speed: float = 8) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 5
        self.color = (200, 200, 200)              # standaard grijs
        self.damage = 1

        # richting berekenen bij spawn
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            self.dx = dx / distance
            self.dy = dy / distance
        else:
            self.dx = 0.0
            self.dy = 0.0

    def update(self) -> None:                                                   # beweeg kogel
        """Beweeg kogel in rechte lijn, subclasses kunnen dit overriden."""
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def is_off_screen(self, screen_width: int, screen_height: int) -> bool:     # check buiten scherm
        """Check of kogel buiten scherm is."""
        return (self.x < -self.radius or self.x > screen_width + self.radius
                or self.y < -self.radius or self.y > screen_height + self.radius)

    def collides_with_enemy(self, enemy_x: float, enemy_y: float, enemy_radius: float) -> bool:
        """Check of kogel een enemy raakt."""
        dx = enemy_x - self.x
        dy = enemy_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < (self.radius + enemy_radius)

    def draw(self, screen: pygame.Surface) -> None:                             # draw kogel
        """Teken kogel, subclasses overriden dit voor eigen visueel."""
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class PlasmaBullet(ProjectileBase):
    """Plasma kogel --> cyaan glow, standaard wapen van de speler."""

    def __init__(self, x: float, y: float, target_x: float, target_y: float) -> None:
        super().__init__(x, y, target_x, target_y, speed=8)
        self.color = (0, 220, 255)                # cyaan, matcht speler
        self.radius = 5
        self.damage = 1

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)

        # glow effect
        glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (0, 220, 255, 60), (self.radius * 2, self.radius * 2), self.radius + 4)
        screen.blit(glow_surface, (x - self.radius * 2, y - self.radius * 2))

        # kern
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        pygame.draw.circle(screen, (200, 245, 255), (x, y), self.radius - 2)     # lichte kern
