from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

sky=Sky()


ground = Entity(
    model='plane',
    texture='grass',
    scale=(10, 1, 10),
    collider='box'
)


def create_grass(x, z):
    grass_patch = Entity(
        model='plane',
        texture='grass',
        position=(x, 0.01, z),
        scale=(0.3, 1, 0.3),  
        collider='box'
    )

for _ in range(100):
    x = random.uniform(-10, 10)
    z = random.uniform(-10, 10)
    create_grass(x, z)


player = FirstPersonController()

app.run()



