import gym
from gym import error, spaces, utils
from gym.utils import seeding

from .eximo.eximo import Eximo
from .eximo.state import State
from .eximo.utils import Direction


class EximoEnv(gym.Env):
    metadata = {'render.modes': ['human']}


    def __init__(self):
        self.game = Eximo(['P', 0, None], ['P', 0, None])
        self.action_space = spaces.Discrete(606) # 54 pieces * 11 moves + 12 placement positions
        return

    # TODO: define the action space and observation space
    def step(self, action):

        state = self.game.state

        # regular move
        if action < 594:    # 54 * 11 = 594
            # get cell index
            cell = action // 11
            cell += 1 if (cell < 6) else 2
            # get cell coords
            pos = (cell // 8, cell % 8)

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

                if state.player == 1:
                    cell += 49

                pos = (cell // 8, cell % 8)

                if state.is_empty(pos):
                    n_state = state.place(pos)
                else:
                    n_state = state

        self.game.state = n_state
        observation = n_state
        done, winner = self.game.game_over(n_state)
        
        if done:
            reward = 100 if (winner == state.player) else -100
        else:
            reward = 0

        return observation, reward, done, winner 

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
        return self.game.state

    def render(self, mode='human'):
        self.game.render()
