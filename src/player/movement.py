"""Movimentação e colisão da personagem, desacopladas da entrada e do desenho."""


def move_with_collision(player, dx, dy, solid_objects):
    """Move a hitbox por eixo e impede a passagem por objetos sólidos."""
    player.hitbox.x += dx
    for obj in solid_objects:
        if player.hitbox.colliderect(obj.hitbox):
            if dx > 0:
                player.hitbox.right = obj.hitbox.left
            elif dx < 0:
                player.hitbox.left = obj.hitbox.right

    player.hitbox.y += dy
    for obj in solid_objects:
        if player.hitbox.colliderect(obj.hitbox):
            if dy > 0:
                player.hitbox.bottom = obj.hitbox.top
            elif dy < 0:
                player.hitbox.top = obj.hitbox.bottom

    player.atualizar_rect_pela_hitbox()
