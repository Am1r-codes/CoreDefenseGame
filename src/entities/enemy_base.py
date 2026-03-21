"""Base enemy class and all enemy type subclasses.

Each enemy type represents a real AI/ML failure mode and overrides
the base class to provide unique stats, visuals, and movement behavior.
"""

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
    """Base enemy representing Corrupted Data.

    Moves in a straight line toward the brain at a constant speed.
    Subclasses override __init__, update, and draw for unique behavior.
    """

    def __init__(self, x: float, y: float, speed: float = ENEMY_BASE_SPEED) -> None:
        """Create an enemy at the given position.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
            speed: Movement speed in pixels per frame.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = ENEMY_BASE_RADIUS
        self.color = ENEMY_BASE_COLOR                   
        self.damage = ENEMY_BASE_DAMAGE
        self.score_value = ENEMY_BASE_SCORE             

    def update(self, target_x: float, target_y: float) -> None:         
        """Move the enemy toward the target position.

        Calculates a normalized direction vector and moves at
        self.speed pixels per frame. Subclasses can override this
        for custom movement patterns.

        Args:
            target_x: X position of the target (brain).
            target_y: Y position of the target (brain).
        """
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen: pygame.Surface) -> None:                     
        """Draw the enemy as a colored circle.

        Subclasses override this for custom visuals like glow
        effects or border rings.

        Args:
            screen: Pygame surface to draw on.
        """
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def collides_with_brain(self, core_x: float, core_y: float, core_radius: float) -> bool:    
        """Check whether this enemy overlaps with the brain core.

        Uses distance between centers vs sum of radii.

        Args:
            core_x: X position of the brain center.
            core_y: Y position of the brain center.
            core_radius: Radius of the brain hitbox.

        Returns:
            True if the enemy and brain circles overlap.
        """
        dx = core_x - self.x
        dy = core_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        return distance < (self.radius + core_radius)

class NoiseEnemy(EnemyBase):
    """Fast enemy representing random Noise interference.

    Very fast and small, making it hard to hit. Renders with
    a layered glow effect around the core circle.
    """

    def __init__(self, x: float, y: float) -> None:
        """Create a Noise enemy at the given position.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
        """
        super().__init__(x, y, speed=NOISE_SPEED)
        self.color = NOISE_COLOR                         
        self.damage = NOISE_DAMAGE
        self.score_value = NOISE_SCORE                    

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the Noise enemy with a layered glow effect.

        Args:
            screen: Pygame surface to draw on.
        """
        x, y = int(self.x), int(self.y)

        for r, alpha in [(self.radius + 10, 40), (self.radius + 6, 70)]:            
            glow_surface = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*NOISE_COLOR, alpha), (r, r), r)
            screen.blit(glow_surface, (x - r, y - r))

        pygame.draw.circle(screen, self.color, (x, y), self.radius)

class BiasEnemy(EnemyBase):
    """Slow, tanky enemy representing systematic Bias.

    Large radius and high damage, rendered with a dark border ring
    around the main body.
    """

    def __init__(self, x: float, y: float) -> None:
        """Create a Bias enemy at the given position.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
        """
        super().__init__(x, y, speed=BIAS_SPEED)
        self.radius = BIAS_RADIUS
        self.color = BIAS_COLOR                           
        self.damage = BIAS_DAMAGE
        self.score_value = BIAS_SCORE                     

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the Bias enemy with a dark border ring.

        Args:
            screen: Pygame surface to draw on.
        """
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, BIAS_BORDER_COLOR, (x, y), self.radius + 3)  # Darker outer ring
        pygame.draw.circle(screen, self.color, (x, y), self.radius)                

class HallucinationEnemy(EnemyBase):
    """Erratic enemy representing AI Hallucination.

    Moves toward the brain but sways randomly each frame,
    creating an unpredictable zigzag path.
    """

    def __init__(self, x: float, y: float) -> None:
        """Create a Hallucination enemy at the given position.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
        """
        super().__init__(x, y, speed=HALLUCINATION_SPEED)
        self.color = HALLUCINATION_COLOR                  
        self.damage = HALLUCINATION_DAMAGE
        self.radius = HALLUCINATION_RADIUS
        self.score_value = HALLUCINATION_SCORE            

    def update(self, target_x: float, target_y: float) -> None:    
        """Move toward the target with random directional sway.

        Overrides EnemyBase.update to add random noise to the
        direction vector each frame, causing erratic movement.

        Args:
            target_x: X position of the target (brain).
            target_y: Y position of the target (brain).
        """
        dx = target_x - self.x
        dy = target_y - self.y

        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        dx += random.uniform(-HALLUCINATION_SWAY, HALLUCINATION_SWAY)   # Random sway added to direction
        dy += random.uniform(-HALLUCINATION_SWAY, HALLUCINATION_SWAY)

        self.x += dx * self.speed                       
        self.y += dy * self.speed

class OverfittingEnemy(EnemyBase):
    """Massive, slow enemy representing Overfitting.

    The largest and most dangerous enemy type. Rendered with a
    dark purple outer ring around a red core.
    """

    def __init__(self, x: float, y: float) -> None:
        """Create an Overfitting enemy at the given position.

        Args:
            x: Starting x position in pixels.
            y: Starting y position in pixels.
        """
        super().__init__(x, y, speed=OVERFITTING_SPEED)
        self.color = OVERFITTING_COLOR                 
        self.damage = OVERFITTING_DAMAGE
        self.radius = OVERFITTING_RADIUS
        self.score_value = OVERFITTING_SCORE             

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the Overfitting enemy with a dark purple border.

        Args:
            screen: Pygame surface to draw on.
        """
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(screen, OVERFITTING_BORDER_COLOR, (x, y), self.radius + 4)   # Darker outer ring
        pygame.draw.circle(screen, self.color, (x, y), self.radius)                     
