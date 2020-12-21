import gym
import numpy as np
from ray.rllib.env import MultiAgentEnv
from src.SimulatorParameters import sim_params
from src.Environment import Environment

class PredatorEnv(gym.Env, MultiAgentEnv):

    def __init__(self):
        self.action_space = gym.spaces.Discrete(5)

        self.observation_space = gym.spaces.Box(low=np.array([0, 0, 0, 0]),
                                            high=np.array([sim_params["hunter_max_age"], np.inf, sim_params["environment_width"], sim_params["environment_height"]]))

        self.environment = Environment(sim_params["environment_width"], sim_params["environment_height"],
                                       sim_params["amount_of_prey"], sim_params["prey_max_age"],
                                       sim_params["prey_birth_rate"],
                                       sim_params["amount_of_hunters"], sim_params["hunter_max_age"],
                                       sim_params["hunter_energy_to_reproduce"],
                                       sim_params["hunter_energy_per_prey_eaten"])

    def reset(self):
        self.environment.reset()
        return self.environment.predator_obs()

    def step(self, action):
        self.environment.step(env="predator", actions=action)
        print(self.environment.predator_dones())
        return self.environment.predator_obs(), self.environment.predator_rewards(), self.environment.predator_dones(), {}