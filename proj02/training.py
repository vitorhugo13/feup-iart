import gym
import gym_eximo
import sys

from stable_baselines.bench import Monitor

# uncomment if the tensorflow binary isnt compiled to use AVX
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import warnings
warnings.filterwarnings("ignore")

if len(sys.argv) != 4:
    print('Usage: python training.py <env> <model> <agent_name>')
    sys.exit()

env_name = sys.argv[1]
model_name = sys.argv[2]
agent_name = sys.argv[3]


# create a directory for the trained agent and logs
MODEL_DIR = 'models/'

agent_dir = MODEL_DIR + '/' + env_name + '/' + agent_name + '/'
os.makedirs(agent_dir, exist_ok=True)

env = gym.make(env_name)
env = Monitor(env, agent_dir)


if model_name == 'dqn':
    from stable_baselines.deepq.policies import MlpPolicy
    from stable_baselines import DQN
    
    model = DQN(MlpPolicy, env, verbose=1, exploration_fraction=0.8, exploration_final_eps=0.15)
    model.learn(total_timesteps=1000000, log_interval=1)
    model.save(agent_dir + 'agent')

elif model_name == 'ppo1':
    from stable_baselines.common.policies import MlpPolicy
    from stable_baselines import PPO1

    model = PPO1(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=3000000, log_interval=1)
    model.save(agent_dir + 'agent')

elif model_name == 'acer':
    from stable_baselines.common.policies import MlpPolicy
    from stable_baselines import ACER 
    model = ACER(MlpPolicy, env, verbose=1)
    model.learn(total_timesteps=1000000, log_interval=1)
    model.save(agent_dir + 'agent')
 
else:
    print('Usage: python training.py <env> <model> <agent_name>')
