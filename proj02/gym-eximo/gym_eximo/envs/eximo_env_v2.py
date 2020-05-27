import gym
from gym import error, spaces, utils
from gym.utils import seeding

import numpy as np

from .eximo.eximo import Eximo
from .eximo.state import State
from .eximo.utils import Direction


class EximoEnv2(gym.Env):
    metadata = {'render.modes': ['human']}

    step_num = 0

    def __init__(self):
        self.game = Eximo(['P', 0, None], ['P', 0, None])
        self.action_space = spaces.Discrete(606) # 54 pieces * 11 moves + 12 placement positions
        max = np.iinfo(np.uint64).max
        self.observation_space = spaces.Box(low=np.array([0,0,0,0], dtype=np.uint64), high=np.array([max,max,2,512], dtype=np.uint64), dtype=np.uint64)


    def step(self, action):

        self.step_num += 1

        if (self.step_num % 1000) == 0:
            print('STEP NUM :: ' + str(self.step_num))
            self.game.state.print()
        # print(self.step_num)

        state = self.game.state

        # regular move
        if action < 594:    # 54 * 11 = 594
            # get cell index
            cell = action // 11
            cell += 1 if (cell < 6) else 2
            # get cell coords
            pos = (cell // 8, cell % 8)

            if state.player == 1:
                pos = (7 - pos[0], 7 - pos[1])

            # get move index
            move = action % 11

            if not state.is_ally(pos):
                n_state = state
            
            else:    
                # start
                if state.action[0] == 1:
                    if state.check_capture():
                        if move > 5:
                            n_state = self.exec_move(move, state, pos)
                        else:
                            n_state = state
                    else:
                        if move > 5:
                            n_state = state
                        else:
                            n_state = self.exec_move(move, state, pos)
                # mid jump
                elif state.action[0] == 2:
                    if 2 < move < 6:
                        if pos == state.action[1]:
                            n_state = self.exec_move(move, state, pos)
                        else:
                            n_state = state
                    else:
                        n_state = state
                # mid capture
                elif state.action[0] == 3:
                    if move > 5:
                        if pos == state.action[1]:
                            n_state = self.exec_move(move, state, pos)
                        else:
                            n_state = state
                    else:
                        n_state = state
                # place mode
                else:
                    n_state = state   
        # placement
        else:
            if state.action[0] != 4:
                n_state = state
            else:
                cell = action - 594
                cell += 1 if (cell < 6) else 3

                pos = (cell // 8, cell % 8)

                if state.player == 1:
                    pos = (7 - pos[0], 7 - pos[1])

                if state.is_empty(pos):
                    n_state = state.place(pos)
                else:
                    n_state = state

        observation = self.encode_state(n_state)
        done, winner = self.game.game_over(n_state)
        
        if done:
            reward = 1000 if (winner == state.player) else -1000
        else:
            reward = -1 if (n_state == state) else 1

        self.game.state = n_state

        info = {
            'winner' : winner
        }

        return observation, reward, done, info

    def encode_state(self, state: State) -> list:

        # [1] [2, (1,2)] [3, (1,2)] [4, 2]
        # 00 01 10 11
        # 01 ou 10 -> 64 posiçoes = 6 bits
        # 11 -> 3 opçoes = 2 bits

        bits_p1 = ''
        bits_p2 = ''
        for x in range(0, 8):
            for y in range(0, 8):
                if (state.board[x][y] == 1):
                    bits_p1 += '1'
                    bits_p2 += '0'
                elif(state.board[x][y] == 2):
                    bits_p1 += '0'
                    bits_p2 += '1'
                else:
                    bits_p1 += '0'
                    bits_p2 += '0'

        board_p1 = np.uint64(int(bits_p1, 2))
        board_p2 = np.uint64(int(bits_p2, 2))

        player = np.uint64(state.player - 1)

        action_num = 0
        if state.action[0] in [2, 3]:
            action_num = state.action[1][0] * 8 + state.action[1][1]
        elif state.action[0] == 4:
            action_num = state.action[1]

        bits_action = "{0:{fill}2b}".format(state.action[0] - 1, fill='0')
        bits_action += "{0:{fill}6b}".format(action_num, fill='0')

        action = np.uint64(int(bits_action, 2))

        return np.array([board_p1, board_p2, player, action], dtype=np.uint64)

    def exec_move(self, move: int, state: State, pos: tuple) -> State:
        if move == 0:
            n_state = state.move(pos, Direction.NORTHWEST)
        elif move == 1:
            n_state = state.move(pos, Direction.NORTH)
        elif move == 2:
            n_state = state.move(pos, Direction.NORTHEAST)
        elif move == 3:
            n_state = state.jump(pos, Direction.NORTHWEST)
        elif move == 4:
            n_state = state.jump(pos, Direction.NORTH)
        elif move == 5:
            n_state = state.jump(pos, Direction.NORTHEAST)
        elif move == 6:
            n_state = state.capture(pos, Direction.WEST)
        elif move == 7:
            n_state = state.capture(pos, Direction.NORTHWEST)
        elif move == 8:
            n_state = state.capture(pos, Direction.NORTH)
        elif move == 9:
            n_state = state.capture(pos, Direction.NORTHEAST)
        else:
            n_state = state.capture(pos, Direction.EAST)

        if n_state == None:
            n_state = state
        
        return n_state

    def reset(self):
        self.game.restart()
        print('reset')
        self.game.render()
        return self.encode_state(self.game.state)

    def render(self, mode='human'):
        self.game.render()
