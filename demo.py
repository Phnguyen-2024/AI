import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq
import time
import random
import math

class PuzzleSolver:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.step = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return None

    def swap(self, state, i1, j1, i2, j2):
        new_state = [list(row) for row in state]
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        return tuple(tuple(row) for row in new_state)

    def apply_move(self, state, move):
        blank_i, blank_j = self.find_blank(state)
        di, dj = self.step[move]
        new_i, new_j = blank_i + di, blank_j + dj
        if 0 <= new_i < 3 and 0 <= new_j < 3:
            return self.swap(state, blank_i, blank_j, new_i, new_j)
        return state

    def apply_moves(self, state, moves):
        current = state
        for move in moves:
            current = self.apply_move(current, move)
        return current

    def bfs(self, start):
        queue = deque([(start, [])])
        seen = set([start])
        while queue:
            current, path = queue.popleft()
            if current == self.goal_state:
                return path
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    if new_state not in seen:
                        queue.append((new_state, path + [move]))
                        seen.add(new_state)
        return None

    def dfs(self, start, max_depth=50):
        stack = [(start, [])]
        seen = set()
        while stack:
            current, path = stack.pop()
            if current == self.goal_state:
                return path
            if len(path) > max_depth:
                continue
            if current in seen:
                continue
            seen.add(current)
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    stack.append((new_state, path + [move]))
        return None

    def ucs(self, start):
        pq = [(0, start, [])]
        cost_map = {start: 0}
        while pq:
            cost, current, path = heapq.heappop(pq)
            if current == self.goal_state:
                return path
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    new_cost = cost + 1
                    if new_state not in cost_map or new_cost < cost_map[new_state]:
                        cost_map[new_state] = new_cost
                        heapq.heappush(pq, (new_cost, new_state, path + [move]))
        return None

    def ids(self, start):
        def dls(state, depth, path, visited):
            if state == self.goal_state:
                return path
            if depth <= 0:
                return None
            blank_i, blank_j = self.find_blank(state)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    if new_state not in visited:
                        visited.add(new_state)
                        result = dls(new_state, depth - 1, path + [move], visited)
                        if result is not None:
                            return result
            return None

        depth = 0
        while True:
            visited = set([start])
            result = dls(start, depth, [], visited)
            if result is not None:
                return result
            depth += 1
            if depth > 50:
                return None

    def heuristic(self, state):
        goal_positions = {}
        for i in range(3):
            for j in range(3):
                value = self.goal_state[i][j]
                if value != 0:
                    goal_positions[value] = (i, j)
        total_distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    gi, gj = goal_positions[value]
                    total_distance += abs(i - gi) + abs(j - gj)
        return total_distance

    def greedy(self, start):
        pq = [(self.heuristic(start), start, [])]
        seen = set()
        while pq:
            _, current, path = heapq.heappop(pq)
            if current == self.goal_state:
                return path
            if current in seen:
                continue
            seen.add(current)
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    if new_state not in seen:
                        heapq.heappush(pq, (self.heuristic(new_state), new_state, path + [move]))
        return None

    def a_star(self, start):
        pq = [(self.heuristic(start), 0, start, [])]
        g_map = {start: 0}
        visited = set()
        while pq:
            f, g, current, path = heapq.heappop(pq)
            if current == self.goal_state:
                return path
            if current in visited:
                continue
            visited.add(current)
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    new_g = g + 1
                    if new_state not in g_map or new_g < g_map[new_state]:
                        g_map[new_state] = new_g
                        h = self.heuristic(new_state)
                        f = new_g + h
                        heapq.heappush(pq, (f, new_g, new_state, path + [move]))
        return None

    def ida_star(self, start):
        def search(state, g, bound, visited, path):
            h = self.heuristic(state)
            f = g + h
            if f > bound:
                return None, f
            if state == self.goal_state:
                return path, f
            min_bound = float('inf')
            blank_i, blank_j = self.find_blank(state)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    if new_state not in visited:
                        visited.add(new_state)
                        new_path = path + [move]
                        result, next_bound = search(new_state, g + 1, bound, visited, new_path)
                        if result is not None:
                            return result, f
                        min_bound = min(min_bound, next_bound)
            return None, min_bound

        bound = self.heuristic(start)
        while True:
            visited = set([start])
            result, new_bound = search(start, 0, bound, visited, [])
            if result is not None:
                return result
            if new_bound == float('inf'):
                return None
            bound = new_bound

    def simple_hill_climbing(self, start):
        current = start
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
            if current == self.goal_state:
                path = []
                temp = start
                while temp != current:
                    blank_i, blank_j = self.find_blank(temp)
                    for move, (di, dj) in self.step.items():
                        new_i, new_j = blank_i + di, blank_j + dj
                        if 0 <= new_i < 3 and 0 <= new_j < 3:
                            next_state = self.swap(temp, blank_i, blank_j, new_i, new_j)
                            if self.heuristic(next_state) < self.heuristic(temp):
                                path.append(move)
                                temp = next_state
                                break
                return path

    def steepest_ascent_hill_climbing(self, start):
        current = start
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
            if current == self.goal_state:
                path = []
                temp = start
                while temp != current:
                    blank_i, blank_j = self.find_blank(temp)
                    for move, (di, dj) in self.step.items():
                        new_i, new_j = blank_i + di, blank_j + dj
                        if 0 <= new_i < 3 and 0 <= new_j < 3:
                            next_state = self.swap(temp, blank_i, blank_j, new_i, new_j)
                            if self.heuristic(next_state) < self.heuristic(temp):
                                path.append(move)
                                temp = next_state
                                break
                return path

    def stochastic_hill_climbing(self, start, max_iterations=1000):
        current = start
        iterations = 0
        while iterations < max_iterations:
            current_h = self.heuristic(current)
            if current == self.goal_state:
                path = []
                temp = start
                while temp != current:
                    blank_i, blank_j = self.find_blank(temp)
                    for move, (di, dj) in self.step.items():
                        new_i, new_j = blank_i + di, blank_j + dj
                        if 0 <= new_i < 3 and 0 <= new_j < 3:
                            next_state = self.swap(temp, blank_i, blank_j, new_i, new_j)
                            if self.heuristic(next_state) < self.heuristic(temp):
                                path.append(move)
                                temp = next_state
                                break
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
            iterations += 1
        return None

    def simulated_annealing(self, start, initial_temp=1000, cooling_rate=0.99, min_temp=0.01, max_iterations=10000):
        current = start
        current_h = self.heuristic(current)
        best = current
        best_h = current_h
        temp = initial_temp
        iterations = 0
        path = []
        while temp > min_temp and iterations < max_iterations:
            if current == self.goal_state:
                return path
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
                path.append(move)
                if current_h < best_h:
                    best = current
                    best_h = current_h
            temp *= cooling_rate
            iterations += 1
        if best_h < self.heuristic(start):
            return path
        return None

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
            return trimmed

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
        trimmed_path = trim_path(start, best_individual)
        return trimmed_path if trimmed_path else None

    def and_or_graph_search(self, start, max_depth=50):
        def or_search(state, path, visited, depth):
            if depth > max_depth:
                return None
            if state == self.goal_state:
                return path
            if state in visited:
                return None
            visited.add(state)
            blank_i, blank_j = self.find_blank(state)
            successors = []
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    successors.append((move, new_state))
            for move, new_state in successors:
                result = or_search(new_state, path + [move], visited, depth + 1)
                if result is not None:
                    return result
            return None

        visited = set()
        return or_search(start, [], visited, 0)
    

    def backtracking_search(self, start, max_depth=50):
        def backtrack(current, path, visited, depth):
            if current == self.goal_state:
                return path
            if depth > max_depth:
                return None
            if current in visited:
                return None
            visited.add(current)
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    result = backtrack(new_state, path + [move], visited, depth + 1)
                    if result is not None:
                        return result
            return None

        visited = set()
        return backtrack(start, [], visited, 0)
    

    def tabu_search(self, start, tabu_size=100, max_iterations=1000):
        current = start
        path = []
        tabu_list = deque(maxlen=tabu_size)
        iteration = 0
        while iteration < max_iterations:
            if current == self.goal_state:
                return path
            tabu_list.append(current)
            best_neighbor = None
            best_move = None
            best_h = float('inf')
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    if new_state not in tabu_list:
                        h = self.heuristic(new_state)
                        if h < best_h:
                            best_h = h
                            best_neighbor = new_state
                            best_move = move
            if best_neighbor is None:
                possible_moves = []
                for move, (di, dj) in self.step.items():
                    new_i, new_j = blank_i + di, blank_j + dj
                    if 0 <= new_i < 3 and 0 <= new_j < 3:
                        new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                        if new_state not in tabu_list:
                            possible_moves.append((new_state, move))
                if possible_moves:
                    best_neighbor, best_move = random.choice(possible_moves)
                else:
                    break
            path.append(best_move)
            current = best_neighbor
            iteration += 1
        return None

    def csp_ac3(self):
        variables = [(i, j) for i in range(3) for j in range(3)]
        domains = {var: list(range(9)) for var in variables}
        constraints = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        if (i, j) != (k, l):
                            constraints.append(((i, j), (k, l), lambda x, y: x != y))

        queue = [(Xi, Xj) for Xi in variables for Xj in variables if Xi != Xj and any(c[0] == Xi and c[1] == Xj for c in constraints)]
        while queue:
            (Xi, Xj) = queue.pop(0)
            revised = False
            to_remove = []
            for x in domains[Xi]:
                support = False
                for y in domains[Xj]:
                    if any(c[2](x, y) for c in constraints if c[0] == Xi and c[1] == Xj):
                        support = True
                        break
                if not support:
                    to_remove.append(x)
                    revised = True
            for x in to_remove:
                domains[Xi].remove(x)
            if revised:
                if len(domains[Xi]) == 0:
                    return None
                for Xk in variables:
                    if Xk != Xi and any(c[0] == Xk and c[1] == Xi for c in constraints):
                        if (Xk, Xi) not in queue:
                            queue.append((Xk, Xi))

        assignment = {}
        for var in variables:
            if len(domains[var]) == 1:
                assignment[var] = domains[var][0]
            else:
                return None

        state = [[0] * 3 for _ in range(3)]
        for (i, j), val in assignment.items():
            state[i][j] = val
        return tuple(tuple(row) for row in state)


