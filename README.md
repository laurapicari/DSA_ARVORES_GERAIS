# atividade_DSA_05-10

***
# ANÁLISE - ÁRVORE BINÁRIA
***
### 1) Por que a expressão precisa ser tokenizada?
#### Porque o programa recebe uma string de caracteres, e os operandos podem ter vários caracteres. Sem tokenizar, "15" seria lido como '1' e '5' separados, e "12.5" seria quebrado no ponto. A tokenização agrupa os caracteres em unidades com significado (números, operadores, parênteses), ignora espaços e é o ponto onde caracteres inválidos são detectados. As etapas seguintes (pós-fixa e árvore) trabalham com tokens, não com caracteres soltos.
***
### 2) Por que uma pilha é adequada para operadores e parênteses?
#### Porque a ordem de resolução segue o princípio LIFO: o último '(' aberto é o primeiro a ser fechado, e o operador de maior prioridade empilhado mais recentemente é o primeiro a ser aplicado. A pilha guarda os operadores "pendentes" e devolve primeiro o mais recente, o que reproduz o alinhamento dos parênteses e permite comparar o operador atual com o topo para respeitar precedência e associatividade.
***
### 3) Por que o primeiro pop na construção da árvore corresponde ao filho direito?
#### Na pós-fixa os operandos aparecem na ordem "esquerdo, direito, operador". Ao empilhar, o operando direito é o último a entrar e, portanto, o primeiro  a sair (LIFO). Assim, o 1º pop é o direito e o 2º é o esquerdo. Inverter isso trocaria a ordem dos operandos e quebraria operações não comutativas: "8 3 -" viraria 3 - 8 = -5 em vez de 8 - 3 = 5.
***
### 4) Qual a relação entre pós-ordem e notação pós-fixa?
#### São a mesma sequência. A pós-ordem visita esquerda, direita e depois a raiz; a pós-fixa escreve os operandos antes do operador. Percorrer a árvore de expressão em pós ordem devolve exatamente a pós-fixa que a gerou (ex.: 8 4 2 * +). Analogamente, pré-ordem equivale à prefixa e em ordem equivale à infixa (sem os parênteses).
***
### 5) Para uma árvore com n nós, qual a complexidade de tempo para calcular toda a expressão? Justifique.
#### O(n). A função calcular visita cada nó exatamente uma vez: cada chamada faz um trabalho de tempo constante (uma comparação e uma operação aritmética) e depois delega para os dois filhos. Como o total de chamadas é n, o tempo total é n * O(1) = O(n).
***
### 6) O que determina a quantidade máxima de chamadas recursivas simultâneas?
#### A altura h da árvore. As chamadas ativas ao mesmo tempo formam um caminho da raiz até um nó (cada chamada espera os filhos terminarem), então no máximo h chamadas ficam empilhadas. O uso de memória da pilha de recursão é O(h): em árvore balanceada h ~ log n; no pior caso (árvore degenerada, como em 1+2+3+4+...) h ~ n. Em Python, isso importa porque o limite padrão de recursão é cerca de 1000 chamadas.
***

***
# ANÁLISE - ÁRVORE GERAL
***
### Diferença entre nó e raiz:
#### Nó é qualquer elemento da árvore. Raiz é o nó do topo, o único sem pai, a árvore guarda apenas a referência a ele (self.raiz) e chega aos demais a partir dele.
***
### Significado de no.esquerda e no.direita:
#### São as referências do nó aos seus dois filhos na árvore binária, a subárvore esquerda e a direita. Valem None quando não há filho.
***
### Por que uma função recursiva recebe um nó:
#### Porque cada chamada trata uma subárvore: o nó recebido é a raiz dessa subárvore. Assim o mesmo código serve para a árvore inteira e para qualquer parte dela, e o caso base (no is None) encerra a descida.
***
### Como um percurso visita todos os nós:
#### Visita o nó atual e chama a si mesmo para cada filho, cada filho faz o mesmo para os seus. A ordem das chamadas, antes, entre ou depois do processamento do nó, define pré-ordem, em ordem ou pós-ordem.
***
### O que mudar para permitir cinco filhos:
#### Na árvore binária seria preciso criar mais atributos fixos, o que é rígido. A solução é trocar esquerda/direita por uma lista de filhos (self.filhos = []), que aceita qualquer quantidade, e trocar as duas chamadas recursivas por um laço for sobre a lista.
***
