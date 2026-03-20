"""Base enemy placeholder for shared behavior."""

import pygame
import math
import random


class EnemyBase:
    """Corrupted data --> standaard snelheid, weinig damage, veel tegelijk"""

    def __init__(self, x: float, y: float, speed: float = 1.5) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 10
        self.color = (80, 150, 255)         # blauw
        self.damage = 1

    def update(self, target_x: float, target_y: float) -> None:         # beweegt naar brein
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen: pygame.Surface) -> None:                     # draw enemy
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collides_with_brain(self, core_x: float, core_y: float, core_radius: float) -> bool:    # checkt of enemy het brein raakt
        dx = core_x - self.x
        dy = core_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        return distance < (self.radius + core_radius)
    
class NoiseEnemy(EnemyBase):
    "Noise enemy -> snel, weinig damage, moeilijk te raken"

    def __init__(self, x, y):
        super().__init__(x, y, speed=4)
        self.color = (255, 150, 50)             # oranje
        self.damage = 1
    
    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)

        for r, alpha in [(self.radius + 10, 40), (self.radius + 6, 70)]:            # blow effect
            glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 150, 50, alpha), (r, r), r)
            screen.blit(glow_surface, (x - r, y - r))

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

class BiasEnemy(EnemyBase):
    "Traag, veel damage, veel HP"

    def __init__(self, x, y):
        super().__init__(x, y, speed=1)
        self.radius = 20
        self.color = (80, 200, 120)              # groen
        self.damage = 3

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, (40, 0, 0), (x, y), self.radius + 3)     # buitenrand (donker)
        pygame.draw.circle(screen, self.color, (x, y), self.radius)         # binnenkant

class HallucinationEnemy(EnemyBase):
    "beweegt random, slingert"

    def __init__(self, x, y):
        super().__init__(x, y, speed=2.2)
        self.color = (255, 220, 50)                    # geel
        self.damage = 2
        self.radius = 14

    def update(self, target_x: float, target_y: float) -> None:     # moet random naar brain gaan
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        dx += random.uniform(-0.5, 0.5)                 # dx, dy = richting naar brain, met chaos
        dy += random.uniform(-0.5, 0.5)

        self.x += dx * self.speed                       # beweging
        self.y += dy * self.speed

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, self.color, (x, y), self.radius)

class OverfittingEnemy(EnemyBase):
    """langzaam, groot en gevaarlijk """

    def __init__(self, x, y):
        super().__init__(x, y, speed=0.9)
        self.color = (255, 60, 60)   # rood
        self.damage = 5
        self.radius = 26

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, (50, 0, 70), (x, y), self.radius + 4)        # donkere buitenkant
        pygame.draw.circle(screen, self.color, (x, y), self.radius)             # binnenkant
