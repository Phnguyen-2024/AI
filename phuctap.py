import random
import heapq
import itertools
from collections import deque
from utils import PuzzleSolverBase

class ComplexSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def observe(self, state, noise_probability=0.1):
        blank_i, blank_j = self.find_blank(state)
        neighbors = {}
        for move, (di, dj) in self.step.items():
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                if random.random() < noise_probability:
                    neighbors[move] = random.randint(0, 8)
                else:
                    neighbors[move] = state[new_i][new_j]
        return (blank_i, blank_j), neighbors

    def partially_observable_search(self, initial_percept, noise_probability=0.1, max_belief_size=100):
        def generate_all_states():
            perms = list(itertools.permutations(range(9)))
            states = []
            for perm in perms:
                state = [[perm[i * 3 + j] for j in range(3)] for i in range(3)]
                states.append(tuple(tuple(row) for row in state))
            return states

        def states_matching_observation(observation):
            blank_pos, neighbors = observation
            blank_i, blank_j = blank_pos
            matching_states = []
            for state in generate_all_states():
                if state[blank_i][blank_j] != 0:
                    continue
                match = True
                for move, value in neighbors.items():
                    di, dj = self.step[move]
                    new_i, new_j = blank_i + di, blank_j + dj
                    if 0 <= new_i < 3 and 0 <= new_j < 3:
                        if state[new_i][new_j] != value:
                            match = False
                            break
                    else:
                        match = False
                        break
                if match:
                    matching_states.append(state)
            return set(random.sample(matching_states, min(len(matching_states), max_belief_size)))

        def predict(belief_state, action):
            new_belief = set()
            for state in belief_state:
                new_state = self.apply_move(state, action)
                if new_state != state:
                    new_belief.add(new_state)
            return new_belief

        def possible_percepts(belief_state):
            percepts = set()
            for state in belief_state:
                percept = self.observe(state, noise_probability)
                percepts.add(tuple(percept))
            return percepts

        def update(predicted_belief, percept):
            percept = tuple(percept)
            new_belief = set()
            for state in predicted_belief:
                state_percept = tuple(self.observe(state, noise_probability))
                if state_percept == percept:
                    new_belief.add(state)
            return new_belief

        def limit_belief_state(belief_state):
            if len(belief_state) <= max_belief_size:
                return belief_state
            state_scores = [(state, self.heuristic(state)) for state in belief_state]
            state_scores.sort(key=lambda x: x[1])
            return set(state for state, _ in state_scores[:max_belief_size])

        def belief_heuristic(belief_state):
            if not belief_state:
                return float('inf')
            total_h = sum(self.heuristic(state) for state in belief_state)
            return total_h / len(belief_state)

        def contains_goal(belief_state):
            return self.goal_state in belief_state

        initial_belief = states_matching_observation(initial_percept)
        initial_belief = limit_belief_state(initial_belief)

        pq = [(belief_heuristic(initial_belief), 0, initial_belief, [])]
        g_map = {frozenset(initial_belief): 0}
        visited = set()
        while pq:
            f, g, belief_state, path = heapq.heappop(pq)
            belief_key = frozenset(belief_state)
            if belief_key in visited:
                continue
            visited.add(belief_key)

            if contains_goal(belief_state):
                return path

            for action in self.step.keys():
                predicted_belief = predict(belief_state, action)
                if not predicted_belief:
                    continue
                percepts = possible_percepts(predicted_belief)
                for percept in percepts:
                    new_belief = update(predicted_belief, percept)
                    new_belief = limit_belief_state(new_belief)
                    if new_belief:
                        new_g = g + 1
                        belief_key = frozenset(new_belief)
                        if belief_key not in g_map or new_g < g_map[belief_key]:
                            g_map[belief_key] = new_g
                            h = belief_heuristic(new_belief)
                            f = new_g + h
                            heapq.heappush(pq, (f, new_g, new_belief, path + [action]))

        return None

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
                    return None
            path.append(best_move)
            current = best_neighbor
            iteration += 1
        return None

    def search_no_observation(self, start):
        # Placeholder for search with no observation
        return None

    def and_or_search(self, start):
        # Placeholder for AND-OR search
        return None