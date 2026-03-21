"""Visual effects manager for transient combat and wave feedback."""

import pygame


class VisualEffectsManager:
    """Manages short-lived particles and glow overlays used during gameplay."""

    def __init__(self, font: pygame.font.Font) -> None:
        """
        Initialize the visual effects manager.
        Args:
            font (pygame.font.Font): Font available for potential text-based effects (unused currently).
        """
        self._muzzle_flashes: list[dict] = []
        self._explosions: list[dict] = []
        self._core_hits: list[dict] = []

    def spawn_muzzle_flash(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        """
        Create a short flash of light simulating a weapon muzzle blast.
        Args:
            x (float): X-coordinate of the flash center.
            y (float): Y-coordinate of the flash center.
            color (tuple[int, int, int]): RGB color of the flash glow.
        """
        self._muzzle_flashes.append({
            "x": x,
            "y": y,
            "color": color,
            "timer": 8,
            "max_timer": 8,
            "radius": 10,
        })

    def spawn_enemy_destroyed(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        """
        Create an expanding explosion effect for destroyed enemies.
        Args:
            x (float): X-coordinate of the explosion center.
            y (float): Y-coordinate of the explosion center.
            color (tuple[int, int, int]): RGB color of the explosion glow.
        """
        self._explosions.append({
            "x": x,
            "y": y,
            "color": color,
            "timer": 18,
            "max_timer": 18,
            "radius": 8,
            "growth": 2.2,
        })

    def spawn_core_hit(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        """
        Create an expanding glow to indicate the player's core being hit.
        Args:
            x (float): X-coordinate of the hit location.
            y (float): Y-coordinate of the hit location.
            color (tuple[int, int, int]): RGB color of the glow effect.
        """
        self._core_hits.append({
            "x": x,
            "y": y,
            "color": color,
            "timer": 20,
            "max_timer": 20,
            "radius": 24,
        })

    def update(self) -> None:
        """
        Update all active effects. Decrease their timers and expand their radii
        when appropriate. Expired effects are removed from their respective lists.
        """
        for effect in self._muzzle_flashes:
            effect["timer"] -= 1
        self._muzzle_flashes = [e for e in self._muzzle_flashes if e["timer"] > 0]

        for effect in self._explosions:
            effect["timer"] -= 1
            effect["radius"] += effect["growth"]
        self._explosions = [e for e in self._explosions if e["timer"] > 0]

        for effect in self._core_hits:
            effect["timer"] -= 1
            effect["radius"] += 1.6
        self._core_hits = [e for e in self._core_hits if e["timer"] > 0]

    def _draw_glow_circle(
        self,
        screen: pygame.Surface,
        x: float,
        y: float,
        radius: float,
        color: tuple[int, int, int],
        alpha: int,
    ) -> None:
        """
        Render a soft circular glow using an alpha-translucent surface.
        Args:
            screen (pygame.Surface): Target surface to draw on.
            x (float): X-coordinate of the circle center.
            y (float): Y-coordinate of the circle center.
            radius (float): Radius of the glow circle.
            color (tuple[int, int, int]): RGB color of the circle.
            alpha (int): Transparency (0–255), where 0 is fully transparent.
        """
        size = int(radius * 2) + 8
        glow = pygame.Surface((size, size), pygame.SRCALPHA)
        center = size // 2
        pygame.draw.circle(glow, (*color, alpha), (center, center), int(radius))
        screen.blit(glow, (int(x - center), int(y - center)))

    def draw(self, screen: pygame.Surface) -> None:
        """
        Render all current visual effects on the given screen surface.
        Each category of effect is drawn with intensity and radius determined
        by its remaining lifetime.
        Args:
            screen (pygame.Surface): Target surface to draw the effects on.
        """
        for flash in self._muzzle_flashes:
            life = flash["timer"] / flash["max_timer"]
            self._draw_glow_circle(
                screen,
                flash["x"],
                flash["y"],
                flash["radius"] + (1.0 - life) * 7,
                flash["color"],
                int(120 * life),
            )

        for explosion in self._explosions:
            life = explosion["timer"] / explosion["max_timer"]
            self._draw_glow_circle(
                screen,
                explosion["x"],
                explosion["y"],
                explosion["radius"],
                explosion["color"],
                int(140 * life),
            )
            pygame.draw.circle(
                screen,
                explosion["color"],
                (int(explosion["x"]), int(explosion["y"])),
                int(explosion["radius"]),
                2,
            )

        for hit in self._core_hits:
            life = hit["timer"] / hit["max_timer"]
            self._draw_glow_circle(screen, hit["x"], hit["y"], hit["radius"], hit["color"], int(90 * life))
            pygame.draw.circle(
                screen,
                hit["color"],
                (int(hit["x"]), int(hit["y"])),
                int(hit["radius"]),
                3,
            )

