from utils import PuzzleSolverBase

class ConstraintSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

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

        for i in range(3):
            for j in range(3):
                domains[(i, j)] = [self.initial_state[i][j]]

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
        result = tuple(tuple(row) for row in state)
        return result if result == self.goal_state else None

    def backtracking_search(self, start, max_depth=50):
        def backtrack(state, path, depth, visited):
            if state == self.goal_state:
                return path
            if depth > max_depth:
                return None
            blank_i, blank_j = self.find_blank(state)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    if new_state not in visited:
                        visited.add(new_state)
                        result = backtrack(new_state, path + [move], depth + 1, visited)
                        if result is not None:
                            return result
                        visited.remove(new_state)
            return None

        visited = set([start])
        return backtrack(start, [], 0, visited)

    def kiem_tra(self, start):
        # Placeholder for kiểm thử algorithm
        return None