def get_state_from_entries(entries):
    numbers = []
    state = []
    for i in range(3):
        row = []
        for j in range(3):
            try:
                num_str = entries[i][j].get()
                if not num_str.isdigit() or len(num_str) != 1:
                    raise ValueError("Invalid input")
                num = int(num_str)
                if num < 0 or num > 8:
                    raise ValueError("Number out of range")
                row.append(num)
                numbers.append(num)
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input for cell ({i+1},{j+1}): {e}")
                return None
        state.append(row)
    if len(set(numbers)) != 9:
        messagebox.showerror("Input Error", "Duplicate numbers or missing numbers")
        return None
    return tuple(tuple(row) for row in state)

delay = 0.5
paused = False
running = False

def update_view(state):
    for i in range(3):
        for j in range(3):
            tile = view_labels[i][j]
            value = state[i][j]
            tile.config(
                text=str(value) if value != 0 else "",
                bg="#D4F0F0" if value == 0 else "#FFFFFF",
                fg="#000000"
            )

def create_state_grid(parent, state_3x3):
    for i in range(3):
        for j in range(3):
            val = state_3x3[i][j]
            bg_color = "#D4F0F0" if val == 0 else "#FFFFFF"
            lbl = tk.Label(
                parent,
                text=str(val) if val != 0 else "",
                width=3,
                height=1,
                font=("Arial", 14, "bold"),
                bg=bg_color,
                fg="#000000",
                bd=2,
                relief="solid"
            )
            lbl.grid(row=i, column=j, padx=2, pady=2)

