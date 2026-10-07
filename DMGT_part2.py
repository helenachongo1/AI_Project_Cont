import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder
import importlib

class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.start_x, self.start_y = 0, 0
        self.current_position = [self.start_x, self.start_y]
        self.start_marker = pygame.image.load("C:/Users/Acer/Downloads/output-onlinepngtools.png").convert_alpha()
        self.path = []
        self.user_path = []
        self.is_won = False
        
        self.end_x = 9
        self.end_y = 0
        self.path_drawn = False  

    def create_path(self):
        start = self.grid.node(self.start_x, self.start_y)
        end = self.grid.node(self.end_x, self.end_y)  
        finder = DijkstraFinder()
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()

        
        self.user_path = [(node.x, node.y) for node in self.path]

    def draw_path(self):
        if self.path and self.path_drawn:
            points = []
            for node in self.path:
                x = node.x * 32
                y = node.y * 32
                points.append((x, y))
            pygame.draw.lines(screen, '#4a4a4a', False, points, 5)

    def draw_start_marker(self):
        screen.blit(self.start_marker, (self.current_position[0] * 32, self.current_position[1] * 32))

    def draw_end_marker(self):
        pygame.draw.circle(screen, (0, 255, 0), (self.end_x * 32 + 16, self.end_y * 32 + 16), 16)  

    def move(self, dx, dy):
        new_x = self.current_position[0] + dx
        new_y = self.current_position[1] + dy
        if (0 <= new_x < len(self.matrix[0]) and 0 <= new_y < len(self.matrix) and 
            self.matrix[new_y][new_x] == 1):
            self.current_position[0] = new_x
            self.current_position[1] = new_y
            
            
            self.user_path.append((new_x, new_y))

            if (self.current_position[0], self.current_position[1]) == (self.end_x, self.end_y):
                self.is_won = True
                self.path_drawn = True  
                self.load_new_map()  

    def update(self):
        self.draw_start_marker()
        self.draw_end_marker()  

        if self.is_won:
            font = pygame.font.Font(None, 74)
            text = font.render("You Won!", True, (0, 255, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

        self.draw_path()  # Draw path only after user wins
        
    def load_new_map(self):
        try:
            new_map = importlib.import_module('DMGT_part3')  
            new_matrix = new_map.matrix  
            self.reset_game(new_matrix)  
        except Exception as e:
            print(f"Error loading new map: {e}")

    def reset_game(self, new_matrix):
        
        self.matrix = new_matrix
        self.grid = Grid(matrix=new_matrix)
        self.start_x, self.start_y = 0, 0
        self.current_position = [self.start_x, self.start_y]
        self.end_x = 9
        self.end_y = 0
        self.path = []
        self.user_path = []
        self.is_won = False
        self.path_drawn = False
        self.create_path()  

pygame.init()
screen = pygame.display.set_mode((750, 500))
clock = pygame.time.Clock()

bg_surf = pygame.image.load("C:/Users/Acer/Downloads/map_15-e.png").convert()

matrix = [
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,0,0,0,0,1,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,1,0,1,1,1,1,0,0,0,0,0,0,1,1,0,0,0],
[0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,0],
[1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1],
[1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1],
[1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,1,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,1,0,0,0,0,1,1,0,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0],
[1,1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0],
[1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1],
[1,1,0,0,1,1,1,1,1,1,1,1,0,1,1,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1],
[1,1,0,0,1,1,1,1,1,1,1,0,0,0,1,1,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1],
[1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,0,1,1,0,0,1,0,0,0,0,1],
[1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1],
[1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,0,0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,1,0,1,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1],
[1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,0,0,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,1,0,0,1,0,1,1,1,1,1,0,0,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1],]

pathfinder = Pathfinder(matrix)
pathfinder.create_path()  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_w:  
                pathfinder.move(0, -1)
            elif event.key == pygame.K_s:  
                pathfinder.move(0, 1)
            elif event.key == pygame.K_a:  
                pathfinder.move(-1, 0)
            elif event.key == pygame.K_d:  
                pathfinder.move(1, 0)

    screen.blit(bg_surf, (0, 0))
    pathfinder.update()

    pygame.display.update()
    clock.tick(60)
