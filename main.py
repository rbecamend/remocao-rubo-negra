VERMELHO = "VERMELHO"
PRETO = "PRETO"

class NoRubroNegro:
    def __init__(self, valor, cor=VERMELHO):
        self.valor = valor
        self.cor = cor
        self.filho_esquerdo = None
        self.filho_direito = None
        self.pai = None

class ArvoreRubroNegra:
    def __init__(self):
        self.NIL = NoRubroNegro(None, PRETO)
        self.NIL.filho_esquerdo = self.NIL
        self.NIL.filho_direito = self.NIL
        self.NIL.pai = None
        self.raiz = self.NIL

    def rotacao_esquerda(self, no_pivot):
        novo_pai = no_pivot.filho_direito
        no_pivot.filho_direito = novo_pai.filho_esquerdo

        if novo_pai.filho_esquerdo != self.NIL:
            novo_pai.filho_esquerdo.pai = no_pivot

        novo_pai.pai = no_pivot.pai

        if no_pivot.pai is None:
            self.raiz = novo_pai
        elif no_pivot == no_pivot.pai.filho_esquerdo:
            no_pivot.pai.filho_esquerdo = novo_pai
        else:
            no_pivot.pai.filho_direito = novo_pai

        novo_pai.filho_esquerdo = no_pivot
        no_pivot.pai = novo_pai

    def rotacao_direita(self, no_pivot):
        novo_pai = no_pivot.filho_esquerdo
        no_pivot.filho_esquerdo = novo_pai.filho_direito

        if novo_pai.filho_direito != self.NIL:
            novo_pai.filho_direito.pai = no_pivot

        novo_pai.pai = no_pivot.pai

        if no_pivot.pai is None:
            self.raiz = novo_pai
        elif no_pivot == no_pivot.pai.filho_direito:
            no_pivot.pai.filho_direito = novo_pai
        else:
            no_pivot.pai.filho_esquerdo = novo_pai

        novo_pai.filho_direito = no_pivot
        no_pivot.pai = novo_pai

    def buscar(self, valor):
        no_atual = self.raiz

        while no_atual != self.NIL and valor != no_atual.valor:
            if valor < no_atual.valor:
                no_atual = no_atual.filho_esquerdo
            else:
                no_atual = no_atual.filho_direito

        return no_atual

    def minimo(self, no):
        no_atual = no
        while no_atual.filho_esquerdo != self.NIL:
            no_atual = no_atual.filho_esquerdo
        return no_atual

    def transplante(self, no_removido, no_substituto):
        if no_removido.pai is None:
            self.raiz = no_substituto
        elif no_removido == no_removido.pai.filho_esquerdo:
            no_removido.pai.filho_esquerdo = no_substituto
        else:
            no_removido.pai.filho_direito = no_substituto

        no_substituto.pai = no_removido.pai

    def inserir_simples(self, valor):
        novo_no = NoRubroNegro(valor, VERMELHO)
        novo_no.filho_esquerdo = self.NIL
        novo_no.filho_direito = self.NIL

        pai = None
        no_atual = self.raiz

        while no_atual != self.NIL:
            pai = no_atual
            if valor < no_atual.valor:
                no_atual = no_atual.filho_esquerdo
            else:
                no_atual = no_atual.filho_direito

        novo_no.pai = pai

        if pai is None:
            self.raiz = novo_no
        elif valor < pai.valor:
            pai.filho_esquerdo = novo_no
        else:
            pai.filho_direito = novo_no

        self.raiz.cor = PRETO

    def remover(self, valor):
        no_removido = self.buscar(valor)
        if no_removido == self.NIL:
            return

        no_que_sai = no_removido
        cor_original = no_que_sai.cor

        if no_removido.filho_esquerdo == self.NIL:
            no_substituto = no_removido.filho_direito
            self.transplante(no_removido, no_removido.filho_direito)

        elif no_removido.filho_direito == self.NIL:
            no_substituto = no_removido.filho_esquerdo
            self.transplante(no_removido, no_removido.filho_esquerdo)

        else:
            no_que_sai = self.minimo(no_removido.filho_direito)
            cor_original = no_que_sai.cor
            no_substituto = no_que_sai.filho_direito

            if no_que_sai.pai == no_removido:
                no_substituto.pai = no_que_sai
            else:
                self.transplante(no_que_sai, no_que_sai.filho_direito)
                no_que_sai.filho_direito = no_removido.filho_direito
                no_que_sai.filho_direito.pai = no_que_sai

            self.transplante(no_removido, no_que_sai)
            no_que_sai.filho_esquerdo = no_removido.filho_esquerdo
            no_que_sai.filho_esquerdo.pai = no_que_sai
            no_que_sai.cor = no_removido.cor

        if cor_original == PRETO:
            self.corrigir_remocao(no_substituto)

    def corrigir_remocao(self, no_atual):
        while no_atual != self.raiz and no_atual.cor == PRETO:

            pai = no_atual.pai

            if no_atual == pai.filho_esquerdo:
                irmao = pai.filho_direito

                if irmao.cor == VERMELHO:
                    irmao.cor = PRETO
                    pai.cor = VERMELHO
                    self.rotacao_esquerda(pai)
                    irmao = pai.filho_direito

                if irmao.filho_esquerdo.cor == PRETO and irmao.filho_direito.cor == PRETO:
                    irmao.cor = VERMELHO
                    no_atual = pai
                else:
                    if irmao.filho_direito.cor == PRETO:
                        irmao.filho_esquerdo.cor = PRETO
                        irmao.cor = VERMELHO
                        self.rotacao_direita(irmao)
                        irmao = pai.filho_direito

                    irmao.cor = pai.cor
                    pai.cor = PRETO
                    irmao.filho_direito.cor = PRETO
                    self.rotacao_esquerda(pai)
                    no_atual = self.raiz

            else:
                irmao = pai.filho_esquerdo

                if irmao.cor == VERMELHO:
                    irmao.cor = PRETO
                    pai.cor = VERMELHO
                    self.rotacao_direita(pai)
                    irmao = pai.filho_esquerdo

                if irmao.filho_direito.cor == PRETO and irmao.filho_esquerdo.cor == PRETO:
                    irmao.cor = VERMELHO
                    no_atual = pai
                else:
                    if irmao.filho_esquerdo.cor == PRETO:
                        irmao.filho_direito.cor = PRETO
                        irmao.cor = VERMELHO
                        self.rotacao_esquerda(irmao)
                        irmao = pai.filho_esquerdo

                    irmao.cor = pai.cor
                    pai.cor = PRETO
                    irmao.filho_esquerdo.cor = PRETO
                    self.rotacao_direita(pai)
                    no_atual = self.raiz

        no_atual.cor = PRETO

    def imprimir(self):
        print("\nRELATÓRIO DA ÁRVORE RUBRO-NEGRA\n")

        if self.raiz == self.NIL:
            print("Árvore vazia.")
            return

        fila = [self.raiz]

        while fila:
            no_atual = fila.pop(0)

            pai = no_atual.pai.valor if no_atual.pai else None
            esquerdo = no_atual.filho_esquerdo.valor if no_atual.filho_esquerdo != self.NIL else "NIL"
            direito = no_atual.filho_direito.valor if no_atual.filho_direito != self.NIL else "NIL"

            print(f"Nó: {no_atual.valor}")
            print(f"  Cor: {no_atual.cor}")
            print(f"  Pai: {pai}")
            print(f"  Filho esquerdo: {esquerdo}")
            print(f"  Filho direito: {direito}")
            print("-" * 30)

            if no_atual.filho_esquerdo != self.NIL:
                fila.append(no_atual.filho_esquerdo)
            if no_atual.filho_direito != self.NIL:
                fila.append(no_atual.filho_direito)

def teste_automatico():
    arvore = ArvoreRubroNegra()

    valores = [40, 20, 60, 10, 30, 50, 70]
    for valor in valores:
        arvore.inserir_simples(valor)

    print("Árvore inicial:")
    arvore.imprimir()

    print("\nRemovendo o nó 40 (dois filhos):")
    arvore.remover(40)
    arvore.imprimir()

    print("\nRemovendo o nó 10 (folha):")
    arvore.remover(10)
    arvore.imprimir()

teste_automatico()
