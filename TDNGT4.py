import sys
import networkx as nx
from pyamaze import maze, agent, textLabel
import matplotlib.pyplot as plt

def build_graph(m):
    """
    Converts the maze into a graph where each cell is a node, and edges exist between adjacent cells without walls.
    """
    G = nx.Graph()
    for x in range(m.rows):
        for y in range(m.cols):
            current = (x, y)
            # Check possible movements: North, South, East, West
            directions = {
                'N': (x-1, y),
                'S': (x+1, y),
                'E': (x, y+1),
                'W': (x, y-1)
            }
            for direction, (nx_pos, ny_pos) in directions.items():
                if 0 <= nx_pos < m.rows and 0 <= ny_pos < m.cols:
                    if not m.maze_map[x][y].walls[direction]:
                        neighbor = (nx_pos, ny_pos)
                        G.add_edge(current, neighbor)
    return G

def get_user_move(current_pos, m):
    """
    Displays available directions to the user and gets the next move.
    """
    x, y = current_pos
    directions = {}
    options = []
    if not m.maze_map[x][y].walls['N']:
        directions['N'] = (x-1, y)
        options.append('N')
    if not m.maze_map[x][y].walls['S']:
        directions['S'] = (x+1, y)
        options.append('S')
    if not m.maze_map[x][y].walls['E']:
        directions['E'] = (x, y+1)
        options.append('E')
    if not m.maze_map[x][y].walls['W']:
        directions['W'] = (x, y-1)
        options.append('W')
    
    print(f"\nCurrent Position: {current_pos}")
    print(f"Available Directions: {', '.join(options)}")
    
    move = input("Enter direction (N/S/E/W): ").strip().upper()
    while move not in options:
        move = input(f"Invalid move. Choose from {', '.join(options)}: ").strip().upper()
    return directions[move]

def visualize_paths(m, user_path, shortest_path):
    """
    Visualizes the maze along with the user's path and the shortest path.
    """
    m.CreateMaze()
    a = agent(m, footprints=True, color='blue')
    m.tracePath({a: user_path}, delay=100)
    
    # Highlight the shortest path in red
    if shortest_path:
        path_agent = agent(m, footprints=True, color='red')
        m.tracePath({path_agent: shortest_path}, delay=100)
    
    m.run()

def main():
    # Maze dimensions
    rows = 10
    cols = 10

    # Generate maze
    m = maze(rows, cols)
    m.CreateMaze()

    # Build graph from maze
    G = build_graph(m)

    # Define start and end points
    start = (m.start_x, m.start_y)
    end = (m.end_x, m.end_y)

    print("Welcome to the Maze Game!")
    print(f"Start Position: {start}")
    print(f"End Position: {end}")

    current_pos = start
    user_path = [current_pos]

    while current_pos != end:
        current_pos = get_user_move(current_pos, m)
        if current_pos in user_path:
            print("You've already been here! Try a different direction.")
        else:
            user_path.append(current_pos)

    print("\nCongratulations! You've reached the destination.")

    # Calculate shortest path using Dijkstra's algorithm
    try:
        shortest_path = nx.dijkstra_path(G, source=start, target=end)
        print(f"\nShortest Path ({len(shortest_path)-1} steps): {shortest_path}")
    except nx.NetworkXNoPath:
        print("No path exists between the start and end points.")
        shortest_path = None

    # Visualize the maze, user's path, and the shortest path
    visualize_paths(m, user_path, shortest_path)

if __name__ == "__main__":
    main()

