import math
import pygame

from inventario import Item
from inimigo import Inimigo


COR_CEU = (117, 190, 224)
COR_MAR = (40, 125, 190)
COR_ESPUMA = (225, 245, 250)
COR_AREIA = (222, 194, 135)
COR_AREIA_SOMBRA = (190, 160, 100)
COR_GRAMA = (75, 145, 85)
COR_GRAMA_ESCURO = (45, 105, 65)

COR_PEDRA = (110, 110, 115)
COR_PEDRA_SOMBRA = (75, 75, 80)
COR_TRONCO = (110, 70, 35)
COR_TRONCO_ESCURO = (75, 45, 25)
COR_ARBUSTO = (40, 120, 65)
COR_ARBUSTO_CLARO = (70, 160, 85)
COR_COQUEIRO_TRONCO = (125, 78, 35)
COR_COQUEIRO_FOLHA = (40, 125, 55)
COR_COQUEIRO_FOLHA_CLARA = (70, 170, 80)
COR_TERRA = (135, 95, 55)
COR_TERRA_ESCURO = (95, 65, 40)
COR_SOMBRA = (0, 0, 0)


class Camera:
    def __init__(self, largura_mundo, altura_mundo, largura_tela, altura_tela):
        self.offset_x = 0
        self.offset_y = 0

        self.largura_mundo = largura_mundo
        self.altura_mundo = altura_mundo

        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

    def atualizar(self, alvo_rect):
        self.offset_x = alvo_rect.centerx - self.largura_tela // 2
        self.offset_y = alvo_rect.centery - self.altura_tela // 2

        self.offset_x = max(0, min(self.offset_x, self.largura_mundo - self.largura_tela))
        self.offset_y = max(0, min(self.offset_y, self.altura_mundo - self.altura_tela))

    def aplicar_rect(self, rect):
        return pygame.Rect(
            rect.x - self.offset_x,
            rect.y - self.offset_y,
            rect.width,
            rect.height
        )

    def aplicar_ponto(self, x, y):
        return x - self.offset_x, y - self.offset_y


