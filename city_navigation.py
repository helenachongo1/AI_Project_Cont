from ursina import *
import heapq

# Initialize the Ursina app
app = Ursina()

# Set up the environment
Sky()
ground = Entity(model='plane', texture='grass', scale=(10, 10))

# Define the graph for the city layout
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Node positions for visualizing the city
positions = {
    'A': (-4, 0, -4),
    'B': (-2, 0, -2),
    'C': (0, 0, 0),
    'D': (2, 0, 2)
}

def create_building(x, z):
    """Create a building at the given coordinates."""
    building = Entity(model='cube', texture='brick', color=color.light_gray, position=(x, 1, z), scale=(1, 2, 1))
    return building

# Create buildings in a grid layout
for name, (x, y, z) in positions.items():
    create_building(x, z)

# Create the player
player = Entity(model='cube', color=color.orange, position=(0, 1, 0), scale=(0.5, 1, 0.5))

def update():
    """Update function for player movement."""
    player.rotation_y += mouse.velocity[0] * 2
    if held_keys['w']:
        player.position += player.forward * 5 * time.dt
    if held_keys['s']:
        player.position -= player.forward * 5 * time.dt
    if held_keys['a']:
        player.position -= player.right * 5 * time.dt
    if held_keys['d']:
        player.position += player.right * 5 * time.dt

def dijkstra(graph, start):
    """Dijkstra's algorithm to find the shortest path in the graph."""
    queue = []
    heapq.heappush(queue, (0, start))
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    shortest_path = {}
    predecessors = {start: None}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node in shortest_path:
            continue

        shortest_path[current_node] = current_distance

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                predecessors[neighbor] = current_node

    return shortest_path, distances, predecessors

def highlight_path(predecessors, end_node):
    """Highlight the shortest path on the grid."""
    current_node = end_node
    path = []

    while current_node:
        path.append(current_node)
        current_node = predecessors.get(current_node)

    path.reverse()

    # Create visual indicators for the path
    for node in path:
        x, y, z = positions[node]
        Entity(model='sphere', color=color.red, position=(x, 0.5, z), scale=0.2)

# Run Dijkstra's algorithm from 'A' to 'D' and visualize the path
_, _, predecessors = dijkstra(graph, 'A')
highlight_path(predecessors, 'D')

# Main loop
app.run()


