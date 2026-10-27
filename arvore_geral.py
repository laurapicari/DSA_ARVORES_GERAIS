print("Nome: Laura Pícari - RM: 569914")




class NoGeral:
    def __init__(self, dado):
        self.dado = dado
        self.filhos = []

    def adicionar_filho(self, filho):
        self.filhos.append(filho)


class ArvoreGeral:
    def __init__(self):
        self.raiz = None

    def criar_raiz(self, dado):
        if self.raiz is not None:
            raise ValueError("A árvore já possui raiz.")
        self.raiz = NoGeral(dado)
        return self.raiz

    def inserir(self, pai, dado):
        if pai is None:
            raise ValueError("Nó pai não informado.")
        novo = NoGeral(dado)
        pai.adicionar_filho(novo)
        return novo

    def pre_ordem(self, no):
        if no is None:
            return
        print(no.dado)
        for filho in no.filhos:
            self.pre_ordem(filho)

    def mostrar(self, no, nivel=0):
        if no is None:
            return
        print("    " * nivel + str(no.dado))
        for filho in no.filhos:
            self.mostrar(filho, nivel + 1)

    def buscar(self, no, valor):
        if no is None:
            return None
        if no.dado == valor:
            return no
        for filho in no.filhos:
            encontrado = self.buscar(filho, valor)
            if encontrado is not None:
                return encontrado
        return None

    def contar_nos(self, no):
        if no is None:
            return 0
        total = 1                  # o próprio nó
        for filho in no.filhos:
            total += self.contar_nos(filho)
        return total

    def altura(self, no):
        """Convenção: árvore vazia = 0; folha = 1."""
        if no is None:
            return 0
        maior_altura = 0
        for filho in no.filhos:
            altura_filho = self.altura(filho)
            if altura_filho > maior_altura:
                maior_altura = altura_filho
        return 1 + maior_altura

    def listar_folhas(self, no):
        if no is None:
            return
        if len(no.filhos) == 0:
            print(no.dado)
            return
        for filho in no.filhos:
            self.listar_folhas(filho)

    def inserir_por_valor(self, valor_pai, dado):
        pai = self.buscar(self.raiz, valor_pai)
        if pai is None:
            return None
        return self.inserir(pai, dado)


    def contar_folhas(self, no):
        """Quantidade de nós sem filhos."""
        if no is None:
            return 0
        if len(no.filhos) == 0:
            return 1
        total = 0
        for filho in no.filhos:
            total += self.contar_folhas(filho)
        return total

    def grau_arvore(self, no):
        """Maior quantidade de filhos de um único nó da árvore."""
        if no is None:
            return 0
        grau = len(no.filhos)
        for filho in no.filhos:
            grau_filho = self.grau_arvore(filho)
            if grau_filho > grau:
                grau = grau_filho
        return grau



def teste_integrado():
    arvore = ArvoreGeral()
    instituicao = arvore.criar_raiz("Instituição")
    graduacao = arvore.inserir(instituicao, "Graduação")
    pos = arvore.inserir(instituicao, "Pós-graduação")
    arvore.inserir(graduacao, "Ciência da Computação")
    arvore.inserir(graduacao, "Sistemas de Informação")
    arvore.inserir(pos, "Mestrado")
    arvore.inserir_por_valor("Graduação", "Engenharia de Software")

    print("HIERARQUIA:")
    arvore.mostrar(arvore.raiz)
    print("TOTAL:", arvore.contar_nos(arvore.raiz))
    print("ALTURA:", arvore.altura(arvore.raiz))
    print("FOLHAS:")
    arvore.listar_folhas(arvore.raiz)
    resultado = arvore.buscar(arvore.raiz, "Mestrado")
    print("BUSCA:", resultado.dado if resultado else "Não encontrado")


    assert arvore.contar_nos(arvore.raiz) == 7
    assert arvore.altura(arvore.raiz) == 3
    assert len(arvore.raiz.filhos) == 2
    assert len(graduacao.filhos) == 3
    assert arvore.buscar(arvore.raiz, "Mestrado") is not None
    assert arvore.buscar(arvore.raiz, "Doutorado") is None
    assert arvore.contar_folhas(arvore.raiz) == 4


    antes = arvore.contar_nos(arvore.raiz)
    assert arvore.inserir_por_valor("Inexistente", "X") is None
    assert arvore.contar_nos(arvore.raiz) == antes


    vazia = ArvoreGeral()
    assert vazia.contar_nos(vazia.raiz) == 0
    assert vazia.altura(vazia.raiz) == 0
    assert vazia.contar_folhas(vazia.raiz) == 0
    assert vazia.grau_arvore(vazia.raiz) == 0
    assert vazia.buscar(vazia.raiz, "A") is None
    assert vazia.inserir_por_valor("A", "B") is None


    so_raiz = ArvoreGeral()
    so_raiz.criar_raiz("Única")
    assert so_raiz.contar_nos(so_raiz.raiz) == 1
    assert so_raiz.altura(so_raiz.raiz) == 1
    assert so_raiz.contar_folhas(so_raiz.raiz) == 1
    assert so_raiz.grau_arvore(so_raiz.raiz) == 0


    try:
        so_raiz.criar_raiz("Outra")
        raise AssertionError("deveria ter lançado ValueError")
    except ValueError:
        pass

    print("\nTestes de validação: OK")



def desafio():
    arvore = ArvoreGeral()
    instituicao = arvore.criar_raiz("Instituição")

    graduacao = arvore.inserir(instituicao, "Graduação")
    pos = arvore.inserir(instituicao, "Pós-graduação")
    administracao = arvore.inserir(instituicao, "Administração")

    arvore.inserir(graduacao, "Ciência da Computação")
    arvore.inserir(graduacao, "Sistemas de Informação")
    arvore.inserir(graduacao, "Engenharia de Software")

    arvore.inserir(pos, "Especialização")
    arvore.inserir(pos, "Mestrado")

    arvore.inserir(administracao, "Secretaria")
    arvore.inserir(administracao, "Biblioteca")

    print("\n" + "=" * 50)
    print("ESTRUTURA ACADÊMICA AMPLIADA")
    print("=" * 50)
    arvore.mostrar(arvore.raiz)

    nos = arvore.contar_nos(arvore.raiz)
    alt = arvore.altura(arvore.raiz)
    folhas = arvore.contar_folhas(arvore.raiz)
    grau = arvore.grau_arvore(arvore.raiz)
    print(f"Nós: {nos} | Altura: {alt} | Folhas: {folhas} | Grau: {grau}")

    assert (nos, alt, folhas, grau) == (11, 3, 7, 3)
    print("Desafio: OK (11 nós, altura 3, 7 folhas, grau 3)")


if __name__ == "__main__":
    teste_integrado()
    desafio()
