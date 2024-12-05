import sys
import time
import random
from typing import List, Dict, Tuple

def ler_arquivo(nome_arquivo: str) -> Tuple[int, int, int, int, List[Dict[str, int]]]:
    with open(nome_arquivo, 'r') as arquivo:
        linhas = arquivo.readlines()
    n = int(linhas[0].strip())  # Número de espaços
    M = int(linhas[1].strip())  # Metragem de cada espaço
    T = int(linhas[2].strip())  # Número de temáticas
    m = int(linhas[3].strip())  # Número de atrações
    
    atracoes = []
    for linha in linhas[4:]:
        t, d = map(int, linha.strip().split())
        atracoes.append({'tematica': t, 'dimensao': d})
    return n, M, T, m, atracoes

def calcular_dispersao(solucao: Dict[int, List[int]], atracoes: List[Dict[str, int]]) -> int:
    dispersao = 0
    tematicas_por_espaco = {i: set() for i in solucao}
    for espaco, atracoes_ids in solucao.items():
        for j in atracoes_ids:
            tematicas_por_espaco[espaco].add(atracoes[j]['tematica'])
    
    todas_tematicas = set(range(1, max([atr['tematica'] for atr in atracoes]) + 1))
    for tematica in todas_tematicas:
        dispersao += sum(1 for espaco in tematicas_por_espaco if tematica in tematicas_por_espaco[espaco])
    return dispersao

def construcao_gulosa_randomizada(n, M, atracoes, alpha):
    solucao = {i: [] for i in range(1, n + 1)}
    espacos_disponiveis = {i: M for i in range(1, n + 1)}
    atracoes_ids = list(range(len(atracoes)))
    random.shuffle(atracoes_ids)
    
    for j in atracoes_ids:
        candidatos = [(i, espacos_disponiveis[i] - atracoes[j]['dimensao']) 
                      for i in espacos_disponiveis if espacos_disponiveis[i] >= atracoes[j]['dimensao']]
        candidatos.sort(key=lambda x: x[1])
        limite = max(1, int(len(candidatos) * alpha))
        selecionado = random.choice(candidatos[:limite])[0] if candidatos else None
        if selecionado:
            solucao[selecionado].append(j)
            espacos_disponiveis[selecionado] -= atracoes[j]['dimensao']
    return solucao

def busca_local(solucao, n, M, atracoes):
    melhor_solucao = solucao
    melhor_dispersao = calcular_dispersao(solucao, atracoes)
    for _ in range(100):
        novo_solucao = construcao_gulosa_randomizada(n, M, atracoes, 0.5)
        nova_dispersao = calcular_dispersao(novo_solucao, atracoes)
        if nova_dispersao < melhor_dispersao:
            melhor_solucao = novo_solucao
            melhor_dispersao = nova_dispersao
    return melhor_solucao

def grasp(n, M, T, m, atracoes, semente, criterio_parada, tipo_parada, alpha):
    random.seed(semente)
    melhor_solucao = None
    melhor_dispersao = float('inf')
    inicio = time.time()
    iteracao = 0
    
    while True:
        iteracao += 1
        solucao_inicial = construcao_gulosa_randomizada(n, M, atracoes, alpha)
        solucao = busca_local(solucao_inicial, n, M, atracoes)
        dispersao = calcular_dispersao(solucao, atracoes)
        
        if dispersao < melhor_dispersao:
            melhor_solucao = solucao
            melhor_dispersao = dispersao
            print(f"Iteração {iteracao}: Melhor dispersão encontrada: {melhor_dispersao}")
        
        if tipo_parada == "tempo":
            if time.time() - inicio >= criterio_parada:
                break
        elif tipo_parada == "iteracoes":
            if iteracao >= criterio_parada:
                break
    
    return melhor_solucao, melhor_dispersao

def main():
    if len(sys.argv) != 6:
        print("Uso: python grasp_eventos.py <arquivo_entrada> <semente> <criterio_parada> <tipo_parada> <alpha>")
        sys.exit(1)
    
    nome_arquivo = sys.argv[1]
    semente = int(sys.argv[2])
    criterio_parada = float(sys.argv[3])
    tipo_parada = sys.argv[4]
    alpha = float(sys.argv[5])
    
    n, M, T, m, atracoes = ler_arquivo(nome_arquivo)
    melhor_solucao, melhor_dispersao = grasp(n, M, T, m, atracoes, semente, criterio_parada, tipo_parada, alpha)
    
    print("Melhor solução encontrada:")
    print(f"Solução: {melhor_solucao}")
    print(f"Dispersão: {melhor_dispersao}")

if __name__ == "__main__":
    main()
