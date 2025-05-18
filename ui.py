# import tkinter as tk
# from tkinter import messagebox, ttk
# import time
# from kthongtin import UninformedSearch
# from cothongtin import InformedSearch
# from cucbo import LocalSearch
# from rangbuoc import ConstraintSearch
# from phuctap import ComplexSearch
# from cungco import ReinforcementSearch
# from utils import PuzzleSolverBase

# def get_state_from_entries(entries):
#     numbers = []
#     state = []
#     for i in range(3):
#         row = []
#         for j in range(3):
#             try:
#                 num_str = entries[i][j].get()
#                 if not num_str.isdigit() or len(num_str) != 1:
#                     raise ValueError("Invalid input")
#                 num = int(num_str)
#                 if num < 0 or num > 8:
#                     raise ValueError("Number out of range")
#                 row.append(num)
#                 numbers.append(num)
#             except ValueError as e:
#                 messagebox.showerror("Input Error", f"Invalid input for cell ({i+1},{j+1}): {e}")
#                 return None
#         state.append(row)
#     if len(set(numbers)) != 9:
#         messagebox.showerror("Input Error", "Duplicate numbers or missing numbers")
#         return None
#     return tuple(tuple(row) for row in state)

# delay = 0.5
# paused = False
# running = False
# view_labels = []
# initial_entries = []
# goal_entries = []
# steps_count = None
# time_label = None
# verification_label = None
# steps_container = None
# # noise_scale = None
# selected_algorithm = None
# displayed_algorithm = None
# root = None
# compare_tree = None
# current_group = None  # Biến để theo dõi nhóm thuật toán hiện tại của bảng so sánh

# def update_view(state):
#     for i in range(3):
#         for j in range(3):
#             tile = view_labels[i][j]
#             value = state[i][j]
#             tile.config(
#                 text=str(value) if value != 0 else "",
#                 bg="#E3F2FD" if value == 0 else "#FFFFFF",
#                 fg="#0D47A1"
#             )

# def create_state_grid(parent, state_3x3):
#     for i in range(3):
#         for j in range(3):
#             val = state_3x3[i][j]
#             bg_color = "#E3F2FD" if val == 0 else "#FFFFFF"
#             lbl = tk.Label(
#                 parent,
#                 text=str(val) if val != 0 else "",
#                 width=4,
#                 height=2,
#                 font=("Helvetica", 14, "bold"),
#                 bg=bg_color,
#                 fg="#0D47A1",
#                 bd=1,
#                 relief="solid"
#             )
#             lbl.grid(row=i, column=j, padx=2, pady=2)

# step_count = 0
# current_row_frame = None

# def add_step_frame(index, move_, state_3x3):
#     global step_count, current_row_frame
#     if step_count % 5 == 0:
#         current_row_frame = tk.Frame(steps_container, bg="#FAFAFA")
#         current_row_frame.pack(side="top", padx=5, pady=5)
#     step_frame = tk.Frame(current_row_frame, bg="#FAFAFA", bd=2, relief="ridge")
#     step_frame.pack(side="left", padx=5, pady=5)
#     lbl_title = tk.Label(
#         step_frame,
#         text=f"Bước {index}",
#         font=("Helvetica", 10, "bold"),
#         fg="#0D47A1",
#         bg="#FAFAFA"
#     )
#     lbl_title.pack(side="top", anchor="w", padx=5, pady=2)
#     grid_holder = tk.Frame(step_frame, bg="#FAFAFA")
#     grid_holder.pack(side="left", padx=5, pady=5)
#     create_state_grid(grid_holder, state_3x3)
#     step_count += 1

# def pause_program():
#     global paused
#     paused = True

# def resume_program():
#     global paused
#     paused = False

# def reset_program():
#     global running, paused, step_count, current_row_frame, current_group
#     running = False
#     paused = False
#     step_count = 0
#     current_row_frame = None
#     current_group = None  # Reset nhóm thuật toán
#     selected_algorithm.set("bfs")
#     for i in range(3):
#         for j in range(3):
#             initial_entries[i][j].delete(0, tk.END)
#             goal_entries[i][j].delete(0, tk.END)
#     for child in steps_container.winfo_children():
#         child.destroy()
#     for child in compare_tree.get_children():
#         compare_tree.delete(child)
#     blank_state = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
#     update_view(blank_state)
#     steps_count.config(text="Số bước: 0")
#     time_label.config(text="Thời gian: 00:00")
#     verification_label.config(text="Verification: ")

# def load_default_initial():
#     default_initial = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
#     # default_initial = [[1,2, 3], [4, 0, 5], [8, 7, 6]]
#     for i in range(3):
#         for j in range(3):
#             initial_entries[i][j].delete(0, tk.END)
#             initial_entries[i][j].insert(0, str(default_initial[i][j]))

# def load_default_goal():
#     default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
#     for i in range(3):
#         for j in range(3):
#             goal_entries[i][j].delete(0, tk.END)
#             goal_entries[i][j].insert(0, str(default_goal[i][j]))

# def update_comparison_table(algorithm_name, steps, total_time):
#     global compare_tree, current_group

