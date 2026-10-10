#FINAL 5x5 Custom Maze
### Maze Info
- Size: 5x5
- Total Nodes: 22 (3 Walls)
- Costs: Normal=1, Mud F,O=10, Water E=20
- Start=S, Goal=X (renamed to GO in code)

### Maze Layout
S A B C D
E # F G H  # = Wall
I J # K L
M N O # X  X = Goal
P Q R U V

### Features of Code
- Builds Graph (Adjacency List) from Maze
- Calculates cost based on cell type (E=20, F,O=10)
- Implements BFS (Queue), DFS (Stack), UCS (Priority Queue)
- Shows full TRACE: Frontier, Explored, Path, Cost
- Final Comparison Table with Optimal check

### Algorithms
**BFS:** Finds path with fewest steps (ignores cost)
**DFS:** Goes deep first, not optimal
**UCS:** Finds lowest-cost path, avoids Water/Mud - Optimal

### How to Run
python maze.py

### Output
1. Maze Layout
2. Adjacency List
3. BFS TRACE
4. DFS TRACE
5. UCS TRACE
6. COMPARISON TABLE

Created for AI Lab Task 1
