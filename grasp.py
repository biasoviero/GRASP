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
    

    def get_neighbors(self) -> List['Solution']:
        neighbors = []

        for i in range(1, self.n + 1):
            if not self.solution[i]:  # Pular espaços vazios
                continue

            for attraction_id in self.solution[i]:
                for j in range(1, self.n + 1):
                    if i != j and self.available_spaces[j] >= self.attractions[attraction_id]['dimensao']:
                        new_solution = Solution(self.n, self.M, self.attractions)
                        new_solution.solution = {k: v.copy() for k, v in self.solution.items()}
                        new_solution.available_spaces = self.available_spaces.copy()

                        # Realiza a troca
                        new_solution.solution[i].remove(attraction_id)
                        new_solution.solution[j].append(attraction_id)
                        new_solution.available_spaces[i] += self.attractions[attraction_id]['dimensao']
                        new_solution.available_spaces[j] -= self.attractions[attraction_id]['dimensao']

                        neighbors.append(new_solution)

        return neighbors


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
        candidates = [
            (i, 
             1 if any(attraction['tematica'] == solution.attractions[j]['tematica'] for attraction_id in solution.solution[i] for attraction in [solution.attractions[attraction_id]]) else 0, 
             solution.available_spaces[i])
            for i in solution.available_spaces 
            if solution.available_spaces[i] >= solution.attractions[j]['dimensao']
        ]
        candidates.sort(key=lambda x: (x[1], x[2]), reverse=True)
        limit = max(1, int(len(candidates) * alpha))
        selected = random.choice(candidates[:limit])[0] if candidates else None
        if selected:
            solution.assign_attraction(selected, j)

def local_search(initial_solution: Solution, max_depth: int, explored: set, alpha: float) -> Solution:
    improved = True
    while True:
        if not improved:
            break
        improved = False

        neighbors = initial_solution.get_neighbors()
        for neighbor in neighbors:
            if neighbor not in explored:
                explored.add(neighbor)
                new_dispersion = neighbor.calculate_dispersion()
                if new_dispersion < initial_solution.calculate_dispersion():
                    initial_solution = neighbor
                    improved = True
                    break

    return initial_solution

def grasp(n: int, M: int, T: int, m: int, attractions: List[Dict[str, int]], random_seed: int, max_iterations: int, alpha: float, max_time: int, file_path: str):
    random.seed(random_seed)
    explored = set()
    start_time = time.time()
    stoppedByTime = False

    initial_solution = Solution(n, M, attractions)
    randomized_greedy_construction(initial_solution, alpha)
    initial_dispersion = initial_solution.calculate_dispersion()
    best_dispersion = initial_dispersion
    best_solution = initial_solution
    avg_dispersion = initial_dispersion

    for i in range(max_iterations - 1):
        if time.time() - start_time > max_time:
            print('Tempo limite atingido. Encerrando')
            stoppedByTime = True
            break

        solution = Solution(n, M, attractions)
        randomized_greedy_construction(solution, alpha)
        dispersion = solution.calculate_dispersion()
        avg_dispersion += dispersion

        if solution in explored:
            continue

        local_solution = local_search(solution, 100, explored, alpha)
        dispersion = local_solution.calculate_dispersion()

        if dispersion < best_dispersion:
            best_solution = local_solution
            best_dispersion = dispersion
            elapsed_time = time.time() - start_time
            print(f"Iteração {i}: Melhor dispersão encontrada: {best_dispersion}")
            print(f"Tempo decorrido: {elapsed_time:.2f} segundos")

    elapsed_time = time.time() - start_time
    avg_dispersion /= i + 1

    print("Instância:", file_path.split('/')[-1])  # Extract instance name from file path
    print(f"Valor da semente de aleatoriedade: {random_seed}")
    print(f"Solução inicial da meta-heurística - Dispersão Si: {initial_dispersion}")
    print(f"Melhor solução encontrada pela meta-heurística - Dispersão Sh: {best_dispersion}")
    print(f"Tempo de execução da meta-heurística (segundos) H T (s).: {elapsed_time:.2f} s")
    print(f"Valor médio da solução encontrada pela formulação Sf: {avg_dispersion}")  # Assuming dispersion as the formulation solution value
    print(f"Limite superior caso termine por limite de tempo Uf: {best_dispersion if stoppedByTime else 'N/A'}")  # No upper bound if completed on time
    print(f"Tempo médio de execução da formulação (segundos) F T (s): {elapsed_time / i:.2f} s")  # Average execution time across iterations (if applicable)

    return best_solution, best_dispersion



def main():
    parser = argparse.ArgumentParser(description="Executa o algoritmo GRASP para eventos.")
    parser.add_argument('-f', '--filepath', type=str, required=True, help='Caminho para o arquivo da instância')
    parser.add_argument('-s', '--seed', type=int, required=True, help='Seed de aleatoriedade')
    parser.add_argument('-t', '--max-time', type=int, required=True, help='Tempo máximo de execução em segundos')
    parser.add_argument('-m', '--max-iterations', type=int, required=True, help='Máximo de iterações a serem executadas')
    parser.add_argument('-a', '--alpha', type=float, required=True, help='Fator de aleatoriedade (alpha) usado no GRASP')

    args = parser.parse_args()

    file_path = args.filepath
    random_seed = args.seed
    max_time = args.max_time
    max_iterations = args.max_iterations
    alpha = args.alpha

    n, M, T, m, attractions = read_file(file_path)
    best_solution, best_dispersion = grasp(n, M, T, m, attractions, random_seed, max_iterations, alpha, max_time, file_path)

    print("Melhor solução encontrada:")
    print(f"Solução: {best_solution.solution}")
    print(f"Dispersão: {best_dispersion}")

if __name__ == "__main__":
    main()
