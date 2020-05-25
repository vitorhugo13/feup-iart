import numpy as np
from gym.spaces import Space

import random

class Action(Space):
    r"""A discrete space in :math:`\{ 0, 1, \\dots, n-1 \}`. 

    Example::

        >>> Discrete(2)

    """
    def __init__(self, actions: list):
        assert actions
        self.possible_actions = actions
        super(Action, self).__init__((), np.int64)

    def sample(self):
        return random.choice(self.possible_actions)

    def contains(self, x):
        if isinstance(x, int):
            as_int = x
        elif isinstance(x, (np.generic, np.ndarray)) and (x.dtype.char in np.typecodes['AllInteger'] and x.shape == ()):
            as_int = int(x)
        else:
            return False
        return as_int in self.possible_actions

    def __repr__(self):
        return "Action(" + self.possible_actions + ")"

    def __eq__(self, other):
        return isinstance(other, Action) and set(self.possible_actions) == set(other.possible_actions)
