import math

import pygame

from src.config import BEACH_MAP, FPS, WINDOW_TITLE
from src.player.inventory import Inventario
from src.maps.beach_map import Camera, MapaPraia
from src.player.player import AssetsMayze, Player
from src.ui.hotbar import draw as desenhar_hotbar
from src.ui.hud import draw_inventory


pygame.init()

info_tela = pygame.display.Info()
LARGURA, ALTURA = info_tela.current_w, info_tela.current_h

tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption(WINDOW_TITLE)

relogio = pygame.time.Clock()

COR_TEXTO_CLARO = (255, 255, 255)
COR_TEXTO = (45, 35, 30)
COR_CAIXA_DIALOGO = (250, 232, 190)
COR_BORDA_DIALOGO = (105, 72, 45)

COR_HP_FUNDO = (75, 28, 28)
COR_HP = (220, 65, 75)
COR_HP_BORDA = (70, 40, 35)
COR_XP_FUNDO = (28, 45, 75)
COR_XP = (80, 155, 255)
COR_RETRATO_FUNDO = (245, 215, 160)

COR_MENU_CEU = (135, 200, 230)
COR_MENU_CEU_ALTO = (95, 170, 215)
COR_MENU_MAR = (40, 125, 190)
COR_MENU_ESPUMA = (225, 245, 250)
COR_MENU_AREIA = (222, 194, 135)
COR_MENU_AREIA_SOMBRA = (195, 165, 105)
COR_MENU_SOL = (255, 235, 150)
COR_MENU_PALMEIRA = (30, 40, 45)

COR_BOTAO = (235, 140, 30)
COR_BOTAO_HOVER = (250, 170, 60)
COR_BOTAO_BORDA = (150, 85, 15)

fonte_dialogo = pygame.font.SysFont("arial", 30)
fonte_dialogo_pequena = pygame.font.SysFont("arial", 22)
fonte_interface = pygame.font.SysFont("arial", 24)
fonte_hud = pygame.font.SysFont("arial", 22)
fonte_titulo = pygame.font.SysFont("arial", 42)
fonte_menu_titulo = pygame.font.SysFont("arial", 130, bold=True)
fonte_menu_subtitulo = pygame.font.SysFont("arial", 34, italic=True)
fonte_menu_botao = pygame.font.SysFont("arial", 32, bold=True)
fonte_menu_rodape = pygame.font.SysFont("arial", 22)

def desenhar_texto(superficie, texto, x, y, fonte, cor):
    imagem_texto = fonte.render(texto, True, cor)
    superficie.blit(imagem_texto, (x, y))


def quebrar_texto(texto, fonte, largura_maxima):
    palavras = texto.split(" ")
    linhas = []
    linha_atual = ""

    for palavra in palavras:
        teste = linha_atual + palavra + " "

        if fonte.size(teste)[0] <= largura_maxima:
            linha_atual = teste
        else:
            linhas.append(linha_atual.strip())
            linha_atual = palavra + " "

    if linha_atual:
        linhas.append(linha_atual.strip())

    return linhas


def desenhar_texto_contornado(superficie, texto, fonte, cor, cor_contorno, centro, espessura=4):
    contorno = fonte.render(texto, True, cor_contorno)

    for dx in range(-espessura, espessura + 1):
        for dy in range(-espessura, espessura + 1):
            if dx == 0 and dy == 0:
                continue

            rect = contorno.get_rect(center=(centro[0] + dx, centro[1] + dy))
            superficie.blit(contorno, rect)

    frente = fonte.render(texto, True, cor)
    rect = frente.get_rect(center=centro)
    superficie.blit(frente, rect)


class Botao:
    def __init__(self, texto, x, y, largura, altura, fonte):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.fonte = fonte
        self.hover = False

    def atualizar(self, pos_mouse):
        self.hover = self.rect.collidepoint(pos_mouse)

    def foi_clicado(self, evento):
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            return self.rect.collidepoint(evento.pos)

        return False

    def desenhar(self, superficie):
        cor = COR_BOTAO_HOVER if self.hover else COR_BOTAO

        sombra = self.rect.move(4, 6)
        pygame.draw.rect(superficie, (0, 0, 0), sombra, border_radius=12)
        pygame.draw.rect(superficie, cor, self.rect, border_radius=12)
        pygame.draw.rect(superficie, COR_BOTAO_BORDA, self.rect, 3, border_radius=12)

        imagem = self.fonte.render(self.texto, True, (255, 255, 255))
        imagem_rect = imagem.get_rect(center=self.rect.center)
        superficie.blit(imagem, imagem_rect)


