import pygame
import random
import numpy as np

pygame.init()



X_MAP = 50
Y_MAP = 50
PIXEL_SIZE = 10

dup1 = pygame.mixer.Sound('duplication1.wav')
dup2 = pygame.mixer.Sound('duplication1.wav')
dup3 = pygame.mixer.Sound('duplication3.wav')

win = pygame.display.set_mode((X_MAP * PIXEL_SIZE, Y_MAP * PIXEL_SIZE))
pygame.display.set_caption("First Game")
clock = pygame.time.Clock()


class Cell(object):
    def __init__(self, x, y, creature=None):
        self.x = x
        self.y = y
        self.creature = creature
        self.isoccupied = 0
        if self.creature is not None:
            self.isoccupied = 1

class GameMap(object):
    def __init__(self, X_SIZE, Y_SIZE):
        # self.obstacles = np.zeros((X_SIZE, Y_SIZE))
        self.shape = (X_SIZE, Y_SIZE)
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


class Bacteria(object):
    def __init__(self, x, y, team, color):
        self.x = x
        self.y = y
        self.energy = 0
        self.team = team
        self.color = color
        self.action_list = ['walk', 'duplicate']
        self.pause = 15

    def print_state(self):
        print("X_coordinate:", self.x)
        print("Y_coordinate:", self.y)
        print("Team:", self.team)
        print("Color:", self.color)
        print("Pause value:", self.pause)
        print("Energy value:", self.energy)
        print("")

    def walk(self, env):
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
            
            case = random.randint(1, 3)
            if case == 1:
                dup1.play()
            elif case == 2:
                dup2.play()
            elif case == 3:
                dup3.play()

            

    def make_action(self, env):
        if self.pause == 0:
            action = np.random.choice(a=self.action_list, p=[0.9, 0.1])
            if action == 'walk':
                self.walk(env)
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

def redrawGameWindow():
    pygame.draw.rect(win, (255, 255, 255), (0, 0, X_MAP * PIXEL_SIZE, Y_MAP * PIXEL_SIZE))
    for bacteria in env.creatures:
        bacteria.draw(win)
    pygame.display.update()


def spawnStart():
    pass



env = GameMap(X_MAP, Y_MAP)

env.creatures.append(Bacteria(15, 15, 0, (255, 255, 0)))
env.placeCreature(15, 15, env.creatures[-1])

env.creatures.append(Bacteria(25, 25, 1, (0, 255, 0)))
env.placeCreature(15, 15, env.creatures[-1])





#mainloop
font = pygame.font.SysFont('comicsans', 30, True)

run = True
#pygame.draw.rect(win, (0, 0, 0), (0, 0, 500, 480))
while run:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bacteria in env.creatures:
        bacteria.get_energy(env)
        #if bacteria.energy >= 100:
        #    #print(len(b_list))
        #    bacteria.duplicate(field, b_list)
        #    #print(field)
        bacteria.make_action(env)
    redrawGameWindow()

#print(field)
#print("len(b_list)", len(b_list))
#print("")
#print_state(b_list[0])
#print_state(b_list[1])
#print_state(b_list[2])
#for bacteria in env.creatures:
    #bacteria.print_state()

pygame.quit()

