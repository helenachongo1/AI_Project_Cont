from PIL import Image
import numpy as np
import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class Pathfinder:
    def __init__(self,matrix):
        self.matrix = matrix
        self.grid = Grid(matrix=matrix)
        #self.select_surf = pygame.image.load("C:/Users/Acer/Downloads/map_13.png").convert_alpha()
        
        self.path=[]
        
    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        #convert mouse position in row and column index
        row = mouse_pos[1] // 32
        col = mouse_pos[0] // 32
        current_cell_value = self.matrix[row][col]
        if current_cell_value == 1:
            rect = pygame.Rect((col * 32,row * 32),(32,32))
            pygame.draw.rect(screen, (255, 0, 0, 128), rect)  # Red rectangle with transparency
     
    def create_path(self):
        #start
        start_x, start_y =[1,1]
        start=self.grid.node(start_x,start_y)
        
        #end
        mouse_pos = pygame.mouse.get_pos()
        end_y = mouse_pos[1] // 32
        end_x = mouse_pos[0] // 32
        end = self.grid.node(end_x, end_y)
        
        #path
        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path,_ = finder.find_path(start,end,self.grid)
        self.grid.cleanup()
        #print(self.path)
        
    def draw_path(self):
        if self.path:
            points = []
            for point in self.path:
                x = point[0] * 32
                y = point[1] * 32
                points.append(x,y)
            pygame.draw.lines(screen,'#4a4a4a',False, points,5)
        
    def update(self):
        self.draw_active_cell()
        self.draw_path()
        
pygame.init()
screen = pygame.display.set_mode((750,500))
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

pathfinder = Pathfinder((matrix))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            end_x = mouse_pos[0] // 32
            end_y = mouse_pos[1] // 32
            
            # Check if the clicked position is within bounds
            if 0 <= end_x < len(matrix[0]) and 0 <= end_y < len(matrix):
                pathfinder.create_path()
            
    screen.blit(bg_surf, (0, 0))
    pathfinder.update()
        
    pygame.display.update()
    clock.tick(60)
