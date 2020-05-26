import gym
import gym_eximo

# from stable_baselines.common.env_checker import check_env
# check_env(env)
from stable_baselines.bench import Monitor

# uncomment if the tensorflow binary isnt compiled to use AVX
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import warnings
warnings.filterwarnings("ignore")


# create a directory for the trained agent and logs
agent = 'change'
MODEL_DIR = 'models/'

agent_dir = MODEL_DIR + agent + '/'
os.makedirs(agent_dir, exist_ok=True)


env = gym.make('eximo-v0')
env = Monitor(env, agent_dir)


# from stable_baselines.deepq.policies import MlpPolicy
# from stable_baselines import DQN

# model = DQN(MlpPolicy, env, verbose=1, learning_rate=0.2, exploration_fraction=0.5)
# model.learn(total_timesteps=5000000, log_interval=1)
# model.save(agent_dir + 'agent')


# from stable_baselines.common.policies import MlpPolicy
# from stable_baselines import PPO1

# model = PPO1(MlpPolicy, env, verbose=1)
# model.learn(total_timesteps=5000000, log_interval=1)
# model.save(agent_dir + 'agent')


# from stable_baselines.common.policies import MlpPolicy
# from stable_baselines import ACER

# model = ACER(MlpPolicy, env, verbose=1, learning_rate=0.01)
# model.learn(total_timesteps=1000000, log_interval=1)
# model.save(agent_dir + 'agent')
