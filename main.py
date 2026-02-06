VERMELHO = "VERMELHO"
PRETO = "PRETO"

class NoRubroNegro:
    def __init__(self, valor, cor=VERMELHO):
        self.valor = valor
        self.cor = cor
        self.esquerda = None
        self.direita = None
        self.pai = None

class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = NoRubroNegro(None, PRETO)
        self.raiz = self.NIL

    def rotacao_esquerda(self, x):
        y = x.direita
        x.direita = y.esquerda
        if y.esquerda != self.NIL:
            y.esquerda.pai = x
        y.pai = x.pai
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.esquerda:
            x.pai.esquerda = y
        else:
            x.pai.direita = y
        y.esquerda = x
        x.pai = y

    def rotacao_direita(self, x):
        y = x.esquerda
        x.esquerda = y.direita
        if y.direita != self.NIL:
            y.direita.pai = x
        y.pai = x.pai
        if x.pai is None:
            self.raiz = y
        elif x == x.pai.direita:
            x.pai.direita = y
        else:
            x.pai.esquerda = y
        y.direita = x
        x.pai = y

    def buscar(self, valor):
        atual = self.raiz
        while atual != self.NIL and valor != atual.valor:
            atual = atual.esquerda if valor < atual.valor else atual.direita
        return atual

    def minimo(self, no):
        while no.esquerda != self.NIL:
            no = no.esquerda
        return no

    def transplante(self, u, v):
        if u.pai is None:
            self.raiz = v
        elif u == u.pai.esquerda:
            u.pai.esquerda = v
        else:
            u.pai.direita = v
        v.pai = u.pai

    def remover(self, valor):
        z = self.buscar(valor)
        if z == self.NIL:
            return

        y = z
        cor_original = y.cor

        if z.esquerda == self.NIL:
            x = z.direita
            self.transplante(z, z.direita)
        elif z.direita == self.NIL:
            x = z.esquerda
            self.transplante(z, z.esquerda)
        else:
            y = self.minimo(z.direita)
            cor_original = y.cor
            x = y.direita
            if y.pai == z:
                x.pai = y
            else:
                self.transplante(y, y.direita)
                y.direita = z.direita
                y.direita.pai = y
            self.transplante(z, y)
            y.esquerda = z.esquerda
            y.esquerda.pai = y
            y.cor = z.cor

        if cor_original == PRETO:
            self.corrigir_remocao(x)

    def corrigir_remocao(self, x):
        while x != self.raiz and x.cor == PRETO:
            if x == x.pai.esquerda:
                w = x.pai.direita
                if w.cor == VERMELHO:
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self.rotacao_esquerda(x.pai)
                    w = x.pai.direita
                if w.esquerda.cor == PRETO and w.direita.cor == PRETO:
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.direita.cor == PRETO:
                        w.esquerda.cor = PRETO
                        w.cor = VERMELHO
                        self.rotacao_direita(w)
                        w = x.pai.direita
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.direita.cor = PRETO
                    self.rotacao_esquerda(x.pai)
                    x = self.raiz
            else:
                w = x.pai.esquerda
                if w.cor == VERMELHO:
                    w.cor = PRETO
                    x.pai.cor = VERMELHO
                    self.rotacao_direita(x.pai)
                    w = x.pai.esquerda
                if w.direita.cor == PRETO and w.esquerda.cor == PRETO:
                    w.cor = VERMELHO
                    x = x.pai
                else:
                    if w.esquerda.cor == PRETO:
                        w.direita.cor = PRETO
                        w.cor = VERMELHO
                        self.rotacao_esquerda(w)
                        w = x.pai.esquerda
                    w.cor = x.pai.cor
                    x.pai.cor = PRETO
                    w.esquerda.cor = PRETO
                    self.rotacao_direita(x.pai)
                    x = self.raiz
        x.cor = PRETO
