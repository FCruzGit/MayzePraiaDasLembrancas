import os
import pygame

from src.config import ASSETS_DIR, PLAYER
from src.player.combat import attack_area
from src.player.movement import move_with_collision
from src.systems.experience import apply_experience


TAMANHO_PLAYER = PLAYER["sprite_size"]
VELOCIDADE_ANDANDO = PLAYER["walk_speed"]
VELOCIDADE_CORRENDO = PLAYER["run_speed"]


def carregar_imagem(caminho, tamanho=None):
    imagem = pygame.image.load(caminho).convert_alpha()

    if tamanho:
        imagem = pygame.transform.scale(imagem, tamanho)

    return imagem


def carregar_sprite_sheet_horizontal(caminho, quantidade_frames, tamanho_frame=None):
    sprite_sheet = pygame.image.load(caminho).convert_alpha()

    largura_total = sprite_sheet.get_width()
    altura_total = sprite_sheet.get_height()

    largura_frame = largura_total // quantidade_frames
    altura_frame = altura_total

    frames = []

    for i in range(quantidade_frames):
        area_frame = pygame.Rect(
            i * largura_frame,
            0,
            largura_frame,
            altura_frame
        )

        frame = sprite_sheet.subsurface(area_frame).copy()

        if tamanho_frame:
            frame = pygame.transform.scale(frame, tamanho_frame)

        frames.append(frame)

    return frames


def inverter_frames_horizontalmente(frames):
    frames_invertidos = []

    for frame in frames:
        frame_invertido = pygame.transform.flip(frame, True, False)
        frames_invertidos.append(frame_invertido)

    return frames_invertidos


class AssetsMayze:
    def __init__(self):
        pasta_mayze = str(ASSETS_DIR / "mayze")

        self.idle_right = carregar_imagem(
            os.path.join(pasta_mayze, "idle_right.png"),
            TAMANHO_PLAYER
        )
        self.idle_left = pygame.transform.flip(self.idle_right, True, False)

        self.idle_front = carregar_imagem(
            os.path.join(pasta_mayze, "idle_front.png"),
            TAMANHO_PLAYER
        )
        self.idle_back = carregar_imagem(
            os.path.join(pasta_mayze, "idle_back.png"),
            TAMANHO_PLAYER
        )
        self.idle_looking_back = carregar_imagem(
            os.path.join(pasta_mayze, "idle_looking_back.png"),
            TAMANHO_PLAYER
        )
        self.idle_laying = carregar_imagem(
            os.path.join(pasta_mayze, "laying.png"),
            TAMANHO_PLAYER
        )

        self.walk_right = carregar_sprite_sheet_horizontal(
            os.path.join(pasta_mayze, "walk.png"),
            quantidade_frames=4,
            tamanho_frame=TAMANHO_PLAYER
        )
        self.walk_left = inverter_frames_horizontalmente(self.walk_right)

        self.run_right = carregar_sprite_sheet_horizontal(
            os.path.join(pasta_mayze, "run.png"),
            quantidade_frames=4,
            tamanho_frame=TAMANHO_PLAYER
        )
        self.run_left = inverter_frames_horizontalmente(self.run_right)

        self.attack_right = carregar_imagem(
            os.path.join(pasta_mayze, "attack.png"),
            TAMANHO_PLAYER
        )
        self.attack_left = pygame.transform.flip(self.attack_right, True, False)

        self.bark_right = carregar_imagem(
            os.path.join(pasta_mayze, "idle_growing.png"),
            TAMANHO_PLAYER
        )
        self.bark_left = pygame.transform.flip(self.bark_right, True, False)

        self.pickup_right = carregar_imagem(
            os.path.join(pasta_mayze, "idle_pickup_item.png"),
            TAMANHO_PLAYER
        )
        self.pickup_left = pygame.transform.flip(self.pickup_right, True, False)

        self.face_looking = carregar_imagem(
            os.path.join(pasta_mayze, "face_looking.png"),
            (150, 150)
        )
        self.face_talking = carregar_imagem(
            os.path.join(pasta_mayze, "face_talking.png"),
            (150, 150)
        )


