# from utils import PuzzleSolverBase

# class ConstraintSearch(PuzzleSolverBase):
#     def __init__(self, initial_state, goal_state):
#         super().__init__(initial_state, goal_state)

#     def csp_ac3(self, max_depth=50):
#         # Hàm kiểm tra tính khả thi của trạng thái dựa trên số lần hoán vị
#         def is_solvable(state):
#             flat_state = [num for row in state for num in row if num != 0]
#             inversions = 0
#             for i in range(len(flat_state)):
#                 for j in range(i + 1, len(flat_state)):
#                     if flat_state[i] > flat_state[j]:
#                         inversions += 1
#             return inversions % 2 == 0

#         # Kiểm tra tính khả thi của trạng thái ban đầu
#         if not is_solvable(self.initial_state):
#             return None

#         # Định nghĩa biến và miền giá trị cho các ô
#         variables = [(i, j) for i in range(3) for j in range(3)]
#         domains = {var: list(range(9)) for var in variables}

#         # Gán giá trị ban đầu từ initial_state
#         for i in range(3):
#             for j in range(3):
#                 if self.initial_state[i][j] != 0:
#                     domains[(i, j)] = [self.initial_state[i][j]]

#         # Định nghĩa ràng buộc: mỗi số từ 0 đến 8 chỉ xuất hiện một lần
#         constraints = []
#         for i in range(3):
#             for j in range(3):
#                 for k in range(3):
#                     for l in range(3):
#                         if (i, j) != (k, l):
#                             constraints.append(((i, j), (k, l), lambda x, y: x != y))

#         # Thuật toán AC-3 để thực thi tính nhất quán cung
#         queue = [(Xi, Xj) for Xi in variables for Xj in variables if Xi != Xj and any(c[0] == Xi and c[1] == Xj for c in constraints)]
#         while queue:
#             Xi, Xj = queue.pop(0)
#             revised = False
#             to_remove = []
#             for x in domains[Xi]:
#                 support = False
#                 for y in domains[Xj]:
#                     if any(c[2](x, y) for c in constraints if c[0] == Xi and c[1] == Xj):
#                         support = True
#                         break
#                 if not support:
#                     to_remove.append(x)
#                     revised = True
#             for x in to_remove:
#                 if x in domains[Xi]:
#                     domains[Xi].remove(x)
#             if revised:
#                 if not domains[Xi]:
#                     return None  # Không có giải pháp
#                 for Xk in variables:
#                     if Xk != Xi and any(c[0] == Xk and c[1] == Xi for c in constraints):
#                         if (Xk, Xi) not in queue:
#                             queue.append((Xk, Xi))

#         # Kiểm tra nếu tất cả các ô đều được gán giá trị duy nhất
#         assignment = {}
#         for var in variables:
#             if len(domains[var]) == 1:
#                 assignment[var] = domains[var][0]
#             else:
#                 return None  # Trạng thái không thể giải quyết chỉ bằng AC-3

#         # Tạo trạng thái từ assignment
#         state = [[0] * 3 for _ in range(3)]
#         for (i, j), val in assignment.items():
#             state[i][j] = val
#         current_state = tuple(tuple(row) for row in state)

#         # Nếu trạng thái hiện tại là goal_state, trả về đường đi rỗng
#         if current_state == self.goal_state:
#             return []

#         # Sử dụng backtracking để tìm đường đi từ trạng thái ban đầu đến mục tiêu
#         def backtrack(state, path, depth, visited):
#             if state == self.goal_state:
#                 return path
#             if depth > max_depth:
#                 return None
#             blank_i, blank_j = self.find_blank(state)
#             for move, (di, dj) in self.step.items():
#                 new_i, new_j = blank_i + di, blank_j + dj
#                 if 0 <= new_i < 3 and 0 <= new_j < 3:
#                     new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
#                     if new_state not in visited:
#                         visited.add(new_state)
#                         result = backtrack(new_state, path + [move], depth + 1, visited)
#                         if result is not None:
#                             return result
#                         visited.remove(new_state)
#             return None

#         visited = set([self.initial_state])
#         return backtrack(self.initial_state, [], 0, visited)

