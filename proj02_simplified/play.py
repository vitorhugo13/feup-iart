import gym
import gym_eximo
import sys

env = gym.make('eximo-v0')


# uncomment if the tensorflow binary isnt compiled to use AVX
# import os
# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

if len(sys.argv) < 2:
    sys.exit('No trained model found...')
    
env.game.play()

# from stable_baselines.deepq.policies import MlpPolicy
# from stable_baselines import DQN
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import PPO1





# model = PPO1.load("deepq_eximo")

# obs = env.reset()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()


# for i_episode in range(1):
#     observation = env.reset()
#     for t in range(1000000):
#         env.render()
#         # print(observation)
#         action = env.action_space.sample()
#         observation, reward, done, winner = env.step(action)
#         if done:
#             print("Episode finished after {} timesteps".format(t+1))
#             print("Winner : " + winner)
#             break
# env.close()