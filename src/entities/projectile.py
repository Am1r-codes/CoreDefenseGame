"""Base projectile class and weapon type subclasses.

ProjectileBase provides shared movement, collision, and lifetime logic.
Subclasses override draw() and stats for different weapon types.
"""

import pygame
import math
from src.settings import (
    PROJECTILE_SPEED, PROJECTILE_RADIUS, PROJECTILE_COLOR, PROJECTILE_DAMAGE,
    PLASMA_COLOR, PLASMA_CORE_COLOR, PLASMA_GLOW_ALPHA,
)


class ProjectileBase:
    """Base projectile that travels in a straight line.

    Calculates a normalized direction vector on creation and moves
    at a constant speed each frame. Subclasses override draw() for
    custom visuals and __init__() for different stats.
    """
    # Basiskogel --> rechte lijn, standaard snelheid en schade.

    def __init__(self, x: float, y: float, target_x: float, target_y: float,
                 speed: float = PROJECTILE_SPEED) -> None:
        """Create a projectile at the given position aimed at a target.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
            target_x: Target x position to aim toward.
            target_y: Target y position to aim toward.
            speed: Movement speed in pixels per frame.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = PROJECTILE_RADIUS
        self.color = PROJECTILE_COLOR                    # standaard grijs
        self.damage = PROJECTILE_DAMAGE

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
        """Move the projectile along its direction vector.

        Subclasses can override this for custom movement patterns
        such as homing or wave motion.
        """
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

    def is_off_screen(self, screen_width: int, screen_height: int) -> bool:     # check buiten scherm
        """Check whether the projectile has left the screen bounds.

        Args:
            screen_width: Width of the game window in pixels.
            screen_height: Height of the game window in pixels.

        Returns:
            True if the projectile is fully outside the screen.
        """
        return (self.x < -self.radius or self.x > screen_width + self.radius
                or self.y < -self.radius or self.y > screen_height + self.radius)

    def collides_with_enemy(self, enemy_x: float, enemy_y: float, enemy_radius: float) -> bool:
        """Check whether this projectile overlaps with an enemy.

        Uses distance between centers vs sum of radii.

        Args:
            enemy_x: X position of the enemy center.
            enemy_y: Y position of the enemy center.
            enemy_radius: Radius of the enemy hitbox.

        Returns:
            True if the projectile and enemy circles overlap.
        """
        dx = enemy_x - self.x
        dy = enemy_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        return distance < (self.radius + enemy_radius)

    def draw(self, screen: pygame.Surface) -> None:                             # draw kogel
        """Draw the projectile as a simple circle.

        Subclasses override this for custom visuals like glow effects.

        Args:
            screen: Pygame surface to draw on.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)


class PlasmaBullet(ProjectileBase):
    """Cyan plasma projectile with a glow effect.

    The default weapon type fired by the player. Overrides draw()
    to render a glowing bullet with a bright inner core.
    """
    # Plasma kogel --> cyaan glow, standaard wapen van de speler.

    def __init__(self, x: float, y: float, target_x: float, target_y: float) -> None:
        """Create a plasma bullet aimed at a target.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
            target_x: Target x position to aim toward.
            target_y: Target y position to aim toward.
        """
        super().__init__(x, y, target_x, target_y)
        self.color = PLASMA_COLOR                        # cyaan, matcht speler

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the plasma bullet with a cyan glow and bright core.

        Args:
            screen: Pygame surface to draw on.
        """
        x, y = int(self.x), int(self.y)

        # glow effect
        glow_surface = pygame.Surface((self.radius * 4, self.radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (*PLASMA_COLOR, PLASMA_GLOW_ALPHA), (self.radius * 2, self.radius * 2), self.radius + 4)
        screen.blit(glow_surface, (x - self.radius * 2, y - self.radius * 2))

        # kern
        pygame.draw.circle(screen, self.color, (x, y), self.radius)
        pygame.draw.circle(screen, PLASMA_CORE_COLOR, (x, y), self.radius - 2)     # lichte kern
