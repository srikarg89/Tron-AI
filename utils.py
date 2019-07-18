def turn_left(direction):
    if direction == [0,1]:
        return [1,0]
    if direction == [0,-1]:
        return [-1,0]
    if direction == [1,0]:
        return [0,-1]
    if direction == [-1,0]:
        return [0,1]

def turn_right(direction):
    if direction == [0,1]:
        return [-1,0]
    if direction == [0,-1]:
        return [1,0]
    if direction == [1,0]:
        return [0,1]
    if direction == [-1,0]:
        return [0,-1]

def dist(self, point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])


"""
frame = np.array([[0 for i in range(self.frame_width)] for j in range(self.frame_height)])
center = (int(self.frame_width/2), int(self.frame_height/2))
frame[center[0]][center[1]] = 1
x,y = player1.head
for a,b in player1.visited: #Player snake loop
    if abs(x - a) <= int(self.frame_width/2) and abs(y - b) <= int(self.frame_height/2):
        frame[a - x + center[0]][b - y + center[1]] = 1
for a,b in player2.visited: #Opponent snake loop
    if abs(x - a) <= int(self.frame_width/2) and abs(y - b) <= int(self.frame_height/2):
        frame[a - x + center[0]][b - y + center[1]] = 3
for a,b in self.wall: #Wall loop
    if abs(x - a) <= int(self.frame_width/2) and abs(y - b) <= int(self.frame_height/2):
        frame[a - x + center[0]][b - y + center[1]] = 4
        x2,y2 = player2.head #Player head check
        if abs(x - x2) <= int(self.frame_width/2) and abs(y - y2) <= int(self.frame_height/2):
            frame[x2 - x + center[0]][y2 - y + center[1]] = 2
        """
