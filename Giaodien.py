import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq
import time
import random
import math


class PuzzleSolver:
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

    def bfs(self, start):
        queue = deque([(start, [])])
        seen = set([start])
        while queue:
            current, path = queue.popleft()
            if current == self.goal_state:
                return path
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    if new_state not in seen:
                        queue.append((new_state, path + [move]))
                        seen.add(new_state)
        return None

    def dfs(self, start, max_depth=50):
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

    def possible_moves(self, state):
        blank_i, blank_j = self.find_blank(state)
        moves = []
        for move, (di, dj) in self.step.items():
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                moves.append(move)
        return moves

    def apply_move(self, state, move):
        blank_i, blank_j = self.find_blank(state)
        di, dj = self.step[move]
        new_i, new_j = blank_i + di, blank_j + dj
        return self.swap(state, blank_i, blank_j, new_i, new_j)

    

    def ids(self, start):
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
        while True:
            visited = set([start])
            result = dls(start, depth, [], visited)
            if result is not None:
                return result
            depth += 1
            # Thêm giới hạn độ sâu tối đa để tránh vòng lặp vô hạn
            if depth > 50:  # Có thể điều chỉnh giá trị này
                return None

    
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
        pq = [(self.heuristic(start), 0, start, [])]  # (f, g, state, path)
        g_map = {start: 0}
        visited = set()  # Changed from set([start]) to set()
        
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


    def simple_hill_climbing(self, start):
        current = start
        while True:
            current_h = self.heuristic(current)
            best_move = None
            best_state = None
            best_h = current_h
            
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    h = self.heuristic(new_state)
                    if h < best_h:
                        best_h = h
                        best_state = new_state
                        best_move = move
                        
            if best_state is None or best_h >= current_h:  # Không tìm thấy trạng thái tốt hơn
                return None  # Hoặc có thể trả về current nếu muốn kết quả gần đúng
            current = best_state
            if current == self.goal_state:
                # Tái tạo đường đi từ start đến goal
                path = []
                temp = start
                while temp != current:
                    blank_i, blank_j = self.find_blank(temp)
                    for move, (di, dj) in self.step.items():
                        new_i, new_j = blank_i + di, blank_j + dj
                        if 0 <= new_i < 3 and 0 <= new_j < 3:
                            next_state = self.swap(temp, blank_i, blank_j, new_i, new_j)
                            if self.heuristic(next_state) < self.heuristic(temp):
                                path.append(move)
                                temp = next_state
                                break
                return path


    def steepest_ascent_hill_climbing(self, start):
        current = start
        while True:
            current_h = self.heuristic(current)
            best_move = None
            best_state = None
            best_h = float('inf')
            
            # Tìm trạng thái tốt nhất trong tất cả các neighbor
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    h = self.heuristic(new_state)
                    if h < best_h:  # Tìm h nhỏ nhất (steepest)
                        best_h = h
                        best_state = new_state
                        best_move = move
                        
            if best_state is None or best_h >= current_h:  # Không tìm thấy trạng thái tốt hơn
                return None  # Hoặc có thể trả về current nếu muốn kết quả gần đúng
            current = best_state
            if current == self.goal_state:
                # Tái tạo đường đi từ start đến goal
                path = []
                temp = start
                while temp != current:
                    blank_i, blank_j = self.find_blank(temp)
                    for move, (di, dj) in self.step.items():
                        new_i, new_j = blank_i + di, blank_j + dj
                        if 0 <= new_i < 3 and 0 <= new_j < 3:
                            next_state = self.swap(temp, blank_i, blank_j, new_i, new_j)
                            if self.heuristic(next_state) < self.heuristic(temp):
                                path.append(move)
                                temp = next_state
                                break
                return path


    def stochastic_hill_climbing(self, start, max_iterations=1000):
        current = start
        iterations = 0
        
        while iterations < max_iterations:
            current_h = self.heuristic(current)
            if current == self.goal_state:
                # Tái tạo đường đi từ start đến goal
                path = []
                temp = start
                while temp != current:
                    blank_i, blank_j = self.find_blank(temp)
                    for move, (di, dj) in self.step.items():
                        new_i, new_j = blank_i + di, blank_j + dj
                        if 0 <= new_i < 3 and 0 <= new_j < 3:
                            next_state = self.swap(temp, blank_i, blank_j, new_i, new_j)
                            if self.heuristic(next_state) < self.heuristic(temp):
                                path.append(move)
                                temp = next_state
                                break
                return path
            
            # Tạo danh sách các neighbor tốt hơn
            better_neighbors = []
            blank_i, blank_j = self.find_blank(current)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    h = self.heuristic(new_state)
                    if h < current_h:
                        better_neighbors.append((new_state, move))
            
            # Nếu không có neighbor tốt hơn, dừng lại
            if not better_neighbors:
                return None
                
            # Chọn ngẫu nhiên một neighbor tốt hơn
            next_state, next_move = random.choice(better_neighbors)
            current = next_state
            
            iterations += 1
        
        return None  # Trả về None nếu đạt max_iterations mà không tìm thấy giải pháp


    def simulated_annealing(self, start, initial_temp=1000, cooling_rate=0.99, min_temp=0.01, max_iterations=10000):
        current = start
        current_h = self.heuristic(current)
        best = current
        best_h = current_h
        temp = initial_temp
        iterations = 0
        path = []  # Lưu đường đi

        while temp > min_temp and iterations < max_iterations:
            # Kiểm tra nếu đã đạt goal
            if current == self.goal_state:
                return path

            # Lấy tất cả các neighbor
            blank_i, blank_j = self.find_blank(current)
            neighbors = []
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                    neighbors.append((new_state, move))

            # Chọn ngẫu nhiên một neighbor
            next_state, move = random.choice(neighbors)
            next_h = self.heuristic(next_state)
            delta_h = next_h - current_h

            # Quyết định chấp nhận trạng thái mới
            if delta_h < 0 or random.random() < math.exp(-delta_h / temp):
                # Chấp nhận trạng thái mới
                current = next_state
                current_h = next_h
                path.append(move)  # Thêm bước di chuyển vào đường đi

                # Cập nhật trạng thái tốt nhất
                if current_h < best_h:
                    best = current
                    best_h = current_h

            # Giảm nhiệt độ
            temp *= cooling_rate
            iterations += 1

        # Nếu không đạt goal, trả về đường đi đến trạng thái tốt nhất (nếu có cải thiện)
        if best_h < self.heuristic(start):
            return path
        return None
    


    def beam_search(self, start, beam_width=2):
        # Hàng đợi ưu tiên lưu (heuristic, state, path)
        beam = [(self.heuristic(start), start, [])]
        visited = set([start])

        while beam:
            # Tạo danh sách các trạng thái mới từ beam hiện tại
            next_beam = []
            for _, current, path in beam:
                if current == self.goal_state:
                    return path

                # Lấy tất cả các neighbor
                blank_i, blank_j = self.find_blank(current)
                for move, (di, dj) in self.step.items():
                    new_i, new_j = blank_i + di, blank_j + dj
                    if 0 <= new_i < 3 and 0 <= new_j < 3:
                        new_state = self.swap(current, blank_i, blank_j, new_i, new_j)
                        if new_state not in visited:
                            visited.add(new_state)
                            h = self.heuristic(new_state)
                            next_beam.append((h, new_state, path + [move]))

            # Sắp xếp theo heuristic và chọn beam_width trạng thái tốt nhất
            next_beam.sort(key=lambda x: x[0])  # Sắp xếp theo heuristic
            beam = next_beam[:beam_width]  # Giữ lại k trạng thái đầu tiên

            # Nếu không còn trạng thái nào để mở rộng
            if not beam:
                return None

        return None


    def and_or_graph_search(self, start):
        def or_search(state, path, visited):
            """OR-search: explores a single state"""
            if state == self.goal_state:
                return path
            if state in visited:
                return None
            
            visited.add(state)
            blank_i, blank_j = self.find_blank(state)
            
            # Try all possible moves (OR nodes)
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    new_state = self.swap(state, blank_i, blank_j, new_i, new_j)
                    result = and_search(new_state, path + [move], visited.copy())
                    if result is not None:
                        return result
            return None

        def and_search(state, path, visited):
            """AND-search: ensures all subproblems are solved"""
            if state == self.goal_state:
                return path
            if state in visited:
                return None
                
            visited.add(state)
            blank_i, blank_j = self.find_blank(state)
            moves = []
            
            # Collect all possible moves
            for move, (di, dj) in self.step.items():
                new_i, new_j = blank_i + di, blank_j + dj
                if 0 <= new_i < 3 and 0 <= new_j < 3:
                    moves.append((move, self.swap(state, blank_i, blank_j, new_i, new_j)))
            
            # AND condition: try to solve all possible moves
            for move, new_state in moves:
                result = or_search(new_state, path + [move], visited.copy())
                if result is not None:
                    return result
            return None

        # Start the search
        visited = set()
        return and_search(start, [], visited)


    def convert_states_to_moves(self, states):
        if not states or len(states) < 2:
            return []
        moves = []
        for i in range(len(states) - 1):
            s1 = states[i]
            s2 = states[i+1]
            blank1 = self.find_blank(s1)
            blank2 = self.find_blank(s2)
            di = blank2[0] - blank1[0]
            dj = blank2[1] - blank1[1]
            for m, (md_i, md_j) in self.step.items():
                if (md_i, md_j) == (di, dj):
                    moves.append(m)
                    break
        return moves

