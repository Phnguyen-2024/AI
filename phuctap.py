import random
import heapq
from collections import deque
from utils import PuzzleSolverBase


class ComplexSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def is_solvable(self, state):
        """Kiểm tra xem trạng thái có thể giải được không dựa trên số lần hoán vị."""
        flat_state = [num for row in state for num in row if num != 0]
        inversions = 0
        for i in range(len(flat_state)):
            for j in range(i + 1, len(flat_state)):
                if flat_state[i] > flat_state[j]:
                    inversions += 1
        return inversions % 2 == 0

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
        # Kiểm tra tính khả thi của trạng thái ban đầu
        if not self.is_solvable(self.initial_state):
            return None

        # Đảm bảo định dạng trạng thái
        self.initial_state = tuple(tuple(row) for row in self.initial_state)
        self.goal_state = tuple(tuple(row) for row in self.goal_state)

        def states_matching_observation(observation, current_belief):
            if not current_belief:
                return set()
            blank_pos, neighbors = observation
            blank_i, blank_j = blank_pos
            # Nếu neighbors là frozenset (từ possible_percepts), chuyển về dict
            if isinstance(neighbors, frozenset):
                neighbors = dict(neighbors)
            matching_states = set()
            for state in current_belief:
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
                    matching_states.add(state)
            return matching_states

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
                blank_i, blank_j = self.find_blank(state)
                neighbors = {}
                for move, (di, dj) in self.step.items():
                    new_i, new_j = blank_i + di, blank_j + dj
                    if 0 <= new_i < 3 and 0 <= new_j < 3:
                        neighbors[move] = state[new_i][new_j]
                percepts.add(((blank_i, blank_j), frozenset(neighbors.items())))
            return percepts

        def update(predicted_belief, percept):
            return states_matching_observation(percept, predicted_belief)

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

        # Initialize belief state
        initial_belief = {self.initial_state}
        initial_belief = states_matching_observation(initial_percept, initial_belief)
        initial_belief = limit_belief_state(initial_belief)

        if contains_goal(initial_belief):
            return []

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

    def search_no_observation(self, start, max_iterations=1000):
        # Đảm bảo định dạng trạng thái
        start = tuple(tuple(row) for row in start)
        if start == self.goal_state:
            return []
        
        # Kiểm tra tính khả thi
        if not self.is_solvable(start):
            return None

        current = start
        path = []
        iteration = 0
        while iteration < max_iterations:
            blank_i, blank_j = self.find_blank(current)
            possible_moves = []
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    possible_moves.append(move)
            if not possible_moves:
                return None
            move = random.choice(possible_moves)
            current = self.apply_move(current, move)
            path.append(move)
            if current == self.goal_state:
                return path
            iteration += 1
        return None

    def and_or_search(self, start, max_depth=50):
        # Đảm bảo định dạng trạng thái
        start = tuple(tuple(row) for row in start)
        if start == self.goal_state:
            return []
        
        # Kiểm tra tính khả thi
        if not self.is_solvable(start):
            return None

        def simulate_disturbance(state):
            blank_i, blank_j = self.find_blank(state)
            possible_moves = []
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    possible_moves.append(move)
            if possible_moves and random.random() < 0.2:  # 20% chance of disturbance
                move = random.choice(possible_moves)
                new_state = self.apply_move(state, move)
                # Kiểm tra tính khả thi sau nhiễu
                if self.is_solvable(new_state):
                    return new_state
            return state

        def search(state, path, depth, visited):
            if state == self.goal_state:
                return path
            if depth > max_depth:
                return None
            if state in visited:
                return None
            visited.add(state)
            blank_i, blank_j = self.find_blank(state)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    # Simulate disturbance (OR node)
                    disturbed_state = simulate_disturbance(new_state)
                    result = search(disturbed_state, path + [move], depth + 1, visited)
                    if result is not None:
                        return result
            return None

        visited = set()
        return search(start, [], 0, visited)