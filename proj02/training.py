import gym
import gym_eximo

# from stable_baselines.common.env_checker import check_env
# check_env(env)
from stable_baselines.bench import Monitor

from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines import DQN
# from stable_baselines.common.policies import MlpPolicy
# from stable_baselines import PPO1

# uncomment if the tensorflow binary isnt compiled to use AVX
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

agent = 'deepq_v2'
MODEL_DIR = 'models/'

# create a directory for the trained agent and logs
agent_dir = MODEL_DIR + agent + '/'
os.makedirs(agent_dir, exist_ok=True)


env = gym.make('eximo-v0')
env = Monitor(env, agent_dir)


model = DQN(MlpPolicy, env, verbose=1, exploration_fraction=0.9)
model.learn(total_timesteps=100000, log_interval=1)
model.save(agent_dir + 'agent')


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