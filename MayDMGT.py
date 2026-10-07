import pygame
from pygame.locals import *

screenDimension=(1000, 750)
screen = pygame.display.set_mode(screenDimension,0,32)

player = pygame.image.load("C:/Users/Acer/Downloads/output-onlinepngtools.png")
keys = [False, False, False, False]
playerpos = [800, 400]
speed = 3 




while True:
    
    screen.blit(player, playerpos)
    
    pygame.display.flip()
    screen.fill(0)
    
    pygame.draw.polygon(screen, (0, 255, 0), ( (10,500),(500,250),(1000,500),(500,800),(10,500) ),0)
    pygame.draw.line(screen, (170, 150, 0), (9,520), (500, 820),42)
    pygame.draw.line(screen, (100, 80, 0), (490,819), (998, 519),42)
    
    house = pygame.image.load("C:/Users/Acer/Downloads/output-onlinepngtools (1).png")
    screen.blit(house, (180,300))
    
    house = pygame.image.load("C:/Users/Acer/Downloads/output-onlinepngtools (3).png")
    screen.blit(house, (630,390))
    
    house = pygame.image.load("C:/Users/Acer/Downloads/output-onlinepngtools (3).png")
    screen.blit(house, (660,430))
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
        
            if event.key == K_w:
                keys[0] =True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True 
            elif event.key == K_d:
                keys[3] = True 
            
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_w:
                keys[0] = False
            elif event.key == pygame.K_a:
                keys[1] = False
            elif event.key == pygame.K_s:
                keys[2] = False 
            elif event.key == pygame.K_d:
                keys[3] = False 
                
        if keys[0]:
            playerpos[1] -= speed
        elif keys[1]:
            playerpos[1] += speed
            
        if keys[2]:
            playerpos[0] -= speed
        elif keys[3]:
            playerpos[0] += speed
        
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)