from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Create a sky
sky = Sky()

# Create ground
ground = Entity(
    model='plane',
    texture='grass',
    scale=(10, 1, 10),
    collider='box'
)

# Function to create grass patches
def create_grass(x, z):
    grass_patch = Entity(
        model='plane',
        texture='grass',
        position=(x, 0.01, z),
        scale=(0.3, 1, 0.3),  
        collider='box'
    )

# Create multiple grass patches
for _ in range(100):
    x = random.uniform(-10, 10)
    z = random.uniform(-10, 10)
    create_grass(x, z)

# Create walls
def create_wall(x, z, height):
    wall = Entity(
        model='cube',
        texture='brick',
        position=(x, height/2, z),
        scale=(1, height, 1),
        collider='box'
    )

# Create a simple path
def create_path(start_x, start_z, length):
    for i in range(length):
        Entity(
            model='cube',
            texture='concrete',
            position=(start_x, 0.5, start_z + i),
            scale=(1, 1, 1),
            collider='box'
        )

# Create walls
create_wall(5, 0, 3)  # Example wall
create_wall(-5, 0, 3) # Another wall

# Create a path
create_path(0, -5, 10)

# Create player
player = FirstPersonController()

app.run()

