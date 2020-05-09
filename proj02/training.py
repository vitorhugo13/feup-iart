import gym
import gym_eximo

from stable_baselines.common.policies import MlpPolicy
from stable_baselines import DQN

env = gym.make('eximo-v0')

model = DQN(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=1000000)
model.save("deepq_eximo")

# del model
# model = DQN.load("deepq_eximo")

obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()


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