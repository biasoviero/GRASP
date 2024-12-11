import sys
import argparse
import time
import random
from typing import List, Dict, Tuple
from collections import defaultdict

class Solution:
    def __init__(self, n: int, M: int, attractions: List[Dict[str, int]]):
        self.n = n
        self.M = M
        self.attractions = attractions
        self.solution = {i: [] for i in range(1, n + 1)}
        self.available_spaces = {i: M for i in range(1, n + 1)}

    def assign_attraction(self, space: int, attraction_id: int):
        self.solution[space].append(attraction_id)
        self.available_spaces[space] -= self.attractions[attraction_id]['dimensao']

    def calculate_dispersion(self) -> int:
        themes_by_space = defaultdict(set)
        for space, attractions_ids in self.solution.items():
            for j in attractions_ids:
                themes_by_space[space].add(self.attractions[j]['tematica'])

        dispersion = 0
        themes = set(range(1, max(atr['tematica'] for atr in self.attractions) + 1))
        for theme in themes:
            dispersion += sum(1 for space in themes_by_space if theme in themes_by_space[space])
        return dispersion

def read_file(file_path: str) -> Tuple[int, int, int, int, List[Dict[str, int]]]:
    with open(file_path, 'r') as file:
        lines = file.readlines()
    n = int(lines[0].strip())  # Número de espaços
    M = int(lines[1].strip())  # Metragem de cada espaço
    T = int(lines[2].strip())  # Número de temáticas
    m = int(lines[3].strip())  # Número de atrações

    attractions = []
    for line in lines[4:]:
        t, d = map(int, line.strip().split())
        attractions.append({'tematica': t, 'dimensao': d})
    return n, M, T, m, attractions

def randomized_greedy_construction(solution: Solution, alpha: float):
    attractions_ids = list(range(len(solution.attractions)))
    random.shuffle(attractions_ids)

    for j in attractions_ids:
        candidates = [(i, solution.available_spaces[i] - solution.attractions[j]['dimensao']) 
                      for i in solution.available_spaces if solution.available_spaces[i] >= solution.attractions[j]['dimensao']]
        candidates.sort(key=lambda x: x[1])
        limit = max(1, int(len(candidates) * alpha))
        selected = random.choice(candidates[:limit])[0] if candidates else None
        if selected:
            solution.assign_attraction(selected, j)

def local_search(initial_solution: Solution, max_depth: int, max_no_improve: int) -> Solution:
    optimal_solution = initial_solution
    best_dispersion = initial_solution.calculate_dispersion()

    for _ in range(max_depth):
        new_solution = Solution(initial_solution.n, initial_solution.M, initial_solution.attractions)
        randomized_greedy_construction(new_solution, 0.5)
        new_dispersion = new_solution.calculate_dispersion()

        if new_dispersion < best_dispersion:
            optimal_solution = new_solution
            best_dispersion = new_dispersion

    return optimal_solution

def grasp(n: int, M: int, T: int, m: int, attractions: List[Dict[str, int]], random_seed: int, max_iterations: int, alpha: float, max_local_search_depth: int, max_no_improve: int):
    random.seed(random_seed)
    best_solution = None
    best_dispersion = float('inf')
    start_time = time.time()

    for i in range(max_iterations):
        if time.time() - start_time > 300:
            print('Tempo limite atingido. Encerrando')
            break

        initial_solution = Solution(n, M, attractions)
        randomized_greedy_construction(initial_solution, alpha)
        local_solution = local_search(initial_solution, max_local_search_depth, max_no_improve)
        dispersion = local_solution.calculate_dispersion()

        if dispersion < best_dispersion:
            best_solution = local_solution
            best_dispersion = dispersion
            elapsed_time = time.time() - start_time
            print(f"Iteração {i}: Melhor dispersão encontrada: {best_dispersion}")
            print(f"Tempo decorrido: {elapsed_time:.2f} segundos")

    return best_solution, best_dispersion

def main():
    parser = argparse.ArgumentParser(description="Executa o algoritmo GRASP para eventos.")
    parser.add_argument('-f', '--filepath', type=str, required=True, help='Caminho para o arquivo da instância')
    parser.add_argument('-s', '--seed', type=int, required=True, help='Seed de aleatoriedade')
    parser.add_argument('-m', '--max-iterations', type=int, required=True, help='Máximo de iterações a serem executadas')
    parser.add_argument('-a', '--alpha', type=float, required=True, help='Fator de aleatoriedade (alpha) usado no GRASP')
    parser.add_argument('-l', '--max-local-search-depth', type=int, required=False, default=100, help='Profundidade máxima da busca local (padrão: 100)')

    args = parser.parse_args()

    # Lendo os argumentos
    file_path = args.filepath
    random_seed = args.seed
    max_iterations = args.max_iterations
    alpha = args.alpha
    max_local_search_depth = args.max_local_search_depth
    max_no_improve = args.max_no_improve

    # Executando as funções
    n, M, T, m, attractions = read_file(file_path)
    best_solution, best_dispersion = grasp(n, M, T, m, attractions, random_seed, max_iterations, alpha, max_local_search_depth, max_no_improve)

    print("Melhor solução encontrada:")
    print(f"Solução: {best_solution.solution}")
    print(f"Dispersão: {best_dispersion}")

if __name__ == "__main__":
    main()