step_count = 0
current_row_frame = None

def add_step_frame(index, move_, state_3x3):
    global step_count, current_row_frame
    if step_count % 7 == 0:
        current_row_frame = tk.Frame(steps_container, bg="#FFFFFF")
        current_row_frame.pack(side="top", padx=5, pady=5)
    step_frame = tk.Frame(current_row_frame, bg="#FFFFFF", bd=2, relief="groove")
    step_frame.pack(side="left", padx=5, pady=5)
    lbl_title = tk.Label(
        step_frame,
        text=f"Bước {index}",
        font=("Arial", 12, "bold"),
        fg="#000000",
        bg="#FFFFFF"
    )
    lbl_title.pack(side="top", anchor="w", padx=5, pady=2)
    grid_holder = tk.Frame(step_frame, bg="#FFFFFF")
    grid_holder.pack(side="left", padx=5, pady=5)
    create_state_grid(grid_holder, state_3x3)
    step_count += 1

def pause_program():
    global paused
    paused = True

def resume_program():
    global paused
    paused = False

def reset_program():
    global running, paused, step_count, current_row_frame
    running = False
    paused = False
    step_count = 0
    current_row_frame = None
    selected_algorithm.set("")
    for i in range(3):
        for j in range(3):
            initial_entries[i][j].delete(0, tk.END)
            goal_entries[i][j].delete(0, tk.END)
    for child in steps_container.winfo_children():
        child.destroy()
    blank_state = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    update_view(blank_state)
    steps_count.config(text="Số bước: 0")
    time_label.config(text="Thời gian: 00:00")
    verification_label.config(text="Verification: ")

