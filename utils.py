import random
from collections import deque
import heapq
import math
import itertools

class PuzzleSolverBase:
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