class Player:
    def __init__(self, x, y, assets):
        self.assets = assets

        self.rect = pygame.Rect(x, y, TAMANHO_PLAYER[0], TAMANHO_PLAYER[1])
        self.hitbox = pygame.Rect(x + 30, y + 55, 60, 28)

        self.direcao = "front"

        self.nivel = 1
        self.xp = 0
        self.xp_para_proximo_nivel = PLAYER["initial_xp_to_level"]

        self.pontos_habilidade = 0
        self.bonus_dano = 0
        self.bonus_velocidade = 0
        self.bonus_cura = 0

        self.hp_max = PLAYER["max_hp"]
        self.hp = self.hp_max

        self.invulneravel = False
        self.tempo_invulneravel = 0
        self.duracao_invulneravel = PLAYER["invulnerability_seconds"]

        self.andando = False
        self.correndo = False
        self.atacando = False
        self.latindo = False
        self.pegando_item = False

        self.frame_atual = 0
        self.tempo_animacao = 0

        self.velocidade_animacao_walk = PLAYER["walk_animation_seconds"]
        self.velocidade_animacao_run = PLAYER["run_animation_seconds"]

        self.tempo_acao = 0
        self.duracao_ataque = PLAYER["attack_seconds"]
        self.duracao_latido = PLAYER["bark_seconds"]
        self.duracao_pickup = PLAYER["pickup_seconds"]

        self.tempo_parado = 0

    @property
    def profundidade(self):
        return self.hitbox.bottom

    def esta_vivo(self):
        return self.hp > 0

    def receber_dano(self, quantidade):
        if self.invulneravel or not self.esta_vivo():
            return

        self.hp -= quantidade
        self.hp = max(0, self.hp)

        self.invulneravel = True
        self.tempo_invulneravel = 0

    def ganhar_xp(self, quantidade):
        apply_experience(self, quantidade, PLAYER["xp_growth_per_level"])

    def curar(self, quantidade):
        quantidade_total = quantidade + self.bonus_cura
        self.hp += quantidade_total
        self.hp = min(self.hp, self.hp_max)

    def dano_ataque(self):
        return 1 + self.bonus_dano

    def gastar_ponto_habilidade(self, habilidade):
        if self.pontos_habilidade <= 0:
            return False

        if habilidade == "vida":
            self.hp_max += PLAYER["skill_bonuses"]["health"]
            self.hp = self.hp_max

        elif habilidade == "dano":
            self.bonus_dano += PLAYER["skill_bonuses"]["damage"]

        elif habilidade == "velocidade":
            self.bonus_velocidade += PLAYER["skill_bonuses"]["speed"]

        elif habilidade == "cura":
            self.bonus_cura += PLAYER["skill_bonuses"]["healing"]

        else:
            return False

        self.pontos_habilidade -= 1
        return True

    def renascer(self, x, y):
        self.hp = self.hp_max
        self.invulneravel = False
        self.tempo_invulneravel = 0

        self.hitbox.x = x + 30
        self.hitbox.y = y + 55
        self.atualizar_rect_pela_hitbox()

        self.andando = False
        self.correndo = False
        self.atacando = False
        self.latindo = False
        self.pegando_item = False
        self.tempo_acao = 0
        self.tempo_parado = 0
        self.direcao = "front"

    def area_de_ataque(self):
        largura, altura = PLAYER["attack_area"]
        return attack_area(self.hitbox, self.direcao, largura, altura)

    def atualizar_rect_pela_hitbox(self):
        self.rect.x = self.hitbox.x - 30
        self.rect.y = self.hitbox.y - 55

    def atualizar(self, dt, objetos_solidos, dialogo_aberto, inventario_aberto):
        if self.invulneravel:
            self.tempo_invulneravel += dt

            if self.tempo_invulneravel >= self.duracao_invulneravel:
                self.invulneravel = False
                self.tempo_invulneravel = 0

        if dialogo_aberto or inventario_aberto or not self.esta_vivo():
            self.andando = False
            self.correndo = False
            self.atualizar_acao_temporizada(dt)
            return

        teclas = pygame.key.get_pressed()

        self.atualizar_acao_temporizada(dt)

        direcao_x = 0
        direcao_y = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direcao_x -= 1
            self.direcao = "left"

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direcao_x += 1
            self.direcao = "right"

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            direcao_y -= 1
            self.direcao = "back"

        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            direcao_y += 1
            self.direcao = "front"

        self.andando = direcao_x != 0 or direcao_y != 0
        self.correndo = self.andando and (
            teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]
        )

        if self.andando:
            self.tempo_parado = 0
        elif not self.atacando and not self.latindo and not self.pegando_item:
            self.tempo_parado += dt

        if direcao_x != 0 and direcao_y != 0:
            direcao_x *= 0.7071
            direcao_y *= 0.7071

        velocidade_base = VELOCIDADE_CORRENDO if self.correndo else VELOCIDADE_ANDANDO
        velocidade_atual = velocidade_base + self.bonus_velocidade

        movimento_x = direcao_x * velocidade_atual * dt
        movimento_y = direcao_y * velocidade_atual * dt

        self.mover_com_colisao(movimento_x, movimento_y, objetos_solidos)
        self.atualizar_animacao_movimento(dt)

    def iniciar_ataque(self):
        if not self.atacando and not self.latindo and not self.pegando_item:
            self.atacando = True
            self.latindo = False
            self.pegando_item = False
            self.tempo_acao = 0
            self.tempo_parado = 0

    def iniciar_latido(self):
        if not self.latindo and not self.atacando and not self.pegando_item:
            self.latindo = True
            self.atacando = False
            self.pegando_item = False
            self.tempo_acao = 0
            self.tempo_parado = 0

    def iniciar_pickup(self):
        self.pegando_item = True
        self.atacando = False
        self.latindo = False
        self.tempo_acao = 0
        self.tempo_parado = 0

    def atualizar_acao_temporizada(self, dt):
        if self.atacando:
            self.tempo_acao += dt

            if self.tempo_acao >= self.duracao_ataque:
                self.atacando = False
                self.tempo_acao = 0

        if self.latindo:
            self.tempo_acao += dt

            if self.tempo_acao >= self.duracao_latido:
                self.latindo = False
                self.tempo_acao = 0

        if self.pegando_item:
            self.tempo_acao += dt

            if self.tempo_acao >= self.duracao_pickup:
                self.pegando_item = False
                self.tempo_acao = 0

    def mover_com_colisao(self, dx, dy, objetos_solidos):
        move_with_collision(self, dx, dy, objetos_solidos)

    def atualizar_animacao_movimento(self, dt):
        if self.correndo:
            velocidade_animacao = self.velocidade_animacao_run
            quantidade_frames = len(self.assets.run_right)
        elif self.andando:
            velocidade_animacao = self.velocidade_animacao_walk
            quantidade_frames = len(self.assets.walk_right)
        else:
            self.frame_atual = 0
            self.tempo_animacao = 0
            return

        self.tempo_animacao += dt

        if self.tempo_animacao >= velocidade_animacao:
            self.tempo_animacao = 0
            self.frame_atual += 1

            if self.frame_atual >= quantidade_frames:
                self.frame_atual = 0

    def pegar_imagem_atual(self):
        if self.pegando_item:
            if self.direcao == "left":
                return self.assets.pickup_left

            return self.assets.pickup_right

        if self.atacando:
            if self.direcao == "left":
                return self.assets.attack_left

            return self.assets.attack_right

        if self.latindo:
            if self.direcao == "left":
                return self.assets.bark_left

            return self.assets.bark_right

        if self.correndo:
            if self.direcao == "left":
                return self.assets.run_left[self.frame_atual]

            return self.assets.run_right[self.frame_atual]

        if self.andando:
            if self.direcao == "left":
                return self.assets.walk_left[self.frame_atual]

            return self.assets.walk_right[self.frame_atual]

        if self.tempo_parado >= 5:
            return self.assets.idle_laying

        if self.tempo_parado >= 2:
            return self.assets.idle_looking_back

        if self.direcao == "left":
            return self.assets.idle_left

        if self.direcao == "right":
            return self.assets.idle_right

        if self.direcao == "back":
            return self.assets.idle_back

        return self.assets.idle_front

    def desenhar(self, superficie, camera):
        imagem_atual = self.pegar_imagem_atual()
        rect_tela = camera.aplicar_rect(self.rect)

        sombra_rect = pygame.Rect(
            rect_tela.x + 30,
            rect_tela.y + 70,
            60,
            18
        )

        pygame.draw.ellipse(superficie, (0, 0, 0), sombra_rect)

        if self.invulneravel and int(self.tempo_invulneravel * 12) % 2 == 0:
            return

        superficie.blit(imagem_atual, rect_tela)
