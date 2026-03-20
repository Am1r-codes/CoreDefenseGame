# Core Collapse

A top-down core defense shooter built with Pygame. You play as a digital defender protecting an AI brain from waves of increasingly dangerous failure types — corrupted data, noise, bias, hallucination, and overfitting. Move, aim, and shoot to keep the core alive as long as possible while racking up combo points.

## Game Concept

In Core Collapse, the central AI core (visualized as a brain) is under attack from five types of enemies, each representing a real failure mode in machine learning:

- **Corrupted Data** — the most common threat. Junk inputs that flood the system in large numbers.
- **Noise** — fast and erratic. Represents random interference that is hard to filter out.
- **Bias** — slow but heavily armored. Systematic errors that deal significant damage when they reach the core.
- **Hallucination** — unpredictable movement. The model generating outputs that don't correspond to reality.
- **Overfitting** — massive and devastating. The model memorizing training data instead of learning patterns, causing catastrophic failure.

Each enemy type has distinct speed, size, damage, and visual behavior that mirrors the AI concept it represents. Defend the core through escalating waves where new enemy types are gradually introduced, forcing the player to adapt their strategy.

## How to Play

| Action         | Control                          |
|----------------|----------------------------------|
| Move           | `W` `A` `S` `D`                 |
| Aim            | Mouse cursor                     |
| Shoot          | Left mouse button (hold to fire) |
| Start game     | `Enter`                          |
| Restart        | `R` (on game over screen)        |
| Quit           | `Esc` or close window            |

**Objective:** Protect the AI brain core from incoming enemies. Enemies spawn from outside the screen in waves, each wave introducing more and tougher enemies. Kill enemies quickly in succession to build a combo multiplier (up to 8x) for higher scores. The game ends when the brain's health reaches zero.

## Enemy Types

| Enemy            | Color    | Speed  | Damage | Score | Behavior                                           |
|------------------|----------|--------|--------|-------|-----------------------------------------------------|
| Corrupted Data   | Blue     | 1.5    | 1      | 10    | Moves straight toward the core                      |
| Noise            | Orange   | 4.0    | 1      | 25    | Very fast, small, hard to hit, glowing effect        |
| Bias             | Green    | 1.0    | 3      | 30    | Slow and large, deals heavy damage                   |
| Hallucination    | Yellow   | 2.2    | 2      | 20    | Sways randomly while approaching the core            |
| Overfitting      | Red      | 0.9    | 5      | 50    | Largest and slowest, devastating on contact          |

**Wave progression:**
- Waves 1–2: Corrupted Data only
- Waves 3–4: + Noise
- Waves 5–6: + Bias
- Waves 7–8: + Hallucination
- Wave 9+: All enemy types, mixed together

## Installation

```bash
git clone <repo-url>
cd CoreDefenseGame
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

## Project Structure

```
CoreDefenseGame/
├── main.py                      # Entry point
├── requirements.txt             # Dependencies (pygame)
├── README.md
├── src/
│   ├── __init__.py
│   ├── settings.py              # All game constants and configuration
│   ├── game.py                  # Main game loop, state management, coordination
│   ├── effects.py               # Visual effects (placeholder)
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── core.py              # Brain entity with health and dynamic visuals
│   │   ├── player.py            # Player movement, aiming, and shooting
│   │   ├── projectile.py        # ProjectileBase + PlasmaBullet subclass
│   │   └── enemy_base.py        # EnemyBase + 4 enemy subclasses
│   ├── managers/
│   │   ├── __init__.py
│   │   └── wave_manager.py      # Wave spawning and progression system
│   └── ui/
│       ├── __init__.py
│       ├── hud.py               # HUD: health, score, combo, enemy legend
│       ├── menu.py              # GameScreen base class + MenuScreen
│       └── game_over.py         # Game over screen with results
└── assets/
    ├── images/
    ├── sounds/
    └── fonts/
```

## Architecture

### OOP Design
The project uses **inheritance and polymorphism** throughout. Enemy types extend `EnemyBase` and override `draw()` and `update()` for unique visuals and behavior — the same pattern applies to projectiles via `ProjectileBase` and `PlasmaBullet`. The game loop interacts with all entities through a shared interface (`update()`, `draw()`), so new types can be added without modifying existing code.

### Game Loop
Each frame follows a fixed three-phase cycle at 60 FPS:

```
handle_events()  →  update()  →  draw()
```

Event handling processes input and shooting. Update moves all entities, checks collisions, manages waves, and updates the score. Draw renders everything to the screen.

### State Management
Game states use the **state pattern** with polymorphism — no if/else chains. A `GameScreen` base class defines the `handle_events()` / `update()` / `draw()` interface. `MenuScreen` and `GameOverScreen` extend it. The `Game` class itself serves as the playing state (it has the same three methods). The active screen is swapped via `game.active_screen`:

```
MenuScreen  →  Game (playing)  →  GameOverScreen
                    ↑                    │
                    └────── restart ──────┘
```

### Wave System
`WaveManager` handles progressive difficulty. Enemy types are unlocked at specific wave thresholds. Enemies spawn in staggered batches (not all at once) from random positions outside the screen edges. A short break between waves gives the player time to prepare.

### Settings
All magic numbers and game constants are centralized in `src/settings.py` — screen dimensions, entity stats, colors, wave parameters, and HUD layout. This makes the game easy to tune and keeps the codebase clean.

## Team

- Amir
- Jamie
- Maaike
- Mats

## Requirements

- Python 3.10+
- Pygame 2.6.1
