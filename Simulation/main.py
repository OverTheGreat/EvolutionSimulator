import pygame
import random
import numpy as np
import configparser
import os
from classes import *
from functions import *

pygame.init()


### READING SOME SETTINGS
config = readConfig()

X_MAP = int(config.get("WORLD", "x_size"))
Y_MAP = int(config.get("WORLD", "y_size"))
PIXEL_SIZE = int(config.get("WORLD", "pixel_size"))

sounds_path = config.get("DIRECTORIES", "sounds")
sounds = []
for sound_name in os.listdir(sounds_path):
    sounds.append(pygame.mixer.Sound(sounds_path + sound_name))

### INITIALIZING THE SIMULATION


win = pygame.display.set_mode((X_MAP * PIXEL_SIZE, Y_MAP * PIXEL_SIZE))
pygame.display.set_caption("Evolution Simulator")
clock = pygame.time.Clock()
font = pygame.font.SysFont('comicsans', 30, True)

env = GameMap(X_MAP, Y_MAP, PIXEL_SIZE)

### PLACING TEST CREATURES

env.creatures.append(Bacteria(15, 15, 0, (255, 255, 0)))
env.placeCreature(15, 15, env.creatures[-1])

env.creatures.append(Bacteria(25, 25, 1, (0, 255, 0)))
env.placeCreature(15, 15, env.creatures[-1])


### MAINLOOP

run = True
while run:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for creature in env.creatures:
        creature.get_energy(env)
        creature.make_action(env)
    env.redrawGameWindow(win)

#for bacteria in env.creatures:
    #bacteria.print_state()

pygame.quit()