class ObjetoCenario:
    def __init__(self, tipo, x, y, largura, altura, solido=True):
        self.tipo = tipo
        self.rect = pygame.Rect(x, y, largura, altura)
        self.solido = solido

        self.hitbox = pygame.Rect(
            x + largura * 0.15,
            y + altura * 0.60,
            largura * 0.70,
            altura * 0.30
        )

        if self.tipo == "coqueiro":
            self.hitbox = pygame.Rect(
                x + largura * 0.36,
                y + altura * 0.72,
                largura * 0.28,
                altura * 0.20
            )

    @property
    def profundidade(self):
        return self.rect.bottom

    def desenhar(self, superficie, camera):
        rect_tela = camera.aplicar_rect(self.rect)

        if self.tipo == "pedra":
            pygame.draw.ellipse(
                superficie,
                COR_SOMBRA,
                (rect_tela.x + 10, rect_tela.y + rect_tela.height - 18, rect_tela.width - 20, 18)
            )
            pygame.draw.ellipse(
                superficie,
                COR_PEDRA_SOMBRA,
                (rect_tela.x + 8, rect_tela.y + 16, rect_tela.width - 16, rect_tela.height - 18)
            )
            pygame.draw.ellipse(
                superficie,
                COR_PEDRA,
                (rect_tela.x, rect_tela.y, rect_tela.width, rect_tela.height - 20)
            )

        elif self.tipo == "tronco":
            pygame.draw.ellipse(
                superficie,
                COR_SOMBRA,
                (rect_tela.x + 8, rect_tela.y + rect_tela.height - 14, rect_tela.width - 16, 16)
            )
            pygame.draw.rect(
                superficie,
                COR_TRONCO_ESCURO,
                (rect_tela.x, rect_tela.y + 20, rect_tela.width, rect_tela.height - 35),
                border_radius=15
            )
            pygame.draw.rect(
                superficie,
                COR_TRONCO,
                (rect_tela.x + 5, rect_tela.y + 10, rect_tela.width - 10, rect_tela.height - 35),
                border_radius=15
            )

        elif self.tipo == "arbusto":
            pygame.draw.ellipse(
                superficie,
                COR_SOMBRA,
                (rect_tela.x + 8, rect_tela.y + rect_tela.height - 12, rect_tela.width - 16, 16)
            )
            pygame.draw.circle(
                superficie,
                COR_ARBUSTO,
                (rect_tela.x + rect_tela.width // 3, rect_tela.y + rect_tela.height // 2),
                rect_tela.width // 3
            )
            pygame.draw.circle(
                superficie,
                COR_ARBUSTO_CLARO,
                (rect_tela.x + rect_tela.width // 2, rect_tela.y + rect_tela.height // 3),
                rect_tela.width // 4
            )
            pygame.draw.circle(
                superficie,
                COR_ARBUSTO,
                (rect_tela.x + rect_tela.width * 2 // 3, rect_tela.y + rect_tela.height // 2),
                rect_tela.width // 3
            )

        elif self.tipo == "coqueiro":
            base_x = rect_tela.centerx
            base_y = rect_tela.y + rect_tela.height - 12
            topo_x = rect_tela.centerx + 16
            topo_y = rect_tela.y + 48

            pygame.draw.ellipse(
                superficie,
                COR_SOMBRA,
                (rect_tela.x + 28, rect_tela.y + rect_tela.height - 22, rect_tela.width - 56, 20)
            )

            pygame.draw.line(
                superficie,
                COR_COQUEIRO_TRONCO,
                (base_x, base_y),
                (topo_x, topo_y),
                18
            )
            pygame.draw.line(
                superficie,
                COR_TRONCO_ESCURO,
                (base_x + 7, base_y),
                (topo_x + 7, topo_y),
                4
            )

            pygame.draw.ellipse(superficie, COR_COQUEIRO_FOLHA, (topo_x - 90, topo_y - 35, 100, 36))
            pygame.draw.ellipse(superficie, COR_COQUEIRO_FOLHA, (topo_x - 10, topo_y - 42, 115, 36))
            pygame.draw.ellipse(superficie, COR_COQUEIRO_FOLHA_CLARA, (topo_x - 58, topo_y - 80, 42, 95))
            pygame.draw.ellipse(superficie, COR_COQUEIRO_FOLHA, (topo_x + 10, topo_y - 82, 42, 100))

            pygame.draw.circle(superficie, (105, 65, 35), (topo_x - 6, topo_y + 6), 8)
            pygame.draw.circle(superficie, (105, 65, 35), (topo_x + 8, topo_y + 4), 7)


class ItemColetavel:
    def __init__(self, nome, x, y):
        self.nome = nome
        self.rect = pygame.Rect(x, y, 42, 42)
        self.coletado = False
        self.tempo = 0

    @property
    def profundidade(self):
        return self.rect.bottom

    def atualizar(self, dt):
        self.tempo += dt

    def desenhar(self, superficie, camera):
        if self.coletado:
            return

        rect_tela = camera.aplicar_rect(self.rect)

        brilho = 8 + int(math.sin(self.tempo * 6) * 4)
        centro = rect_tela.center

        pygame.draw.circle(superficie, (255, 245, 150), centro, 26 + brilho)
        pygame.draw.circle(superficie, (255, 220, 60), centro, 20)
        pygame.draw.circle(superficie, (180, 110, 40), centro, 14)
        pygame.draw.circle(superficie, (255, 245, 190), (centro[0] - 5, centro[1] - 5), 5)

    def tentar_coletar(self, player, inventario):
        if self.coletado:
            return False

        if player.hitbox.colliderect(self.rect):
            if self.nome == "Biscoito":
                item = Item(self.nome, (255, 210, 65), consumivel=True, cura=4)
            else:
                item = Item(self.nome, (255, 210, 65))

            if inventario.adicionar_item(item):
                self.coletado = True
                player.iniciar_pickup()
                return True

        return False


class MapaPraia:
    def __init__(self):
        self.largura = 2200
        self.altura = 2600

        self.chunk_atual = "praia"

        self.portal_para_inimigos = pygame.Rect(850, 2480, 500, 120)
        self.portal_para_praia = pygame.Rect(850, 430, 500, 90)

        self.objetos_cenario = [
            ObjetoCenario("pedra", 530, 740, 90, 65),
            ObjetoCenario("pedra", 870, 640, 120, 80),
            ObjetoCenario("pedra", 1360, 800, 100, 70),
            ObjetoCenario("tronco", 760, 980, 190, 80),
            ObjetoCenario("tronco", 1450, 1080, 220, 85),
            ObjetoCenario("arbusto", 360, 1050, 120, 90),
            ObjetoCenario("arbusto", 1750, 820, 140, 100),
            ObjetoCenario("arbusto", 1580, 1230, 130, 95),

            ObjetoCenario("coqueiro", 250, 1220, 180, 240),
            ObjetoCenario("coqueiro", 620, 1350, 180, 240),
            ObjetoCenario("coqueiro", 1720, 1300, 180, 240),
            ObjetoCenario("coqueiro", 1880, 1660, 180, 240),
            ObjetoCenario("coqueiro", 430, 1840, 180, 240),
            ObjetoCenario("coqueiro", 1180, 2020, 180, 240),

            ObjetoCenario("pedra", 780, 1760, 120, 80),
            ObjetoCenario("arbusto", 950, 1930, 140, 100),
            ObjetoCenario("tronco", 1320, 2200, 230, 85),
        ]

        self.objetos_cenario_inimigos = [
            ObjetoCenario("pedra", 360, 610, 120, 80),
            ObjetoCenario("pedra", 1640, 650, 130, 90),
            ObjetoCenario("tronco", 650, 980, 210, 80),
            ObjetoCenario("arbusto", 1180, 760, 150, 105),
            ObjetoCenario("arbusto", 430, 1540, 150, 105),
            ObjetoCenario("coqueiro", 1580, 1250, 180, 240),
            ObjetoCenario("coqueiro", 920, 1780, 180, 240),
            ObjetoCenario("pedra", 1340, 2040, 130, 90),
        ]

        self.itens = [
            ItemColetavel("Biscoito", 1180, 850)
        ]

        self.itens_inimigos = [
            ItemColetavel("Concha Dourada", 1040, 1180)
        ]

        self.inimigos = [
            Inimigo(620, 820, "Caranguejo Bravo", nivel=1, hp_max=3),
            Inimigo(1250, 980, "Caranguejo Bravo", nivel=1, hp_max=3),
            Inimigo(1540, 1660, "Caranguejo Bravo", nivel=2, hp_max=4),
            Inimigo(780, 1960, "Caranguejo Ancião", nivel=2, hp_max=5),
        ]

    def trocar_para_chunk(self, nome_chunk, player):
        self.chunk_atual = nome_chunk

        if nome_chunk == "inimigos":
            player.renascer(980, 520)
        else:
            player.renascer(980, 2300)

    def objetos_solidos(self):
        if self.chunk_atual == "inimigos":
            return [objeto for objeto in self.objetos_cenario_inimigos if objeto.solido]

        return [objeto for objeto in self.objetos_cenario if objeto.solido]

    def atualizar(self, dt, player, inventario):
        if self.chunk_atual == "praia" and player.hitbox.colliderect(self.portal_para_inimigos):
            self.trocar_para_chunk("inimigos", player)

        elif self.chunk_atual == "inimigos" and player.hitbox.colliderect(self.portal_para_praia):
            self.trocar_para_chunk("praia", player)

        if self.chunk_atual == "inimigos":
            itens_ativos = self.itens_inimigos
        else:
            itens_ativos = self.itens

        for item in itens_ativos:
            item.atualizar(dt)
            item.tentar_coletar(player, inventario)

        if self.chunk_atual == "inimigos":
            for inimigo in self.inimigos:
                inimigo.atualizar(dt, player)

    def processar_ataque_player(self, player):
        if not player.atacando:
            return

        if self.chunk_atual != "inimigos":
            return

        area_ataque = player.area_de_ataque()

        for inimigo in self.inimigos:
            if inimigo.vivo and area_ataque.colliderect(inimigo.hitbox):
                inimigo.receber_dano(player.dano_ataque())

                if not inimigo.vivo:
                    player.ganhar_xp(inimigo.xp_recompensa)

    def limitar_player_no_mapa(self, player):
        player.hitbox.left = max(0, player.hitbox.left)
        player.hitbox.right = min(self.largura, player.hitbox.right)
        player.hitbox.top = max(430, player.hitbox.top)
        player.hitbox.bottom = min(self.altura, player.hitbox.bottom)

        player.atualizar_rect_pela_hitbox()

    def desenhar_base(self, superficie, camera):
        if self.chunk_atual == "inimigos":
            self.desenhar_base_inimigos(superficie, camera)
            return

        tela_rect = pygame.Rect(0, 0, camera.largura_tela, camera.altura_tela)

        pygame.draw.rect(superficie, COR_CEU, tela_rect)

        mar_mundo = pygame.Rect(0, 0, self.largura, 430)
        areia_mundo = pygame.Rect(0, 360, self.largura, 900)
        grama_mundo = pygame.Rect(0, 1180, self.largura, 560)
        terra_mundo = pygame.Rect(0, 1680, self.largura, self.altura - 1680)

        pygame.draw.rect(superficie, COR_MAR, camera.aplicar_rect(mar_mundo))
        pygame.draw.rect(superficie, COR_AREIA, camera.aplicar_rect(areia_mundo))
        pygame.draw.rect(superficie, COR_GRAMA, camera.aplicar_rect(grama_mundo))
        pygame.draw.rect(superficie, COR_TERRA, camera.aplicar_rect(terra_mundo))

        for i in range(8):
            y_mundo = 320 + i * 35
            x_tela, y_tela = camera.aplicar_ponto(0, y_mundo)

            pygame.draw.arc(
                superficie,
                COR_ESPUMA,
                (x_tela - 120, y_tela, self.largura + 240, 45),
                0,
                3.14,
                4
            )

        for i in range(14):
            y_mundo = 470 + i * 48
            x_tela, y_tela = camera.aplicar_ponto(0, y_mundo)

            pygame.draw.line(
                superficie,
                COR_AREIA_SOMBRA,
                (x_tela, y_tela),
                (x_tela + self.largura, y_tela + 20),
                2
            )

        for i in range(28):
            x_mundo = 60 + i * 115
            y_mundo = 1210 + (i % 6) * 70
            x_tela, y_tela = camera.aplicar_ponto(x_mundo, y_mundo)

            pygame.draw.line(superficie, COR_GRAMA_ESCURO, (x_tela, y_tela + 25), (x_tela + 10, y_tela), 3)
            pygame.draw.line(superficie, COR_GRAMA_ESCURO, (x_tela + 12, y_tela + 28), (x_tela + 20, y_tela + 2), 3)
            pygame.draw.line(superficie, COR_GRAMA_ESCURO, (x_tela + 22, y_tela + 25), (x_tela + 30, y_tela + 5), 3)

        for i in range(18):
            y_mundo = 1740 + i * 45
            x_tela, y_tela = camera.aplicar_ponto(0, y_mundo)

            pygame.draw.line(
                superficie,
                COR_TERRA_ESCURO,
                (x_tela, y_tela),
                (x_tela + self.largura, y_tela + 10),
                1
            )

        x_tela, y_tela = camera.aplicar_ponto(
            self.portal_para_inimigos.x,
            self.portal_para_inimigos.y
        )

        pygame.draw.rect(
            superficie,
            (90, 70, 45),
            (x_tela, y_tela, self.portal_para_inimigos.width, 18),
            border_radius=8
        )

    def desenhar_base_inimigos(self, superficie, camera):
        tela_rect = pygame.Rect(0, 0, camera.largura_tela, camera.altura_tela)

        pygame.draw.rect(superficie, (38, 82, 72), tela_rect)

        areia_mundo = pygame.Rect(0, 0, self.largura, self.altura)
        mato_mundo = pygame.Rect(0, 430, self.largura, self.altura - 430)

        pygame.draw.rect(superficie, (188, 155, 95), camera.aplicar_rect(areia_mundo))
        pygame.draw.rect(superficie, (48, 110, 72), camera.aplicar_rect(mato_mundo))

        for i in range(36):
            x_mundo = 55 + i * 70
            y_mundo = 520 + (i % 10) * 190
            x_tela, y_tela = camera.aplicar_ponto(x_mundo, y_mundo)

            pygame.draw.line(superficie, COR_GRAMA_ESCURO, (x_tela, y_tela + 28), (x_tela + 12, y_tela), 4)
            pygame.draw.line(superficie, COR_GRAMA_ESCURO, (x_tela + 16, y_tela + 30), (x_tela + 28, y_tela + 3), 4)
            pygame.draw.line(superficie, COR_GRAMA_ESCURO, (x_tela + 32, y_tela + 25), (x_tela + 42, y_tela + 6), 3)

        for i in range(22):
            y_mundo = 620 + i * 85
            x_tela, y_tela = camera.aplicar_ponto(0, y_mundo)

            pygame.draw.line(
                superficie,
                (34, 88, 58),
                (x_tela, y_tela),
                (x_tela + self.largura, y_tela + 16),
                2
            )

        x_tela, y_tela = camera.aplicar_ponto(
            self.portal_para_praia.x,
            self.portal_para_praia.y
        )

        pygame.draw.rect(
            superficie,
            (230, 205, 140),
            (x_tela, y_tela, self.portal_para_praia.width, 18),
            border_radius=8
        )

    def entidades_para_desenhar(self, player):
        entidades = []

        if self.chunk_atual == "inimigos":
            entidades.extend(self.objetos_cenario_inimigos)

            for item in self.itens_inimigos:
                if not item.coletado:
                    entidades.append(item)

            for inimigo in self.inimigos:
                if inimigo.vivo:
                    entidades.append(inimigo)
        else:
            entidades.extend(self.objetos_cenario)

            for item in self.itens:
                if not item.coletado:
                    entidades.append(item)

        entidades.append(player)
        entidades.sort(key=lambda entidade: entidade.profundidade)

        return entidades