def get_state_from_entries(entries):
    numbers = []
    state = []
    for i in range(3):
        row = []
        for j in range(3):
            try:
                num_str = entries[i][j].get()
                if not num_str.isdigit() or len(num_str) != 1:
                    raise ValueError("Invalid input")
                num = int(num_str)
                if num < 0 or num > 8:
                    raise ValueError("Number out of range")
                row.append(num)
                numbers.append(num)
            except ValueError as e:
                messagebox.showerror("Input Error", f"Invalid input for cell ({i+1},{j+1}): {e}")
                return None
        state.append(row)
    if len(set(numbers)) != 9:
        messagebox.showerror("Input Error", "Duplicate numbers or missing numbers")
        return None
    return tuple(tuple(row) for row in state)

delay = 0.5
paused = False
running = False

def update_view(state):
    for i in range(3):
        for j in range(3):
            tile = view_labels[i][j]
            value = state[i][j]
            tile.config(
                text=str(value) if value != 0 else "",
                bg="#D4F0F0" if value == 0 else "#FFFFFF",
                fg="#000000"
            )

def create_state_grid(parent, state_3x3):
    for i in range(3):
        for j in range(3):
            val = state_3x3[i][j]
            bg_color = "#D4F0F0" if val == 0 else "#FFFFFF"
            lbl = tk.Label(
                parent,
                text=str(val) if val != 0 else "",
                width=3,
                height=1,
                font=("Arial", 14, "bold"),
                bg=bg_color,
                fg="#000000",
                bd=2,
                relief="solid"
            )
            lbl.grid(row=i, column=j, padx=2, pady=2)