#     # Xác định nhóm của thuật toán hiện tại
#     algo_group = "uninformed"
#     if algorithm_name in ["a_star", "ida_star", "greedy"]:
#         algo_group = "informed"
#     elif algorithm_name in ["genetic_algorithm", "beam_search", "simulated_annealing",
#                            "simple_hill_climbing", "steepest_ascent_hill_climbing",
#                            "stochastic_hill_climbing"]:
#         algo_group = "local"
#     elif algorithm_name in ["csp_ac3", "backtracking_search", "forward_checking"]:
#         algo_group = "constraint"
#     elif algorithm_name in ["partially_observable_search", "search_no_observation", "and_or_search"]:
#         algo_group = "complex"
#     elif algorithm_name in ["q_learning"]:
#         algo_group = "reinforcement"

#     # Nếu nhóm thay đổi hoặc bảng rỗng, xóa bảng và cập nhật nhóm
#     if current_group != algo_group or not compare_tree.get_children():
#         for child in compare_tree.get_children():
#             compare_tree.delete(child)
#         current_group = algo_group

#     # Kiểm tra xem thuật toán đã có trong bảng chưa
#     algo_display_name = algorithm_display.get(algorithm_name, algorithm_name)
#     for child in compare_tree.get_children():
#         if compare_tree.item(child)["values"][0] == algo_display_name:
#             compare_tree.delete(child)  # Xóa hàng cũ của thuật toán nếu đã tồn tại

#     # Thêm thông tin của thuật toán vào bảng
#     compare_tree.insert("", "end", values=(
#         algo_display_name,
#         steps,
#         f"{total_time:.2f}s"
#     ))

# def solve(algorithm_name):
#     global result, paused, running, step_count, current_row_frame
#     if not algorithm_name:
#         messagebox.showwarning("Selection Error", "Please select an algorithm!")
#         return
#     running = True
#     step_count = 0
#     current_row_frame = None
#     for child in steps_container.winfo_children():
#         child.destroy()

#     initial_state = get_state_from_entries(initial_entries)
#     if initial_state is None:
#         return
#     goal_state = get_state_from_entries(goal_entries)
#     if goal_state is None:
#         return
#     result = goal_state
#     update_view(initial_state)

#     # Chạy thuật toán được chọn
#     if algorithm_name in ["bfs", "dfs", "ucs", "ids"]:
#         solver = UninformedSearch(initial_state, goal_state)
#     elif algorithm_name in ["a_star", "ida_star", "greedy"]:
#         solver = InformedSearch(initial_state, goal_state)
#     elif algorithm_name in ["genetic_algorithm", "beam_search", "simulated_annealing",
#                            "simple_hill_climbing", "steepest_ascent_hill_climbing",
#                            "stochastic_hill_climbing"]:
#         solver = LocalSearch(initial_state, goal_state)
#     elif algorithm_name in ["csp_ac3", "backtracking_search", "forward_checking"]:
#         solver = ConstraintSearch(initial_state, goal_state)
#     elif algorithm_name in ["partially_observable_search", "search_no_observation", "and_or_search"]:
#         solver = ComplexSearch(initial_state, goal_state)
#     elif algorithm_name in ["q_learning"]:
#         solver = ReinforcementSearch(initial_state, goal_state)
#     else:
#         messagebox.showerror("Error", "Unsupported algorithm!")
#         return

#     algorithm = getattr(solver, algorithm_name)
#     start_time = time.time()

#     if algorithm_name == "csp_ac3":
#         solution = algorithm()
#         steps = 1 if solution else 0
#         if solution is not None:
#             final_state = solution
#             if final_state == goal_state:
#                 verification_result = "Correct"
#                 add_step_frame(0, "Start", initial_state)
#                 add_step_frame(1, "Solved", final_state)
#                 update_view(final_state)
#                 steps_count.config(text="Số bước: 1 (CSP)")
#                 total_time = time.time() - start_time
#                 time_label.config(text=f"Thời gian: {total_time:.2f}s")
#             else:
#                 verification_result = "Incorrect"
#                 messagebox.showinfo("Result", "Solution does not match goal state!")
#         else:
#             verification_result = "No solution"
#             steps_count.config(text="Số bước: 0")
#             time_label.config(text="Thời gian: 0s")
#             messagebox.showinfo("Result", "No solution found!")
#         verification_label.config(text=f"Verification: {verification_result}")
#     else:
#         if algorithm_name == "partially_observable_search":
#             noise_prob = noise_scale.get()
#             initial_percept = solver.observe(initial_state, noise_probability=noise_prob)
#             solution = algorithm(initial_percept, noise_probability=noise_prob)
#         else:
#             solution = algorithm(initial_state)
#         steps = len(solution) if solution else 0
#         if solution is not None:
#             try:
#                 final_state = solver.apply_moves(initial_state, solution)
#                 if final_state == goal_state:
#                     verification_result = "Correct"
#                 else:
#                     verification_result = "Incorrect"
#             except ValueError as e:
#                 verification_result = "Invalid moves"
#                 messagebox.showerror("Error", f"Invalid move in solution: {e}")
#                 solution = None
#         else:
#             verification_result = "No solution"
#         verification_label.config(text=f"Verification: {verification_result}")

