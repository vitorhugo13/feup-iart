import warnings
warnings.filterwarnings("ignore")

from stable_baselines import bench
import matplotlib.pyplot as plt

def cumulative_plot(file: str, title: str) -> None:
    df = bench.monitor.load_results(file).copy()
    rewards = df.get('r').values
    timesteps = df.get('l').values

    for i in range(1, len(rewards)):
        rewards[i] = rewards[i - 1] + rewards[i]
        timesteps[i] = timesteps[i - 1] + timesteps[i]

    plt.plot(timesteps, rewards)
    plt.ylabel('Cumulative Rewards')
    plt.xlabel('Timesteps')
    plt.title(title)
    plt.tight_layout()

def regular_plot(file: str, title: str) -> None:
    df = bench.monitor.load_results(file).copy()
    rewards = df.get('r').values
    timesteps = df.get('l').values

    for i in range(1, len(rewards)):
        timesteps[i] = timesteps[i - 1] + timesteps[i]

    plt.plot(timesteps, rewards)
    plt.ylabel('Rewards')
    plt.xlabel('Timesteps')
    plt.title(title)
    plt.tight_layout()