def desenhar_palmeira(superficie, base_x, base_y, escala):
    altura_tronco = int(210 * escala)
    passos = 26

    topo_x = base_x
    topo_y = base_y

    for i in range(passos):
        t = i / (passos - 1)
        x = base_x + int(math.sin(t * 1.3) * 40 * escala)
        y = base_y - int(altura_tronco * t)
        raio = max(2, int((13 - t * 7) * escala))
        pygame.draw.circle(superficie, COR_MENU_PALMEIRA, (x, y), raio)
        topo_x = x
        topo_y = y

    pygame.draw.circle(superficie, COR_MENU_PALMEIRA, (topo_x, topo_y), int(9 * escala))

    for angulo in (-85, -50, -18, 18, 50, 85):
        rad = math.radians(angulo)

        meio_x = topo_x + int(math.sin(rad) * 75 * escala)
        meio_y = topo_y - int(math.cos(rad) * 48 * escala)

        ponta_x = topo_x + int(math.sin(rad) * 140 * escala)
        ponta_y = meio_y + int(38 * escala)

        pygame.draw.line(superficie, COR_MENU_PALMEIRA, (topo_x, topo_y), (meio_x, meio_y), int(9 * escala))
        pygame.draw.line(superficie, COR_MENU_PALMEIRA, (meio_x, meio_y), (ponta_x, ponta_y), int(7 * escala))


def desenhar_fundo_menu(superficie, tempo):
    superficie.fill(COR_MENU_CEU)

    pygame.draw.rect(superficie, COR_MENU_CEU_ALTO, (0, 0, LARGURA, int(ALTURA * 0.2)))

    sol_x = int(LARGURA * 0.78)
    sol_y = int(ALTURA * 0.22)
    pygame.draw.circle(superficie, COR_MENU_SOL, (sol_x, sol_y), 90)

    mar_y = int(ALTURA * 0.45)
    pygame.draw.rect(superficie, COR_MENU_MAR, (0, mar_y, LARGURA, int(ALTURA * 0.22)))

    for i in range(3):
        onda_y = mar_y + 30 + i * 45 + int(math.sin(tempo * 2 + i) * 6)
        pygame.draw.line(superficie, COR_MENU_ESPUMA, (0, onda_y), (LARGURA, onda_y), 3)

    areia_y = int(ALTURA * 0.67)
    pygame.draw.rect(superficie, COR_MENU_AREIA, (0, areia_y, LARGURA, ALTURA - areia_y))
    pygame.draw.line(superficie, COR_MENU_ESPUMA, (0, areia_y), (LARGURA, areia_y), 6)

    for i in range(0, LARGURA, 60):
        offset = int(math.sin(tempo * 1.5 + i) * 8)
        pygame.draw.arc(
            superficie,
            COR_MENU_ESPUMA,
            (i, areia_y - 14 + offset, 60, 28),
            math.pi,
            2 * math.pi,
            3
        )

    desenhar_palmeira(superficie, int(LARGURA * 0.14), int(ALTURA * 0.72), 1.4)
    desenhar_palmeira(superficie, int(LARGURA * 0.24), int(ALTURA * 0.70), 1.0)


