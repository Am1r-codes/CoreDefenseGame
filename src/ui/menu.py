"""Start menu screen and base class for all game state screens."""

import pygame
from src.settings import BG_COLOR, COLOR_CYAN, COLOR_SUBTITLE, COLOR_WHITE, FONT_SIZE_TITLE, FONT_SIZE_SUBTITLE, MENU_BLINK_INTERVAL


class GameScreen:
    """Abstract base class for game state screens.

    Defines the shared interface (handle_events, update, draw) that
    all screens implement. The Game class dispatches to the active
    screen each frame using this interface (state pattern).
    """

    def __init__(self, game) -> None:
        """Create a screen linked to the parent game instance.

        Args:
            game: Reference to the Game object for accessing shared
                resources like the display surface, font, and HUD.
        """
        self.game = game

    def handle_events(self) -> None:
        """Process input events for this screen. Override in subclasses."""
        pass

    def update(self) -> None:
        """Update logic for this screen. Override in subclasses."""
        pass

    def draw(self) -> None:
        """Render this screen to the display. Override in subclasses."""
        pass


class MenuScreen(GameScreen):
    """Main menu screen shown when the game starts.

    Displays the game title, subtitle, a blinking start prompt,
    and an enemy type preview legend. Pressing Enter transitions
    to the playing state.
    """

    def __init__(self, game) -> None:
        """Create the menu screen with title and subtitle fonts.

        Args:
            game: Reference to the parent Game object.
        """
        super().__init__(game)
        self._frame_counter = 0
        self._title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)
        self._subtitle_font = pygame.font.SysFont(None, FONT_SIZE_SUBTITLE)

    def handle_events(self) -> None:
        """Process menu input events.

        Handles window close and Enter key to start the game.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.game.play_sound("menu_start")
                self.game.start_playing()

    def update(self) -> None:
        """Advance the frame counter for the blinking text animation."""
        self._frame_counter += 1

    def draw(self) -> None:
        """Render the menu screen with title, subtitle, prompt, and legend."""
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
