import pygame
import random
import numpy as np
import configparser
import os
from classes import *

def readConfig(path='config.ini'):
    config = configparser.ConfigParser()
    config.read(path)
    return config





def spawnStart():
    pass