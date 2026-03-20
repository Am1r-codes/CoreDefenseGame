"""Top-level game loop and coordination."""

import pygame
from src.entities.core import Brain
from src.entities.enemy_base import EnemyBase, NoiseEnemy, BiasEnemy, HallucinationEnemy, OverfittingEnemy
from src.ui.hud import HUD

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
        self.brain = Brain(self.width // 2, self.height // 2)
        
        self.enemies = []
        
        self.enemies.append(EnemyBase(50, self.height // 2))    # test enemy links
        self.enemies.append(EnemyBase(50, 150))
        self.enemies.append(NoiseEnemy(200, 300))
        self.enemies.append(BiasEnemy(400, 600))
        self.enemies.append(HallucinationEnemy(1000, 500))
        self.enemies.append(OverfittingEnemy(300, 700))
        self.enemies.append(OverfittingEnemy(100, 700))

        self.hud = HUD(self.width, self.font)
        self.damage_texts = []                          # lijst waar je alle tijdelijke damage teksten opslaat

    def handle_events(self) -> None:                    # kijkt naar gebeurtenissen van pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False                    # spel stopt als speler op kruisje drukt

    def update(self) -> None:                           # kunnen we later: enemies bewegen + botsing checken + kogels bewegen + score updaten
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

    def draw(self) -> None:                             # tekent alles op het scherm
        self.screen.fill((20, 20, 30))                  # maakt achtergrond donker
        self.brain.draw(self.screen, self.font)
        self.brain.draw_health(self.screen, self.font)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.hud.draw_enemy_legend(self.screen)         # legenda

        for dmg in self.damage_texts:
            text_surface = self.font.render(dmg["text"], True, dmg['color'])
            self.screen.blit(text_surface, (dmg["x"], dmg["y"]))

        pygame.display.flip()                           # laat nieuw frame zien

    def run(self) -> None:                              # main game loop: zolang running = True: steed opnieuw dit
        while self.running:
            self.clock.tick(60)                         # 60 frames per second
            self.handle_events()
            self.update()
            self.draw()

        pygame.quit()