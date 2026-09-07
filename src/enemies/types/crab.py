"""Fábrica do inimigo caranguejo."""

from ..enemy import Inimigo


def create_crab(x, y, name="Caranguejo Bravo", level=1, max_hp=3):
    return Inimigo(x, y, name, nivel=level, hp_max=max_hp)