#         if solution:
#             current_state = initial_state
#             add_step_frame(0, "Start", current_state)
#             for i, move_ in enumerate(solution, start=1):
#                 if not running:
#                     break
#                 while paused and running:
#                     root.update()
#                     time.sleep(0.1)
#                 root.update()
#                 time.sleep(delay)
#                 blank_i, blank_j = solver.find_blank(current_state)
#                 try:
#                     new_state = solver.swap(current_state, blank_i, blank_j,
#                                            blank_i + solver.step[move_][0],
#                                            blank_j + solver.step[move_][1])
#                     update_view(new_state)
#                     current_state = new_state
#                     add_step_frame(i, move_, new_state)
#                 except ValueError as e:
#                     messagebox.showerror("Error", f"Invalid move {move_}: {e}")
#                     break
#             if running:
#                 steps_count.config(text=f"Số bước: {len(solution)}")
#                 total_time = time.time() - start_time
#                 time_label.config(text=f"Thời gian: {total_time:.2f}s")
#         else:
#             total_time = time.time() - start_time
#             steps_count.config(text="Số bước: 0")
#             time_label.config(text="Thời gian: 0s")
#             messagebox.showinfo("Result", "No solution found!")

#     # Cập nhật bảng so sánh với thông tin của thuật toán được chọn
#     update_comparison_table(algorithm_name, steps, total_time)

# algorithm_display = {
#     "bfs": "BFS",
#     "dfs": "DFS",
#     "ucs": "UCS",
#     "ids": "IDS",
#     "a_star": "A*",
#     "ida_star": "IDA*",
#     "greedy": "Greedy",
#     "genetic_algorithm": "Genetic Algorithm",
#     "beam_search": "Beam Search",
#     "simulated_annealing": "Simulated Annealing",
#     "simple_hill_climbing": "Simple Hill Climbing",
#     "steepest_ascent_hill_climbing": "Steepest Ascent Hill Climbing",
#     "stochastic_hill_climbing": "Stochastic Hill Climbing",
#     "csp_ac3": "AC-3",
#     "backtracking_search": "Backtracking Search",
#     "forward_checking": "Forward Checking",
#     "partially_observable_search": "Partially Observable Search",
#     "search_no_observation": "Search with No Observation",
#     "and_or_search": "AND-OR Search",
#     "q_learning": "Q-Learning"
# }

# def run_gui():
#     global view_labels, initial_entries, goal_entries, steps_count, time_label
#     global verification_label, steps_container, noise_scale, selected_algorithm, displayed_algorithm
#     global root, compare_tree

#     root = tk.Tk()
#     root.title("8-Puzzle Solver - Trần Hồ Phương Nguyên")
#     root.geometry("1200x700")
#     root.configure(bg="#ECEFF1")

#     style = ttk.Style()
#     style.configure("TButton", font=("Helvetica", 10), padding=5)
#     style.configure("TLabel", font=("Helvetica", 12), background="#ECEFF1")
#     style.configure("TCombobox", font=("Helvetica", 10))
#     style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
#     style.configure("Treeview", font=("Helvetica", 11))

#     selected_algorithm = tk.StringVar(value="bfs")
#     displayed_algorithm = tk.StringVar(value="BFS")

#     def update_displayed_algorithm(*args):
#         alg = selected_algorithm.get()
#         displayed_algorithm.set(algorithm_display.get(alg, "None"))

#     selected_algorithm.trace("w", update_displayed_algorithm)

#     menubar = tk.Menu(root)
#     uninformed_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
#     informed_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
#     local_search_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
#     complex_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
#     constraint_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
#     reinforcement_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))

#     for alg in ["bfs", "dfs", "ucs", "ids"]:
#         uninformed_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
#     for alg in ["a_star", "greedy", "ida_star"]:
#         informed_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
#     for alg in ["genetic_algorithm", "beam_search", "simulated_annealing",
#                 "simple_hill_climbing", "steepest_ascent_hill_climbing", "stochastic_hill_climbing"]:
#         local_search_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
#     for alg in ["and_or_search", "partially_observable_search", "search_no_observation"]:
#         complex_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
#     for alg in ["backtracking_search", "csp_ac3", "forward_checking"]:
#         constraint_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
#     for alg in ["q_learning"]:
#         reinforcement_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)

#     menubar.add_cascade(label="Uninformed Search", menu=uninformed_menu)
#     menubar.add_cascade(label="Informed Search", menu=informed_menu)
#     menubar.add_cascade(label="Local Search Algorithms", menu=local_search_menu)
#     menubar.add_cascade(label="Search in Complex Environments", menu=complex_menu)
#     menubar.add_cascade(label="Constraint Satisfaction Search", menu=constraint_menu)
#     menubar.add_cascade(label="Reinforcement Learning", menu=reinforcement_menu)
#     root.config(menu=menubar)

#     main_frame = tk.Frame(root, bg="#ECEFF1")
#     main_frame.pack(fill="both", expand=True, padx=20, pady=20)

