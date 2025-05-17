from collections import deque
import heapq
from utils import PuzzleSolverBase

class UninformedSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def bfs(self, start):
        if start == self.goal_state:
            return []
        queue = deque([(start, [])])
        seen = set([start])
        while queue:
            current, path = queue.popleft()
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    if new_state not in seen:
                        if new_state == self.goal_state:
                            return path + [move]
                        queue.append((new_state, path + [move]))
                        seen.add(new_state)
        return None

    def dfs(self, start, max_depth=50):
        if start == self.goal_state:
            return []
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
        if start == self.goal_state:
            return []
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

    def ids(self, start, max_depth_limit=50):
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
        while depth <= max_depth_limit:
            visited = set([start])
            result = dls(start, depth, [], visited)
            if result is not None:
                return result
            depth += 1
        return None