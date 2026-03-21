"""Player entity with WASD movement, mouse aiming, and shooting."""

import pygame
import math
from src.entities.projectile import PlasmaBullet
from src.settings import (
    PLAYER_SPEED, PLAYER_RADIUS, PLAYER_COLOR,
    PLAYER_CORE_COLOR, PLAYER_GLOW_ALPHA, PLAYER_SHOOT_DELAY, COLOR_WHITE,
)


class Player:
    """Player-controlled entity that moves around the brain and shoots enemies.

    Uses WASD for movement with diagonal normalization, rotates toward
    the mouse cursor, and fires projectiles with a cooldown system.
    Encapsulates shooting logic internally via try_shoot().
    """

    def __init__(self, x: float, y: float) -> None:
        """Create a player at the given position.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
        """
        self.x = x
        self.y = y
        self.speed = PLAYER_SPEED
        self.radius = PLAYER_RADIUS
        self.color = PLAYER_COLOR                        
        self._angle = 0.0                                
        self._shoot_cooldown = 0                         
        self._shoot_delay = PLAYER_SHOOT_DELAY           

    def update(self, keys: pygame.key.ScancodeWrapper, mouse_x: int, mouse_y: int,
               screen_width: int, screen_height: int,
               core_x: float, core_y: float, core_radius: float) -> None:
        """Update player position, aim angle, and shoot cooldown.

        Handles WASD movement with diagonal normalization, clamps position
        to screen bounds, pushes player out of the brain core if overlapping,
        and updates the aim angle toward the mouse cursor.

        Args:
            keys: Current keyboard state from pygame.key.get_pressed().
            mouse_x: Current mouse x position in pixels.
            mouse_y: Current mouse y position in pixels.
            screen_width: Width of the game window in pixels.
            screen_height: Height of the game window in pixels.
            core_x: X position of the brain center.
            core_y: Y position of the brain center.
            core_radius: Radius of the brain hitbox.
        """
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

        if dx != 0 and dy != 0:
            length = math.sqrt(dx**2 + dy**2)
            dx /= length
            dy /= length

        self.x += dx * self.speed
        self.y += dy * self.speed

        self.x = max(self.radius, min(screen_width - self.radius, self.x))
        self.y = max(self.radius, min(screen_height - self.radius, self.y))

        dist_to_core = math.sqrt((self.x - core_x)**2 + (self.y - core_y)**2)
        min_dist = self.radius + core_radius
        if dist_to_core < min_dist and dist_to_core > 0:
            push_dx = (self.x - core_x) / dist_to_core
            push_dy = (self.y - core_y) / dist_to_core
            self.x = core_x + push_dx * min_dist
            self.y = core_y + push_dy * min_dist

        self._angle = math.atan2(mouse_y - self.y, mouse_x - self.x)

    
        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

    def try_shoot(self, mouse_x: int, mouse_y: int) -> PlasmaBullet | None:
        """Attempt to fire a projectile toward the mouse position.

        Only fires if the internal cooldown has elapsed. Resets the
        cooldown timer on a successful shot.

        Args:
            mouse_x: Target x position in pixels (mouse cursor).
            mouse_y: Target y position in pixels (mouse cursor).

        Returns:
            A new PlasmaBullet if the cooldown allows, otherwise None.
        """
        if self._shoot_cooldown <= 0:
            self._shoot_cooldown = self._shoot_delay
            return PlasmaBullet(self.x, self.y, mouse_x, mouse_y)
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the player with a glow effect, inner core, and aim line.

        Args:
            screen: Pygame surface to draw on.
        """
        x, y = int(self.x), int(self.y)

        # Glow effect
        glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*PLAYER_COLOR, PLAYER_GLOW_ALPHA), (self.radius * 2, self.radius * 2), self.radius + 8)
        screen.blit(glow_surface, (x - self.radius * 2, y - self.radius * 2))

        # Main body circle
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        pygame.draw.circle(screen, PLAYER_CORE_COLOR, (x, y), self.radius - 4)     # Inner light core

        # Line towards mouse (aim indicator)
        line_length = self.radius + 10
        end_x = x + int(math.cos(self._angle) * line_length)
        end_y = y + int(math.sin(self._angle) * line_length)
        pygame.draw.line(screen, COLOR_WHITE, (x, y), (end_x, end_y), 3)