step_count = 0  # Biến toàn cục để đếm số bước
current_row_frame = None 

def add_step_frame(index, move_, state_3x3):
    global step_count, current_row_frame


    if step_count % 4 == 0:
        current_row_frame = tk.Frame(steps_container, bg="#FFFFFF")
        current_row_frame.pack(side="top", padx=5, pady=5)

    # Tạo khung cho bước hiện tại
    step_frame = tk.Frame(current_row_frame, bg="#FFFFFF", bd=2, relief="groove")
    step_frame.pack(side="left", padx=5, pady=5)  # Xếp ngang trong row_frame
    lbl_title = tk.Label(
        step_frame,
        text=f"Số bước {index}",
        font=("Arial", 12, "bold"),
        fg="#000000",
        bg="#FFFFFF"
    )
    lbl_title.pack(side="top", anchor="w", padx=5, pady=2)
    grid_holder = tk.Frame(step_frame, bg="#FFFFFF")
    grid_holder.pack(side="left", padx=5, pady=5)
    create_state_grid(grid_holder, state_3x3)

    step_count += 1  # Tăng số đếm bước

def pause_program():
    global paused
    paused = True

def resume_program():
    global paused
    paused = False

def reset_program():
    global running, paused, step_count, current_row_frame
    running = False
    paused = False
    step_count = 0  # Reset số đếm bước
    current_row_frame = None  # Reset khung dòng hiện tại
    selected_algorithm.set("")  # Reset lựa chọn thuật toán
    for i in range(3):
        for j in range(3):
            initial_entries[i][j].delete(0, tk.END)
            goal_entries[i][j].delete(0, tk.END)
    for child in steps_container.winfo_children():
        child.destroy()
    blank_state = ((0,0,0),(0,0,0),(0,0,0))
    update_view(blank_state)
    steps_count.config(text="Số bước: 0")
    time_label.config(text="Thời gian: 00:00")