#     def backtracking_search(self, start, max_depth=50):
#         if start == self.goal_state:
#             return []
#         def backtrack(state, path, depth, visited):
#             if state == self.goal_state:
#                 return path
#             if depth > max_depth:
#                 return None
#             blank_i, blank_j = self.find_blank(state)
#             for move, (di, dj) in self.step.items():
#                 new_i, new_j = blank_i + di, blank_j + dj
#                 if 0 <= new_i < 3 and 0 <= new_j < 3:
#                     new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
#                     if new_state not in visited:
#                         visited.add(new_state)
#                         result = backtrack(new_state, path + [move], depth + 1, visited)
#                         if result is not None:
#                             return result
#                         visited.remove(new_state)
#             return None

#         visited = set([start])
#         return backtrack(start, [], 0, visited)

#     def forward_checking(self, start, max_depth=50):
#         def forward_check(state, depth, path, visited):
#             if state == self.goal_state:
#                 return path
#             if depth > max_depth:
#                 return None
#             blank_i, blank_j = self.find_blank(state)
#             current_h = self.heuristic(state)
#             possible_moves = []
#             for move, (di, dj) in self.step.items():
#                 new_i, new_j = blank_i + di, blank_j + dj
#                 if 0 <= new_i < 3 and 0 <= new_j < 3:
#                     new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
#                     if new_state not in visited:
#                         new_h = self.heuristic(new_state)
#                         if new_h <= current_h:  # Prune if heuristic doesn't improve
#                             possible_moves.append((new_state, move))
#             for new_state, move in possible_moves:
#                 visited.add(new_state)
#                 result = forward_check(new_state, depth + 1, path + [move], visited)
#                 if result is not None:
#                     return result
#                 visited.remove(new_state)
#             return None

#         if start == self.goal_state:
#             return []
#         visited = set([start])
#         return forward_check(start, 0, [], visited)

from utils import PuzzleSolverBase

class ConstraintSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def csp_ac3(self, max_depth=50):
        initial_state = [list(row) for row in self.initial_state]
        def is_solvable(state):
            flat_state = [num for row in state for num in row if num != 0]
            inversions = 0
            for i in range(len(flat_state)):
                for j in range(i + 1, len(flat_state)):
                    if flat_state[i] > flat_state[j]:
                        inversions += 1
            return inversions % 2 == 0

        if not is_solvable(initial_state):
            return None

        variables = [f"move{i}" for i in range(max_depth)]
        domains = {var: ['Up', 'Down', 'Left', 'Right'] for var in variables}

        constraints = []
        for i in range(len(variables) - 1):
            var1, var2 = variables[i], variables[i + 1]
            constraints.append((var1, var2, lambda a, b: not (
                (a == 'Up' and b == 'Down') or
                (a == 'Down' and b == 'Up') or
                (a == 'Left' and b == 'Right') or
                (a == 'Right' and b == 'Left')
            )))

        def revise(xi, xj, constraint):
            revised = False
            to_remove = []
            for x in domains[xi]:
                supported = False
                for y in domains[xj]:
                    if constraint(x, y):
                        supported = True
                        break
                if not supported:
                    to_remove.append(x)
                    revised = True
            for x in to_remove:
                domains[xi].remove(x)
            return revised

        queue = [(xi, xj) for xi, xj, _ in constraints]
        while queue:
            xi, xj = queue.pop(0)
            constraint = next(c[2] for c in constraints if c[0] == xi and c[1] == xj)
            if revise(xi, xj, constraint):
                if not domains[xi]:
                    return None
                for xk in variables:
                    if xk != xj and any(c[0] == xk and c[1] == xi for c in constraints):
                        queue.append((xk, xi))

        def backtrack(state, path, depth, domains, visited):
            if state == self.goal_state:
                return path
            if depth >= max_depth:
                return None
            blank_i, blank_j = self.find_blank(state)
            current_domains = domains[f"move{depth}"]
            for move in current_domains:
                di, dj = self.step[move]
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:  # Boundary check
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    new_state_tuple = tuple(tuple(row) for row in new_state)
                    if new_state_tuple not in visited:
                        visited.add(new_state_tuple)
                        result = backtrack(new_state, path + [move], depth + 1, domains, visited)
                        if result is not None:
                            return result
                        visited.remove(new_state_tuple)
            return None

        visited = {tuple(tuple(row) for row in initial_state)}
        solution = backtrack(initial_state, [], 0, domains, visited)
        print("Generated solution from csp_ac3:", solution)  # Debug output
        return solution

    def backtracking_search(self, start, max_depth=50):
        if start == self.goal_state:
            return []
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

    def forward_checking(self, start, max_depth=50):
        def forward_check(state, depth, path, visited):
            if state == self.goal_state:
                return path
            if depth > max_depth:
                return None
            blank_i, blank_j = self.find_blank(state)
            current_h = self.heuristic(state)
            possible_moves = []
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    if new_state not in visited:
                        new_h = self.heuristic(new_state)
                        if new_h <= current_h:  # Prune if heuristic doesn't improve
                            possible_moves.append((new_state, move))
            for new_state, move in possible_moves:
                visited.add(new_state)
                result = forward_check(new_state, depth + 1, path + [move], visited)
                if result is not None:
                    return result
                visited.remove(new_state)
            return None

        if start == self.goal_state:
            return []
        visited = set([start])
        return forward_check(start, 0, [], visited)