# def solve(algorithm_name):
#     global result, paused, running, step_count, current_row_frame
#     running = True
#     step_count = 0
#     current_row_frame = None
#     for child in steps_container.winfo_children():
#         child.destroy()
#     lbl_all_steps = tk.Label(
#         steps_container,
#         font=("Arial", 14, "bold"),
#         fg="#000000",
#         bg="#FFFFFF"
#     )
#     lbl_all_steps.pack(side="top", pady=5)

#     initial_state = get_state_from_entries(initial_entries)
#     if initial_state is None:
#         return
#     goal_state = get_state_from_entries(goal_entries)
#     if goal_state is None:
#         return
#     result = goal_state
#     update_view(initial_state)

#     solver = PuzzleSolver(initial_state, goal_state)
#     algorithm = getattr(solver, algorithm_name)
#     start_time = time.time()
#     solution = algorithm(initial_state)

#     if solution is not None:
#         final_state = solver.apply_moves(initial_state, solution)
#         if final_state == goal_state:
#             verification_result = "Correct"
#         else:
#             verification_result = "Incorrect"
#     else:
#         verification_result = "No solution"
#     verification_label.config(text=f"Verification: {verification_result}")

#     if solution:
#         current_state = initial_state
#         add_step_frame(0, "Start", current_state)
#         for i, move_ in enumerate(solution, start=1):
#             if not running:
#                 break
#             while paused and running:
#                 root.update()
#                 time.sleep(0.1)
#             root.update()
#             time.sleep(delay)
#             blank_i, blank_j = solver.find_blank(current_state)
#             new_state = solver.swap(current_state, blank_i, blank_j,
#                                    blank_i + solver.step[move_][0],
#                                    blank_j + solver.step[move_][1])
#             update_view(new_state)
#             current_state = new_state
#             add_step_frame(i, move_, new_state)
#         if running:
#             steps_count.config(text=f"Số bước: {len(solution)}")
#             total_time = time.time() - start_time
#             time_label.config(text=f"Thời gian: {total_time:.2f}s")
#     else:
#         steps_count.config(text="Số bước: 0")
#         time_label.config(text="Thời gian: 0s")
#         messagebox.showinfo("Kết quả", "Không tìm thấy giải pháp!")