def solve(algorithm_name):
    global result, paused, running, step_count, current_row_frame
    running = True
    step_count = 0  # Reset số đếm bước khi bắt đầu giải
    current_row_frame = None  # Reset khung dòng hiện tại
    for child in steps_container.winfo_children():
        child.destroy()
    lbl_all_steps = tk.Label(
        steps_container,
        # text="Tất Cả Các Bước",
        font=("Arial", 14, "bold"),
        fg="#000000",
        bg="#FFFFFF"
    )
    lbl_all_steps.pack(side="top", pady=5)  # Tiêu đề vẫn ở trên cùng

    initial_state = get_state_from_entries(initial_entries)
    if initial_state is None:
        return
    goal_state = get_state_from_entries(goal_entries)
    if goal_state is None:
        return
    result = goal_state
    update_view(initial_state)

    solver = PuzzleSolver(initial_state, goal_state)
    algorithm = getattr(solver, algorithm_name)
    start_time = time.time()
    solution = algorithm(initial_state)
    if solution:
        current_state = initial_state
        add_step_frame(0, "Start", current_state)
        for i, move_ in enumerate(solution, start=1):
            if not running:
                break
            while paused and running:
                root.update()
                time.sleep(0.1)
            root.update()
            time.sleep(delay)
            blank_i, blank_j = solver.find_blank(current_state)
            new_state = solver.swap(current_state, blank_i, blank_j,
                                 blank_i + solver.step[move_][0],
                                 blank_j + solver.step[move_][1])
            update_view(new_state)
            current_state = new_state
            add_step_frame(i, move_, new_state)
        if running:
            steps_count.config(text=f"Số bước: {len(solution)}")
            total_time = time.time() - start_time
            time_label.config(text=f"Thời gian: {total_time:.2f}s")
    else:
        messagebox.showerror("Thất bại", "Không tìm thấy giải pháp!")

def start_solving():
    if not selected_algorithm.get():
        messagebox.showwarning("Cảnh báo", "Vui lòng chọn thuật toán trước.")
        return
    solve(selected_algorithm.get())

# Tạo cửa sổ gốc trước khi khai báo biến Tkinter
root = tk.Tk()
root.title("8-Puzzle Trần Hồ Phương Nguyên - 23110271")

# Khai báo selected_algorithm sau khi root được tạo
selected_algorithm = tk.StringVar()


main_frame = tk.Frame(root, bg="#FFFFFF")
main_frame.pack(side="top", fill="both", expand=True)

# Khung bên trái với bố cục mới
left_frame = tk.Frame(main_frame, bg="#FFFFFF")
left_frame.pack(side="left", fill="y", padx=10, pady=10)

top_frame = tk.Frame(left_frame, bg="#FFFFFF")
top_frame.pack(side="top", fill="x", padx=5, pady=5)

frame_start = tk.LabelFrame(
    top_frame,
    text="Initial State",
    bg="#FFFFFF",
    fg="#D00000",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="solid"
)
frame_start.pack(side="left", padx=10, pady=5)

# Căn giữa các ô nhập liệu trong frame_start
initial_entries = []
for i in range(3):
    frame_start.grid_rowconfigure(i, weight=1)
    frame_start.grid_columnconfigure(i, weight=1)
    row = []
    for j in range(3):
        e = tk.Entry(frame_start, width=3, font=("Arial", 16),
                     justify="center", bg="#D4F0F0")
        e.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        row.append(e)
    initial_entries.append(row)

frame_goal = tk.LabelFrame(
    top_frame,
    text="Goal State",
    bg="#FFFFFF",
    fg="#D00000",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="solid"
)
frame_goal.pack(side="left", padx=10, pady=5)

goal_entries = []
for i in range(3):
    row = []
    for j in range(3):
        e = tk.Entry(frame_goal, width=3, font=("Arial", 16),
                     justify="center", bg="#D4F0F0")
        e.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        row.append(e)
    goal_entries.append(row)

# Điền trạng thái đích mặc định: 123456780
default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
for i in range(3):
    for j in range(3):
        goal_entries[i][j].insert(0, str(default_goal[i][j]))

