"""Base enemy placeholder for shared behavior."""

import pygame
import math
import random
from src.settings import (
    ENEMY_BASE_SPEED, ENEMY_BASE_RADIUS, ENEMY_BASE_COLOR, ENEMY_BASE_DAMAGE, ENEMY_BASE_SCORE,
    NOISE_SPEED, NOISE_COLOR, NOISE_DAMAGE, NOISE_SCORE,
    BIAS_SPEED, BIAS_RADIUS, BIAS_COLOR, BIAS_DAMAGE, BIAS_SCORE, BIAS_BORDER_COLOR,
    HALLUCINATION_SPEED, HALLUCINATION_RADIUS, HALLUCINATION_COLOR,
    HALLUCINATION_DAMAGE, HALLUCINATION_SCORE, HALLUCINATION_SWAY,
    OVERFITTING_SPEED, OVERFITTING_RADIUS, OVERFITTING_COLOR,
    OVERFITTING_DAMAGE, OVERFITTING_SCORE, OVERFITTING_BORDER_COLOR,
)


class EnemyBase:
    """Corrupted data --> standaard snelheid, weinig damage, veel tegelijk"""

    def __init__(self, x: float, y: float, speed: float = ENEMY_BASE_SPEED) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = ENEMY_BASE_RADIUS
        self.color = ENEMY_BASE_COLOR                    # blauw
        self.damage = ENEMY_BASE_DAMAGE
        self.score_value = ENEMY_BASE_SCORE              # punten bij kill

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
        super().__init__(x, y, speed=NOISE_SPEED)
        self.color = NOISE_COLOR                          # oranje
        self.damage = NOISE_DAMAGE
        self.score_value = NOISE_SCORE                    # snel, moeilijk te raken

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)

        for r, alpha in [(self.radius + 10, 40), (self.radius + 6, 70)]:            # glow effect
            glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*NOISE_COLOR, alpha), (r, r), r)
            screen.blit(glow_surface, (x - r, y - r))

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

class BiasEnemy(EnemyBase):
    "Traag, veel damage, veel HP"

    def __init__(self, x, y):
        super().__init__(x, y, speed=BIAS_SPEED)
        self.radius = BIAS_RADIUS
        self.color = BIAS_COLOR                           # groen
        self.damage = BIAS_DAMAGE
        self.score_value = BIAS_SCORE                     # tanky

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, BIAS_BORDER_COLOR, (x, y), self.radius + 3)     # buitenrand (donker)
        pygame.draw.circle(screen, self.color, (x, y), self.radius)                # binnenkant

class HallucinationEnemy(EnemyBase):
    "beweegt random, slingert"

    def __init__(self, x, y):
        super().__init__(x, y, speed=HALLUCINATION_SPEED)
        self.color = HALLUCINATION_COLOR                  # geel
        self.damage = HALLUCINATION_DAMAGE
        self.radius = HALLUCINATION_RADIUS
        self.score_value = HALLUCINATION_SCORE            # slingert, onvoorspelbaar

    def update(self, target_x: float, target_y: float) -> None:     # moet random naar brain gaan
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        dx += random.uniform(-HALLUCINATION_SWAY, HALLUCINATION_SWAY)   # richting naar brain, met chaos
        dy += random.uniform(-HALLUCINATION_SWAY, HALLUCINATION_SWAY)

        self.x += dx * self.speed                       # beweging
        self.y += dy * self.speed

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, self.color, (x, y), self.radius)

class OverfittingEnemy(EnemyBase):
    """langzaam, groot en gevaarlijk """

    def __init__(self, x, y):
        super().__init__(x, y, speed=OVERFITTING_SPEED)
        self.color = OVERFITTING_COLOR                    # rood
        self.damage = OVERFITTING_DAMAGE
        self.radius = OVERFITTING_RADIUS
        self.score_value = OVERFITTING_SCORE              # groot en gevaarlijk

    def draw(self, screen: pygame.Surface) -> None:
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, OVERFITTING_BORDER_COLOR, (x, y), self.radius + 4)   # donkere buitenkant
        pygame.draw.circle(screen, self.color, (x, y), self.radius)                     # binnenkant
