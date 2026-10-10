# Maze size 5x5 - 22 nodes - Costs: Normal=1, Mud F,O=10, Water E=20

# Import deque for BFS queue
from collections import deque
# Import heapq for priority queue (UCS)
import heapq

# Define MAZE - 5 rows, 5 columns
# S = Start, X = Goal (GO), # = Wall, Others = Normal cells
# E = Water (cost 20), F,O = Mud (cost 10)
MAZE = [
    "SABCD", # Row 0
    "E#FGH", # Row 1 - # is wall
    "IJ#KL", # Row 2 - # is wall
    "MNO#X", # Row 3 - # is wall, X is Goal
    "PQRUV", # Row 4 - Custom row to make 5x5 (22 nodes)
]

# Define movement cost for each cell type
def get_cost(char):
    # If cell is E, it is Water
    if char == 'E':
        # Water cost is 20
        return 20
    # If cell is F or O, it is Mud
    if char in ('F', 'O'):
        # Mud cost is 10
        return 10
    # All other cells are normal
    # Normal cost is 1
    return 1

# Define possible actions for agent
ACTIONS = [
    (-1, 0, 'Up'), # Move Up
    (1, 0, 'Down'), # Move Down
    (0, -1, 'Left'), # Move Left
    (0, 1, 'Right'), # Move Right
]

# Function to convert Maze into Graph (Adjacency List)
def build_graph(maze):
    # Create empty graph
    graph = {}
    # Create dictionary to store name to position
    name_to_pos = {}
    # Create dictionary to store position to name
    pos_to_name = {}

    # First pass: create all nodes
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            ch = maze[r][c]
            # Skip if wall
            if ch == '#':
                continue
            # If X, rename to GO
            if ch == 'X':
                name = 'GO'
            else:
                name = ch
            # Save position
            name_to_pos[name] = (r, c)
            pos_to_name[(r, c)] = name
            graph[name] = []

    # Second pass: create edges
    for (r, c), name in pos_to_name.items():
        for dr, dc, act in ACTIONS:
            # Calculate new position
            nr = r + dr
            nc = c + dc
            # Check if inside maze
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]):
                # Check if next cell exists and not wall
                if (nr, nc) in pos_to_name:
                    dest = pos_to_name[(nr, nc)]
                    # Get cost of destination cell
                    cost = get_cost(maze[nr][nc])
                    # Add edge
                    graph[name].append((dest, cost, act))
    # Return graph and mappings
    return graph, name_to_pos, pos_to_name

# Function to calculate total path cost
def path_cost(graph, path):
    # Initialize total to zero
    total = 0
    # Loop through path
    for i in range(len(path)-1):
        a = path[i]
        b = path[i+1]
        # Find cost between a and b
        for nbr, c, _ in graph[a]:
            if nbr == b:
                total += c
                break
    return total

# Function to reconstruct path from parent
def reconstruct(parent, goal):
    # Start from goal
    path = [goal]
    # Go backwards using parent
    while parent[path[-1]] is not None:
        path.append(parent[path[-1]])
    # Reverse to get start to goal
    path.reverse()
    return path

# BFS - Breadth First Search
def bfs(graph, start, goal):
    # Frontier as queue
    frontier = deque([start])
    # Parent dictionary
    parent = {start: None}
    # Explored list
    explored = []
    explored_set = set()
    # Trace for report
    trace = []
    while frontier:
        # Pop from front
        node = frontier.popleft()
        if node in explored_set:
            continue
        explored.append(node)
        explored_set.add(node)
        cur_path = reconstruct(parent, node)
        cost = path_cost(graph, cur_path)
        trace.append((node, list(frontier), list(explored), cur_path, cost))
        # Check goal
        if node == goal:
            return cur_path, cost, len(explored), trace
        # Add children
        for child, _, _ in graph[node]:
            if child not in parent:
                parent[child] = node
                frontier.append(child)
    return None, 0, len(explored), trace

