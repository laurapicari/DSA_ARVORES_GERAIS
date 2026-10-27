print("Nome: Laura Pícari - RM: 569914")


class No:
    def __init__(self, valor):
        self.valor = valor
        self.esquerda = None
        self.direita = None


OPERADORES = ("+", "-", "*", "/", "^")


def eh_operador(token):
    return isinstance(token, str) and token in OPERADORES


def tokenizar(expressao):
    if expressao is None or expressao.strip() == "":
        raise ValueError("expressão vazia.")

    tokens = []
    i = 0
    n = len(expressao)

    while i < n:
        c = expressao[i]

        if c.isspace():
            i += 1
            continue

        anterior = tokens[-1] if tokens else None
        sinal_unario = (
            c == "-"
            and (anterior is None or anterior == "(" or eh_operador(anterior))
            and i + 1 < n
            and (expressao[i + 1].isdigit() or expressao[i + 1] == ".")
        )

        if c.isdigit() or c == "." or sinal_unario:
            inicio = i
            if sinal_unario:
                i += 1
            pontos = 0
            while i < n and (expressao[i].isdigit() or expressao[i] == "."):
                if expressao[i] == ".":
                    pontos += 1
                i += 1
            texto = expressao[inicio:i]
            if pontos > 1 or not any(ch.isdigit() for ch in texto):
                raise ValueError(f"número inválido: '{texto}'.")
            tokens.append(texto)
            continue

        if c in OPERADORES or c in "()":
            tokens.append(c)
            i += 1
            continue

        raise ValueError(f"caractere não aceito: '{c}' (posição {i}).")

    return tokens


def precedencia(operador):
    if operador == "^":
        return 3
    if operador in ("*", "/"):
        return 2
    if operador in ("+", "-"):
        return 1
    return 0


def para_posfixa(tokens):
    saida = []
    pilha = []

    for token in tokens:
        if token == "(":
            pilha.append(token)
        elif token == ")":
            while pilha and pilha[-1] != "(":
                saida.append(pilha.pop())
            if not pilha:
                raise ValueError("parênteses incompatíveis: ')' sem '(' correspondente.")
            pilha.pop()
        elif eh_operador(token):
            while pilha and pilha[-1] != "(":
                topo = pilha[-1]
                if precedencia(topo) > precedencia(token) or (
                    precedencia(topo) == precedencia(token) and token != "^"
                ):
                    saida.append(pilha.pop())
                else:
                    break
            pilha.append(token)
        else:
            saida.append(token)

    while pilha:
        topo = pilha.pop()
        if topo == "(":
            raise ValueError("parênteses incompatíveis: '(' sem ')' correspondente.")
        saida.append(topo)

    return saida


def converter_numero(token):
    return float(token) if "." in token else int(token)


def construir_arvore(posfixa):
    if not posfixa:
        raise ValueError("expressão vazia.")

    pilha = []
    for token in posfixa:
        if eh_operador(token):
            if len(pilha) < 2:
                raise ValueError(f"expressão malformada: faltam operandos para '{token}'.")
            direita = pilha.pop()
            esquerda = pilha.pop()
            no = No(token)
            no.esquerda = esquerda
            no.direita = direita
            pilha.append(no)
        else:
            pilha.append(No(converter_numero(token)))

    if len(pilha) != 1:
        raise ValueError("expressão malformada: faltam operadores ou há operandos sobrando.")
    return pilha[0]


def formatar(valor):
    if isinstance(valor, float):
        if valor == int(valor) and abs(valor) < 1e15:
            return str(int(valor))
        return str(round(valor, 10))
    return str(valor)


def pre_ordem(no):
    if no is None:
        return []
    return [formatar(no.valor)] + pre_ordem(no.esquerda) + pre_ordem(no.direita)


def em_ordem(no):
    if no is None:
        return []
    return em_ordem(no.esquerda) + [formatar(no.valor)] + em_ordem(no.direita)


def pos_ordem(no):
    if no is None:
        return []
    return pos_ordem(no.esquerda) + pos_ordem(no.direita) + [formatar(no.valor)]


def gerar_expressao(no):
    if no.esquerda is None and no.direita is None:
        return formatar(no.valor)
    return f"({gerar_expressao(no.esquerda)} {no.valor} {gerar_expressao(no.direita)})"


def calcular(no):
    if no.esquerda is None and no.direita is None:  # folha
        return no.valor

    a = calcular(no.esquerda)
    b = calcular(no.direita)

    if no.valor == "+":
        return a + b
    if no.valor == "-":
        return a - b
    if no.valor == "*":
        return a * b
    if no.valor == "/":
        if b == 0:
            raise ZeroDivisionError("divisão por zero.")
        return a / b
    if no.valor == "^":
        try:
            resultado = a ** b
        except ZeroDivisionError:
            raise ZeroDivisionError("zero elevado a expoente negativo.")
        except OverflowError:
            raise ValueError("resultado grande demais na potência.")
        if isinstance(resultado, complex):
            raise ValueError("potência com resultado não real.")
        return resultado

    raise ValueError(f"operador desconhecido: '{no.valor}'.")


