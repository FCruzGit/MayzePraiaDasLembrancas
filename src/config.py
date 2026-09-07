"""Ajustes de jogo versionados.

Use este módulo para valores de balanceamento e apresentação. Variáveis de
ambiente são reservadas para segredos e diferenças de infraestrutura; não são
adequadas para regras de jogo que precisam ser reproduzíveis.
"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"

WINDOW_TITLE = "Mayze - A Praia das Lembranças"
FPS = 60

PLAYER = {
    "sprite_size": (120, 90),
    "walk_speed": 350,
    "run_speed": 620,
    "max_hp": 10,
    "invulnerability_seconds": 0.8,
    "attack_seconds": 0.35,
    "bark_seconds": 0.45,
    "pickup_seconds": 0.55,
    "walk_animation_seconds": 0.12,
    "run_animation_seconds": 0.08,
    "initial_xp_to_level": 5,
    "xp_growth_per_level": 3,
    "skill_bonuses": {"health": 3, "damage": 1, "speed": 35, "healing": 1},
    "attack_area": (85, 60),
}

ENEMY = {
    "patrol_speed": 90,
    "chase_speed": 215,
    "attack_cooldown_seconds": 0.85,
    "attack_range": 95,
    "view_distance": 430,
    "give_up_distance": 680,
    "respawn_seconds": 10,
}

BEACH_MAP = {
    "width": 2200,
    "height": 2600,
    "player_spawn": (980, 760),
    "enemy_area_spawn": (980, 520),
    "beach_return_spawn": (980, 2300),
}
