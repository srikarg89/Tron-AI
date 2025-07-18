from human import Human
from environment import Environment
from control import ControlAI

def game(player1, player2):
    env = Environment((board_width, board_height), speed, True)
    #Reset environment
    env.reset(player1, player2)
    #Other initialization stuff
    result = ""
    while True:

        state = env.get_state(player1, player2)
        action = player1.predict(state, player2, True)
        env.act(player1, action)

        state = env.get_frame(player2, player1)
        action = player2.predict(state, player1)
        env.act(player2, action)

        env.render(player1, player2)

        if env.check_collision(player1, player2):
            result = "Blue Won"
        if env.check_collision(player2, player1):
            result = "Red Won"
            if env.check_collision(player1, player2):
                result = "Tie Game"
        
        if result != "":
            break

    return result

if  __name__ == '__main__':
    board_width = 50
    board_height = 50
    action_size = 3
    
    speed = 10 # Decrease this value to make the game slower, increase it to make the game faster

    player1 = Human()
    player2 = ControlAI(action_size, (board_width, board_height))

    for i in range(5): # Change this number to change the number of rounds you play
        print(game(player1, player2))