def mostrar_arvore(no, nivel=0):
    if no is None:
        return
    mostrar_arvore(no.direita, nivel + 1)
    print("    " * nivel + formatar(no.valor))
    mostrar_arvore(no.esquerda, nivel + 1)


def contar_nos(no):
    if no is None:
        return 0
    return 1 + contar_nos(no.esquerda) + contar_nos(no.direita)


def contar_folhas(no):
    if no is None:
        return 0
    if no.esquerda is None and no.direita is None:
        return 1
    return contar_folhas(no.esquerda) + contar_folhas(no.direita)


def altura(no):
    if no is None:
        return 0
    return 1 + max(altura(no.esquerda), altura(no.direita))


def processar(expressao, exibir=True):
    tokens = tokenizar(expressao)
    posfixa = para_posfixa(tokens)
    raiz = construir_arvore(posfixa)
    resultado = calcular(raiz)

    if exibir:
        print("\nTokens reconhecidos:")
        print(" ", tokens)
        print("Pós-fixa:")
        print(" ", " ".join(posfixa))
        print("Pré-ordem:")
        print(" ", " ".join(pre_ordem(raiz)))
        print("Em ordem:")
        print(" ", " ".join(em_ordem(raiz)))
        print("Pós-ordem:")
        print(" ", " ".join(pos_ordem(raiz)))
        print("Expressão reconstruída:")
        print(" ", gerar_expressao(raiz))
        print("Árvore (raiz à esquerda):")
        mostrar_arvore(raiz)
        print(f"Nós: {contar_nos(raiz)} | Folhas: {contar_folhas(raiz)} | Altura: {altura(raiz)}")
        print("Resultado (calculado pela árvore):")
        print(" ", formatar(resultado))

    return resultado


def executar_testes():
    print("=" * 60)
    print("Testes Obrigatórios")
    print("=" * 60)

    casos = [
        ("8 + 4 * 2", 16),
        ("(8 + 4) * 2", 24),
        ("((15 - 3) / 4) + (2 * 5)", 13),
        ("((20 / 5) + 3) * (9 - (2 + 1))", 42),
        ("12.5 + 2.5 * 4", 22.5),
        ("((8 + 4) * (10 - 6))", 48),
        ("10 - 3 - 2", 5),
        ("100 / 10 / 5", 2),
        ("2 ^ 3 ^ 2", 512),
        ("-3 + 5", 2),
        ("(-2) * 4", -8),
        (" 7*(2+3) ", 35),
    ]

    falhas = 0
    for i, (expr, esperado) in enumerate(casos, 1):
        obtido = processar(expr, exibir=False)
        ok = abs(obtido - esperado) < 1e-9
        falhas += 0 if ok else 1
        print(f"Teste {i:2d}: {expr:<34} esperado={formatar(esperado):<5} "
              f"obtido={formatar(obtido):<5} {'OK' if ok else 'FALHOU'}")

    print("\n" + "=" * 60)
    print("Testes de Validação")
    print("=" * 60)

    invalidos = [
        ("8 / (4 - 4)", "divisão por zero"),
        ("", "expressão vazia"),
        (" ", "expressão vazia"),
        ("(8 + 4", "parêntese aberto sem fechar"),
        ("8 + 4)", "parêntese fechado sem abrir"),
        ("8 + a", "caractere não aceito"),
        ("8 + * 2", "operador sem operando"),
        ("8 4", "operandos sem operador"),
        ("()", "parênteses vazios"),
        ("1.2.3 + 1", "número malformado"),
        ("8 +", "operador sem segundo operando"),
    ]

    for expr, descricao in invalidos:
        try:
            processar(expr, exibir=False)
            print(f"FALHOU : '{expr}' ({descricao}) foi aceita!")
            falhas += 1
        except (ValueError, ZeroDivisionError) as erro:
            print(f"OK : '{expr}' ({descricao}) -> {erro}")

    print("\n" + ("Todos os testes passaram." if falhas == 0 else f"{falhas} teste(s) falharam."))
    print()
    return falhas == 0


def main():
    executar_testes()
    print("Calculadora de Expressões com Árvore Binária")
    print("Operadores: + - * / ^ e parênteses. Digite 'sair' para encerrar.")

    while True:
        try:
            expressao = input("\nDigite uma expressão: ")
        except EOFError:
            break
        if expressao.strip().lower() == "sair":
            break
        try:
            processar(expressao)
        except ZeroDivisionError as erro:
            print(f"Erro: {erro}")
        except ValueError as erro:
            print(f"Erro: {erro}")

    print("Encerrado.")


if __name__ == "__main__":
    main()