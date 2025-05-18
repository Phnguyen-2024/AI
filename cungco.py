import random
import numpy as np
from utils import PuzzleSolverBase

class ReinforcementSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def q_learning(self, start, episodes=10000, alpha=0.1, gamma=0.9, epsilon_start=0.3, epsilon_end=0.01, epsilon_decay=0.995):
        actions = list(self.step.keys())
        q_table = {}
        epsilon = epsilon_start

        def get_q(state, action):
            return q_table.get((state, action), 0.0)

        def choose_action(state):
            if random.random() < epsilon:
                return random.choice(actions)
            q_values = [get_q(state, a) for a in actions]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(actions, q_values) if q == max_q]
            return random.choice(best_actions)

        q_deltas = []
        max_delta_window = 100

        for episode in range(episodes):
            state = start
            visited_in_episode = set()
            episode_steps = 0
            max_steps_per_episode = 200

            while state != self.goal_state and episode_steps < max_steps_per_episode:
                if state in visited_in_episode:
                    reward = -50
                    action = choose_action(state)
                    old_q = get_q(state, action)
                    q_table[(state, action)] = old_q + alpha * (reward - old_q)
                    break
                visited_in_episode.add(state)

                action = choose_action(state)
                try:
                    next_state = self.apply_move(state, action)
                    reward = 100 if next_state == self.goal_state else -1
                    if next_state != state:
                        reward += (self.heuristic(state) - self.heuristic(next_state)) * 2.0
                except ValueError:
                    next_state = state
                    reward = -10

                old_q = get_q(state, action)
                next_q = max([get_q(next_state, a) for a in actions])
                new_q = old_q + alpha * (reward + gamma * next_q - old_q)
                q_table[(state, action)] = new_q

                delta = abs(new_q - old_q)
                q_deltas.append(delta)
                if len(q_deltas) > max_delta_window:
                    q_deltas.pop(0)

                state = next_state
                episode_steps += 1

            epsilon = max(epsilon_end, epsilon * epsilon_decay)

            if len(q_deltas) == max_delta_window and max(q_deltas) < 0.01:
                print(f"Converged after {episode + 1} episodes")
                break

        state = start
        path = []
        visited = set()
        max_steps = 1000
        step = 0
        while state != self.goal_state and step < max_steps:
            if state in visited:
                path = path[:-2] if len(path) >= 2 else []
                state = self.apply_moves(start, path)
                visited.clear()
                visited.add(state)
                continue
            visited.add(state)
            q_values = [get_q(state, a) for a in actions]
            max_q = max(q_values)
            if max_q == 0:
                moves = [(a, self.heuristic(self.apply_move(state, a))) for a in actions 
                         if self.apply_move(state, a) != state]
                action = min(moves, key=lambda x: x[1])[0] if moves else random.choice(actions)
            else:
                action = actions[np.argmax(q_values)]
            try:
                next_state = self.apply_move(state, action)
                if next_state == state:
                    break
                path.append(action)
                state = next_state
            except ValueError:
                break
            step += 1

        return path if state == self.goal_state else None