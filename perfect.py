import random
from collections import deque
import numpy as np
import math
import time
from utils import turn_left, turn_right

class PerfectAI:

    def __init__(self, num_actions, board):
        (board_width, board_height) = board
        self.board_width = board_width
        self.board_height = board_height
        self.num_actions = num_actions
        self.num_last_frames = 2
#        self.distance_board = np.array([[-1 for i in range(self.board_width)] for j in range(self.board_height)])
    
    def perform(self, env, opponent):
        self.predict(env.get_frame(), opponent)

    def predict(self, board, opponent):
#        board = state[self.num_last_frames - 1]
        #Direction: 0 = straight, 1 = left, 2 = right
#        print(state.shape)
        opponent_head = None
        for i,row in enumerate(board):
            for j,val in enumerate(row):
                if val == 3:
                    opponent_head = (i,j)
                    break
            if opponent_head:
                break
        
        if not opponent_head:
            return 0
        temp_board = board.copy()
        temp_board[opponent_head[0],opponent_head[1]] = 0
        opponent_board = self.BFS((opponent_head[0],opponent_head[1]), temp_board)
        temp_board[opponent_head[0],opponent_head[1]] = 3
        temp_direction = [i for i in self.direction]
        temp_board[self.head[0],self.head[1]] = 2

        max_gain = -100000
        best_move = 0
        for move in range(self.num_actions):
            direction = self.interpret(move)
            new_head = [x + y for x,y in zip(direction, self.head)]
            if temp_board[new_head[0],new_head[1]] != 0:
                continue
            temp_board[new_head[0],new_head[1]] = 1
            self_board = self.BFS((new_head[0],new_head[1]), temp_board)
            diff = self_board - opponent_board
            count = self.count_control(temp_board, diff)
            if count > max_gain:
                best_move = move
                max_gain = count
            temp_board[new_head[0],new_head[1]] = 0
        return best_move
        
    def count_control(self, board, dist):
        count = 0
        for row in range(self.board_width):
            for col in range(self.board_height):
                if board[row,col] == 0:
#                    print(dist[row,col])
                    if dist[row,col] < 0:
                        count += 1
                    elif dist[row,col] > 0:
                        count -= 1
        return count

    def BFS(self, starting, board):
        dist = np.full((self.board_width, self.board_height), 1000000)
        Q = deque([starting])
        visited = set()
        visited.add(starting)
        dist[starting] = 1
        found = 0
        while Q:
            node = Q.popleft()
            found += 1
#            print(node)
            neighbor = (node[0] - 1, node[1])
            if board[neighbor[0],neighbor[1]] == 0 and neighbor not in visited:
                visited.add(neighbor)
                Q.append(neighbor)
                dist[neighbor[0],neighbor[1]] = dist[node] + 1
            neighbor = (node[0] + 1, node[1])
            if board[neighbor[0],neighbor[1]] == 0 and neighbor not in visited:
                visited.add(neighbor)
                Q.append(neighbor)
                dist[neighbor[0],neighbor[1]] = dist[node] + 1
            neighbor = (node[0], node[1] - 1)
            if board[neighbor[0],neighbor[1]] == 0 and neighbor not in visited:
                visited.add(neighbor)
                Q.append(neighbor)
                dist[neighbor[0],neighbor[1]] = dist[node] + 1
            neighbor = (node[0], node[1] + 1)
            if board[neighbor[0],neighbor[1]] == 0 and neighbor not in visited:
                visited.add(neighbor)
                Q.append(neighbor)
                dist[neighbor[0],neighbor[1]] = dist[node] + 1
        return dist

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
#        self.distance_board = np.array([[dist(self.head,[i,j]) for i in range(self.board_width)] for j in range(self.board_height)])