#     input_frame = tk.Frame(main_frame, bg="#FFFFFF", bd=2, relief="flat")
#     input_frame.pack(side="left", padx=10, pady=10, fill="y")

#     initial_frame = tk.Frame(input_frame, bg="#FFFFFF")
#     initial_frame.pack(pady=10)
#     tk.Label(initial_frame, text="Initial State", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
#     initial_entries = []
#     for i in range(3):
#         row = []
#         frame = tk.Frame(initial_frame, bg="#FFFFFF")
#         frame.pack()
#         for j in range(3):
#             entry = ttk.Entry(frame, width=4, font=("Helvetica", 12), justify="center")
#             entry.pack(side="left", padx=2, pady=2)
#             row.append(entry)
#         initial_entries.append(row)
#     ttk.Button(initial_frame, text="Load Default", command=load_default_initial).pack(pady=5)

#     goal_frame = tk.Frame(input_frame, bg="#FFFFFF")
#     goal_frame.pack(pady=10)
#     tk.Label(goal_frame, text="Goal State", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
#     goal_entries = []
#     for i in range(3):
#         row = []
#         frame = tk.Frame(goal_frame, bg="#FFFFFF")
#         frame.pack()
#         for j in range(3):
#             entry = ttk.Entry(frame, width=4, font=("Helvetica", 12), justify="center")
#             entry.pack(side="left", padx=2, pady=2)
#             row.append(entry)
#         goal_entries.append(row)
#     ttk.Button(goal_frame, text="Load Default", command=load_default_goal).pack(pady=5)

#     compare_frame = tk.Frame(input_frame, bg="#FFFFFF")
#     compare_frame.pack(pady=10, fill="x")
#     tk.Label(compare_frame, text="Algorithm Performance", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
#     compare_tree = ttk.Treeview(compare_frame, columns=("Algorithm", "Steps", "Time"), show="headings", height=5)
#     compare_tree.heading("Algorithm", text="Algorithm")
#     compare_tree.heading("Steps", text="Steps")
#     compare_tree.heading("Time", text="Time (s)")
#     compare_tree.column("Algorithm", width=200)
#     compare_tree.column("Steps", width=100)
#     compare_tree.column("Time", width=100)
#     compare_tree.pack(fill="x", padx=5, pady=5)

#     algo_frame = tk.Frame(input_frame, bg="#FFFFFF")
#     algo_frame.pack(pady=10, fill="x")
#     tk.Label(algo_frame, text="Selected Algorithm:", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1").pack()
#     tk.Label(algo_frame, textvariable=displayed_algorithm, font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1").pack()

#     # noise_frame = tk.Frame(input_frame, bg="#FFFFFF")
#     # noise_frame.pack(pady=10)
#     # tk.Label(noise_frame, text="Noise Probability:", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1").pack(side="left")
#     # noise_scale = tk.Scale(noise_frame, from_=0.0, to=0.5, resolution=0.01, orient="horizontal", length=100, bg="#FFFFFF", fg="#0D47A1", font=("Helvetica", 10))
#     # noise_scale.set(0.1)
#     # noise_scale.pack(side="left", padx=5)

#     display_frame = tk.Frame(main_frame, bg="#FFFFFF", bd=2, relief="flat")
#     display_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

#     info_frame = tk.Frame(display_frame, bg="#FFFFFF")
#     info_frame.pack(fill="x", pady=5)
#     steps_count = tk.Label(info_frame, text="Số bước: 0", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1")
#     steps_count.pack(side="left", padx=10)
#     time_label = tk.Label(info_frame, text="Thời gian: 00:00", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1")
#     time_label.pack(side="left", padx=10)
#     verification_label = tk.Label(info_frame, text="Verification: ", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1")
#     verification_label.pack(side="left", padx=10)

#     view_frame = tk.Frame(display_frame, bg="#FFFFFF")
#     view_frame.pack(pady=10)
#     tk.Label(view_frame, text="Current State", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
#     view_labels = []
#     for i in range(3):
#         row = []
#         frame = tk.Frame(view_frame, bg="#FFFFFF")
#         frame.pack()
#         for j in range(3):
#             label = tk.Label(
#                 frame,
#                 text="",
#                 width=4,
#                 height=2,
#                 font=("Helvetica", 14, "bold"),
#                 bg="#FFFFFF",
#                 fg="#0D47A1",
#                 bd=1,
#                 relief="solid"
#             )
#             label.pack(side="left", padx=2, pady=2)
#             row.append(label)
#         view_labels.append(row)

#     control_frame = tk.Frame(display_frame, bg="#FFFFFF")
#     control_frame.pack(pady=10)
#     ttk.Button(control_frame, text="Solve", command=lambda: solve(selected_algorithm.get())).pack(side="left", padx=5)
#     ttk.Button(control_frame, text="Pause", command=pause_program).pack(side="left", padx=5)
#     ttk.Button(control_frame, text="Resume", command=resume_program).pack(side="left", padx=5)
#     ttk.Button(control_frame, text="Reset", command=reset_program).pack(side="left", padx=5)

