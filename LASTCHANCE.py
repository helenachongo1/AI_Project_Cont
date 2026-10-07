from PIL import Image
import numpy as np
import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement


class Pathfinder:
    def __init__(self,matrix):
        self.matrix = b_matrix
        self.grid = Grid(matrix=b_matrix)
        #self.select_surf = pygame.image.load("C:/Users/Acer/Downloads/map_13.png").convert_alpha()

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        #convert mouse position in row and column index
        row = mouse_pos[1] // 32
        col = mouse_pos[0] // 32
        current_cell_value = self.matrix[row][col]
        if current_cell_value == 1:
            rect = pygame.Rect((col * 32,row * 32),(32,32))
            pygame.draw.rect(screen, (255, 0, 0, 128), rect)  # Red rectangle with transparency
        
    def update(self):
        self.draw_active_cell()
pygame.init()
screen = pygame.display.set_mode((635,500))
clock = pygame.time.Clock()

bg_surf = pygame.image.load("C:/Users/Acer/Downloads/map62.png").convert()
image = Image.open("C:/Users/Acer/Downloads/map62.png")

g_image = image.convert("L")

image_matrix = np.array(g_image)
threshold = 128

b_matrix = (image_matrix > threshold).astype(int)
pathfinder = Pathfinder((b_matrix))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.blit(bg_surf,(0,0))
    pathfinder.draw_active_cell()
        
    pygame.display.update()
    clock.tick(60)

