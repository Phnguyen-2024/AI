import heapq
from utils import PuzzleSolverBase

class InformedSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

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