#     steps_frame = tk.Frame(display_frame, bg="#FFFFFF")
#     steps_frame.pack(fill="both", expand=True)
#     tk.Label(steps_frame, text="Solution Steps", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
#     canvas = tk.Canvas(steps_frame, bg="#FAFAFA")
#     scrollbar = tk.Scrollbar(steps_frame, orient="vertical", command=canvas.yview)
#     scrollable_frame = tk.Frame(canvas, bg="#FAFAFA")
#     scrollable_frame.bind(
#         "<Configure>",
#         lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
#     )
#     canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
#     canvas.configure(yscrollcommand=scrollbar.set)
#     scrollbar.pack(side="right", fill="y")
#     canvas.pack(side="left", fill="both", expand=True)
#     steps_container = scrollable_frame

#     root.mainloop()

# if __name__ == "__main__":
#     run_gui()


import tkinter as tk
from tkinter import messagebox, ttk
import time
from kthongtin import UninformedSearch
from cothongtin import InformedSearch
from cucbo import LocalSearch
from rangbuoc import ConstraintSearch
from phuctap import ComplexSearch
from cungco import ReinforcementSearch
from utils import PuzzleSolverBase

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
view_labels = []
initial_entries = []
goal_entries = []
steps_count = None
time_label = None
verification_label = None
steps_container = None
selected_algorithm = None
displayed_algorithm = None
root = None
compare_tree = None
current_group = None  # Biến để theo dõi nhóm thuật toán hiện tại của bảng so sánh
algorithm_list = [
    "bfs", "dfs", "ucs", "ids",
    "a_star", "ida_star", "greedy",
    "genetic_algorithm", "beam_search", "simulated_annealing",
    "simple_hill_climbing", "steepest_ascent_hill_climbing", "stochastic_hill_climbing",
    "csp_ac3", "backtracking_search", "forward_checking",
    "partially_observable_search", "search_no_observation", "and_or_search",
    "q_learning"
]
current_algorithm_index = 0  # Theo dõi chỉ số thuật toán hiện tại

def update_view(state):
    for i in range(3):
        for j in range(3):
            tile = view_labels[i][j]
            value = state[i][j]
            tile.config(
                text=str(value) if value != 0 else "",
                bg="#E3F2FD" if value == 0 else "#FFFFFF",
                fg="#0D47A1"
            )

def create_state_grid(parent, state_3x3):
    for i in range(3):
        for j in range(3):
            val = state_3x3[i][j]
            bg_color = "#E3F2FD" if val == 0 else "#FFFFFF"
            lbl = tk.Label(
                parent,
                text=str(val) if val != 0 else "",
                width=4,
                height=2,
                font=("Helvetica", 14, "bold"),
                bg=bg_color,
                fg="#0D47A1",
                bd=1,
                relief="solid"
            )
            lbl.grid(row=i, column=j, padx=2, pady=2)

step_count = 0
current_row_frame = None

def add_step_frame(index, move_, state_3x3):
    global step_count, current_row_frame
    if step_count % 5 == 0:
        current_row_frame = tk.Frame(steps_container, bg="#FAFAFA")
        current_row_frame.pack(side="top", padx=5, pady=5)
    step_frame = tk.Frame(current_row_frame, bg="#FAFAFA", bd=2, relief="ridge")
    step_frame.pack(side="left", padx=5, pady=5)
    lbl_title = tk.Label(
        step_frame,
        text=f"Bước {index}",
        font=("Helvetica", 10, "bold"),
        fg="#0D47A1",
        bg="#FAFAFA"
    )
    lbl_title.pack(side="top", anchor="w", padx=5, pady=2)
    grid_holder = tk.Frame(step_frame, bg="#FAFAFA")
    grid_holder.pack(side="left", padx=5, pady=5)
    create_state_grid(grid_holder, state_3x3)
    step_count += 1

def pause_program():
    global paused
    paused = True

def resume_program():
    global paused
    paused = False

def reset_program():
    global running, paused, step_count, current_row_frame, current_group, current_algorithm_index
    running = False
    paused = False
    step_count = 0
    current_row_frame = None
    current_group = None  # Reset nhóm thuật toán
    current_algorithm_index = 0  # Reset về thuật toán đầu tiên
    selected_algorithm.set("bfs")
    for i in range(3):
        for j in range(3):
            initial_entries[i][j].delete(0, tk.END)
            goal_entries[i][j].delete(0, tk.END)
    for child in steps_container.winfo_children():
        child.destroy()
    for child in compare_tree.get_children():
        compare_tree.delete(child)
    blank_state = ((0, 0, 0), (0, 0, 0), (0, 0, 0))
    update_view(blank_state)
    steps_count.config(text="Số bước: 0")
    time_label.config(text="Thời gian: 00:00")
    verification_label.config(text="Verification: ")

def load_default_initial():
    default_initial = [[2, 6, 5], [0, 8, 7], [4, 3, 1]]
    for i in range(3):
        for j in range(3):
            initial_entries[i][j].delete(0, tk.END)
            initial_entries[i][j].insert(0, str(default_initial[i][j]))

def load_default_goal():
    default_goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    for i in range(3):
        for j in range(3):
            goal_entries[i][j].delete(0, tk.END)
            goal_entries[i][j].insert(0, str(default_goal[i][j]))

