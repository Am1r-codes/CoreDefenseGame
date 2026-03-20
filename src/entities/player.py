"""Player entity placeholder."""

import pygame
import math
from src.entities.projectile import PlasmaBullet
from src.settings import (
    PLAYER_SPEED, PLAYER_RADIUS, PLAYER_COLOR,
    PLAYER_CORE_COLOR, PLAYER_GLOW_ALPHA, PLAYER_SHOOT_DELAY, COLOR_WHITE,
)


class Player:
    """Speler die rond het brein beweegt en op enemies schiet."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.speed = PLAYER_SPEED
        self.radius = PLAYER_RADIUS
        self.color = PLAYER_COLOR                        # cyaan
        self._angle = 0.0                                # interne hoek richting muis
        self._shoot_cooldown = 0                         # interne timer tussen schoten
        self._shoot_delay = PLAYER_SHOOT_DELAY           # frames tussen elk schot

    def update(self, keys: pygame.key.ScancodeWrapper, mouse_x: int, mouse_y: int,
               screen_width: int, screen_height: int,
               core_x: float, core_y: float, core_radius: float) -> None:
        """Beweeg speler met WASD, draai richting muis, blijf binnen scherm en buiten brein."""
        dx = 0.0
        dy = 0.0

        if keys[pygame.K_w]:
            dy -= 1
        if keys[pygame.K_s]:
            dy += 1
        if keys[pygame.K_a]:
            dx -= 1
        if keys[pygame.K_d]:
            dx += 1

        # diagonale normalisatie
        if dx != 0 and dy != 0:
            length = math.sqrt(dx**2 + dy**2)
            dx /= length
            dy /= length

        self.x += dx * self.speed
        self.y += dy * self.speed

        # binnen scherm houden
        self.x = max(self.radius, min(screen_width - self.radius, self.x))
        self.y = max(self.radius, min(screen_height - self.radius, self.y))

        # niet overlappen met brein
        dist_to_core = math.sqrt((self.x - core_x)**2 + (self.y - core_y)**2)
        min_dist = self.radius + core_radius
        if dist_to_core < min_dist and dist_to_core > 0:
            push_dx = (self.x - core_x) / dist_to_core
            push_dy = (self.y - core_y) / dist_to_core
            self.x = core_x + push_dx * min_dist
            self.y = core_y + push_dy * min_dist

        # hoek naar muis berekenen
        self._angle = math.atan2(mouse_y - self.y, mouse_x - self.x)

        # cooldown aftellen
        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

    def try_shoot(self, mouse_x: int, mouse_y: int) -> PlasmaBullet | None:
        """Probeer te schieten, geeft kogel terug of None als cooldown actief is."""
        if self._shoot_cooldown <= 0:
            self._shoot_cooldown = self._shoot_delay
            return PlasmaBullet(self.x, self.y, mouse_x, mouse_y)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Teken speler als cyaan cirkel met richtingindicator."""
        x, y = int(self.x), int(self.y)

        # glow effect
        glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*PLAYER_COLOR, PLAYER_GLOW_ALPHA), (self.radius * 2, self.radius * 2), self.radius + 8)
        screen.blit(glow_surface, (x - self.radius * 2, y - self.radius * 2))

        # hoofdcirkel
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        pygame.draw.circle(screen, PLAYER_CORE_COLOR, (x, y), self.radius - 4)     # lichtere kern

        # richtinglijn naar muis
        line_length = self.radius + 10
        end_x = x + int(math.cos(self._angle) * line_length)
        end_y = y + int(math.sin(self._angle) * line_length)
        pygame.draw.line(screen, COLOR_WHITE, (x, y), (end_x, end_y), 3)
