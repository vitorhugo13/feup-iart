import gym
import numpy as np
import random
import gym_eximo

env = gym.make('eximo-v0')

state_size = env.observation_space.n
action_size = env.action_space.n      

state = env.observation_space

qtable = np.zeros((state_size, action_size))

# QLearning parameters
total_episodes = 1
learning_rate = 0.75
max_steps = 10000
gamma = 0.95

epsilon = 1.0
max_epsilon = 1.0
min_epsilon = 0.01
decay_rate = 0.001

# Rewards
rewards = []