def solve(algorithm_name):
    global result, paused, running, step_count, current_row_frame
    running = True
    step_count = 0
    current_row_frame = None
    for child in steps_container.winfo_children():
        child.destroy()
    lbl_all_steps = tk.Label(
        steps_container,
        font=("Arial", 14, "bold"),
        fg="#000000",
        bg="#FFFFFF"
    )
    lbl_all_steps.pack(side="top", pady=5)

    initial_state = get_state_from_entries(initial_entries)
    if initial_state is None:
        return
    goal_state = get_state_from_entries(goal_entries)
    if goal_state is None:
        return
    result = goal_state
    update_view(initial_state)

    solver = PuzzleSolver(initial_state, goal_state)
    algorithm = getattr(solver, algorithm_name)
    start_time = time.time()

    if algorithm_name == "csp_ac3":
        solution = algorithm()
        if solution is not None:
            final_state = solution
            if final_state == goal_state:
                verification_result = "Correct"
                add_step_frame(0, "Start", initial_state)
                add_step_frame(1, "Solved", final_state)
                update_view(final_state)
                steps_count.config(text="Số bước: 1 (CSP)")
                total_time = time.time() - start_time
                time_label.config(text=f"Thời gian: {total_time:.2f}s")
            else:
                verification_result = "Incorrect"
                messagebox.showinfo("Kết quả", "Giải pháp không khớp với mục tiêu!")
        else:
            verification_result = "No solution"
            steps_count.config(text="Số bước: 0")
            time_label.config(text="Thời gian: 0s")
            messagebox.showinfo("Kết quả", "Không tìm thấy giải pháp!")
        verification_label.config(text=f"Verification: {verification_result}")
    else:
        solution = algorithm(initial_state)
        if solution is not None:
            final_state = solver.apply_moves(initial_state, solution)
            if final_state == goal_state:
                verification_result = "Correct"
            else:
                verification_result = "Incorrect"
        else:
            verification_result = "No solution"
        verification_label.config(text=f"Verification: {verification_result}")

        if solution:
            current_state = initial_state
            add_step_frame(0, "Start", current_state)
            for i, move_ in enumerate(solution, start=1):
                if not running:
                    break
                while paused and running:
                    root.update()
                    time.sleep(0.1)
                root.update()
                time.sleep(delay)
                blank_i, blank_j = solver.find_blank(current_state)
                new_state = solver.swap(current_state, blank_i, blank_j,
                                       blank_i + solver.step[move_][0],
                                       blank_j + solver.step[move_][1])
                update_view(new_state)
                current_state = new_state
                add_step_frame(i, move_, new_state)
            if running:
                steps_count.config(text=f"Số bước: {len(solution)}")
                total_time = time.time() - start_time
                time_label.config(text=f"Thời gian: {total_time:.2f}s")
        else:
            steps_count.config(text="Số bước: 0")
            time_label.config(text="Thời gian: 0s")
            messagebox.showinfo("Kết quả", "Không tìm thấy giải pháp!")

# Thiết lập GUI
root = tk.Tk()
root.title("23110271_Trần Hồ Phương Nguyên 8-Puzzle Solver")
root.geometry("1000x600")
root.configure(bg="#F0F0F0")

# Frame cho nhập liệu
input_frame = tk.Frame(root, bg="#F0F0F0")
input_frame.pack(side="left", padx=10, pady=10, fill="y")

# Trạng thái ban đầu
initial_frame = tk.Frame(input_frame, bg="#F0F0F0")
initial_frame.pack(pady=5)
tk.Label(initial_frame, text="Trạng thái ban đầu", font=("Arial", 14, "bold"), bg="#F0F0F0").pack()
initial_entries = []
for i in range(3):
    row = []
    frame = tk.Frame(initial_frame, bg="#F0F0F0")
    frame.pack()
    for j in range(3):
        entry = tk.Entry(frame, width=3, font=("Arial", 12), justify="center")
        entry.pack(side="left", padx=2, pady=2)
        row.append(entry)
    initial_entries.append(row)

# Trạng thái mục tiêu
goal_frame = tk.Frame(input_frame, bg="#F0F0F0")
goal_frame.pack(pady=5)
tk.Label(goal_frame, text="Trạng thái mục tiêu", font=("Arial", 14, "bold"), bg="#F0F0F0").pack()
goal_entries = []
for i in range(3):
    row = []
    frame = tk.Frame(goal_frame, bg="#F0F0F0")
    frame.pack()
    for j in range(3):
        entry = tk.Entry(frame, width=3, font=("Arial", 12), justify="center")
        entry.pack(side="left", padx=2, pady=2)
        row.append(entry)
    goal_entries.append(row)

