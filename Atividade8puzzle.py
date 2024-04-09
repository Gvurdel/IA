estado_inicial = [
    [1, 0, 3],
    [4, 2, 5],
    [7, 8, 6]
]

estado_final = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

# Função para encontrar a posição de um número em uma matriz

def encontrar_posicao(matriz, numero):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == numero:
                return (i, j)

# Heurística - Distância de Manhattan

def heuristica_distancia_manhattan(estado_atual):
    distancia_total = 0
    for i in range(len(estado_atual)):
        for j in range(len(estado_atual[i])):
            if estado_atual[i][j] != 0:
                pos_atual = (i, j)
                pos_final = encontrar_posicao(estado_final, estado_atual[i][j])
                distancia_total += abs(pos_atual[0] - pos_final[0]) + abs(pos_atual[1] - pos_final[1])
    return distancia_total

# Definindo ações possíveis

def acoes_possiveis(estado_atual):
    acoes = []
    linha, coluna = encontrar_posicao(estado_atual, 0)  # Encontra a posição do espaço vazio (0)
    movimentos = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Movimentos possíveis: baixo, cima, direita, esquerda
    
    for movimento in movimentos:
        nova_linha = linha + movimento[0]
        nova_coluna = coluna + movimento[1]
        if 0 <= nova_linha < len(estado_atual) and 0 <= nova_coluna < len(estado_atual[0]):
            novo_estado = [list(row) for row in estado_atual]  # Criar uma cópia do estado atual
            novo_estado[linha][coluna], novo_estado[nova_linha][nova_coluna] = novo_estado[nova_linha][nova_coluna], novo_estado[linha][coluna]
            acoes.append(novo_estado)
    
    return acoes

# Algoritmo A*

def busca_a_estrela(estado_inicial, estado_final):
    fronteira = [(0 + heuristica_distancia_manhattan(estado_inicial), estado_inicial)]  # Inicializa a fronteira com a heurística + custo inicial
    visitados = set()
    custo = {tuple(map(tuple, estado_inicial)): 0}  # Dicionário para armazenar o custo de cada estado
    caminho = {}  # Dicionário para armazenar o caminho percorrido

    while fronteira:
        custo_total, estado_atual = min(fronteira)  # Extrai o estado com menor custo total da fronteira
        fronteira.remove((custo_total, estado_atual))
        
        if tuple(map(tuple, estado_atual)) == tuple(map(tuple, estado_final)):  # Corrigido: comparar tuplas
            # Reconstrói o caminho percorrido
            solucao = []
            while tuple(map(tuple, estado_atual)) in caminho:  # Corrigido: verificar tuplas
                solucao.append(estado_atual)
                estado_atual = caminho[tuple(map(tuple, estado_atual))]  # Corrigido: usar tupla como chave
            solucao.append(estado_inicial)
            solucao.reverse()
            return solucao
        
        visitados.add(tuple(map(tuple, estado_atual)))  # Adiciona o estado atual aos visitados
        
        for prox_estado in acoes_possiveis(estado_atual):
            custo_prox_estado = custo[tuple(map(tuple, estado_atual))] + 1
            if tuple(map(tuple, prox_estado)) not in custo or custo_prox_estado < custo[tuple(map(tuple, prox_estado))]:
                custo[tuple(map(tuple, prox_estado))] = custo_prox_estado
                custo_total = custo_prox_estado + heuristica_distancia_manhattan(prox_estado)
                fronteira.append((custo_total, prox_estado))
                caminho[tuple(map(tuple, prox_estado))] = estado_atual

# Executando a busca A* e imprimindo a solução

solucao = busca_a_estrela(estado_inicial, estado_final)
for passo, estado in enumerate(solucao):
    print(f"Passo {passo}:")
    for linha in estado:
        print(linha)
    print()