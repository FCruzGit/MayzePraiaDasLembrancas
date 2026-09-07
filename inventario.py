import pygame


COR_SLOT = (238, 210, 160)
COR_SLOT_SELECIONADO = (255, 245, 180)
COR_BORDA = (92, 62, 38)
COR_TEXTO = (45, 35, 30)
COR_FUNDO_INVENTARIO = (35, 28, 24)


class Item:
    def __init__(self, nome, cor=(255, 220, 80), consumivel=False, cura=0):
        self.nome = nome
        self.cor = cor
        self.consumivel = consumivel
        self.cura = cura


class Inventario:
    def __init__(self):
        self.linhas = 5
        self.colunas = 5
        self.total_slots = self.linhas * self.colunas
        self.itens = [None for _ in range(self.total_slots)]

        self.slot_mao = 0
        self.aberto = False

        self.fonte = pygame.font.SysFont("arial", 22)
        self.fonte_pequena = pygame.font.SysFont("arial", 18)

    def alternar(self):
        self.aberto = not self.aberto

    def adicionar_item(self, item):
        for indice in range(self.total_slots):
            if self.itens[indice] is None:
                self.itens[indice] = item
                return True

        return False

    def selecionar_slot_mao(self, numero):
        if 0 <= numero <= 4:
            self.slot_mao = numero

    def item_na_mao(self):
        return self.itens[self.slot_mao]

    def consumir_item_da_mao(self, player):
        item = self.item_na_mao()

        if item is None:
            return False

        if not item.consumivel:
            return False

        if item.cura <= 0:
            return False

        if player.hp >= player.hp_max:
            return False

        player.curar(item.cura)
        self.itens[self.slot_mao] = None
        return True

    def desenhar_item(self, superficie, item, rect):
        if item is None:
            return

        centro_x = rect.centerx
        centro_y = rect.centery

        pygame.draw.circle(superficie, item.cor, (centro_x, centro_y), 14)
        pygame.draw.circle(superficie, (255, 255, 210), (centro_x - 5, centro_y - 5), 5)

        inicial = item.nome[0].upper()
        texto = self.fonte_pequena.render(inicial, True, COR_TEXTO)
        texto_rect = texto.get_rect(center=(centro_x, centro_y + 1))
        superficie.blit(texto, texto_rect)

    def desenhar_hotbar(self, superficie, largura_tela, altura_tela):
        tamanho_slot = 58
        espacamento = 8
        quantidade_slots = 5

        largura_total = quantidade_slots * tamanho_slot + (quantidade_slots - 1) * espacamento
        inicio_x = largura_tela // 2 - largura_total // 2
        y = altura_tela - tamanho_slot - 24

        for indice in range(quantidade_slots):
            x = inicio_x + indice * (tamanho_slot + espacamento)
            rect = pygame.Rect(x, y, tamanho_slot, tamanho_slot)

            cor = COR_SLOT_SELECIONADO if indice == self.slot_mao else COR_SLOT

            pygame.draw.rect(superficie, cor, rect, border_radius=8)
            pygame.draw.rect(superficie, COR_BORDA, rect, 4, border_radius=8)

            self.desenhar_item(superficie, self.itens[indice], rect)

            numero = self.fonte_pequena.render(str(indice + 1), True, COR_TEXTO)
            superficie.blit(numero, (x + 5, y + 3))

        item = self.item_na_mao()

        if item is not None and item.consumivel:
            dica = self.fonte_pequena.render("C: consumir item da mão", True, (255, 255, 255))
            superficie.blit(dica, (inicio_x, y - 26))

    def desenhar_inventario_completo(self, superficie, largura_tela, altura_tela):
        if not self.aberto:
            return

        tamanho_slot = 64
        espacamento = 10

        largura_grid = self.colunas * tamanho_slot + (self.colunas - 1) * espacamento
        altura_grid = self.linhas * tamanho_slot + (self.linhas - 1) * espacamento

        painel_largura = largura_grid + 80
        painel_altura = altura_grid + 130

        painel_x = largura_tela // 2 - painel_largura // 2
        painel_y = altura_tela // 2 - painel_altura // 2

        painel = pygame.Rect(painel_x, painel_y, painel_largura, painel_altura)

        pygame.draw.rect(superficie, COR_FUNDO_INVENTARIO, painel, border_radius=18)
        pygame.draw.rect(superficie, COR_BORDA, painel, 5, border_radius=18)

        titulo = self.fonte.render("Inventário da Mayze", True, (255, 235, 190))
        superficie.blit(titulo, (painel_x + 32, painel_y + 22))

        inicio_x = painel_x + 40
        inicio_y = painel_y + 75

        for linha in range(self.linhas):
            for coluna in range(self.colunas):
                indice = linha * self.colunas + coluna

                x = inicio_x + coluna * (tamanho_slot + espacamento)
                y = inicio_y + linha * (tamanho_slot + espacamento)

                rect = pygame.Rect(x, y, tamanho_slot, tamanho_slot)

                cor = COR_SLOT_SELECIONADO if indice == self.slot_mao else COR_SLOT

                pygame.draw.rect(superficie, cor, rect, border_radius=8)
                pygame.draw.rect(superficie, COR_BORDA, rect, 4, border_radius=8)

                self.desenhar_item(superficie, self.itens[indice], rect)

        dica = self.fonte_pequena.render(
            "E: fechar inventário | 1-5: selecionar item da mão | C: consumir biscoito",
            True,
            (255, 235, 190)
        )
        superficie.blit(dica, (painel_x + 32, painel_y + painel_altura - 35))