# Lựa chọn thuật toán
algo_frame = tk.Frame(input_frame, bg="#F0F0F0")
algo_frame.pack(pady=10)
tk.Label(algo_frame, text="Chọn thuật toán", font=("Arial", 14, "bold"), bg="#F0F0F0").pack()
selected_algorithm = tk.StringVar()
algorithms = [
    ("BFS", "bfs"),
    ("DFS", "dfs"),
    ("UCS", "ucs"),
    ("IDS", "ids"),
    ("Greedy", "greedy"),
    ("A*", "a_star"),
    ("IDA*", "ida_star"),
    ("Simple Hill Climbing", "simple_hill_climbing"),
    ("Steepest Ascent Hill Climbing", "steepest_ascent_hill_climbing"),
    ("Stochastic Hill Climbing", "stochastic_hill_climbing"),
    ("Simulated Annealing", "simulated_annealing"),
    ("Beam Search", "beam_search"),
    ("Genetic Algorithm", "genetic_algorithm"),
    ("And-Or Graph Search", "and_or_graph_search"),
    ("Backtracking Search","backtracking_search"),
    ("Tabu Search","tabu_search"),
    ("AC-3","csp_ac3")
]
for algo_name, algo_value in algorithms:
    tk.Radiobutton(algo_frame, text=algo_name, variable=selected_algorithm, value=algo_value,
                   font=("Arial", 12), bg="#F0F0F0").pack(anchor="w")

# Frame hiển thị
display_frame = tk.Frame(root, bg="#F0F0F0")
display_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

# Thông tin
info_frame = tk.Frame(display_frame, bg="#F0F0F0")
info_frame.pack(fill="x")
steps_count = tk.Label(info_frame, text="Số bước: 0", font=("Arial", 12), bg="#F0F0F0")
steps_count.pack(side="left", padx=10)
time_label = tk.Label(info_frame, text="Thời gian: 00:00", font=("Arial", 12), bg="#F0F0F0")
time_label.pack(side="left", padx=10)
verification_label = tk.Label(info_frame, text="Verification: ", font=("Arial", 12), bg="#F0F0F0")
verification_label.pack(side="left", padx=10)

# Trạng thái hiện tại
view_frame = tk.Frame(display_frame, bg="#F0F0F0")
view_frame.pack(pady=10)
tk.Label(view_frame, text="Trạng thái hiện tại", font=("Arial", 14, "bold"), bg="#F0F0F0").pack()
view_labels = []
for i in range(3):
    row = []
    frame = tk.Frame(view_frame, bg="#F0F0F0")
    frame.pack()
    for j in range(3):
        label = tk.Label(
            frame,
            text="",
            width=3,
            height=1,
            font=("Arial", 14, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            bd=2,
            relief="solid"
        )
        label.pack(side="left", padx=2, pady=2)
        row.append(label)
    view_labels.append(row)

# Nút điều khiển (di chuyển vào display_frame, trước steps_frame)
control_frame = tk.Frame(display_frame, bg="#F0F0F0")
control_frame.pack(pady=10)
tk.Button(control_frame, text="Solve", command=lambda: solve(selected_algorithm.get()),
          font=("Arial", 10), bg="#4CAF50", fg="white").pack(side="left", padx=5)
tk.Button(control_frame, text="Pause", command=pause_program,
          font=("Arial", 10), bg="#FFC107", fg="black").pack(side="left", padx=5)
tk.Button(control_frame, text="Resume", command=resume_program,
          font=("Arial", 10), bg="#2196F3", fg="white").pack(side="left", padx=5)
tk.Button(control_frame, text="Reset", command=reset_program,
          font=("Arial", 10), bg="#F44336", fg="white").pack(side="left", padx=5)

# Các bước giải
steps_frame = tk.Frame(display_frame, bg="#F0F0F0")
steps_frame.pack(fill="both", expand=True)
tk.Label(steps_frame, text="Các bước giải", font=("Arial", 12, "bold"), bg="#F0F0F0").pack()
canvas = tk.Canvas(steps_frame, bg="#FFFFFF")
scrollbar = tk.Scrollbar(steps_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#FFFFFF")
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
steps_container = scrollable_frame

root.mainloop()