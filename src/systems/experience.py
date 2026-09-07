"""Regras de progressão independentes da entidade Player."""


def apply_experience(player, amount, xp_growth_per_level):
    """Aplica XP e retorna quantos níveis foram conquistados."""
    player.xp += amount
    levels_gained = 0
    while player.xp >= player.xp_para_proximo_nivel:
        player.xp -= player.xp_para_proximo_nivel
        player.nivel += 1
        player.pontos_habilidade += 1
        player.xp_para_proximo_nivel += xp_growth_per_level
        player.hp = player.hp_max
        levels_gained += 1
    return levels_gained