frame_current = tk.LabelFrame(
    left_frame,
    text="Current State",
    bg="#FFFFFF",
    fg="#D00000",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="solid"
)
frame_current.pack(side="top", fill="both", padx=5, pady=15)

info_frame = tk.Frame(frame_current, bg="#FFFFFF")
info_frame.pack(side="top", fill="x", padx=5, pady=5)

steps_count = tk.Label(info_frame, text="Số bước: 0", font=("Arial", 10),
                       fg="#000000", bg="#FFFFFF")
steps_count.pack(side="left", padx=5)

time_label = tk.Label(info_frame, text="Thời gian: 00:00",
                      font=("Arial", 10), fg="#000000", bg="#FFFFFF")
time_label.pack(side="left", padx=10)

grid_frame = tk.Frame(frame_current, bg="#FFFFFF")
grid_frame.pack(side="top", padx=5, pady=5)

view_labels = []
for i in range(3):
    row = []
    for j in range(3):
        lbl = tk.Label(
            grid_frame,
            text="",
            width=3,
            height=1,
            font=("Arial", 16, "bold"),
            bg="#FFFFFF",
            fg="#000000",
            bd=2,
            relief="solid"
        )
        lbl.grid(row=i, column=j, padx=3, pady=3)
        row.append(lbl)
    view_labels.append(row)

# Thêm khung Điều Khiển vào left_frame, dưới frame_current
frame_control = tk.LabelFrame(
    left_frame,
    bg="#FFFFFF",
    fg="#D00000",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="solid"
)
frame_control.pack(side="top", fill="both", padx=5, pady=5)

# Tăng kích thước các nút
tk.Button(frame_control, text="Start", bg="#D4F0F0", fg="#000000", 
          command=start_solving, width=10, height=2, font=("Arial", 12)).pack(padx=5, pady=5)
tk.Button(frame_control, text="Stop", bg="#D4F0F0", fg="#000000", 
          command=pause_program, width=10, height=2, font=("Arial", 12)).pack(padx=5, pady=5)
tk.Button(frame_control, text="Continue", bg="#D4F0F0", fg="#000000", 
          command=resume_program, width=10, height=2, font=("Arial", 12)).pack(padx=5, pady=5)
tk.Button(frame_control, text="Reset", bg="#D4F0F0", fg="#000000", 
          command=reset_program, width=10, height=2, font=("Arial", 12)).pack(padx=5, pady=5)

# Khung giữa với canvas
center_frame = tk.Frame(main_frame, bg="#FFFFFF")
center_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

canvas = tk.Canvas(center_frame, bg="#FFFFFF")
canvas.pack(side="left", fill="both", expand=True)

scrollbar_y = tk.Scrollbar(center_frame, orient="vertical", command=canvas.yview)
scrollbar_y.pack(side="right", fill="y")

scrollbar_x = tk.Scrollbar(center_frame, orient="horizontal", command=canvas.xview)
scrollbar_x.pack(side="bottom", fill="x")

canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

steps_container = tk.Frame(canvas, bg="#FFFFFF")
canvas.create_window((0,0), window=steps_container, anchor="nw")

def on_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
steps_container.bind("<Configure>", on_configure)

# Khung bên phải chỉ còn chứa khung thuật toán
right_frame = tk.Frame(main_frame, bg="#FFFFFF")
right_frame.pack(side="right", fill="y", padx=10, pady=10)

frame_algo = tk.LabelFrame(
    right_frame,
    text="Thuật toán",
    bg="#FFFFFF",
    fg="#D00000",
    font=("Arial", 12, "bold"),
    bd=2,
    relief="solid"
)
frame_algo.pack(padx=5, pady=5, fill="both")


algorithms = ["bfs", "dfs", "ucs", "ids", "greedy", "a*", "ida*", "simple_hill_climbing","steepest_ascent_hill_climbing", "stochastic_hill_climbing", "simulated_annealing", "beam_search", "and_or_graph_search"]
for algo in algorithms:
    display_name = algo.replace("_", " ").title()
    tk.Radiobutton(frame_algo, text=display_name, variable=selected_algorithm, 
                   value=algo, bg="#FFFFFF", fg="#000000", font=("Arial", 14)).pack(anchor="w", padx=5, pady=3)

root.mainloop()