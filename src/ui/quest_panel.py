"""Modelo mínimo do painel de objetivos, sem acoplamento ao mapa."""


class QuestPanel:
    def __init__(self):
        self.objectives = []

    def add(self, text, completed=False):
        self.objectives.append({"text": text, "completed": completed})