# from utils import PuzzleSolverBase

# class ConstraintSearch(PuzzleSolverBase):
#     def __init__(self, initial_state, goal_state):
#         super().__init__(initial_state, goal_state)

#     def manhattan_distance(self, state):
#         """Calculate the Manhattan distance heuristic for the 8-puzzle."""
#         total_distance = 0
#         goal_positions = {(val, (i, j)) for i in range(3) for j in range(3) for val in range(9)
#                          if (i, j) == self.find_goal_position(val, self.goal_state)}
#         for i in range(3):
#             for j in range(3):
#                 val = state[i][j]
#                 if val != 0:
#                     goal_i, goal_j = self.find_goal_position(val, self.goal_state)
#                     total_distance += abs(i - goal_i) + abs(j - goal_j)
#         return total_distance

#     def find_goal_position(self, value, goal_state):
#         """Find the position of a value in the goal state."""
#         for i in range(3):
#             for j in range(3):
#                 if goal_state[i][j] == value:
#                     return i, j
#         return None

#     def csp_ac3(self, max_depth=50):
#         """Use AC-3 to constrain move domains, then backtrack to find a solution."""
#         initial_state = [list(row) for row in self.initial_state]
#         def is_solvable(state):
#             flat_state = [num for row in state for num in row if num != 0]
#             inversions = 0
#             for i in range(len(flat_state)):
#                 for j in range(i + 1, len(flat_state)):
#                     if flat_state[i] > flat_state[j]:
#                         inversions += 1
#             return inversions % 2 == 0

#         if not is_solvable(initial_state):
#             print("State is not solvable.")
#             return None

#         # Define variables as move sequences
#         variables = [f"move{i}" for i in range(max_depth)]
#         domains = {var: ['Up', 'Down', 'Left', 'Right'] for var in variables}

#         # Define constraints: consecutive moves cannot be opposites
#         constraints = []
#         for i in range(len(variables) - 1):
#             var1, var2 = variables[i], variables[i + 1]
#             constraints.append((var1, var2, lambda a, b: not (
#                 (a == 'Up' and b == 'Down') or
#                 (a == 'Down' and b == 'Up') or
#                 (a == 'Left' and b == 'Right') or
#                 (a == 'Right' and b == 'Left')
#             )))

#         # AC-3 algorithm
#         def revise(xi, xj, constraint):
#             revised = False
#             to_remove = []
#             for x in domains[xi]:
#                 supported = False
#                 for y in domains[xj]:
#                     if constraint(x, y):
#                         supported = True
#                         break
#                 if not supported:
#                     to_remove.append(x)
#                     revised = True
#             for x in to_remove:
#                 if x in domains[xi]:
#                     domains[xi].remove(x)
#             return revised

