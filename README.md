# 8 Puzzle
## 1. Mục tiêu
Bài toán 8-puzzle là một dạng bài toán cổ điển trong trí tuệ nhân tạo, thuộc lớp các bài toán tìm kiếm trong không gian trạng thái. Đề tài này hướng đến việc giải bài toán 8-puzzle bằng nhiều phương pháp tìm kiếm khác nhau, từ cơ bản đến nâng cao, nhằm đạt được các mục tiêu cụ thể sau:
### 1.1. Mô hình hóa và giải quyết bài toán 8-puzzle

- Ánh xạ bài toán thực tế về một không gian trạng thái rời rạc, trong đó mỗi trạng thái là một cấu hình hợp lệ của lưới 3x3 gồm các ô từ 0 đến 8 (với 0 đại diện cho ô trống).

- Xây dựng các phép toán chuyển trạng thái (di chuyển ô trống lên, xuống, trái, phải).

- Phát triển hàm đánh giá và điều kiện dừng phù hợp để dẫn tới trạng thái đích.

### 1.2. Triển khai và thử nghiệm nhiều nhóm thuật toán tìm kiếm
Mỗi nhóm thuật toán đại diện cho một hướng tiếp cận khác nhau trong việc giải quyết bài toán:

a. Thuật toán tìm kiếm không thông tin (Uninformed Search)
BFS (Breadth-First Search): Tìm theo bề rộng, đảm bảo tìm ra lời giải ngắn nhất nếu tồn tại.

DFS (Depth-First Search): Tìm theo chiều sâu, yêu cầu giới hạn độ sâu để tránh lặp vô tận.

UCS (Uniform Cost Search): Ưu tiên mở rộng trạng thái có chi phí thấp nhất.

IDS (Iterative Deepening Search): Kết hợp BFS và DFS để tận dụng ưu điểm của cả hai.

b. Thuật toán tìm kiếm có thông tin (Informed Search)
Greedy Best-First Search: Dựa hoàn toàn vào hàm heuristic, đi đến trạng thái có ước lượng gần đích nhất.

A* (A-Star Search): Kết hợp giữa chi phí thực tế và heuristic, vừa nhanh vừa tối ưu.

IDA* (Iterative Deepening A*): Tiết kiệm bộ nhớ hơn A*, duyệt theo ngưỡng f = g + h.

c. Thuật toán tìm kiếm cục bộ (Local Search)
Simple Hill Climbing: Tăng dần theo hướng cải thiện.

Steepest Ascent Hill Climbing: Chọn hướng cải thiện tốt nhất tại mỗi bước.

Stochastic Hill Climbing: Ngẫu nhiên chọn một cải thiện hợp lệ.

Simulated Annealing: Chấp nhận tạm thời các bước tồi hơn để tránh kẹt cực trị địa phương.

Beam Search: Duy trì một số lượng nhỏ các trạng thái tốt nhất theo beam width.

Genetic Algorithm: Sử dụng khái niệm quần thể, lai ghép và đột biến để tiến hóa lời giải.

d. Thuật toán trong môi trường phức tạp (Complex Environment Search)
Partially Observable Search: Tìm kiếm trong điều kiện chỉ quan sát một phần trạng thái.

Search with No Observation: Giải bài toán khi không có thông tin quan sát nào.

AND-OR Search: Xử lý môi trường không chắc chắn bằng cây quyết định phức hợp.

e. Tìm kiếm thỏa mãn ràng buộc (Constraint Satisfaction Problem - CSP)
AC-3 (Arc Consistency): Đảm bảo miền giá trị không mâu thuẫn thông qua loại bỏ dần.

Backtracking Search: Tìm lời giải bằng cách thử và quay lui khi vi phạm ràng buộc.

Forward Checking: Kiểm tra trước để tránh mở rộng những nhánh không hợp lệ.

f. Học tăng cường (Reinforcement Learning)
Q-Learning: Học chính sách hành động tối ưu qua tương tác với môi trường mà không cần mô hình trạng thái.

### 1.3. Xây dựng giao diện người dùng trực quan
- Sử dụng thư viện Tkinter để thiết kế giao diện nhập trạng thái ban đầu và đích.
- Hiển thị từng bước di chuyển của thuật toán.
- Cho phép chọn và chạy từng thuật toán khác nhau.
- Cung cấp bảng thống kê để hỗ trợ đánh giá hiệu quả.

## 2. Nội dung
## 3. Kết luận

