import gym
import gym_eximo

env = gym.make('eximo-v0')
for i_episode in range(1):
    observation = env.reset()
    for t in range(1000000):
        env.render()
        # print(observation)
        action = env.action_space.sample()
        observation, reward, done, winner = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            print("Winner : " + winner)
            break
env.close()