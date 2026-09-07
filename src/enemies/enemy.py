import pygame

from src.config import ENEMY


COR_SOMBRA = (0, 0, 0)
COR_INIMIGO = (150, 90, 65)
COR_INIMIGO_RAIVA = (190, 70, 55)
COR_DETALHE = (80, 45, 35)
COR_HP_FUNDO = (70, 25, 25)
COR_HP = (210, 60, 60)
COR_EXCLAMACAO = (255, 235, 70)


class Inimigo:
    def __init__(self, x, y, nome="Caranguejo", nivel=1, hp_max=3):
        self.nome = nome
        self.nivel = nivel
        self.hp_max = hp_max
        self.hp = hp_max

        self.rect = pygame.Rect(x, y, 70, 48)
        self.hitbox = pygame.Rect(x + 8, y + 24, 54, 20)

        self.spawn_x = x
        self.spawn_y = y
        self.spawn_hitbox_x = x + 8
        self.spawn_hitbox_y = y + 24

        self.spot_centro = self.hitbox.center

        self.pontos_ronda = [
            (self.spot_centro[0] - 120, self.spot_centro[1]),
            (self.spot_centro[0], self.spot_centro[1] - 85),
            (self.spot_centro[0] + 120, self.spot_centro[1]),
            (self.spot_centro[0], self.spot_centro[1] + 85),
        ]

        self.indice_ronda = 0
        self.velocidade_ronda = ENEMY["patrol_speed"]
        self.velocidade_raiva = ENEMY["chase_speed"]

        self.vivo = True
        self.agressivo = False
        self.raiva = False

        self.tempo_raiva = 0
        self.tempo_entre_ataques = 0
        self.cooldown_ataque = ENEMY["attack_cooldown_seconds"]

        self.dano = 1 + nivel // 2
        self.xp_recompensa = nivel + 1

        self.distancia_visao = ENEMY["view_distance"]
        self.distancia_desistir = ENEMY["give_up_distance"]

        self.tempo_respawn = 0
        self.tempo_para_respawnar = ENEMY["respawn_seconds"]

    @property
    def profundidade(self):
        return self.hitbox.bottom

    def atualizar(self, dt, player):
        if not self.vivo:
            self.tempo_respawn += dt

            if self.tempo_respawn >= self.tempo_para_respawnar:
                self.respawnar()

            return

        distancia_x = player.hitbox.centerx - self.hitbox.centerx
        distancia_y = player.hitbox.centery - self.hitbox.centery
        distancia_quadrada = distancia_x * distancia_x + distancia_y * distancia_y

        if distancia_quadrada <= self.distancia_visao * self.distancia_visao:
            self.raiva = True
            self.agressivo = True
            self.tempo_raiva = 0

        if self.raiva:
            self.atualizar_com_raiva(dt, player, distancia_quadrada)
        else:
            self.patrulhar(dt)

    def atualizar_com_raiva(self, dt, player, distancia_quadrada):
        self.tempo_raiva += dt
        self.tempo_entre_ataques += dt

        self.mover_em_direcao(
            player.hitbox.centerx,
            player.hitbox.centery,
            self.velocidade_raiva,
            dt
        )

        if distancia_quadrada <= ENEMY["attack_range"] ** 2:
            if self.tempo_entre_ataques >= self.cooldown_ataque:
                player.receber_dano(self.dano)
                self.tempo_entre_ataques = 0

        if distancia_quadrada >= self.distancia_desistir * self.distancia_desistir:
            self.raiva = False
            self.agressivo = False
            self.tempo_raiva = 0
            self.tempo_entre_ataques = 0

    def patrulhar(self, dt):
        destino_x, destino_y = self.pontos_ronda[self.indice_ronda]

        chegou = self.mover_em_direcao(
            destino_x,
            destino_y,
            self.velocidade_ronda,
            dt
        )

        if chegou:
            self.indice_ronda += 1

            if self.indice_ronda >= len(self.pontos_ronda):
                self.indice_ronda = 0

    def mover_em_direcao(self, destino_x, destino_y, velocidade, dt):
        distancia_x = destino_x - self.hitbox.centerx
        distancia_y = destino_y - self.hitbox.centery

        distancia = (distancia_x * distancia_x + distancia_y * distancia_y) ** 0.5

        if distancia < 8:
            return True

        if distancia == 0:
            return True

        movimento_x = distancia_x / distancia * velocidade * dt
        movimento_y = distancia_y / distancia * velocidade * dt

        self.hitbox.x += movimento_x
        self.hitbox.y += movimento_y

        self.rect.x = self.hitbox.x - 8
        self.rect.y = self.hitbox.y - 24

        return False

    def receber_dano(self, quantidade):
        if not self.vivo:
            return

        self.hp -= quantidade
        self.raiva = True
        self.agressivo = True
        self.tempo_raiva = 0

        if self.hp <= 0:
            self.hp = 0
            self.vivo = False
            self.raiva = False
            self.agressivo = False
            self.tempo_respawn = 0

    def respawnar(self):
        self.hp = self.hp_max
        self.vivo = True
        self.raiva = False
        self.agressivo = False
        self.tempo_raiva = 0
        self.tempo_entre_ataques = 0
        self.tempo_respawn = 0
        self.indice_ronda = 0

        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.hitbox.x = self.spawn_hitbox_x
        self.hitbox.y = self.spawn_hitbox_y

    def desenhar(self, superficie, camera):
        if not self.vivo:
            return

        rect_tela = camera.aplicar_rect(self.rect)

        sombra_rect = pygame.Rect(
            rect_tela.x + 7,
            rect_tela.y + rect_tela.height - 8,
            rect_tela.width - 14,
            14
        )
        pygame.draw.ellipse(superficie, COR_SOMBRA, sombra_rect)

        cor_corpo = COR_INIMIGO_RAIVA if self.raiva else COR_INIMIGO

        pygame.draw.ellipse(
            superficie,
            cor_corpo,
            (rect_tela.x, rect_tela.y + 10, rect_tela.width, rect_tela.height - 12)
        )

        pygame.draw.circle(superficie, COR_DETALHE, (rect_tela.x + 20, rect_tela.y + 24), 4)
        pygame.draw.circle(superficie, COR_DETALHE, (rect_tela.x + 48, rect_tela.y + 24), 4)

        pygame.draw.line(
            superficie,
            COR_DETALHE,
            (rect_tela.x + 12, rect_tela.y + 38),
            (rect_tela.x - 8, rect_tela.y + 48),
            4
        )
        pygame.draw.line(
            superficie,
            COR_DETALHE,
            (rect_tela.x + 58, rect_tela.y + 38),
            (rect_tela.x + 78, rect_tela.y + 48),
            4
        )

        pygame.draw.line(
            superficie,
            COR_DETALHE,
            (rect_tela.x + 20, rect_tela.y + 43),
            (rect_tela.x + 6, rect_tela.y + 58),
            3
        )
        pygame.draw.line(
            superficie,
            COR_DETALHE,
            (rect_tela.x + 50, rect_tela.y + 43),
            (rect_tela.x + 64, rect_tela.y + 58),
            3
        )

        self.desenhar_barra_hp(superficie, rect_tela)

        if self.raiva:
            self.desenhar_exclamacao(superficie, rect_tela)

    def desenhar_barra_hp(self, superficie, rect_tela):
        largura = 58
        altura = 7

        x = rect_tela.centerx - largura // 2
        y = rect_tela.y - 14

        porcentagem = self.hp / self.hp_max
        largura_hp = int(largura * porcentagem)

        pygame.draw.rect(superficie, COR_HP_FUNDO, (x, y, largura, altura), border_radius=3)
        pygame.draw.rect(superficie, COR_HP, (x, y, largura_hp, altura), border_radius=3)

    def desenhar_exclamacao(self, superficie, rect_tela):
        x = rect_tela.centerx
        y = rect_tela.y - 40

        pygame.draw.circle(superficie, COR_EXCLAMACAO, (x, y), 16)
        pygame.draw.line(superficie, (80, 45, 20), (x, y - 8), (x, y + 3), 4)
        pygame.draw.circle(superficie, (80, 45, 20), (x, y + 8), 2)
