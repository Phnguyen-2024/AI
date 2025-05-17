import random
import heapq
import math
from utils import PuzzleSolverBase

class LocalSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def simple_hill_climbing(self, start):
        current = start
        path = []
        while True:
            current_h = self.heuristic(current)
            best_move = None
            best_state = None
            best_h = current_h
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    h = self.heuristic(new_state)
                    if h < best_h:
                        best_h = h
                        best_state = new_state
                        best_move = move
            if best_state is None or best_h >= current_h:
                return None
            current = best_state
            path.append(best_move)
            if current == self.goal_state:
                return path

    def steepest_ascent_hill_climbing(self, start):
        current = start
        path = []
        while True:
            current_h = self.heuristic(current)
            best_move = None
            best_state = None
            best_h = float('inf')
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    h = self.heuristic(new_state)
                    if h < best_h:
                        best_h = h
                        best_state = new_state
                        best_move = move
            if best_state is None or best_h >= current_h:
                return None
            current = best_state
            path.append(best_move)
            if current == self.goal_state:
                return path

    def stochastic_hill_climbing(self, start, max_iterations=1000):
        current = start
        iterations = 0
        path = []
        while iterations < max_iterations:
            current_h = self.heuristic(current)
            if current == self.goal_state:
                return path
            better_neighbors = []
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    h = self.heuristic(new_state)
                    if h < current_h:
                        better_neighbors.append((new_state, move))
            if not better_neighbors:
                return None
            next_state, next_move = random.choice(better_neighbors)
            current = next_state
            path.append(next_move)
            iterations += 1
        return None

    def simulated_annealing(self, start, initial_temp=1000, cooling_rate=0.99, min_temp=0.01, max_iterations=10000):
        current = start
        current_h = self.heuristic(current)
        best = current
        best_path = []
        temp = initial_temp
        iterations = 0
        while temp > min_temp and iterations < max_iterations:
            if current == self.goal_state:
                return best_path
            blank_i, blank_j = self.find_blank(current)
            neighbors = []
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    neighbors.append((new_state, move))
            next_state, move = random.choice(neighbors)
            next_h = self.heuristic(next_state)
            delta_h = next_h - current_h
            if delta_h < 0 or random.random() < math.exp(-delta_h / temp):
                current = next_state
                current_h = next_h
                if current_h < self.heuristic(best):
                    best = current
                    best_path.append(move)
                if current == self.goal_state:
                    return best_path
            temp *= cooling_rate
            iterations += 1
        return None if best != self.goal_state else best_path

    def beam_search(self, start, beam_width=2):
        beam = [(self.heuristic(start), start, [])]
        visited = set([start])
        while beam:
            next_beam = []
            for _, current, path in beam:
                if current == self.goal_state:
                    return path
                blank_i, blank_j = self.find_blank(current)
                for move, (di, dj) in self.step.items():
                    new_i, new_j = blank_i + di, blank_j + dj
                    if 0 <= new_i < 3 and 0 <= new_j < 3:
                        new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                        if new_state not in visited:
                            visited.add(new_state)
                            h = self.heuristic(new_state)
                            next_beam.append((h, new_state, path + [move]))
            next_beam.sort(key=lambda x: x[0])
            beam = next_beam[:beam_width]
            if not beam:
                return None
        return None

    def genetic_algorithm(self, start, population_size=100, max_generations=1000, mutation_rate=0.1, max_path_length=30):
        def generate_individual():
            length = random.randint(1, max_path_length)
            return [random.choice(list(self.step.keys())) for _ in range(length)]

        def fitness(moves):
            final_state = self.apply_moves(start, moves)
            h = self.heuristic(final_state)
            length_penalty = len(moves) * 0.1
            return -h - length_penalty

        def crossover(parent1, parent2):
            min_len = min(len(parent1), len(parent2))
            if min_len < 2:
                return parent1.copy()
            cut = random.randint(1, min_len - 1)
            child = parent1[:cut] + parent2[cut:]
            return child

        def mutate(individual):
            mutated = individual.copy()
            for i in range(len(mutated)):
                if random.random() < mutation_rate:
                    mutated[i] = random.choice(list(self.step.keys()))
            if random.random() < 0.1 and len(mutated) < max_path_length:
                mutated.append(random.choice(list(self.step.keys())))
            elif random.random() < 0.1 and len(mutated) > 1:
                mutated.pop(random.randint(0, len(mutated) - 1))
            return mutated

        def trim_path(state, moves):
            current = state
            trimmed = []
            seen_states = {current}
            for move in moves:
                next_state = self.apply_move(current, move)
                if next_state != current and next_state not in seen_states:
                    trimmed.append(move)
                    current = next_state
                    seen_states.add(current)
                if current == self.goal_state:
                    break
            return trimmed if current == self.goal_state else None

        population = [generate_individual() for _ in range(population_size)]
        for generation in range(max_generations):
            population_with_fitness = [(ind, fitness(ind)) for ind in population]
            population_with_fitness.sort(key=lambda x: x[1], reverse=True)
            best_individual, best_fitness = population_with_fitness[0]
            best_state = self.apply_moves(start, best_individual)
            if best_state == self.goal_state:
                return trim_path(start, best_individual)
            elite_size = max(1, population_size // 2)
            elite = [ind for ind, _ in population_with_fitness[:elite_size]]
            new_population = elite.copy()
            while len(new_population) < population_size:
                parent1, parent2 = random.sample(elite, 2)
                child = crossover(parent1, parent2)
                child = mutate(child)
                new_population.append(child)
            population = new_population
        best_individual = population_with_fitness[0][0]
        return trim_path(start, best_individual)