"""Runtime sound effect manager using small synthesized tones."""

import math
import random
from array import array
from pathlib import Path

import pygame


class SoundManager:
    """Loads or synthesizes simple sound effects and provides named playback."""

    _TITLE_MUSIC_FILENAME = "Title_Screen_Music.mp3"
    _GAME_MUSIC_FILENAME = "Game_Music.mp3"
    _LOW_HEALTH_MUSIC_FILENAME = "Low_Health.mp3"
    _BOOM_SOUND_FILENAME = "Boom.mp3"
    _GAME_OVER_SOUND_FILENAME = "Game_Over.mp3"

    _TITLE_MUSIC_HINTS = ("title", "menu", "screen", "music")
    _GAME_MUSIC_HINTS = ("game_music", "game music", "battle", "play")
    _LOW_HEALTH_MUSIC_HINTS = ("low_health", "low health", "critical", "warning")
    _BOOM_SOUND_HINTS = ("boom", "alert", "alarm")
    _GAME_OVER_SOUND_HINTS = ("game_over", "game over", "defeat", "failure")
    _TITLE_MUSIC_FADEOUT_MS = 900
    _TITLE_MUSIC_FADEIN_MS = 1300
    _GAME_MUSIC_FADEIN_MS = 700
    _LOW_HEALTH_FADEIN_MS = 1000

    def __init__(self) -> None:
        """
        Initialize the sound system, discover music files, and build the synthesized SFX bank.
        This tries to initialize the mixer; if that fails, the manager is disabled.
        It also locates music assets in the sounds directory and pre-computes tone-based effects.
        """
        self._enabled = False
        self._sounds: dict[str, list[pygame.mixer.Sound]] = {}
        self._title_music_path: Path | None = None
        self._game_music_path: Path | None = None
        self._low_health_music_path: Path | None = None
        self._current_music_track: str | None = None
        self._cooldowns_ms = {
            "shoot": 25,
            "enemy_destroyed": 30,
            "core_hit": 80,
            "wave_start": 500,
            "game_over": 1000,
            "menu_start": 150,
            "boom": 700,
        }
        self._last_played_ms: dict[str, int] = {}

        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
        except pygame.error:
            return

        self._enabled = pygame.mixer.get_init() is not None
        if not self._enabled:
            return

        self._title_music_path = self._find_title_music_file()
        self._game_music_path = self._find_game_music_file()
        self._low_health_music_path = self._find_low_health_music_file()
        self._build_sfx_bank()

    def _find_sound_dir(self) -> Path:
        """
        Return the base directory where sound assets are expected to be located.
        The path is resolved relative to the project root as 'assets/sounds'.
        """
        return Path(__file__).resolve().parents[2] / "assets" / "sounds"

    def _find_music_file(self, exact_filename: str, hints: tuple[str, ...]) -> Path | None:
        """
        Find a music file by exact name or by matching filename hints.
        First checks for the provided exact filename, then searches all '.mp3' files and
        returns the first whose stem contains any of the given hint strings (case-insensitive),
        or None if no suitable file is found.
        
        Args:
            exact_filename: The exact filename to look for.
            hints: A tuple of hint strings to search for in filenames.

        """
        base_dir = self._find_sound_dir()
        if not base_dir.exists():
            return None

        exact_path = base_dir / exact_filename
        if exact_path.exists():
            return exact_path

        candidates = sorted(base_dir.glob("*.mp3"))
        if not candidates:
            return None

        preferred = [
            p for p in candidates
            if any(hint in p.stem.lower() for hint in hints)
        ]
        return preferred[0] if preferred else None

    def _find_title_music_file(self) -> Path | None:
        """
        Locate the title screen music file if available.
        Uses the predefined filename and hint set for title music to select an asset.
        """
        return self._find_music_file(self._TITLE_MUSIC_FILENAME, self._TITLE_MUSIC_HINTS)

    def _find_game_music_file(self) -> Path | None:
        """
        Locate the in-game music file if available.
        Uses the predefined filename and hint set for main game music to select an asset.
        """
        return self._find_music_file(self._GAME_MUSIC_FILENAME, self._GAME_MUSIC_HINTS)

    def _find_low_health_music_file(self) -> Path | None:
        """
        Locate the low-health music file if available.
        Uses the predefined filename and hint set for low-health or warning music to select an asset.
        """
        return self._find_music_file(self._LOW_HEALTH_MUSIC_FILENAME, self._LOW_HEALTH_MUSIC_HINTS)

    def _find_game_over_sound_file(self) -> Path | None:
        """
        Locate a game-over sound effect file if available.
        Prefers a specific game-over filename, but falls back to scanning common audio formats
        and picking a file whose stem matches any game-over hint; returns None if no match is found.
        """
        base_dir = self._find_sound_dir()
        if not base_dir.exists():
            return None

        exact_path = base_dir / self._GAME_OVER_SOUND_FILENAME
        if exact_path.exists():
            return exact_path

        candidates = sorted(
            [*base_dir.glob("*.mp3"), *base_dir.glob("*.wav"), *base_dir.glob("*.ogg")]
        )
        if not candidates:
            return None

        preferred = [
            p for p in candidates
            if any(hint in p.stem.lower() for hint in self._GAME_OVER_SOUND_HINTS)
        ]
        return preferred[0] if preferred else None

    def _find_boom_sound_file(self) -> Path | None:
        """
        Locate a 'boom' style explosion or alarm sound file if available.
        Prefers a specific boom filename, but falls back to scanning common audio formats
        and picking a file whose stem matches any boom hint; returns None if no match is found.
        """
        base_dir = self._find_sound_dir()
        if not base_dir.exists():
            return None

        exact_path = base_dir / self._BOOM_SOUND_FILENAME
        if exact_path.exists():
            return exact_path

        candidates = sorted(
            [*base_dir.glob("*.mp3"), *base_dir.glob("*.wav"), *base_dir.glob("*.ogg")]
        )
        if not candidates:
            return None

        preferred = [
            p for p in candidates
            if any(hint in p.stem.lower() for hint in self._BOOM_SOUND_HINTS)
        ]
        return preferred[0] if preferred else None

    def _play_music_track(self, track_name: str, track_path: Path, volume: float, fade_in_ms: int = 0) -> None:
        """
        Start playback of a looping music track if it is not already playing.
        Loads the given file path into the music mixer channel, applies the given volume,
        and plays it on an infinite loop with an optional fade-in time in milliseconds.
        
        Args:
            track_name: A unique name for this track (e.g. "title", "game").
            track_path: The Path to the music file.
            volume: Volume level as a float between 0.0 and 1.0.
            fade_in_ms: Optional fade-in duration in milliseconds; 0 for no fade.
        """
        if self._current_music_track == track_name and pygame.mixer.music.get_busy():
            return

        try:
            pygame.mixer.music.load(str(track_path))
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1, 0.0, max(0, fade_in_ms))
            self._current_music_track = track_name
        except pygame.error:
            self._current_music_track = None

    def _build_tone(self, frequency: float, duration_s: float, volume: float = 0.35) -> pygame.mixer.Sound:
        """
        Synthesize a short sine-wave tone as a Sound object.
        Generates PCM samples at the current mixer sample rate using a sine wave at the
        given frequency and duration, applies a simple attack/release envelope to reduce clicks,
        and returns a pygame Sound with the requested volume.
        
        Args:
            frequency: The frequency of the sine wave in Hz.
            duration_s: The duration of the tone in seconds.
            volume: The volume factor (0.0-1.0) for the tone, default 0.35.
        """
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            raise RuntimeError("Mixer is not initialized")

        sample_rate, _sample_size, channels = mixer_info
        sample_count = max(1, int(sample_rate * duration_s))

        samples = array("h")
        for i in range(sample_count):
            t = i / sample_rate

            # Fast attack/release envelope to avoid audible clicks.
            attack = min(1.0, i / max(1, int(sample_count * 0.08)))
            release = min(1.0, (sample_count - i) / max(1, int(sample_count * 0.2)))
            envelope = min(attack, release)

            wave = math.sin(2.0 * math.pi * frequency * t)
            value = int(32767 * volume * envelope * wave)

            if channels == 2:
                samples.append(value)
                samples.append(value)
            else:
                samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _build_sfx_bank(self) -> None:
        """
        Construct the library of named sound effects from synthesized tones and optional assets.
        Creates a small set of tonal effects for events (shooting, destruction, UI, etc.),
        performs basic per-event volume balancing, and replaces synthesized 'game_over' and 'boom'
        sounds with real audio files when those assets are present.
        """
        self._sounds = {
            "shoot": [
                self._build_tone(940.0, 0.04, 0.20),
                self._build_tone(1020.0, 0.03, 0.18),
            ],
            "enemy_destroyed": [
                self._build_tone(420.0, 0.06, 0.30),
                self._build_tone(500.0, 0.05, 0.28),
            ],
            "core_hit": [
                self._build_tone(170.0, 0.13, 0.34),
            ],
            "wave_start": [
                self._build_tone(520.0, 0.08, 0.32),
            ],
            "game_over": [
                self._build_tone(120.0, 0.34, 0.35),
            ],
            "menu_start": [
                self._build_tone(680.0, 0.06, 0.26),
            ],
            "boom": [
                self._build_tone(110.0, 0.25, 0.40),
            ],
        }

        # Slight per-event gain balancing after synthesis.
        self._set_volume("shoot", 0.38)
        self._set_volume("enemy_destroyed", 0.45)
        self._set_volume("core_hit", 0.55)
        self._set_volume("wave_start", 0.65)
        self._set_volume("game_over", 0.75)
        self._set_volume("menu_start", 0.55)
        self._set_volume("boom", 0.95)

        # Prefer a real game-over sound asset when available.
        game_over_file = self._find_game_over_sound_file()
        if game_over_file is not None:
            try:
                loaded = pygame.mixer.Sound(str(game_over_file))
                loaded.set_volume(0.9)
                self._sounds["game_over"] = [loaded]
            except pygame.error:
                pass

        boom_file = self._find_boom_sound_file()
        if boom_file is not None:
            try:
                loaded = pygame.mixer.Sound(str(boom_file))
                loaded.set_volume(1.0)
                self._sounds["boom"] = [loaded]
            except pygame.error:
                pass

    def _set_volume(self, name: str, volume: float) -> None:
        """
        Set the playback volume for all sound variants registered under a given name.
        If the name is not present in the sound bank, this method has no effect.

        Args:
            name: The event name under which sounds are registered (e.g. "shoot").
            volume: The volume level as a float between 0.0 and 1.0.
        """
        for sound in self._sounds.get(name, []):
            sound.set_volume(volume)

    def play(self, name: str) -> None:
        """
        Play a named sound effect if enabled and not on cooldown.
        Randomly selects one of the available variants for the given name, checks a
        per-event cooldown based on the last playback timestamp, and triggers the sound
        if the cooldown has elapsed.

        Args:
            name: The name of the sound event (e.g. "shoot", "enemy_destroyed").
        """
        if not self._enabled:
            return

        options = self._sounds.get(name)
        if not options:
            return

        now = pygame.time.get_ticks()
        cooldown = self._cooldowns_ms.get(name, 0)
        previous = self._last_played_ms.get(name, -10_000)
        if now - previous < cooldown:
            return

        self._last_played_ms[name] = now
        random.choice(options).play()

    def play_title_music(self, fade_in_ms: int | None = None) -> None:
        """
        Start or switch to looping title-screen music with an optional fade-in.
        If a title track is available and sound is enabled, plays it on the music channel
        with either the default fade-in duration or the provided override.

        Args:
            fade_in_ms: Optional fade‑in duration in milliseconds; uses default if None.
        """
        if not self._enabled or self._title_music_path is None:
            return
        fade = self._TITLE_MUSIC_FADEIN_MS if fade_in_ms is None else fade_in_ms
        self._play_music_track("title", self._title_music_path, 0.45, fade)

    def play_game_music(self, fade_in_ms: int | None = None) -> None:
        """
        Start or switch to looping in-game music with an optional fade-in.
        If a game track is available and sound is enabled, plays it on the music channel
        with either the default fade-in duration or the provided override.

        Args:
            fade_in_ms: Optional fade‑in duration in milliseconds; uses default if None.
        """
        if not self._enabled or self._game_music_path is None:
            return
        fade = self._GAME_MUSIC_FADEIN_MS if fade_in_ms is None else fade_in_ms
        self._play_music_track("game", self._game_music_path, 0.40, fade)

    def play_low_health_music(self, fade_in_ms: int | None = None) -> None:
        """
        Start or switch to looping low-health music with an optional fade-in.
        If a low-health track is available and sound is enabled, plays it on the music channel
        with either the default fade-in duration or the provided override.

        Args:
            fade_in_ms: Optional fade‑in duration in milliseconds; uses default if None.
        """
        if not self._enabled or self._low_health_music_path is None:
            return
        fade = self._LOW_HEALTH_FADEIN_MS if fade_in_ms is None else fade_in_ms
        self._play_music_track("low_health", self._low_health_music_path, 0.42, fade)

    def stop_music(self, fadeout_ms: int | None = None) -> None:
        """
        Stop any currently playing music with an optional fade-out.
        Uses the default fade-out time when no value is provided, then clears the
        internal record of the currently active music track.

        Args:
            fadeout_ms: Optional fade‑out duration in milliseconds; uses default if None.
        """
        if not self._enabled:
            return

        fade = self._TITLE_MUSIC_FADEOUT_MS if fadeout_ms is None else max(0, fadeout_ms)
        pygame.mixer.music.fadeout(fade)
        self._current_music_track = None

    def stop_title_music(self) -> None:
        """
        Convenience alias to stop any current music playback.
        This is intended for stopping title music but simply delegates to stop_music.
        """
        self.stop_music()

    @property
    def enabled(self) -> bool:
        """
        Whether the sound manager is currently active and able to play audio.
        Returns True when the mixer was successfully initialized, False otherwise.
        """
        return self._enabled
