from human import Human
from environment import Environment
from perfect import PerfectAI

def game(player1, player2):
    env = Environment((board_width, board_height), True)
    #Reset environment
    env.reset(player1, player2)
    #Other initialization stuff
    alive = True
    while alive:

        state = env.get_state(player1, player2)
        action = player1.predict(state, player2, True)
        env.act(player1, action)

        state = env.get_frame(player2, player1)
        action = player2.predict(state, player1)
        env.act(player2, action)

        env.render(player1, player2)

        if env.check_collision(player1, player2) or env.check_collision(player2, player1):
            break

        env.score += 1
    print('Score: ', str(env.score))
    return env.score

if  __name__ == '__main__':
    board_width = 50
    board_height = 50
    state_shape = (board_width, board_height)

    starting_positions1 = [[int(x), int(y)] for x in range(int(board_width/4),int(board_width*3/4)) for y in range(int(board_height/4),int(board_height*3/4))]
    starting_positions2 = [[int(x), int(y)] for x in range(int(board_width/4),int(board_width*3/4)) for y in range(int(board_height/4),int(board_height*3/4))]

    action_size = 3

#    player1 = PerfectAI(action_size, (board_width, board_height))
    player1 = Human()
    player2 = PerfectAI(action_size, (board_width, board_height))

    for i in range(1):
        game(player1, player2)
