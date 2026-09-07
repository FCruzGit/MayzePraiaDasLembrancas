import pygame

from inventario import Inventario
from mapa import Camera, MapaPraia
from mayze import AssetsMayze, Player


pygame.init()

info_tela = pygame.display.Info()
LARGURA, ALTURA = info_tela.current_w, info_tela.current_h

tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption("Mayze - A Praia das Lembranças")

relogio = pygame.time.Clock()
FPS = 60

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

fonte_dialogo = pygame.font.SysFont("arial", 30)
fonte_dialogo_pequena = pygame.font.SysFont("arial", 22)
fonte_interface = pygame.font.SysFont("arial", 24)
fonte_hud = pygame.font.SysFont("arial", 22)
fonte_titulo = pygame.font.SysFont("arial", 42)

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

    titulo = fonte_titulo.render("Habilidades da Mayze", True, (255, 235, 180))
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

player = Player(980, 760, assets_mayze)

falas_iniciais = [
    {
        "tipo": "pensamento",
        "nome": "Mayze",
        "texto": "O som das ondas... areia fria nas patas... Onde eu estou?"
    },
    {
        "tipo": "fala",
        "nome": "Mayze",
        "texto": "Au...? Tem alguém aí?"
    },
    {
        "tipo": "pensamento",
        "nome": "Mayze",
        "texto": "Eu lembro de vozes. Uma casa. Um cheiro conhecido... mas tudo parece distante."
    },
    {
        "tipo": "fala",
        "nome": "Mayze",
        "texto": "Eu preciso encontrar minha família. Eles devem estar me procurando."
    },
    {
        "tipo": "pensamento",
        "nome": "Mayze",
        "texto": "Talvez se eu seguir a praia para o sul, encontre alguma pista... ou alguém que saiba de algo."
    },
    {
        "tipo": "fala",
        "nome": "Mayze",
        "texto": "Não vou desistir. Eu vou voltar para casa."
    }
]

falas_desmaio = [
    {
        "tipo": "pensamento",
        "nome": "Mayze",
        "texto": "Um frio atravessou minhas patas. O som das ondas ficou longe... e então o mundo inteiro apagou."
    },
    {
        "tipo": "fala",
        "nome": "Mayze",
        "texto": "Nossa... o que aconteceu? Eu estava andando e, de repente, tudo ficou escuro."
    },
    {
        "tipo": "pensamento",
        "nome": "Mayze",
        "texto": "Meu coração ainda está disparado. A praia parece a mesma, mas sinto como se algo tivesse me puxado de volta."
    },
    {
        "tipo": "fala",
        "nome": "Mayze",
        "texto": "Preciso ter mais cuidado. Eu ainda vou encontrar minha família."
    }
]

dialogo = Dialogo(falas_iniciais, assets_mayze)

tempo_desmaio = 0
desmaio_processado = False

tela_habilidades_aberta = False
nivel_anterior = player.nivel
rodando = True

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

    inventario.desenhar_hotbar(tela, LARGURA, ALTURA)
    inventario.desenhar_inventario_completo(tela, LARGURA, ALTURA)

    if tela_habilidades_aberta:
        desenhar_tela_habilidades(player)

    if dialogo.aberto:
        dialogo.desenhar(tela)

    if not player.esta_vivo():
        overlay = pygame.Surface((LARGURA, ALTURA))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        tela.blit(overlay, (0, 0))

        texto = fonte_dialogo.render("Mayze desmaiou...", True, (255, 230, 220))
        texto_rect = texto.get_rect(center=(LARGURA // 2, ALTURA // 2))
        tela.blit(texto, texto_rect)

    pygame.display.flip()

pygame.quit()