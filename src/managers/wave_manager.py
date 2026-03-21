"""Wave spawning system with progressive difficulty.

Controls when and where enemies spawn, which types are available,
and how wave difficulty scales over time.
"""

import random
from src.entities.enemy_base import EnemyBase, NoiseEnemy, BiasEnemy, HallucinationEnemy, OverfittingEnemy
from src.settings import (
    WAVE_SPAWN_DELAY, WAVE_BREAK_DURATION, WAVE_SPAWN_MARGIN,
    WAVE_BASE_COUNT, WAVE_COUNT_SCALE,
    WAVE_UNLOCK_NOISE, WAVE_UNLOCK_BIAS, WAVE_UNLOCK_HALLUCINATION, WAVE_UNLOCK_OVERFITTING,
)


class WaveManager:
    """Manages enemy wave spawning, timing, and progressive difficulty.

    Enemies are spawned in staggered batches from random positions
    outside the screen. Each wave introduces more enemies and unlocks
    tougher types at specific wave thresholds. A short break is given
    between waves.
    """

    def __init__(self, screen_width: int, screen_height: int) -> None:
        """Create a wave manager for the given screen dimensions.

        Args:
            screen_width: Width of the game window in pixels.
            screen_height: Height of the game window in pixels.
        """
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._wave_number = 0
        self._spawn_queue: list[type] = []        
        self._spawn_timer = 0                     
        self._spawn_delay = WAVE_SPAWN_DELAY     
        self._break_timer = 0                     
        self._break_duration = WAVE_BREAK_DURATION

    @property
    def wave_number(self) -> int:
        """Return the current wave number for display on the HUD."""
        return self._wave_number

    @property
    def is_between_waves(self) -> bool:
        """Return True if the game is in a break period between waves."""
        return self._break_timer > 0

    def _get_spawn_position(self) -> tuple[float, float]:
        """Generate a random spawn position outside the screen edges.

        Picks a random edge (top, bottom, left, right) and returns
        a position offset beyond that edge by WAVE_SPAWN_MARGIN pixels.

        Returns:
            A tuple of (x, y) coordinates outside the visible screen.
        """
        edge = random.choice(["top", "bottom", "left", "right"])

        if edge == "top":
            return random.uniform(0, self._screen_width), -WAVE_SPAWN_MARGIN
        elif edge == "bottom":
            return random.uniform(0, self._screen_width), self._screen_height + WAVE_SPAWN_MARGIN
        elif edge == "left":
            return -WAVE_SPAWN_MARGIN, random.uniform(0, self._screen_height)
        else:
            return self._screen_width + WAVE_SPAWN_MARGIN, random.uniform(0, self._screen_height)

    def _get_enemy_types(self) -> list[type]:
        """Determine which enemy types are unlocked for the current wave.

        New types are added at specific wave thresholds defined in settings.

        Returns:
            A list of enemy class references available for spawning.
        """
        types = [EnemyBase]

        if self._wave_number >= WAVE_UNLOCK_NOISE:
            types.append(NoiseEnemy)
        if self._wave_number >= WAVE_UNLOCK_BIAS:
            types.append(BiasEnemy)
        if self._wave_number >= WAVE_UNLOCK_HALLUCINATION:
            types.append(HallucinationEnemy)
        if self._wave_number >= WAVE_UNLOCK_OVERFITTING:
            types.append(OverfittingEnemy)

        return types

    def _build_wave(self) -> list[type]:
        """Build a spawn queue of enemy classes for the current wave.

        Enemy count scales with the wave number using the formula:
        WAVE_BASE_COUNT + wave_number * WAVE_COUNT_SCALE.

        Returns:
            A list of enemy class references to be spawned.
        """
        available_types = self._get_enemy_types()
        enemy_count = WAVE_BASE_COUNT + self._wave_number * WAVE_COUNT_SCALE

        queue = []
        for _ in range(enemy_count):
            enemy_class = random.choice(available_types)
            queue.append(enemy_class)

        return queue

    def _start_next_wave(self) -> None:
        """Increment the wave number and build the spawn queue."""
        self._wave_number += 1
        self._spawn_queue = self._build_wave()
        self._spawn_timer = 0

    def update(self, enemies: list) -> None:
        """Advance the wave state by one frame.

        Handles break countdowns, triggers new waves, and spawns
        enemies from the queue with staggered timing. Called once
        per frame from the game loop.

        Args:
            enemies: The live enemy list to append newly spawned enemies to.
        """

        # Count down the break between waves
        if self._break_timer > 0:
            self._break_timer -= 1
            if self._break_timer <= 0:
                self._start_next_wave()
            return

        if self._wave_number == 0:
            self._break_timer = self._break_duration
            return

        if len(self._spawn_queue) == 0 and len(enemies) == 0:
            self._break_timer = self._break_duration
            return

        if len(self._spawn_queue) > 0:
            self._spawn_timer -= 1
            if self._spawn_timer <= 0:
                enemy_class = self._spawn_queue.pop(0)
                x, y = self._get_spawn_position()
                enemies.append(enemy_class(x, y))
                self._spawn_timer = self._spawn_delay
