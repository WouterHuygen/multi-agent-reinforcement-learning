import gym
from gym import error, spaces, utils
from gym.utils import seeding

class preyEnv(gym.Env):
    def __init__(self):
        self.action_space = ['Up', 'Down', 'Left', 'Right',]
        self.observation_space = ['age', 'xDistance', 'yDistance']
        self.simulator

    def reset(self):
        pass

    def step(self, action):
        pass
        #return <obs> : obs, <reward: float>: reward, <done: bool>: done