# DFS - Depth First Search
def dfs(graph, start, goal):
    # Frontier as stack
    frontier = [start]
    parent = {start: None}
    explored = []
    explored_set = set()
    trace = []
    while frontier:
        # Pop from back
        node = frontier.pop()
        if node in explored_set:
            continue
        explored.append(node)
        explored_set.add(node)
        cur_path = reconstruct(parent, node)
        cost = path_cost(graph, cur_path)
        trace.append((node, list(frontier), list(explored), cur_path, cost))
        if node == goal:
            return cur_path, cost, len(explored), trace
        # Add children in reverse order
        for child, _, _ in reversed(graph[node]):
            if child not in parent:
                parent[child] = node
                frontier.append(child)
    return None, 0, len(explored), trace

# UCS - Uniform Cost Search
def ucs(graph, start, goal):
    counter = 0
    # Frontier as priority queue (cost, counter, node)
    frontier = [(0, 0, start)]
    # Best cost dictionary
    best_cost = {start: 0}
    parent = {start: None}
    explored = []
    explored_set = set()
    trace = []
    # Helper to view frontier
    def frontier_view():
        live = [(g, k, n) for (g, k, n) in frontier if n not in explored_set and g == best_cost.get(n, float('inf'))]
        live.sort()
        return [f"{g}:{n}" for g, k, n in live]
    while frontier:
        # Pop lowest cost
        g, _, node = heapq.heappop(frontier)
        if node in explored_set:
            continue
        if g!= best_cost[node]:
            continue
        explored.append(node)
        explored_set.add(node)
        cur_path = reconstruct(parent, node)
        trace.append((node, frontier_view(), list(explored), cur_path, g))
        if node == goal:
            return cur_path, g, len(explored), trace
        # Expand neighbours
        for child, step_cost, _ in graph[node]:
            new_cost = g + step_cost
            if new_cost < best_cost.get(child, float('inf')):
                best_cost[child] = new_cost
                parent[child] = node
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, child))
    return None, float('inf'), len(explored), trace

# Display maze
def show_maze(maze):
    print("Maze Layout (5x5):")
    for row in maze:
        print(" ".join(row))
    print("Costs:.=1, F,O(Mud)=10, E(Water)=20, #=Wall\n")

# Display graph
def show_graph(graph):
    print("Adjacency List (Graph):")
    for node, edges in graph.items():
        txt = ", ".join([f"{n}({c})" for n, c, a in edges])
        print(f" {node} -> {txt}")
    print()

# Display trace table
def show_trace(title, trace):
    print(f"--- {title} TRACE ---")
    print(f"{'Step':<5}{'Node':<6}{'Frontier':<30}{'Explored':<20}{'Cost':>6}")
    for i, (node, front, expl, path, cost) in enumerate(trace, 1):
        f = ", ".join(front) if front else "-"
        print(f"{i:<5}{node:<6}{f:<30}{','.join(expl):<20}{cost:>6}")
    print()

# Main function
def main():
    graph, name_to_pos, pos_to_name = build_graph(MAZE)
    start = 'S'
    goal = 'GO'
    show_maze(MAZE)
    show_graph(graph)
    bfs_path, bfs_cost, bfs_n, bfs_trace = bfs(graph, start, goal)
    dfs_path, dfs_cost, dfs_n, dfs_trace = dfs(graph, start, goal)
    ucs_path, ucs_cost, ucs_n, ucs_trace = ucs(graph, start, goal)
    show_trace('BFS', bfs_trace)
    show_trace('DFS', dfs_trace)
    show_trace('UCS', ucs_trace)
    print("=== COMPARISON (FINAL RESULT) ===")
    results = [
        ('BFS', bfs_path, bfs_cost, bfs_n),
        ('DFS', dfs_path, dfs_cost, dfs_n),
        ('UCS', ucs_path, ucs_cost, ucs_n),
    ]
    optimal = ucs_cost
    print(f"{'Algorithm':<10}{'Path':<50}{'Length':>7}{'Cost':>6}{'Expanded':>10}{'Optimal?':>10}")
    for name, path, cost, n in results:
        length = len(path)-1 if path else 0
        is_opt = "Yes" if cost == optimal else "No"
        path_str = " -> ".join(path) if path else "None"
        print(f"{name:<10}{path_str:<50}{length:>7}{cost:>6}{n:>10}{is_opt:>10}")

# Run main
if __name__ == "__main__":
    main()
