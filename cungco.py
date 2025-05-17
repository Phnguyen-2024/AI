import random
import numpy as np
from utils import PuzzleSolverBase

class ReinforcementSearch(PuzzleSolverBase):
    def __init__(self, initial_state, goal_state):
        super().__init__(initial_state, goal_state)

    def q_learning(self, start, episodes=5000, alpha=0.1, gamma=0.9, epsilon_start=0.3, epsilon_end=0.01, epsilon_decay=0.995):
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

        # For convergence check
        q_deltas = []
        max_delta_window = 100

        for episode in range(episodes):
            state = start
            visited_in_episode = set()
            episode_steps = 0
            max_steps_per_episode = 200

            while state != self.goal_state and episode_steps < max_steps_per_episode:
                if state in visited_in_episode:
                    break  # Avoid loops within an episode
                visited_in_episode.add(state)

                action = choose_action(state)
                try:
                    next_state = self.apply_move(state, action)
                    reward = 100 if next_state == self.goal_state else -1
                    # Add heuristic-based reward to guide learning
                    if next_state != state:
                        reward += (self.heuristic(state) - self.heuristic(next_state)) * 0.5
                except ValueError:
                    next_state = state
                    reward = -10  # Penalize invalid moves

                # Q-Value update
                old_q = get_q(state, action)
                next_q = max([get_q(next_state, a) for a in actions])
                new_q = old_q + alpha * (reward + gamma * next_q - old_q)
                q_table[(state, action)] = new_q

                # Track Q-value change for convergence
                delta = abs(new_q - old_q)
                q_deltas.append(delta)
                if len(q_deltas) > max_delta_window:
                    q_deltas.pop(0)

                state = next_state
                episode_steps += 1

            # Decay epsilon
            epsilon = max(epsilon_end, epsilon * epsilon_decay)

            # Check for convergence
            if len(q_deltas) == max_delta_window and max(q_deltas) < 0.01:
                print(f"Converged after {episode + 1} episodes")
                break

        # Extract policy
        state = start
        path = []
        visited = set()
        max_steps = 500  # Increase to allow for longer solutions
        step = 0
        while state != self.goal_state and step < max_steps:
            if state in visited:
                break
            visited.add(state)
            q_values = [get_q(state, a) for a in actions]
            max_q = max(q_values)
            if max_q == 0:  # If no Q-values are trained for this state, try a random move
                action = random.choice(actions)
            else:
                action = actions[np.argmax(q_values)]
            try:
                next_state = self.apply_move(state, action)
                if next_state == state:  # Move didn't change state
                    break
                path.append(action)
                state = next_state
            except ValueError:
                break  # Invalid move
            step += 1

        return path if state == self.goal_state else None