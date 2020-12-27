
import gym
import numpy as np
from ray.rllib.env import MultiAgentEnv
from src.Environment import Environment
from src.SimulatorParameters import sim_params

class PreyEnv(gym.Env, MultiAgentEnv):

    def __init__(self):

        self.action_space = gym.spaces.Discrete(4)

        self.observation_space = gym.spaces.Box(low=np.array([0, 0, 0]),
                                                high=np.array([sim_params["prey_max_age"],sim_params["environment_width"], sim_params["environment_height"]]))

        self.environment = Environment(sim_params["environment_width"], sim_params["environment_height"], sim_params["max_amount_of_prey"], sim_params["prey_max_age"], sim_params["prey_birth_rate"],
                                       sim_params["max_amount_of_hunters"], sim_params["hunter_max_age"], sim_params["hunter_energy_to_reproduce"], sim_params["hunter_energy_per_prey_eaten"],
                                       sim_params["hunter_init_energy"])




    def reset(self):
        #print("Number of preys: "+str(len(self.environment.prey_list)))
        self.environment.reset()
        return self.environment.prey_obs()

    def step(self, action):
        self.environment.step( env= "prey", actions = action)
        return self.environment.prey_obs(), self.environment.prey_rewards(), self.environment.prey_dones(), {}