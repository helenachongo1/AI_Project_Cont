import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.dijkstra import DijkstraFinder

class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        self.start_x, self.start_y = 30, 14
        self.current_position = [self.start_x, self.start_y]
        self.start_marker = pygame.image.load("C:/Users/Acer/Downloads/output-onlinepngtools.png").convert_alpha()
        self.path = []
        self.user_path = []
        self.is_won = False
        self.is_lost = False
        
        
        self.end_x = 10
        self.end_y = 5
        self.path_drawn = False  

    def create_path(self):
        start = self.grid.node(self.start_x, self.start_y)
        end = self.grid.node(self.end_x, self.end_y)  
        finder = DijkstraFinder()
        self.path, _ = finder.find_path(start, end, self.grid)
        self.grid.cleanup()

        
        self.correct_path = [(node.x, node.y) for node in self.path]

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
                self.compare_paths()  

    def compare_paths(self):
        """
        Compare user path to the correct path after the endpoint is reached.
        If the user path is "close enough" to the correct path, they win.
        Otherwise, they lose.
        """
        tolerance = 2  

        
        correct_set = set(self.correct_path)
        user_set = set(self.user_path)

        
        matched_tiles = 0
        for user_node in self.user_path:
            if user_node in correct_set:
                matched_tiles += 1

        if matched_tiles >= len(self.correct_path) - tolerance:
            self.is_won = True
        else:
            self.is_lost = True

    def update(self):
        self.draw_start_marker()
        self.draw_end_marker()  

        if self.is_lost:
            font = pygame.font.Font(None, 74)
            text = font.render("You Lost!", True, (255, 0, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

        elif self.is_won:
            font = pygame.font.Font(None, 74)
            text = font.render("You Won!", True, (0, 255, 0))
            screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))

        self.draw_path()  

def make_roads_walkable(matrix, top_left, bottom_right):
    for y in range(top_left[1], bottom_right[1]):
        for x in range(top_left[0], bottom_right[0]):
            if 0 <= x < len(matrix[0]) and 0 <= y < len(matrix):
                matrix[y][x] = 1

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()

bg_surf = pygame.image.load("C:/Users/Acer/Downloads/map651.jpg").convert()

matrix = [
[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,1,0,0,1,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,1,1,0,1,1,0,1,0,0,1,0,1,1,0,0,1,0,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,1,1,0,0,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1],
[1,1,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,0,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,0,0,1,0,0,0,0,0,0,1,1,1,1,0,1,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,0,0,1,1,1,0,1,1,0,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,1,1,0,0,0,1,1,1,0,1,1],
[1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],#
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0],
[1,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,0,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,1,0,0,1,1,0,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,1,1,1],
[1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,1,0,1,0,1,1,1,1],
[1,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1],
[1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
[1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[0,1,0,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

pathfinder = Pathfinder(matrix)


make_roads_walkable(matrix, (30, 30), (40, 40))  

pathfinder.grid = Grid(matrix=matrix)  
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