def update_comparison_table(algorithm_name, steps, total_time):
    global compare_tree, current_group

    # Xác định nhóm của thuật toán hiện tại
    algo_group = "uninformed"
    if algorithm_name in ["a_star", "ida_star", "greedy"]:
        algo_group = "informed"
    elif algorithm_name in ["genetic_algorithm", "beam_search", "simulated_annealing",
                           "simple_hill_climbing", "steepest_ascent_hill_climbing",
                           "stochastic_hill_climbing"]:
        algo_group = "local"
    elif algorithm_name in ["csp_ac3", "backtracking_search", "forward_checking"]:
        algo_group = "constraint"
    elif algorithm_name in ["partially_observable_search", "search_no_observation", "and_or_search"]:
        algo_group = "complex"
    elif algorithm_name in ["q_learning"]:
        algo_group = "reinforcement"

    # Nếu nhóm thay đổi hoặc bảng rỗng, xóa bảng và cập nhật nhóm
    if current_group != algo_group or not compare_tree.get_children():
        for child in compare_tree.get_children():
            compare_tree.delete(child)
        current_group = algo_group

    # Kiểm tra xem thuật toán đã có trong bảng chưa
    algo_display_name = algorithm_display.get(algorithm_name, algorithm_name)
    for child in compare_tree.get_children():
        if compare_tree.item(child)["values"][0] == algo_display_name:
            compare_tree.delete(child)  # Xóa hàng cũ của thuật toán nếu đã tồn tại

    # Thêm thông tin của thuật toán vào bảng
    compare_tree.insert("", "end", values=(
        algo_display_name,
        steps,
        f"{total_time:.2f}s"
    ))

def solve(algorithm_name):
    global result, paused, running, step_count, current_row_frame, current_algorithm_index
    if not algorithm_name:
        messagebox.showwarning("Selection Error", "Please select an algorithm!")
        return
    running = True
    step_count = 0
    current_row_frame = None
    for child in steps_container.winfo_children():
        child.destroy()

    initial_state = get_state_from_entries(initial_entries)
    if initial_state is None:
        return
    goal_state = get_state_from_entries(goal_entries)
    if goal_state is None:
        return
    result = goal_state
    update_view(initial_state)

    # Chạy thuật toán được chọn
    if algorithm_name in ["bfs", "dfs", "ucs", "ids"]:
        solver = UninformedSearch(initial_state, goal_state)
    elif algorithm_name in ["a_star", "ida_star", "greedy"]:
        solver = InformedSearch(initial_state, goal_state)
    elif algorithm_name in ["genetic_algorithm", "beam_search", "simulated_annealing",
                           "simple_hill_climbing", "steepest_ascent_hill_climbing",
                           "stochastic_hill_climbing"]:
        solver = LocalSearch(initial_state, goal_state)
    elif algorithm_name in ["csp_ac3", "backtracking_search", "forward_checking"]:
        solver = ConstraintSearch(initial_state, goal_state)
    elif algorithm_name in ["partially_observable_search", "search_no_observation", "and_or_search"]:
        solver = ComplexSearch(initial_state, goal_state)
    elif algorithm_name in ["q_learning"]:
        solver = ReinforcementSearch(initial_state, goal_state)
    else:
        messagebox.showerror("Error", "Unsupported algorithm!")
        return

    algorithm = getattr(solver, algorithm_name)
    start_time = time.time()

    if algorithm_name == "csp_ac3":
        solution = algorithm()
        steps = 1 if solution else 0
        if solution is not None:
            final_state = solution
            if final_state == goal_state:
                verification_result = "Correct"
                add_step_frame(0, "Start", initial_state)
                add_step_frame(1, "Solved", final_state)
                update_view(final_state)
                steps_count.config(text="Số bước: 1 (CSP)")
                total_time = time.time() - start_time
                time_label.config(text=f"Thời gian: {total_time:.2f}s")
            else:
                verification_result = "Incorrect"
                messagebox.showinfo("Result", "Solution does not match goal state!")
        else:
            verification_result = "No solution"
            steps_count.config(text="Số bước: 0")
            time_label.config(text="Thời gian: 0s")
            messagebox.showinfo("Result", "No solution found!")
        verification_label.config(text=f"Verification: {verification_result}")
    else:
        if algorithm_name == "partially_observable_search":
            initial_percept = solver.observe(initial_state, noise_probability=0.0)
            solution = algorithm(initial_percept, noise_probability=0.0)
        else:
            solution = algorithm(initial_state)
        steps = len(solution) if solution else 0
        if solution is not None:
            try:
                final_state = solver.apply_moves(initial_state, solution)
                if final_state == goal_state:
                    verification_result = "Correct"
                else:
                    verification_result = "Incorrect"
            except ValueError as e:
                verification_result = "Invalid moves"
                messagebox.showerror("Error", f"Invalid move in solution: {e}")
                solution = None
        else:
            verification_result = "No solution"
        verification_label.config(text=f"Verification: {verification_result}")

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
                try:
                    new_state = solver.swap(current_state, blank_i, blank_j,
                                           blank_i + solver.step[move_][0],
                                           blank_j + solver.step[move_][1])
                    update_view(new_state)
                    current_state = new_state
                    add_step_frame(i, move_, new_state)
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid move {move_}: {e}")
                    break
            if running:
                steps_count.config(text=f"Số bước: {len(solution)}")
                total_time = time.time() - start_time
                time_label.config(text=f"Thời gian: {total_time:.2f}s")
        else:
            total_time = time.time() - start_time
            steps_count.config(text="Số bước: 0")
            time_label.config(text="Thời gian: 0s")
            messagebox.showinfo("Result", "No solution found!")

    # Cập nhật bảng so sánh với thông tin của thuật toán được chọn
    update_comparison_table(algorithm_name, steps, total_time)

    # Chuyển sang thuật toán tiếp theo
    current_algorithm_index = (current_algorithm_index + 1) % len(algorithm_list)
    next_algorithm = algorithm_list[current_algorithm_index]
    selected_algorithm.set(next_algorithm)
    displayed_algorithm.set(algorithm_display.get(next_algorithm, next_algorithm))

