"""Start menu scherm en basis klasse voor game states."""

import pygame
from src.settings import BG_COLOR, COLOR_CYAN, COLOR_SUBTITLE, COLOR_WHITE, FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE, MENU_BLINK_INTERVAL


class GameScreen:
    """Basis klasse voor game schermen, subclasses overriden handle_events, update, draw."""

    def __init__(self, game) -> None:
        self.game = game

    def handle_events(self) -> None:
        """Verwerk input, subclasses overriden dit."""
        pass

    def update(self) -> None:
        """Update logica, subclasses overriden dit."""
        pass

    def draw(self) -> None:
        """Teken scherm, subclasses overriden dit."""
        pass


class MenuScreen(GameScreen):
    """Startscherm met titel, instructies en enemy preview."""

    def __init__(self, game) -> None:
        super().__init__(game)
        self._frame_counter = 0
        self._title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)
        self._subtitle_font = pygame.font.SysFont(None, FONT_SIZE_SUBTITLE)

    def handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game.start_playing()

    def update(self) -> None:
        self._frame_counter += 1

    def draw(self) -> None:
        screen = self.game.screen
        width = self.game.width
        height = self.game.height

        screen.fill(BG_COLOR)

        # titel
        title = self._title_font.render("Core Collapse", True, COLOR_CYAN)
        title_rect = title.get_rect(center=(width // 2, height // 4))
        screen.blit(title, title_rect)

        # ondertitel
        subtitle = self._subtitle_font.render("Defend the AI Core", True, COLOR_SUBTITLE)
        sub_rect = subtitle.get_rect(center=(width // 2, height // 4 + 60))
        screen.blit(subtitle, sub_rect)

        # knipperende "Press ENTER" tekst (wissel elke 30 frames)
        if (self._frame_counter // MENU_BLINK_INTERVAL) % 2 == 0:
            start_text = self.game.font.render("Press ENTER to start", True, COLOR_WHITE)
            start_rect = start_text.get_rect(center=(width // 2, height - 100))
            screen.blit(start_text, start_rect)

        # enemy preview (hergebruik legenda)
        self.game.hud.draw_enemy_legend(screen)
