print("Nome: Laura Pícari - RM: 569914")


class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


class BST:
    def __init__(self):
        self.raiz = None


    def inserir(self, valor):
        self.raiz = self._inserir(self.raiz, valor)

    def _inserir(self, no, valor):
        if no is None:
            return No(valor)
        if valor < no.valor:
            no.esquerda = self._inserir(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._inserir(no.direita, valor)

        return no


    def buscar(self, valor):
        return self._buscar(self.raiz, valor)

    def _buscar(self, no, valor):
        if no is None:
            return None
        if valor == no.valor:
            return no
        if valor < no.valor:
            return self._buscar(no.esquerda, valor)
        return self._buscar(no.direita, valor)


    def pre_ordem(self, no="raiz"):
        no = self.raiz if no == "raiz" else no
        if no is None:
            return []
        return [no.valor] + self.pre_ordem(no.esquerda) + self.pre_ordem(no.direita)

    def em_ordem(self, no="raiz"):
        no = self.raiz if no == "raiz" else no
        if no is None:
            return []
        return self.em_ordem(no.esquerda) + [no.valor] + self.em_ordem(no.direita)

    def pos_ordem(self, no="raiz"):
        no = self.raiz if no == "raiz" else no
        if no is None:
            return []
        return self.pos_ordem(no.esquerda) + self.pos_ordem(no.direita) + [no.valor]


    def contar_nos(self, no="raiz"):
        no = self.raiz if no == "raiz" else no
        if no is None:
            return 0
        return 1 + self.contar_nos(no.esquerda) + self.contar_nos(no.direita)

    def altura(self, no="raiz"):
        no = self.raiz if no == "raiz" else no
        if no is None:
            return 0
        return 1 + max(self.altura(no.esquerda), self.altura(no.direita))

    def minimo(self):
        no = self.raiz
        if no is None:
            return None
        while no.esquerda is not None:
            no = no.esquerda
        return no.valor

    def maximo(self):
        no = self.raiz
        if no is None:
            return None
        while no.direita is not None:
            no = no.direita
        return no.valor


    def remover(self, valor):
        self.raiz = self._remover(self.raiz, valor)

    def _remover(self, no, valor):
        if no is None:
            return None
        if valor < no.valor:
            no.esquerda = self._remover(no.esquerda, valor)
        elif valor > no.valor:
            no.direita = self._remover(no.direita, valor)
        else:
            if no.esquerda is None:
                return no.direita
            if no.direita is None:
                return no.esquerda

            sucessor = no.direita
            while sucessor.esquerda is not None:
                sucessor = sucessor.esquerda
            no.valor = sucessor.valor
            no.direita = self._remover(no.direita, sucessor.valor)
        return no


    def mostrar(self, no="raiz", nivel=0):
        no = self.raiz if no == "raiz" else no
        if no is None:
            return
        self.mostrar(no.direita, nivel + 1)
        print("    " * nivel + str(no.valor))
        self.mostrar(no.esquerda, nivel + 1)


def main():
    arvore = BST()
    for v in [50, 30, 70, 20, 40, 60, 80, 30]:
        arvore.inserir(v)

    print("Árvore:")
    arvore.mostrar()
    print("Pré-ordem :", arvore.pre_ordem())
    print("Em ordem  :", arvore.em_ordem())
    print("Pós-ordem :", arvore.pos_ordem())
    print("Nós:", arvore.contar_nos(), "| Altura:", arvore.altura())
    print("Mínimo:", arvore.minimo(), "| Máximo:", arvore.maximo())

    assert arvore.em_ordem() == [20, 30, 40, 50, 60, 70, 80]
    assert arvore.contar_nos() == 7 and arvore.altura() == 3
    assert arvore.buscar(60) is not None and arvore.buscar(65) is None

    arvore.remover(20)
    arvore.remover(70)
    arvore.remover(50)
    print("Após remover 20, 70 e 50:", arvore.em_ordem())
    assert arvore.em_ordem() == [30, 40, 60, 80]

    vazia = BST()
    assert vazia.altura() == 0 and vazia.contar_nos() == 0
    assert vazia.minimo() is None and vazia.buscar(1) is None
    print("Testes da BST: OK")


if __name__ == "__main__":
    main()