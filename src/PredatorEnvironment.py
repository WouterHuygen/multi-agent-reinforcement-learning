import ray
from ray.tune.registry import register_env
from src.Simulator import Simulator
import gym


def env_creator(env_config):
    return PredatorEnv()

register_env("PredatorEnv", env_creator)

class PredatorEnv(gym.Env):

    def __init__(self):
        self.action_space = 0
        # self.observation_space = ..# zie opgave
        self.simulator = Simulator()

    def reset(self):
        self.simulator.reset()

    def step(self, action):
        return 0
        # return<obs>, <reward: float>, <done: bool>