#         queue = [(xi, xj) for xi, xj, _ in constraints]
#         while queue:
#             xi, xj = queue.pop(0)
#             constraint = next(c[2] for c in constraints if c[0] == xi and c[1] == xj)
#             if revise(xi, xj, constraint):
#                 if not domains[xi]:
#                     print("No consistent domain found.")
#                     return None
#                 for xk in variables:
#                     if xk != xj and any(c[0] == xk and c[1] == xi for c in constraints):
#                         queue.append((xk, xi))

#         # Backtrack to find the path
#         def backtrack(state, path, depth, visited):
#             if tuple(tuple(row) for row in state) == self.goal_state:
#                 print(f"Solution found: {path}")
#                 return path
#             if depth >= max_depth:
#                 print("Max depth reached.")
#                 return None
#             blank_i, blank_j = self.find_blank(state)
#             current_domain = domains.get(f"move{depth}", ['Up', 'Down', 'Left', 'Right'])
#             for move in current_domain:
#                 di, dj = self.step[move]
#                 new_i, new_j = blank_i + di, blank_j + dj
#                 if 0 <= new_i < 3 and 0 <= new_j < 3:
#                     new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
#                     new_state_tuple = tuple(tuple(row) for row in new_state)
#                     if new_state_tuple not in visited:
#                         visited.add(new_state_tuple)
#                         result = backtrack(new_state, path + [move], depth + 1, visited)
#                         if result is not None:
#                             return result
#                         visited.remove(new_state_tuple)
#             return None

#         visited = {tuple(tuple(row) for row in initial_state)}
#         solution = backtrack(initial_state, [], 0, visited)
#         return solution if solution else None

#     def backtracking_search(self, max_depth=50):
#         """Backtracking search starting from initial_state."""
#         if tuple(tuple(row) for row in self.initial_state) == self.goal_state:
#             return []
#         def backtrack(state, path, depth, visited):
#             if tuple(tuple(row) for row in state) == self.goal_state:
#                 return path
#             if depth > max_depth:
#                 return None
#             blank_i, blank_j = self.find_blank(state)
#             for move, (di, dj) in self.step.items():
#                 new_i, new_j = blank_i + di, blank_j + dj
#                 if 0 <= new_i < 3 and 0 <= new_j < 3:
#                     new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
#                     new_state_tuple = tuple(tuple(row) for row in new_state)
#                     if new_state_tuple not in visited:
#                         visited.add(new_state_tuple)
#                         result = backtrack(new_state, path + [move], depth + 1, visited)
#                         if result is not None:
#                             return result
#                         visited.remove(new_state_tuple)
#             return None

#         visited = {tuple(tuple(row) for row in self.initial_state)}
#         return backtrack(self.initial_state, [], 0, visited)

#     def forward_checking(self, max_depth=50):
#         """Forward checking with heuristic pruning."""
#         if tuple(tuple(row) for row in self.initial_state) == self.goal_state:
#             return []
#         def forward_check(state, depth, path, visited):
#             if tuple(tuple(row) for row in state) == self.goal_state:
#                 return path
#             if depth > max_depth:
#                 return None
#             blank_i, blank_j = self.find_blank(state)
#             current_h = self.manhattan_distance(state)
#             possible_moves = []
#             for move, (di, dj) in self.step.items():
#                 new_i, new_j = blank_i + di, blank_j + dj
#                 if 0 <= new_i < 3 and 0 <= new_j < 3:
#                     new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
#                     new_state_tuple = tuple(tuple(row) for row in new_state)
#                     if new_state_tuple not in visited:
#                         new_h = self.manhattan_distance(new_state)
#                         if new_h <= current_h:  # Prune if heuristic doesn't improve
#                             possible_moves.append((new_state, move))
#             for new_state, move in possible_moves:
#                 visited.add(tuple(tuple(row) for row in new_state))
#                 result = forward_check(new_state, depth + 1, path + [move], visited)
#                 if result is not None:
#                     return result
#                 visited.remove(tuple(tuple(row) for row in new_state))
#             return None

#         visited = {tuple(tuple(row) for row in self.initial_state)}
#         return forward_check(self.initial_state, 0, [], visited)