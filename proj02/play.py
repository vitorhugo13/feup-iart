import gym
import gym_eximo
import sys

import warnings
warnings.filterwarnings("ignore")

if len(sys.argv) < 3:
    sys.exit('No trained model found...')

env = gym.make('eximo-v0')

model_type = sys.argv[1]
model_name = sys.argv[2] + '/agent'

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
