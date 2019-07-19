import pygame
from pygame import Color, Rect, Surface
import numpy as np
from collections import deque

class Environment():
    
    def __init__(self, board, speed, visual):
        (self.board_width, self.board_height) = board
        self.speed = speed
        self.wall = [(0,i) for i in range(self.board_width)] + [(i,0) for i in range(self.board_height)] + [(self.board_height-1,i) for i in range(self.board_width)] + [(i,self.board_width-1) for i in range(self.board_height)]
        self.score_reward_multiple = 0.01
        self.num_last_frames = 2
        self.tile_width = 10
        self.tile_height = 10
        self.distance_board = [[-1 for i in range(self.board_width)] for j in range(self.board_height)]
        self.game_display = None
        self.visual = visual
        if self.visual:
            pygame.display.set_caption('Tron')
            background = pygame.Surface((self.board_width*self.tile_width, self.board_height*self.tile_height))
            self.game_display = pygame.display.set_mode((self.board_width*self.tile_width, self.board_height*self.tile_height))
            self.game_display.blit(background, (0,0))
            self.clock = pygame.time.Clock()

    def reset(self, p1, p2):
        self.score = 0
        self.reward_sum = 0
        self.frame = None
        self.frames = None
        distX, distY = 0, 0
        while abs(distX) < 5:
            distX = np.random.randint(int(self.board_width/2))
            distX -= int(self.board_width/4)
        while abs(distY) < 5:
            distY = np.random.randint(int(self.board_height/2))
            distY -= int(self.board_height/4)
        p1.reset([int(self.board_width/2) + distX, int(self.board_height/2) + distY])
        p2.reset([int(self.board_width/2) - distX, int(self.board_height/2) - distY])
        if self.visual:
            gray = Color(200,200,200)
            black = Color(0,0,0)
            self.game_display.fill(gray)
            tile_width = self.tile_width
            tile_height = self.tile_height
            for x,y in self.wall:
                pygame.draw.rect(self.game_display, black, Rect(x*tile_width, y*tile_width, tile_width, tile_height))
            self.render(p1, p2)

    def render(self, p1, p2):
        if self.visual:
            red = Color(255,0,0)
            blue = Color(0,0,255)
            tile_width = self.tile_width
            tile_height = self.tile_height
            x,y = p1.head
            pygame.draw.rect(self.game_display, red, Rect(x*tile_width, y*tile_width, tile_width, tile_height))
            x,y = p2.head
            pygame.draw.rect(self.game_display, blue, Rect(x*tile_width, y*tile_width, tile_width, tile_height))
            pygame.display.update()
            self.clock.tick(self.speed)
    
    def act(self, player, action):
        player.direction = player.interpret(action)
        player.visited.append(player.head)
        player.head = [x + y for x,y in zip(player.direction, player.head)]
    
    def dist_reward(self, head, obstacles):
        x,y = head
        minDist = float("inf")
        for a,b in obstacles:
            dist = abs(x-a) + abs(y-b)
            if dist < minDist:
                minDist = dist
        return 1/(dist + 1)
    
    def control_reward(self, player1, player2):
        count = 0
        count2 = 0
        total_count = self.board_width * self.board_height
        c = player1.distance_board - player2.distance_board
        for row in c:
            for value in row:
                if value > 0:
                    count += 1
                elif value < 0:
                    count2 += 1
        return count/total_count, count2/total_count

    def analyze(self, player1, player2):
#        reward = self.dist_reward(player1.head, player2.visited + [player2.head])
#        reward = int(self.score/5) * self.score_reward_multiple
#        reward1, reward2 = self.control_reward(player1, player2)
        game_over1 = self.check_collision(player1, player2)
        game_over2 = self.check_collision(player2, player1)
        if not game_over1 and not game_over2:
            return 0
        if game_over1 and game_over2:
            return 1
        if not game_over1 and game_over2:
            return 2
        if game_over1 and not game_over2:
            return 3
 #       state_next1 = self.get_state(player1, player2)
 #       state_next2 = self.get_state(player2, player1)
 #       self.reward_sum += reward1 + reward2
 #       return [[reward1, state_next1, game_over1], [reward2, state_next2, game_over2]]

    def check_collision(self, p1, p2):
        for a,b in p1.visited:
            if p1.head[0] == a and p1.head[1] == b:
                return 1
        if p1.head[0] <= 0 or p1.head[1] <= 0 or p1.head[0] >= self.board_width - 1 or p1.head[1] >= self.board_height - 1:
            return 2
        if p1.head in p2.visited:
            return 3
        return 0
    
    def get_frame(self, player1, player2):
        frame = np.array([[0 for i in range(self.board_width)] for j in range(self.board_height)])
        for a,b in player1.visited:
            frame[a,b] = 2
        frame[player1.head[0],player1.head[1]] = 1

        for a,b in player2.visited:
            frame[a,b] = 4
        frame[player2.head[0], player2.head[1]] = 3
        
        for a,b in self.wall:
            frame[a,b] = 5

        return frame

    def get_state(self, player1, player2):
        #0 = nothing, 1 = head, 2 = snake, 3 = opponent head, 4 = opponent snake, 5 = wall
        self.frame = self.get_frame(player1, player2)
        if self.frames is None:
            self.frames = deque([self.frame] * self.num_last_frames)
        else:
            self.frames.append(self.frame)
            self.frames.popleft()
        return np.expand_dims(self.frames, 0).reshape(self.num_last_frames, *self.frame.shape) 