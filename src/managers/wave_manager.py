"""Wave spawning and progression placeholder."""

import random
from entities.enemy_base import EnemyBase, NoiseEnemy, BiasEnemy, HallucinationEnemy, OverfittingEnemy

class WaveManager:
    def __init__(self):
        """
        De waves worden aangemaakt in de vorm van een dict, waarin de key een soort enemey is en de 
        value gelijk is aan de hoeveelheid. We starten bij wave 0, dus de current wave staat voor het begin op
        -1. Er zijn aan het begin nog geen actieve enemies, en er is dus ook geen actieve wave. Spawn timer
        houd de tijd bij sinds de vorige gespanwde enemy. De interval is de tijd tussen iedere spawn. 
        enemies_to_spawn houd bij welke enemies er nog gespawned moeten worden.  
        """
        self.waves = [
            {'NoiseEnemy': 5, 'BiasEnemy': 2},
            {'NoiseEnemy': 8, 'HallucinationEnemy': 3},
            {'OverfittingEnemy': 1, 'NoiseEnemy': 10},   
        ]
        self.current_wave_index = -1 
        self.active_enemies = []
        self.wave_in_progress = False
        self.spawn_timer = 0 
        self.spawn_interval = 30        
        self.enemies_to_spawn = []        

    def start_next_wave(self):
        """Start de volgende wave als die er is, door hem te vergelijken met het totale lengte van"""
        self.current_wave_index += 1
        if self.current_wave_index >= len(self.waves):
            print("All waves completed!")
            return False
        wave = self.waves[self.current_wave_index]
        self.enemies_to_spawn = []
        for enemy_type, count in wave.items():
            for _ in range(count):
                self.enemies_to_spawn.append(enemy_type)
        self.wave_in_progress = True
        print(f"Wave {self.current_wave_index + 1} started with {len(self.enemies_to_spawn)} enemies.")
        return True

    def update(self, screen_width=1000, screen_height=700):
        """Update enemies spawns en active enemies"""
        if self.enemies_to_spawn:
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = 0
                enemy_type_name = self.enemies_to_spawn.pop(0)
                x, y = self.random_spawn_position(screen_width, screen_height)
                enemy_class = globals()[enemy_type_name]
                enemy_instance = enemy_class(x, y)
                self.active_enemies.append(enemy_instance)

        if not self.enemies_to_spawn and not self.active_enemies:
            self.wave_in_progress = False

    def random_spawn_position(self, width, height):
        """Spawn aan rand van scherm"""
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            return random.randint(0, width), 0
        elif side == 'bottom':
            return random.randint(0, width), height
        elif side == 'left':
            return 0, random.randint(0, height)
        else:
            return width, random.randint(0, height)
