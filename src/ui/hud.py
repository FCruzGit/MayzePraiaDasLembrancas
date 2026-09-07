"""Componentes do HUD durante a partida."""


def draw_inventory(inventory, surface, width, height):
    """Desenha o painel de inventário se ele estiver aberto."""
    inventory.desenhar_inventario_completo(surface, width, height)
