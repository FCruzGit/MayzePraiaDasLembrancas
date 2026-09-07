"""Ponto de integração da hotbar.

A renderização permanece encapsulada em ``Inventario`` porque ela depende
diretamente do estado dos slots. Este módulo é o local para temas e atalhos
visuais quando a UI crescer.
"""


def draw(inventory, surface, width, height):
    inventory.desenhar_hotbar(surface, width, height)
