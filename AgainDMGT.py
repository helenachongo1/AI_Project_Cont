'''TILE_SIZE = 32
tiles = {
    'G': (0, 255, 0),  # Green for grass
    'W': (0, 0, 255),  # Blue for water
    'S': (255, 255, 0) # Yellow for sand
}
map_layout = [
    ['G', 'G', 'G', 'W', 'W'],
    ['G', 'S', 'S', 'W', 'W'],
    ['G', 'G', 'G', 'G', 'G'],
    ['S', 'S', 'G', 'G', 'G'],
    ['W', 'W', 'S', 'S', 'G']
]
import pygame
pygame.init()
screen = pygame.display.set_mode((TILE_SIZE * len(map_layout[0]), TILE_SIZE * len(map_layout)))
def draw_map():
    for y, row in enumerate(map_layout):
        for x, tile in enumerate(row):
            pygame.draw.rect(screen, tiles[tile], (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw_map()
    pygame.display.flip()
pygame.quit()'''


import pygame
import heapq

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualization")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Node class
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.distance = float('inf')
        self.previous = None

    def draw(self, color):
        pygame.draw.circle(screen, color, (self.x, self.y), 5)

# Create nodes and edges
nodes = [Node(100, 100), Node(200, 200), Node(300, 100), Node(400, 200)]
nodes[0].neighbors = [(nodes[1], 1), (nodes[2], 2)]
nodes[1].neighbors = [(nodes[0], 1), (nodes[3], 1)]
nodes[2].neighbors = [(nodes[0], 2), (nodes[3], 1)]
nodes[3].neighbors = [(nodes[1], 1), (nodes[2], 1)]

# Dijkstra's algorithm
def dijkstra(start):
    start.distance = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > current_node.distance:
            continue
        for neighbor, weight in current_node.neighbors:
            distance = current_distance + weight
            if distance < neighbor.distance:
                neighbor.distance = distance
                neighbor.previous = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

# Main loop
running = True
start_node = nodes[0]
end_node = nodes[3]
dijkstra(start_node)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw edges
    for node in nodes:
        for neighbor, _ in node.neighbors:
            pygame.draw.line(screen, BLACK, (node.x, node.y), (neighbor.x, neighbor.y))

    # Draw nodes
    for node in nodes:
        node.draw(BLUE)

    # Draw shortest path
    current = end_node
    while current.previous:
        pygame.draw.line(screen, RED, (current.x, current.y), (current.previous.x, current.previous.y), 2)
        current = current.previous

    pygame.display.flip()

pygame.quit()
