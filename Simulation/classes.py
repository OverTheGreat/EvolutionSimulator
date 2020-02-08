import pygame
import random
import numpy as np
import configparser
import os
from functions import *


class Cell(object):
    def __init__(self, x, y, creature=None):
        self.x = x
        self.y = y
        self.creature = creature
        self.isoccupied = 0
        if self.creature is not None:
            self.isoccupied = 1

class GameMap(object):
    def __init__(self, X_SIZE, Y_SIZE, pixel_size):
        # self.obstacles = np.zeros((X_SIZE, Y_SIZE))
        self.shape = (X_SIZE, Y_SIZE)
        self.pixel_size = pixel_size
        self.cells = []
        self.sun = np.abs(np.random.normal(0, 1, (X_SIZE, Y_SIZE)))
        self.creatures = []
        for i in range(X_SIZE):
            row = []
            for j in range(Y_SIZE):
                row.append(Cell(i, j))
            self.cells.append(row)

    def placeCreature(self, x, y, creature):
        self.cells[x][y].creature = creature
        self.cells[x][y].isoccupied = 1

    def removeCreature(self, x, y):
        self.cells[x][y].creature = None
        self.cells[x][y].isoccupied = 0

    def redrawGameWindow(self, win):
        pygame.draw.rect(win, (255, 255, 255), (0, 0, self.shape[0] * self.pixel_size, self.shape[1] * self.pixel_size))
        for creature in self.creatures:
            creature.draw(win)
        pygame.display.update()


class Bacteria(object):
    def __init__(self, x, y, team, color):
        self.x = x
        self.y = y
        self.energy = 0
        self.team = team
        self.color = color
        self.action_list = ['random_step', 'duplicate']
        self.pause = 15

    def print_state(self):
        print("X_coordinate:", self.x)
        print("Y_coordinate:", self.y)
        print("Team:", self.team)
        print("Color:", self.color)
        print("Pause value:", self.pause)
        print("Energy value:", self.energy)
        print("")

    def random_step(self, env):
        dir_x = random.randint(-1, 1)
        dir_y = random.randint(-1, 1)
        if (self.x + dir_x > 0 and 
            self.x + dir_x < env.shape[0] - 1 and
            self.y + dir_y > 0 and
            self.y + dir_y < env.shape[1] - 1 and
            env.cells[self.x + dir_x][self.y + dir_y].isoccupied == 0):

            env.placeCreature(self.x + dir_x, self.y + dir_y, self)
            env.removeCreature(self.x, self.y)

            self.x += dir_x
            self.y += dir_y



    def duplicate(self, env):
        #print("searching for a free place")
        dir_x = random.randint(-1, 1)
        dir_y = random.randint(-1, 1)

        if (self.x + dir_x > 0 and 
            self.x + dir_x < env.shape[0] - 1 and
            self.y + dir_y > 0 and
            self.y + dir_y < env.shape[1] - 1 and
            env.cells[self.x + dir_x][self.y + dir_y].isoccupied == 0 and
            self.energy > 99):
            #print("place found")
            
            env.creatures.append(Bacteria(self.x + dir_x, self.y + dir_y, self.team, self.color))
            env.placeCreature(self.x + dir_x, self.y + dir_y, env.creatures[-1])
            
            #print("new creature placed")
            self.energy = 0
            
            #case = random.randint(1, 3)
            #if case == 1:
            #    dup1.play()
            #elif case == 2:
            #    dup2.play()
            #elif case == 3:
            #    dup3.play()

            

    def make_action(self, env):
        if self.pause == 0:
            action = np.random.choice(a=self.action_list, p=[0.9, 0.1])
            if action == 'random_step':
                self.random_step(env)
                self.pause = 15
            elif action == 'duplicate' and self.energy > 99:
                #print('duplicatin started')
                self.duplicate(env)
        self.pause = max(self.pause - 1, 0)

    def get_energy(self, env):
        if self.energy < 120:
            self.energy += env.sun[self.x, self.y]

    def draw(self, win):
        pygame.draw.rect(win, (min(255, self.color[0] * self.energy // 100) , min(255, self.color[1] * self.energy // 100), min(255, self.color[2] * self.energy // 100)), (self.x * 10, self.y * 10, 10, 10))