algorithm_display = {
    "bfs": "BFS",
    "dfs": "DFS",
    "ucs": "UCS",
    "ids": "IDS",
    "a_star": "A*",
    "ida_star": "IDA*",
    "greedy": "Greedy",
    "genetic_algorithm": "Genetic Algorithm",
    "beam_search": "Beam Search",
    "simulated_annealing": "Simulated Annealing",
    "simple_hill_climbing": "Simple Hill Climbing",
    "steepest_ascent_hill_climbing": "Steepest Ascent Hill Climbing",
    "stochastic_hill_climbing": "Stochastic Hill Climbing",
    "csp_ac3": "AC-3",
    "backtracking_search": "Backtracking Search",
    "forward_checking": "Forward Checking",
    "partially_observable_search": "Partially Observable Search",
    "search_no_observation": "Search with No Observation",
    "and_or_search": "AND-OR Search",
    "q_learning": "Q-Learning"
}

def run_gui():
    global view_labels, initial_entries, goal_entries, steps_count, time_label
    global verification_label, steps_container, selected_algorithm, displayed_algorithm
    global root, compare_tree

    root = tk.Tk()
    root.title("8-Puzzle Solver - Trần Hồ Phương Nguyên")
    root.geometry("1200x700")
    root.configure(bg="#ECEFF1")

    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 10), padding=5)
    style.configure("TLabel", font=("Helvetica", 12), background="#ECEFF1")
    style.configure("TCombobox", font=("Helvetica", 10))
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
    style.configure("Treeview", font=("Helvetica", 11))

    selected_algorithm = tk.StringVar(value="bfs")
    displayed_algorithm = tk.StringVar(value="BFS")

    def update_displayed_algorithm(*args):
        alg = selected_algorithm.get()
        displayed_algorithm.set(algorithm_display.get(alg, "None"))

    selected_algorithm.trace("w", update_displayed_algorithm)

    menubar = tk.Menu(root)
    uninformed_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
    informed_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
    local_search_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
    complex_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
    constraint_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))
    reinforcement_menu = tk.Menu(menubar, tearoff=0, font=("Helvetica", 10))

    for alg in ["bfs", "dfs", "ucs", "ids"]:
        uninformed_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
    for alg in ["a_star", "greedy", "ida_star"]:
        informed_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
    for alg in ["genetic_algorithm", "beam_search", "simulated_annealing",
                "simple_hill_climbing", "steepest_ascent_hill_climbing", "stochastic_hill_climbing"]:
        local_search_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
    for alg in ["and_or_search", "partially_observable_search", "search_no_observation"]:
        complex_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
    for alg in ["backtracking_search", "csp_ac3", "forward_checking"]:
        constraint_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)
    for alg in ["q_learning"]:
        reinforcement_menu.add_radiobutton(label=algorithm_display[alg], variable=selected_algorithm, value=alg)

    menubar.add_cascade(label="Uninformed Search", menu=uninformed_menu)
    menubar.add_cascade(label="Informed Search", menu=informed_menu)
    menubar.add_cascade(label="Local Search Algorithms", menu=local_search_menu)
    menubar.add_cascade(label="Search in Complex Environments", menu=complex_menu)
    menubar.add_cascade(label="Constraint Satisfaction Search", menu=constraint_menu)
    menubar.add_cascade(label="Reinforcement Learning", menu=reinforcement_menu)
    root.config(menu=menubar)

    main_frame = tk.Frame(root, bg="#ECEFF1")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)

    input_frame = tk.Frame(main_frame, bg="#FFFFFF", bd=2, relief="flat")
    input_frame.pack(side="left", padx=10, pady=10, fill="y")

    initial_frame = tk.Frame(input_frame, bg="#FFFFFF")
    initial_frame.pack(pady=10)
    tk.Label(initial_frame, text="Initial State", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
    initial_entries = []
    for i in range(3):
        row = []
        frame = tk.Frame(initial_frame, bg="#FFFFFF")
        frame.pack()
        for j in range(3):
            entry = ttk.Entry(frame, width=4, font=("Helvetica", 12), justify="center")
            entry.pack(side="left", padx=2, pady=2)
            row.append(entry)
        initial_entries.append(row)
    ttk.Button(initial_frame, text="Load Default", command=load_default_initial).pack(pady=5)

    goal_frame = tk.Frame(input_frame, bg="#FFFFFF")
    goal_frame.pack(pady=10)
    tk.Label(goal_frame, text="Goal State", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
    goal_entries = []
    for i in range(3):
        row = []
        frame = tk.Frame(goal_frame, bg="#FFFFFF")
        frame.pack()
        for j in range(3):
            entry = ttk.Entry(frame, width=4, font=("Helvetica", 12), justify="center")
            entry.pack(side="left", padx=2, pady=2)
            row.append(entry)
        goal_entries.append(row)
    ttk.Button(goal_frame, text="Load Default", command=load_default_goal).pack(pady=5)

    # compare_frame = tk.Frame(input_frame, bg="#FFFFFF")
    # compare_frame.pack(pady=10, fill="x")
    # tk.Label(compare_frame, text="Algorithm Performance", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
    # compare_tree = ttk.Treeview(compare_frame, columns=("Algorithm", "Steps", "Time"), show="headings", height=10)
    # compare_tree.heading("Algorithm", text="Algorithm")
    # compare_tree.heading("Steps", text="Steps")
    # compare_tree.heading("Time", text="Time (s)")
    # compare_tree.column("Algorithm", width=200)
    # compare_tree.column("Steps", width=100)
    # compare_tree.column("Time", width=100)
    # compare_tree.pack(fill="x", padx=5, pady=5)

    compare_frame = tk.Frame(input_frame, bg="#FFFFFF", height=300)  # Đặt chiều cao cố định (300 pixel)
    compare_frame.pack(pady=10, fill="x")
    compare_frame.pack_propagate(False)  # Ngăn frame co lại theo nội dung
    tk.Label(compare_frame, text="Algorithm Performance", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
    compare_tree = ttk.Treeview(compare_frame, columns=("Algorithm", "Steps", "Time"), show="headings", height=6)  # Tăng height để lấp đầy
    compare_tree.heading("Algorithm", text="Algorithm")
    compare_tree.heading("Steps", text="Steps")
    compare_tree.heading("Time", text="Time (s)")
    compare_tree.column("Algorithm", width=200)
    compare_tree.column("Steps", width=100)
    compare_tree.column("Time", width=100)
    compare_tree.pack(fill="both", expand=True, padx=5, pady=5)  # Sử dụng fill="both" và expand=True

    algo_frame = tk.Frame(input_frame, bg="#FFFFFF")
    algo_frame.pack(pady=10, fill="x")
    tk.Label(algo_frame, text="Selected Algorithm:", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1").pack()
    tk.Label(algo_frame, textvariable=displayed_algorithm, font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1").pack()

    display_frame = tk.Frame(main_frame, bg="#FFFFFF", bd=2, relief="flat")
    display_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    info_frame = tk.Frame(display_frame, bg="#FFFFFF")
    info_frame.pack(fill="x", pady=5)
    steps_count = tk.Label(info_frame, text="Số bước: 0", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1")
    steps_count.pack(side="left", padx=10)
    time_label = tk.Label(info_frame, text="Thời gian: 00:00", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1")
    time_label.pack(side="left", padx=10)
    verification_label = tk.Label(info_frame, text="Verification: ", font=("Helvetica", 12), bg="#FFFFFF", fg="#0D47A1")
    verification_label.pack(side="left", padx=10)

    view_frame = tk.Frame(display_frame, bg="#FFFFFF")
    view_frame.pack(pady=10)
    tk.Label(view_frame, text="Current State", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
    view_labels = []
    for i in range(3):
        row = []
        frame = tk.Frame(view_frame, bg="#FFFFFF")
        frame.pack()
        for j in range(3):
            label = tk.Label(
                frame,
                text="",
                width=4,
                height=2,
                font=("Helvetica", 14, "bold"),
                bg="#FFFFFF",
                fg="#0D47A1",
                bd=1,
                relief="solid"
            )
            label.pack(side="left", padx=2, pady=2)
            row.append(label)
        view_labels.append(row)

    control_frame = tk.Frame(display_frame, bg="#FFFFFF")
    control_frame.pack(pady=10)
    ttk.Button(control_frame, text="Solve", command=lambda: solve(selected_algorithm.get())).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Pause", command=pause_program).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Resume", command=resume_program).pack(side="left", padx=5)
    ttk.Button(control_frame, text="Reset", command=reset_program).pack(side="left", padx=5)

    steps_frame = tk.Frame(display_frame, bg="#FFFFFF")
    steps_frame.pack(fill="both", expand=True)
    tk.Label(steps_frame, text="Solution Steps", font=("Helvetica", 14, "bold"), bg="#FFFFFF", fg="#0D47A1").pack()
    canvas = tk.Canvas(steps_frame, bg="#FAFAFA")
    scrollbar = tk.Scrollbar(steps_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#FAFAFA")
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    steps_container = scrollable_frame

    root.mainloop()

if __name__ == "__main__":
    run_gui()