def executar_menu():
    largura_botao = 360
    altura_botao = 72
    espaco = 26
    centro_x = LARGURA // 2
    inicio_y = int(ALTURA * 0.58)

    textos_botoes = ["Novo Jogo", "Controles", "Sair"]
    botoes = []

    for i, texto in enumerate(textos_botoes):
        y = inicio_y + i * (altura_botao + espaco)
        botao = Botao(texto, centro_x - largura_botao // 2, y, largura_botao, altura_botao, fonte_menu_botao)
        botoes.append(botao)

    mostrando_controles = False
    no_menu = True
    acao = "sair"

    while no_menu:
        tempo = pygame.time.get_ticks() / 1000.0
        relogio.tick(FPS)
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                no_menu = False
                acao = "sair"

            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if mostrando_controles:
                    mostrando_controles = False
                else:
                    no_menu = False
                    acao = "sair"

            if mostrando_controles:
                if evento.type == pygame.MOUSEBUTTONDOWN or evento.type == pygame.KEYDOWN:
                    mostrando_controles = False
            else:
                if botoes[0].foi_clicado(evento):
                    no_menu = False
                    acao = "jogar"

                if botoes[1].foi_clicado(evento):
                    mostrando_controles = True

                if botoes[2].foi_clicado(evento):
                    no_menu = False
                    acao = "sair"

        for botao in botoes:
            botao.atualizar(pos_mouse)

        desenhar_fundo_menu(tela, tempo)

        desenhar_texto_contornado(
            tela,
            "Mayze",
            fonte_menu_titulo,
            (45, 35, 30),
            (255, 255, 255),
            (centro_x, int(ALTURA * 0.28)),
            espessura=5
        )

        desenhar_texto_contornado(
            tela,
            "A Praia das Lembrancas",
            fonte_menu_subtitulo,
            (255, 255, 255),
            (60, 45, 35),
            (centro_x, int(ALTURA * 0.28) + 95),
            espessura=2
        )

        if mostrando_controles:
            desenhar_painel_controles()
        else:
            for botao in botoes:
                botao.desenhar(tela)

        rodape = fonte_menu_rodape.render("v1.0  -  feito com pygame", True, (60, 45, 35))
        tela.blit(rodape, (LARGURA - rodape.get_width() - 25, ALTURA - 40))

        pygame.display.flip()

    return acao


def desenhar_painel_controles():
    largura = 620
    altura = 430
    x = LARGURA // 2 - largura // 2
    y = int(ALTURA * 0.50)

    painel = pygame.Rect(x, y, largura, altura)
    pygame.draw.rect(tela, COR_CAIXA_DIALOGO, painel, border_radius=18)
    pygame.draw.rect(tela, COR_BORDA_DIALOGO, painel, 5, border_radius=18)

    titulo = fonte_titulo.render("Controles", True, COR_BORDA_DIALOGO)
    titulo_rect = titulo.get_rect(center=(LARGURA // 2, y + 45))
    tela.blit(titulo, titulo_rect)

    linhas = [
        "WASD / setas  -  mover",
        "SHIFT  -  correr",
        "ESPACO  -  atacar",
        "B  -  latir / rosnar",
        "E  -  abrir inventario",
        "C  -  consumir item da mao",
        "H  -  habilidades",
        "1-5  -  selecionar item",
        "ESC  -  sair",
    ]

    linha_y = y + 100

    for linha in linhas:
        texto = fonte_interface.render(linha, True, COR_TEXTO)
        tela.blit(texto, (x + 55, linha_y))
        linha_y += 35

    dica = fonte_dialogo_pequena.render("Clique ou aperte uma tecla para voltar", True, COR_BORDA_DIALOGO)
    dica_rect = dica.get_rect(center=(LARGURA // 2, y + altura - 30))
    tela.blit(dica, dica_rect)


def executar_tela_nome(assets):
    nome_digitado = ""
    max_caracteres = 12

    centro_x = LARGURA // 2

    painel_largura = 740
    painel_altura = 380
    painel_x = centro_x - painel_largura // 2
    painel_y = ALTURA // 2 - painel_altura // 2

    largura_botao = 200
    altura_botao = 60
    espaco = 40
    botoes_y = painel_y + painel_altura - 90

    botao_cancelar = Botao(
        "Cancelar",
        centro_x - largura_botao - espaco // 2,
        botoes_y,
        largura_botao,
        altura_botao,
        fonte_menu_botao
    )
    botao_confirmar = Botao(
        "Confirmar",
        centro_x + espaco // 2,
        botoes_y,
        largura_botao,
        altura_botao,
        fonte_menu_botao
    )

    caixa_texto = pygame.Rect(painel_x + 250, painel_y + 150, painel_largura - 300, 56)

    na_tela = True
    resultado = None

    while na_tela:
        tempo = pygame.time.get_ticks() / 1000.0
        relogio.tick(FPS)
        pos_mouse = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                na_tela = False
                resultado = None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    na_tela = False
                    resultado = None

                elif evento.key == pygame.K_RETURN:
                    na_tela = False
                    resultado = nome_digitado

                elif evento.key == pygame.K_BACKSPACE:
                    nome_digitado = nome_digitado[:-1]

                elif len(nome_digitado) < max_caracteres and evento.unicode.isprintable():
                    nome_digitado += evento.unicode

            if botao_cancelar.foi_clicado(evento):
                na_tela = False
                resultado = None

            if botao_confirmar.foi_clicado(evento):
                na_tela = False
                resultado = nome_digitado

        botao_cancelar.atualizar(pos_mouse)
        botao_confirmar.atualizar(pos_mouse)

        desenhar_fundo_menu(tela, tempo)

        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(90)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        painel = pygame.Rect(painel_x, painel_y, painel_largura, painel_altura)
        pygame.draw.rect(tela, COR_CAIXA_DIALOGO, painel, border_radius=20)
        pygame.draw.rect(tela, COR_BORDA_DIALOGO, painel, 5, border_radius=20)

        retrato = pygame.transform.scale(assets.face_looking, (150, 150))
        retrato_x = painel_x + 55
        retrato_y = painel_y + 90

        pygame.draw.rect(tela, COR_RETRATO_FUNDO, (retrato_x - 10, retrato_y - 10, 170, 170), border_radius=14)
        pygame.draw.rect(tela, COR_BORDA_DIALOGO, (retrato_x - 10, retrato_y - 10, 170, 170), 4, border_radius=14)
        tela.blit(retrato, (retrato_x, retrato_y))

        titulo = fonte_interface.render("Dê um nome para a Mayze.", True, COR_TEXTO)
        tela.blit(titulo, (painel_x + 250, painel_y + 60))

        sub = fonte_dialogo_pequena.render("(Máx. 12 caracteres)", True, COR_BORDA_DIALOGO)
        tela.blit(sub, (painel_x + 250, painel_y + 100))

        pygame.draw.rect(tela, (255, 255, 255), caixa_texto, border_radius=8)
        pygame.draw.rect(tela, COR_BORDA_DIALOGO, caixa_texto, 3, border_radius=8)

        texto_render = fonte_dialogo.render(nome_digitado, True, COR_TEXTO)
        tela.blit(texto_render, (caixa_texto.x + 12, caixa_texto.y + 10))

        if int(tempo * 2) % 2 == 0:
            cursor_x = caixa_texto.x + 14 + texto_render.get_width()
            pygame.draw.line(
                tela,
                COR_TEXTO,
                (cursor_x, caixa_texto.y + 12),
                (cursor_x, caixa_texto.bottom - 12),
                2
            )

        botao_cancelar.desenhar(tela)
        botao_confirmar.desenhar(tela)

        pygame.display.flip()

    return resultado


class Dialogo:
    def __init__(self, falas, assets_mayze):
        self.falas = falas
        self.assets_mayze = assets_mayze
        self.indice = 0
        self.aberto = True

    def fala_atual(self):
        if self.indice >= len(self.falas):
            return None

        return self.falas[self.indice]

    def avancar(self):
        self.indice += 1

        if self.indice >= len(self.falas):
            self.aberto = False

    def desenhar(self, superficie):
        if not self.aberto:
            return

        fala = self.fala_atual()

        if fala is None:
            return

        tipo = fala["tipo"]
        nome = fala["nome"]
        texto = fala["texto"]

        caixa_largura = int(LARGURA * 0.82)
        caixa_altura = 210
        caixa_x = int((LARGURA - caixa_largura) / 2)
        caixa_y = ALTURA - caixa_altura - 115

        sombra = pygame.Rect(caixa_x + 8, caixa_y + 8, caixa_largura, caixa_altura)
        caixa = pygame.Rect(caixa_x, caixa_y, caixa_largura, caixa_altura)

        pygame.draw.rect(superficie, (0, 0, 0), sombra, border_radius=18)
        pygame.draw.rect(superficie, COR_CAIXA_DIALOGO, caixa, border_radius=18)
        pygame.draw.rect(superficie, COR_BORDA_DIALOGO, caixa, 5, border_radius=18)

        retrato = self.assets_mayze.face_talking

        if tipo == "pensamento":
            retrato = self.assets_mayze.face_looking

        retrato_x = caixa_x + 25
        retrato_y = caixa_y + 30

        pygame.draw.rect(
            superficie,
            (235, 210, 165),
            (retrato_x - 8, retrato_y - 8, 166, 166),
            border_radius=12
        )
        pygame.draw.rect(
            superficie,
            COR_BORDA_DIALOGO,
            (retrato_x - 8, retrato_y - 8, 166, 166),
            4,
            border_radius=12
        )

        superficie.blit(retrato, (retrato_x, retrato_y))

        nome_x = caixa_x + 205
        nome_y = caixa_y + 28

        if tipo == "pensamento":
            nome_exibido = f"{nome} pensa"
        else:
            nome_exibido = nome

        desenhar_texto(superficie, nome_exibido, nome_x, nome_y, fonte_dialogo_pequena, COR_BORDA_DIALOGO)

        linhas = quebrar_texto(texto, fonte_dialogo, caixa_largura - 250)

        texto_x = caixa_x + 205
        texto_y = caixa_y + 70

        for linha in linhas:
            desenhar_texto(superficie, linha, texto_x, texto_y, fonte_dialogo, COR_TEXTO)
            texto_y += 38

        dica = "ENTER ou ESPAÇO para continuar"
        desenhar_texto(
            superficie,
            dica,
            caixa_x + caixa_largura - 330,
            caixa_y + caixa_altura - 35,
            fonte_dialogo_pequena,
            COR_BORDA_DIALOGO
        )


def desenhar_interface():
    desenhar_texto(tela, "WASD/setas: mover", 30, 125, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "SHIFT: correr", 30, 155, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "ESPAÇO: atacar / diálogo", 30, 185, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "B: latir/rosnar", 30, 215, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "E: abrir inventário", 30, 245, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "C: consumir item da mão", 30, 275, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "H: habilidades", 30, 305, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "1-5: selecionar item da mão", 30, 335, fonte_interface, COR_TEXTO_CLARO)
    desenhar_texto(tela, "ESC: sair", 30, 365, fonte_interface, COR_TEXTO_CLARO)


def desenhar_hud_player(player, assets_mayze):
    retrato_x = 34
    retrato_y = 26
    raio = 34

    pygame.draw.circle(tela, COR_HP_BORDA, (retrato_x + raio, retrato_y + raio), raio + 5)
    pygame.draw.circle(tela, COR_RETRATO_FUNDO, (retrato_x + raio, retrato_y + raio), raio)

    retrato = pygame.transform.scale(assets_mayze.face_looking, (58, 58))
    tela.blit(retrato, (retrato_x + 5, retrato_y + 5))

    barra_x = retrato_x + 78
    barra_y = retrato_y + 12
    barra_largura = 220
    barra_altura = 24

    porcentagem_hp = player.hp / player.hp_max
    largura_hp = int(barra_largura * porcentagem_hp)

    pygame.draw.rect(
        tela,
        COR_HP_BORDA,
        (barra_x - 4, barra_y - 4, barra_largura + 8, barra_altura + 8),
        border_radius=10
    )
    pygame.draw.rect(
        tela,
        COR_HP_FUNDO,
        (barra_x, barra_y, barra_largura, barra_altura),
        border_radius=8
    )
    pygame.draw.rect(
        tela,
        COR_HP,
        (barra_x, barra_y, largura_hp, barra_altura),
        border_radius=8
    )

    texto_hp = fonte_hud.render(f"HP {player.hp}/{player.hp_max}", True, (255, 255, 255))
    tela.blit(texto_hp, (barra_x + 68, barra_y + 1))

    xp_y = barra_y + 34
    xp_altura = 16

    porcentagem_xp = player.xp / player.xp_para_proximo_nivel
    largura_xp = int(barra_largura * porcentagem_xp)

    pygame.draw.rect(
        tela,
        COR_HP_BORDA,
        (barra_x - 3, xp_y - 3, barra_largura + 6, xp_altura + 6),
        border_radius=8
    )
    pygame.draw.rect(
        tela,
        COR_XP_FUNDO,
        (barra_x, xp_y, barra_largura, xp_altura),
        border_radius=6
    )
    pygame.draw.rect(
        tela,
        COR_XP,
        (barra_x, xp_y, largura_xp, xp_altura),
        border_radius=6
    )

    texto_xp = fonte_hud.render(
        f"XP {player.xp}/{player.xp_para_proximo_nivel}",
        True,
        (255, 255, 255)
    )
    tela.blit(texto_xp, (barra_x + 76, xp_y - 4))

    texto_nivel = fonte_hud.render(f"Nível {player.nivel}", True, (255, 255, 255))
    tela.blit(texto_nivel, (barra_x, xp_y + 24))

    texto_pontos = fonte_hud.render(f"Pontos de habilidade: {player.pontos_habilidade}", True, (255, 245, 150))
    tela.blit(texto_pontos, (barra_x, xp_y + 50))

def desenhar_tela_habilidades(player):
    overlay = pygame.Surface((LARGURA, ALTURA))
    overlay.set_alpha(215)
    overlay.fill((18, 14, 18))
    tela.blit(overlay, (0, 0))

    painel_largura = 760
    painel_altura = 500
    painel_x = LARGURA // 2 - painel_largura // 2
    painel_y = ALTURA // 2 - painel_altura // 2

    painel = pygame.Rect(painel_x, painel_y, painel_largura, painel_altura)

    pygame.draw.rect(tela, (48, 38, 34), painel, border_radius=20)
    pygame.draw.rect(tela, (230, 190, 115), painel, 5, border_radius=20)

    titulo = fonte_titulo.render(f"Habilidades da {NOME_PLAYER}", True, (255, 235, 180))
    titulo_rect = titulo.get_rect(center=(LARGURA // 2, painel_y + 55))
    tela.blit(titulo, titulo_rect)

    pontos = fonte_interface.render(
        f"Pontos disponíveis: {player.pontos_habilidade}",
        True,
        (255, 255, 255)
    )
    tela.blit(pontos, (painel_x + 55, painel_y + 110))

    linhas = [
        "1 - Vida Forte: aumenta HP máximo em +3",
        "2 - Mordida Forte: aumenta dano em +1",
        "3 - Patas Rápidas: aumenta velocidade",
        "4 - Barriga Feliz: biscoitos curam mais",
    ]

    y = painel_y + 170

    for linha in linhas:
        texto = fonte_interface.render(linha, True, (255, 230, 190))
        tela.blit(texto, (painel_x + 70, y))
        y += 55

    status = [
        f"HP máximo: {player.hp_max}",
        f"Dano extra: {player.bonus_dano}",
        f"Velocidade extra: {player.bonus_velocidade}",
        f"Cura extra: {player.bonus_cura}",
    ]

    y = painel_y + 170

    for linha in status:
        texto = fonte_interface.render(linha, True, (185, 235, 255))
        tela.blit(texto, (painel_x + 460, y))
        y += 55

    dica = fonte_dialogo_pequena.render(
        "Pressione 1-4 para gastar pontos | H para fechar",
        True,
        (255, 255, 255)
    )
    tela.blit(dica, (painel_x + 145, painel_y + painel_altura - 55))

assets_mayze = AssetsMayze()

mapa = MapaPraia()
camera = Camera(mapa.largura, mapa.altura, LARGURA, ALTURA)

inventario = Inventario()

player = Player(*BEACH_MAP["player_spawn"], assets_mayze)

NOME_PLAYER = "Mayze"
iniciar_jogo = False
telas_iniciais = True

while telas_iniciais:
    acao_menu = executar_menu()

    if acao_menu != "jogar":
        telas_iniciais = False
        break

    nome_escolhido = executar_tela_nome(assets_mayze)

    if nome_escolhido is None:
        continue

    NOME_PLAYER = nome_escolhido.strip() or "Mayze"
    iniciar_jogo = True
    telas_iniciais = False

falas_iniciais = [
    {
        "tipo": "pensamento",
        "nome": NOME_PLAYER,
        "texto": "O som das ondas... areia fria nas patas... Onde eu estou?"
    },
    {
        "tipo": "fala",
        "nome": NOME_PLAYER,
        "texto": "Au...? Tem alguém aí?"
    },
    {
        "tipo": "pensamento",
        "nome": NOME_PLAYER,
        "texto": "Eu lembro de vozes. Uma casa. Um cheiro conhecido... mas tudo parece distante."
    },
    {
        "tipo": "fala",
        "nome": NOME_PLAYER,
        "texto": "Eu preciso encontrar minha família. Eles devem estar me procurando."
    },
    {
        "tipo": "pensamento",
        "nome": NOME_PLAYER,
        "texto": "Talvez se eu seguir a praia para o sul, encontre alguma pista... ou alguém que saiba de algo."
    },
    {
        "tipo": "fala",
        "nome": NOME_PLAYER,
        "texto": "Não vou desistir. Eu vou voltar para casa."
    }
]

falas_desmaio = [
    {
        "tipo": "pensamento",
        "nome": NOME_PLAYER,
        "texto": "Um frio atravessou minhas patas. O som das ondas ficou longe... e então o mundo inteiro apagou."
    },
    {
        "tipo": "fala",
        "nome": NOME_PLAYER,
        "texto": "Nossa... o que aconteceu? Eu estava andando e, de repente, tudo ficou escuro."
    },
    {
        "tipo": "pensamento",
        "nome": NOME_PLAYER,
        "texto": "Meu coração ainda está disparado. A praia parece a mesma, mas sinto como se algo tivesse me puxado de volta."
    },
    {
        "tipo": "fala",
        "nome": NOME_PLAYER,
        "texto": "Preciso ter mais cuidado. Eu ainda vou encontrar minha família."
    }
]

dialogo = Dialogo(falas_iniciais, assets_mayze)

tempo_desmaio = 0
desmaio_processado = False

tela_habilidades_aberta = False
nivel_anterior = player.nivel

rodando = iniciar_jogo

while rodando:
    dt = relogio.tick(FPS) / 1000.0

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False

            if dialogo.aberto:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                    dialogo.avancar()
            else:
                if evento.key == pygame.K_h:
                    tela_habilidades_aberta = not tela_habilidades_aberta
                    inventario.aberto = False

                if tela_habilidades_aberta:
                    if evento.key == pygame.K_1:
                        player.gastar_ponto_habilidade("vida")

                    if evento.key == pygame.K_2:
                        player.gastar_ponto_habilidade("dano")

                    if evento.key == pygame.K_3:
                        player.gastar_ponto_habilidade("velocidade")

                    if evento.key == pygame.K_4:
                        player.gastar_ponto_habilidade("cura")

                else:
                    if evento.key == pygame.K_e:
                        inventario.alternar()

                    if evento.key == pygame.K_c:
                        inventario.consumir_item_da_mao(player)

                    if not inventario.aberto:
                        if evento.key == pygame.K_SPACE:
                            player.iniciar_ataque()
                            mapa.processar_ataque_player(player)

                        if evento.key == pygame.K_b:
                            player.iniciar_latido()

                    if evento.key == pygame.K_1:
                        inventario.selecionar_slot_mao(0)

                    if evento.key == pygame.K_2:
                        inventario.selecionar_slot_mao(1)

                    if evento.key == pygame.K_3:
                        inventario.selecionar_slot_mao(2)

                    if evento.key == pygame.K_4:
                        inventario.selecionar_slot_mao(3)

                    if evento.key == pygame.K_5:
                        inventario.selecionar_slot_mao(4)

    jogo_pausado = tela_habilidades_aberta

    player.atualizar(dt, mapa.objetos_solidos(), dialogo.aberto, inventario.aberto or jogo_pausado)

    mapa.limitar_player_no_mapa(player)
    if not jogo_pausado:
        mapa.atualizar(dt, player, inventario)

    if not player.esta_vivo():
        tempo_desmaio += dt

        if tempo_desmaio >= 1.4 and not desmaio_processado:
            desmaio_processado = True
            tempo_desmaio = 0

            mapa.trocar_para_chunk("praia", player)
            player.renascer(980, 760)

            dialogo = Dialogo(falas_desmaio, assets_mayze)
    else:
        tempo_desmaio = 0
        desmaio_processado = False

    if player.nivel > nivel_anterior:
        nivel_anterior = player.nivel
        tela_habilidades_aberta = True
        inventario.aberto = False

    camera.atualizar(player.rect)

    mapa.desenhar_base(tela, camera)

    entidades = mapa.entidades_para_desenhar(player)

    for entidade in entidades:
        entidade.desenhar(tela, camera)

    desenhar_hud_player(player, assets_mayze)
    desenhar_interface()

    desenhar_hotbar(inventario, tela, LARGURA, ALTURA)
    draw_inventory(inventario, tela, LARGURA, ALTURA)

    if tela_habilidades_aberta:
        desenhar_tela_habilidades(player)

    if dialogo.aberto:
        dialogo.desenhar(tela)

    if not player.esta_vivo():
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        texto = fonte_dialogo.render(f"{NOME_PLAYER} desmaiou...", True, (255, 230, 220))
        texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))
        tela.blit(texto, texto_rect)

    pygame.display.flip()

pygame.quit()
