import random
from collections import deque
import numpy as np
import math
import time
from utils import turn_left, turn_right
import pygame

class Human:

    def __init__(self):
        self.keypressed = False
        self.possible_keys = [pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN]
    
    def predict(self, board, opponent, verbose=False):

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if not self.keypressed and event.key in self.possible_keys:
                    if event.key == pygame.K_LEFT:
                        direction = [-1,0]
                    elif event.key == pygame.K_RIGHT:
                        direction = [1,0]
                    elif event.key == pygame.K_UP:
                        direction = [0,-1]
                    elif event.key == pygame.K_DOWN:
                        direction = [0,1]
                    self.keypressed = True
                    if direction[0] == self.direction[0]*-1 and direction[1] == self.direction[1]*-1:
                        continue
                    self.direction = direction
            elif event.type == pygame.KEYUP:
                if self.keypressed and event.key in self.possible_keys:
                    self.keypressed = False


    def interpret(self, action):
        #Direction: 0 = straight, 1 = left, 2 = right
        if action == 1:
            return turn_left(self.direction)
        elif action == 2:
            return turn_right(self.direction)
        return self.direction
            
    def reset(self, starting_position):
        self.head = [i for i in starting_position]
        self.direction = [0,-1]
        self.visited = []