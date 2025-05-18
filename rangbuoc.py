# from utils import PuzzleSolverBase
# from collections import deque

# class ConstraintSearch(PuzzleSolverBase):
#     def __init__(self, initial_state, goal_state):
#         super().__init__(initial_state, goal_state)

#     def csp_ac3(self, max_depth=200):  # Increased max_depth to 200
#         # Ensure states are lists for manipulation
#         initial_state = [list(row) for row in self.initial_state]
#         goal_state = [list(row) for row in self.goal_state]

#         def is_solvable(state):
#             flat_state = [num for row in state for num in row if num != 0]
#             inversions = 0
#             for i in range(len(flat_state)):
#                 for j in range(i + 1, len(flat_state)):
#                     if flat_state[i] > flat_state[j]:
#                         inversions += 1
#             return inversions % 2 == 0

#         if not is_solvable(initial_state):
#             return None

#         def is_valid_move(state, move):
#             blank_i, blank_j = self.find_blank(state)
#             di, dj = self.step.get(move, (0, 0))
#             new_i, new_j = blank_i + di, blank_j + dj
#             return 0 <= new_i < 3 and 0 <= new_j < 3

#         def get_valid_moves(state):
#             blank_i, blank_j = self.find_blank(state)
#             valid_moves = []
#             for move, (di, dj) in self.step.items():
#                 new_i, new_j = blank_i + di, blank_j + dj
#                 if 0 <= new_i < 3 and 0 <= new_j < 3:
#                     valid_moves.append(move)
#             return valid_moves

#         def backtrack(state, path, depth, visited):
#             # Convert state to tuple for comparison
#             state_tuple = tuple(tuple(row) for row in state)
#             goal_tuple = tuple(tuple(row) for row in goal_state)
#             if state_tuple == goal_tuple:
#                 return path
#             if depth >= max_depth:
#                 return None

#             # Get valid moves for the current state
#             current_domain = get_valid_moves(state)
#             if not current_domain:
#                 return None

#             # Sort moves by heuristic value (ascending)
#             moves = [(move, self.heuristic(self.apply_move(state, move))) for move in current_domain]
#             moves.sort(key=lambda x: x[1])  # Sort by heuristic to prioritize better states

#             for move, _ in moves:
#                 new_state = self.apply_move(state, move)
#                 new_state_tuple = tuple(tuple(row) for row in new_state)
#                 if new_state_tuple not in visited:
#                     visited.add(new_state_tuple)
#                     result = backtrack(new_state, path + [move], depth + 1, visited)
#                     if result is not None:
#                         # Verify the final state matches the goal state
#                         final_state = initial_state.copy()
#                         for m in result:
#                             final_state = self.apply_move(final_state, m)
#                         if tuple(tuple(row) for row in final_state) == goal_tuple:
#                             return result
#                     visited.remove(new_state_tuple)
#             return None

#         visited = {tuple(tuple(row) for row in initial_state)}
#         return backtrack(initial_state, [], 0, visited)

#     def backtracking_search(self, start, max_depth=100):
#         if start == self.goal_state:
#             return []
#         def backtrack(state, path, depth, visited):
#             if state == self.goal_state:
#                 return path
#             if depth > max_depth:
#                 return None
#             blank_i, blank_j = self.find_blank(state)
#             moves = [(move, self.heuristic(self.apply_move(state, move))) 
#                      for move, (di, dj) in self.step.items() 
#                      if 0 <= blank_i + di < 3 and 0 <= blank_j + dj < 3]
#             moves.sort(key=lambda x: x[1])
#             for move, _ in moves:
#                 new_state = self.swap(state, blank_i, blank_j, 
#                                      blank_i + self.step[move][0], 
#                                      blank_j + self.step[move][1])
#                 if new_state not in visited:
#                     visited.add(new_state)
#                     result = backtrack(new_state, path + [move], depth + 1, visited)
#                     if result is not None:
#                         return result
#                     visited.remove(new_state)
#             return None

#         visited = set([start])
#         return backtrack(start, [], 0, visited)

#     def forward_checking(self, start, max_depth=100):
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
#                         if new_h <= current_h + 2:
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
from collections import deque

class ConstraintSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def csp_ac3(self, max_depth=200):
        initial_state = [list(row) for row in self.initial_state]
        goal_state = [list(row) for row in self.goal_state]

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

        def get_valid_moves(state):
            blank_i, blank_j = self.find_blank(state)
            valid_moves = []
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    valid_moves.append(move)
            return valid_moves

        def backtrack(state, path, depth, visited):
            state_tuple = tuple(tuple(row) for row in state)
            goal_tuple = tuple(tuple(row) for row in goal_state)
            if state_tuple == goal_tuple:
                # Kiểm tra đường đi bằng cách áp dụng các bước di chuyển
                current = [list(row) for row in self.initial_state]
                for move in path:
                    current = self.apply_move(current, move)
                if tuple(tuple(row) for row in current) == goal_tuple:
                    return path
                return None

            if depth >= max_depth:
                return None

            current_domain = get_valid_moves(state)
            if not current_domain:
                return None

            moves = [(move, self.heuristic(self.apply_move(state, move))) for move in current_domain]
            moves.sort(key=lambda x: x[1])

            for move, _ in moves:
                new_state = self.apply_move(state, move)
                new_state_tuple = tuple(tuple(row) for row in new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    result = backtrack(new_state, path + [move], depth + 1, visited)
                    if result is not None:
                        return result
                    visited.remove(new_state_tuple)
            return None

        visited = {tuple(tuple(row) for row in initial_state)}
        path = backtrack(initial_state, [], 0, visited)
        if path:
            # Trong giao diện, csp_ac3 được kỳ vọng trả về trạng thái cuối
            final_state = initial_state.copy()
            for move in path:
                final_state = self.apply_move(final_state, move)
            return final_state
        return None

    def backtracking_search(self, start, max_depth=100):
        if start == self.goal_state:
            return []
        def backtrack(state, path, depth, visited):
            if state == self.goal_state:
                return path
            if depth > max_depth:
                return None
            blank_i, blank_j = self.find_blank(state)
            moves = [(move, self.heuristic(self.apply_move(state, move))) 
                     for move, (di, dj) in self.step.items() 
                     if 0 <= blank_i + di < 3 and 0 <= blank_j + dj < 3]
            moves.sort(key=lambda x: x[1])
            for move, _ in moves:
                new_state = self.swap(state, blank_i, blank_j, 
                                     blank_i + self.step[move][0], 
                                     blank_j + self.step[move][1])
                if new_state not in visited:
                    visited.add(new_state)
                    result = backtrack(new_state, path + [move], depth + 1, visited)
                    if result is not None:
                        return result
                    visited.remove(new_state)
            return None

        visited = set([start])
        return backtrack(start, [], 0, visited)

    def forward_checking(self, start, max_depth=100):
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
                        if new_h <= current_h + 2:
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