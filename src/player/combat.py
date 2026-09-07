"""Cálculos de combate da personagem."""

import pygame


def attack_area(hitbox, direction, width, height):
    """Retorna a área atingida pelo ataque para a direção atual."""
    if direction == "left":
        return pygame.Rect(hitbox.left - width, hitbox.centery - height // 2, width, height)
    if direction == "right":
        return pygame.Rect(hitbox.right, hitbox.centery - height // 2, width, height)
    if direction == "back":
        return pygame.Rect(hitbox.centerx - width // 2, hitbox.top - height, width, height)
    return pygame.Rect(hitbox.centerx - width // 2, hitbox.bottom, width, height)
