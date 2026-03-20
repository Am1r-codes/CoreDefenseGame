"""Top-level game loop, state management, and coordination.

The Game class serves as both the main coordinator and the playing
state screen. It manages transitions between menu, playing, and
game over states using the state pattern via active_screen.
"""

import pygame
from src.entities.core import Brain
from src.entities.player import Player
from src.entities.projectile import ProjectileBase
from src.managers.wave_manager import WaveManager
from src.ui.hud import HUD
from src.ui.menu import MenuScreen
from src.ui.game_over import GameOverScreen
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, FONT_SIZE, BG_COLOR, COLOR_CYAN,
    COMBO_MAX, COMBO_DURATION, SCORE_TEXT_TIMER,
    DAMAGE_TEXT_TIMER, DAMAGE_TEXT_X, DAMAGE_TEXT_Y,
)


class Game:
    """Main game object that controls the window, game loop, and state transitions.

    Acts as the playing state screen itself — its handle_events(),
    update(), and draw() methods are called directly when the game is
    in the playing state, using the same interface as MenuScreen and
    GameOverScreen (state pattern via duck typing).
    """

    def __init__(self) -> None:
        """Initialize pygame, create the window, HUD, and state screens."""
        pygame.init()
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Core Collapse")     # titel venster
        self.clock = pygame.time.Clock()                # nodig voor FPS
        self.running = True                             # game loop moet doorgaan

        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.hud = HUD(self.width, self.font)

        # scherm-states: menu, playing (= self), game_over
        self.menu_screen = MenuScreen(self)
        self.game_over_screen = GameOverScreen(self)
        self.active_screen = self.menu_screen           # start op menu

    def start_playing(self) -> None:
        """Reset all gameplay objects and switch to the playing state."""
        self._reset_gameplay()
        self.active_screen = self                       # Game zelf is de playing screen

    def _reset_gameplay(self) -> None:
        """Initialize or reset all gameplay objects for a new game.

        Creates fresh instances of the brain, player, wave manager,
        and clears all projectiles, enemies, scores, and floating texts.
        """
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
        """Process input events during the playing state.

        Handles window close and continuous shooting while the
        left mouse button is held down.
        """
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
        """Update all gameplay systems for one frame.

        Advances wave spawning, moves the player and projectiles,
        checks projectile-enemy and enemy-brain collisions, updates
        the score and combo multiplier, and triggers game over when
        the brain's health reaches zero.
        """
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
                    self._combo_multiplier = min(self._combo_multiplier + 1, COMBO_MAX)
                    self._combo_timer = COMBO_DURATION

                    # zwevende score tekst op kill positie
                    self.score_texts.append({
                        'x': enemy.x,
                        'y': enemy.y,
                        'text': f"+{points}",
                        'timer': SCORE_TEXT_TIMER,
                        'color': COLOR_CYAN
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
                    'x': DAMAGE_TEXT_X,                 # tonen even breedt bij health:..
                    'y': DAMAGE_TEXT_Y,                 # tonen onder health: ..
                    'text': f"-{enemy.damage}",
                    'timer': DAMAGE_TEXT_TIMER,
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
        """Render all gameplay elements to the screen.

        Draws the brain, enemies, projectiles, player, HUD elements,
        wave announcements, and floating damage/score texts.
        """
        self.screen.fill(BG_COLOR)                      # maakt achtergrond donker
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
            wave_text = self.font.render("Get Ready...", True, COLOR_CYAN)
        elif self.wave_manager.is_between_waves:
            wave_text = self.font.render(f"Wave {self.wave_manager.wave_number + 1}", True, COLOR_CYAN)
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
        """Run the main game loop until the player quits.

        Ticks at FPS frames per second. Each frame dispatches to
        the active screen's handle_events, update, and draw methods.
        """
        while self.running:
            self.clock.tick(FPS)                         # 60 frames per second
            self.active_screen.handle_events()
            self.active_screen.update()
            self.active_screen.draw()
            pygame.display.flip()                       # laat nieuw frame zien

        pygame.quit()
