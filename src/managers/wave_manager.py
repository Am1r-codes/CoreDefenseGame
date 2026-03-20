"""Wave spawning and progression placeholder."""

import random
from src.entities.enemy_base import EnemyBase, NoiseEnemy, BiasEnemy, HallucinationEnemy, OverfittingEnemy


class WaveManager:
    """Beheert enemy waves, spawning en progressie."""

    def __init__(self, screen_width: int, screen_height: int) -> None:
        self._screen_width = screen_width
        self._screen_height = screen_height
        self._wave_number = 0
        self._spawn_queue: list[type] = []        # enemy-klassen die nog gespawned moeten worden
        self._spawn_timer = 0                     # frames tot volgende spawn
        self._spawn_delay = 15                    # frames tussen spawns (staggered)
        self._break_timer = 0                     # pauze-teller tussen waves
        self._break_duration = 150                # 2.5 seconden bij 60 FPS

    @property
    def wave_number(self) -> int:
        """Huidige wave nummer, leesbaar voor HUD."""
        return self._wave_number

    @property
    def is_between_waves(self) -> bool:
        """True tijdens pauze tussen waves."""
        return self._break_timer > 0

    def _get_spawn_position(self) -> tuple[float, float]:
        """Geeft random positie buiten het scherm terug."""
        edge = random.choice(["top", "bottom", "left", "right"])
        margin = 40                               # hoe ver buiten scherm

        if edge == "top":
            return random.uniform(0, self._screen_width), -margin
        elif edge == "bottom":
            return random.uniform(0, self._screen_width), self._screen_height + margin
        elif edge == "left":
            return -margin, random.uniform(0, self._screen_height)
        else:
            return self._screen_width + margin, random.uniform(0, self._screen_height)

    def _get_enemy_types(self) -> list[type]:
        """Bepaalt welke enemy types beschikbaar zijn voor huidige wave."""
        types = [EnemyBase]

        if self._wave_number >= 3:
            types.append(NoiseEnemy)
        if self._wave_number >= 5:
            types.append(BiasEnemy)
        if self._wave_number >= 7:
            types.append(HallucinationEnemy)
        if self._wave_number >= 9:
            types.append(OverfittingEnemy)

        return types

    def _build_wave(self) -> list[type]:
        """Bouwt spawn-queue voor de huidige wave, steeds moeilijker."""
        available_types = self._get_enemy_types()
        enemy_count = 3 + self._wave_number * 2   # wave 1 = 5, wave 5 = 13, wave 10 = 23

        queue = []
        for _ in range(enemy_count):
            enemy_class = random.choice(available_types)
            queue.append(enemy_class)

        return queue

    def _start_next_wave(self) -> None:
        """Start de volgende wave: verhoog nummer, bouw queue."""
        self._wave_number += 1
        self._spawn_queue = self._build_wave()
        self._spawn_timer = 0

    def update(self, enemies: list) -> None:
        """Update wave state, spawnt enemies geleidelijk. Wordt elk frame aangeroepen."""

        # pauze tussen waves aftellen
        if self._break_timer > 0:
            self._break_timer -= 1
            if self._break_timer <= 0:
                self._start_next_wave()
            return

        # nog geen wave gestart -> begin eerste wave na korte pauze
        if self._wave_number == 0:
            self._break_timer = self._break_duration
            return

        # als queue leeg en alle enemies dood -> pauze voor volgende wave
        if len(self._spawn_queue) == 0 and len(enemies) == 0:
            self._break_timer = self._break_duration
            return

        # spawn volgende enemy uit queue met vertraging
        if len(self._spawn_queue) > 0:
            self._spawn_timer -= 1
            if self._spawn_timer <= 0:
                enemy_class = self._spawn_queue.pop(0)
                x, y = self._get_spawn_position()
                enemies.append(enemy_class(x, y))
                self._spawn_timer = self._spawn_delay
