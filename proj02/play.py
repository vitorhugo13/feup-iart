import gym
import gym_eximo
import sys

import warnings
warnings.filterwarnings("ignore")

if len(sys.argv) != 4:
    print('Usage: python play.py <env> <model> <agent_name>')
    sys.exit()

env_name = sys.argv[1]
model_type = sys.argv[2]
model_name = sys.argv[3] + '/agent'

env = gym.make(env_name)

if model_type == 'ppo1':
    from stable_baselines.common.policies import MlpPolicy
    from stable_baselines import PPO1
    model = PPO1.load(model_name)

elif model_type == 'dqn':
    from stable_baselines.deepq.policies import MlpPolicy
    from stable_baselines import DQN
    model = DQN.load(model_name)

elif model_type == 'acer':
    from stable_baselines.common.policies import MlpPolicy
    from stable_baselines import ACER
    model = ACER.load(model_name)

obs = env.reset()
done = False
while not done:
    action, _states = model.predict(obs)
    obs, rewards, done, info = env.step(action)
    env.render()
