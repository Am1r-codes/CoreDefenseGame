"""Entry point for the Core Collapse project."""

from src.game import Game

def main() -> None:
    """Initialize and run the Core Collapse game."""
    game = Game()
    game.run()

if __name__ == "__main__":
    main()