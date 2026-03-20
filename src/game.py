"""Top-level game loop and coordination."""

import pygame
from src.entities.core import Brain
from src.entities.player import Player
from src.entities.projectile import ProjectileBase
from src.managers.wave_manager import WaveManager
from src.ui.hud import HUD
from src.ui.menu import MenuScreen
from src.ui.game_over import GameOverScreen


class Game:
    """Main game object that controls the window and game loop."""

    def __init__(self) -> None:
        pygame.init()
        self.width = 1000
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Core Collapse")     # titel venster
        self.clock = pygame.time.Clock()                # nodig voor FPS
        self.running = True                             # game loop moet doorgaan

        self.font = pygame.font.SysFont(None, 36)
        self.hud = HUD(self.width, self.font)

        # scherm-states: menu, playing (= self), game_over
        self.menu_screen = MenuScreen(self)
        self.game_over_screen = GameOverScreen(self)
        self.active_screen = self.menu_screen           # start op menu

    def start_playing(self) -> None:
        """Reset gameplay en schakel naar playing state."""
        self._reset_gameplay()
        self.active_screen = self                       # Game zelf is de playing screen

    def _reset_gameplay(self) -> None:
        """Initialiseer of reset alle gameplay objecten."""
        self.brain = Brain(self.width // 2, self.height // 2)
        self.enemies = []
        self.wave_manager = WaveManager(self.width, self.height)
        self.player = Player(self.width // 2, self.height // 2 + 100)
        self.projectiles: list[ProjectileBase] = []

        self.score = 0
        self._combo_multiplier = 1                      # combo vermenigvuldiger
        self._combo_timer = 0                           # frames sinds laatste kill

        self.damage_texts = []                          # lijst waar je alle tijdelijke damage teksten opslaat
        self.score_texts = []                           # zwevende "+X pts" bij kill positie

    def handle_events(self) -> None:                    # kijkt naar gebeurtenissen van pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False                    # spel stopt als speler op kruisje drukt

        # continu schieten bij ingedrukte muisknop
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            projectile = self.player.try_shoot(mouse_x, mouse_y)
            if projectile is not None:
                self.projectiles.append(projectile)

    def update(self) -> None:                           # enemies bewegen + botsing checken + kogels bewegen + score updaten
        self.wave_manager.update(self.enemies)

        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.player.update(keys, mouse_x, mouse_y,
                           self.width, self.height,
                           self.brain.x, self.brain.y, self.brain.radius)

        # kogels updaten en off-screen verwijderen
        for projectile in self.projectiles:
            projectile.update()
        self.projectiles = [p for p in self.projectiles if not p.is_off_screen(self.width, self.height)]

        # combo timer bijhouden
        if self._combo_timer > 0:
            self._combo_timer -= 1
        else:
            self._combo_multiplier = 1                  # reset na 3 sec zonder kill

        # kogel-enemy botsing
        remaining_projectiles = []
        for projectile in self.projectiles:
            hit = False
            for enemy in self.enemies:
                if projectile.collides_with_enemy(enemy.x, enemy.y, enemy.radius):
                    self.enemies.remove(enemy)          # enemy verdwijnt bij hit

                    # score toekennen met combo
                    points = enemy.score_value * self._combo_multiplier
                    self.score += points
                    self._combo_multiplier = min(self._combo_multiplier + 1, 8)   # max 8x
                    self._combo_timer = 180             # 3 seconden bij 60 FPS

                    # zwevende score tekst op kill positie
                    self.score_texts.append({
                        'x': enemy.x,
                        'y': enemy.y,
                        'text': f"+{points}",
                        'timer': 50,
                        'color': (0, 220, 255)
                    })

                    hit = True
                    break
            if not hit:
                remaining_projectiles.append(projectile)
        self.projectiles = remaining_projectiles

        # enemies bewegen en brein-botsing
        remaining_enemies = []
        for enemy in self.enemies:
            enemy.update(self.brain.x, self.brain.y)
            if enemy.collides_with_brain(self.brain.x, self.brain.y, self.brain.radius):
                self.brain.health -= enemy.damage

                self.damage_texts.append({
                    'x': 140,                           # tonen even breedt bij health:..
                    'y': 30,                            # tonen onder health: ..
                    'text': f"-{enemy.damage}",
                    'timer': 60,
                    'color': enemy.color
                })
            else:
                remaining_enemies.append(enemy)
        self.enemies = remaining_enemies

        for dmg in self.damage_texts:
            dmg["y"] -= 1
            dmg["timer"] -= 1
        self.damage_texts = [d for d in self.damage_texts if d["timer"] > 0]

        for st in self.score_texts:
            st["y"] -= 1
            st["timer"] -= 1
        self.score_texts = [s for s in self.score_texts if s["timer"] > 0]

        # game over check
        if self.brain.health <= 0:
            self.game_over_screen.set_results(self.score, self.wave_manager.wave_number)
            self.active_screen = self.game_over_screen
            return

    def draw(self) -> None:                             # tekent alles op het scherm
        self.screen.fill((20, 20, 30))                  # maakt achtergrond donker
        self.brain.draw(self.screen, self.font)
        self.brain.draw_health(self.screen, self.font)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for projectile in self.projectiles:
            projectile.draw(self.screen)

        self.player.draw(self.screen)
        self.hud.draw_enemy_legend(self.screen)         # legenda
        self.hud.draw_wave_counter(self.screen, self.wave_manager.wave_number)
        self.hud.draw_score(self.screen, self.score, self._combo_multiplier)

        # "Wave X" tekst tijdens pauze tussen waves
        if self.wave_manager.is_between_waves and self.wave_manager.wave_number < 1:
            wave_text = self.font.render("Get Ready...", True, (0, 220, 255))
        elif self.wave_manager.is_between_waves:
            wave_text = self.font.render(f"Wave {self.wave_manager.wave_number + 1}", True, (0, 220, 255))
        else:
            wave_text = None

        if wave_text is not None:
            text_rect = wave_text.get_rect(center=(self.width // 2, self.height // 2 - 160))
            self.screen.blit(wave_text, text_rect)

        for dmg in self.damage_texts:
            text_surface = self.font.render(dmg["text"], True, dmg['color'])
            self.screen.blit(text_surface, (dmg["x"], dmg["y"]))

        for st in self.score_texts:
            score_surface = self.font.render(st["text"], True, st['color'])
            self.screen.blit(score_surface, (int(st["x"]), int(st["y"])))

    def run(self) -> None:                              # main game loop: zolang running = True: steed opnieuw dit
        while self.running:
            self.clock.tick(60)                         # 60 frames per second
            self.active_screen.handle_events()
            self.active_screen.update()
            self.active_screen.draw()
            pygame.display.flip()                       # laat nieuw frame zien

        pygame.quit()
