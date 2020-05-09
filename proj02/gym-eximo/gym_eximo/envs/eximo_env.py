import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np

from eximo import Eximo
from utils import Direction


class EximoEnv(gym.Env):
    metadata = {'render.modes': ['human']}


    def __init__(self):
        self.game = Eximo(['P', 0, None], ['P', 0, None])
        self.action_space = Space.Discrete(606) # 54 pieces * 11 moves + 12 placement positions
        return

    # TODO: define the action space and observation space
    def step(self, action):

        # regular move
        if action < 594:
            # get cell index
            cell = action // 11
            cell += 1 if (cell < 6) else 2
            # get cell coords
            pos = (cell // 8, cell % 8)

            # get move index
            move = action % 11

            if move == 0:
                self.game.state.move(pos, Direction.NORTHWEST)
            elif move == 1:
                self.game.state.move(pos, Direction.NORTH)
            elif move == 2:
                self.game.state.move(pos, Direction.NORTHEAST)
            elif move == 3:
                self.game.state.jump(pos, Direction.NORTHWEST)
            elif move == 4:
                self.game.state.jump(pos, Direction.NORTH)
            elif move == 5:
                self.game.state.jump(pos, Direction.NORTHEAST)
            elif move == 6:
                self.game.state.capture(pos, Direction.WEST)
            elif move == 7:
                self.game.state.capture(pos, Direction.NORTHWEST)
            elif move == 8:
                self.game.state.capture(pos, Direction.NORTH)
            elif move == 9:
                self.game.state.capture(pos, Direction.NORTHEAST)
            else:
                self.game.state.capture(pos, Direction.EAST)

        # placement
        else:
            cell = action - 594
            cell += 1 if (cell < 6) else 3

            pos = (cell // 8, cell % 8)

            self.game.state.place(pos)


        



        # if self.game.state.player == 2 and self.game.state.action[0] == 1:
        #     self.game.state.board = np.flipud(self.game.state.board) # still not fliped correctly

        # observation - state of the game
        # reward - should be 1 when it wins, -1 otherwise
        # done - true when an episode ends 
        return observation, reward, done, winner 

    def reset(self):
        self.game.restart()

    def render(self, mode='human'):
        self.game.render()

    def close(self):
        return