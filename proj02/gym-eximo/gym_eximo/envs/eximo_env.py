import gym
from gym import error, spaces, utils
from gym.utils import seeding

from eximo import Eximo


class EximoEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = Eximo(['P', 0, None], ['P', 0, None])
        return

    # TODO: define the action space and observation space
    def step(self, action):
        


        return observation, reward, done, winner 

    def reset(self):
        return 

    def render(self, mode='human'):
        self.game.state.print()
        return

    def close(self):
        return