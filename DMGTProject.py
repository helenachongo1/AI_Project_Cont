import pygame
import heapq

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
GRID_WIDTH = WIDTH // COLS
GRID_HEIGHT = HEIGHT // ROWS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualization")
clock = pygame.time.Clock()

# Class for each cell in the grid
class Cell:
    def _init_(self, row, col):  # Corrected method with double underscores
        self.row = row
        self.col = col
        self.x = col * GRID_WIDTH
        self.y = row * GRID_HEIGHT
        self.color = WHITE
        self.neighbors = []
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, GRID_WIDTH, GRID_HEIGHT))

    def make_start(self):
        self.color = GREEN
    
    def make_goal(self):
        self.color = RED
    
    def make_wall(self):
        self.color = BLACK
    
    def make_path(self):
        self.color = BLUE

    def reset(self):
        self.color = WHITE

# Create grid
grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]

# Draw grid
def draw_grid(screen, grid):
    for row in grid:
        for cell in row:
            cell.draw(screen)
    for i in range(ROWS):
        pygame.draw.line(screen, BLACK, (0, i * GRID_HEIGHT), (WIDTH, i * GRID_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(screen, BLACK, (j * GRID_WIDTH, 0), (j * GRID_WIDTH, HEIGHT))

def get_clicked_pos(pos):
    x, y = pos
    row = y // GRID_HEIGHT
    col = x // GRID_WIDTH
    return row, col

"""# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
ROWS, COLS = 20, 20
GRID_WIDTH = WIDTH // COLS
GRID_HEIGHT = HEIGHT // ROWS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Create screen object
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm Visualization")
clock = pygame.time.Clock()

# Class for each cell in the grid
class Cell:
    def _init_(self, row, col):
        self.row = row
        self.col = col
        self.x = col * GRID_WIDTH
        self.y = row * GRID_HEIGHT
        self.color = WHITE
        self.neighbors = []
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, GRID_WIDTH, GRID_HEIGHT))

    def make_start(self):
        self.color = GREEN
    
    def make_goal(self):
        self.color = RED
    
    def make_wall(self):
        self.color = BLACK
    
    def make_path(self):
        self.color = BLUE

    def reset(self):
        self.color = WHITE

# Create grid
grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]

# Draw grid
def draw_grid(screen, grid):
    for row in grid:
        for cell in row:
            cell.draw(screen)
    for i in range(ROWS):
        pygame.draw.line(screen, BLACK, (0, i * GRID_HEIGHT), (WIDTH, i * GRID_HEIGHT))
        for j in range(COLS):
            pygame.draw.line(screen, BLACK, (j * GRID_WIDTH, 0), (j * GRID_WIDTH, HEIGHT))

def get_clicked_pos(pos):
    x, y = pos
    row = y // GRID_HEIGHT
    col = x // GRID_WIDTH
    return row, col"""

"""def dijkstra(grid, start, goal):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))
    distances = {cell: float('infinity') for row in grid for cell in row}
    distances[start] = 0
    prev = {cell: None for row in grid for cell in row}

    while priority_queue:
        current_distance, current_cell = heapq.heappop(priority_queue)

        if current_cell == goal:
            reconstruct_path(prev, start, goal, grid)
            return True

        for neighbor in get_neighbors(grid, current_cell):
            temp_dist = current_distance + 1  # Assuming each edge has equal weight

            if temp_dist < distances[neighbor]:
                distances[neighbor] = temp_dist
                prev[neighbor] = current_cell
                heapq.heappush(priority_queue, (temp_dist, neighbor))
                neighbor.color = YELLOW  # Mark as visited
            
        draw_grid(screen, grid)
        pygame.display.update()
        clock.tick(30)  # Control the speed of animation

    return False

def reconstruct_path(prev, start, goal, grid):
    current = goal
    while current != start:
        current = prev[current]
        if current != start:
            current.make_path()
        draw_grid(screen, grid)
        pygame.display.update()
        clock.tick(30)  # Control the speed of animation"""

