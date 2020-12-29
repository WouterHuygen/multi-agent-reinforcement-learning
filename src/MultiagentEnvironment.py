import gym
import numpy as np
from ray.rllib.env import MultiAgentEnv
from src.Environment import Environment
from src.SimulatorParameters import sim_params

class MAEnvironment(gym.Env, MultiAgentEnv):

    def __init__(self):

        self.action_space_prey = gym.spaces.Discrete(4)

        self.observation_space_prey = gym.spaces.Box(low=np.array([0, 0, 0]),
                                                high=np.array([sim_params["prey_max_age"],sim_params["environment_width"], sim_params["environment_height"]]))

        self.action_space_predator = gym.spaces.Discrete(5)

        self.observation_space_predator = gym.spaces.Box(low=np.array([0, 0, 0, 0]),
                                                high=np.array([sim_params["hunter_max_age"], np.inf,
                                                               sim_params["environment_width"],
                                                               sim_params["environment_height"]]))

        self.environment = Environment(sim_params["environment_width"], sim_params["environment_height"], sim_params["max_amount_of_prey"], sim_params["prey_max_age"], sim_params["prey_birth_rate"],
                                       sim_params["max_amount_of_hunters"], sim_params["hunter_max_age"], sim_params["hunter_energy_to_reproduce"], sim_params["hunter_energy_per_prey_eaten"],
                                       sim_params["hunter_init_energy"])




    def reset(self):
        print("Number of preys: "+str(len(self.environment.prey_list)))
        print("Number of Predator: "+str(len(self.environment.predator_list)))
        self.environment.reset()
        return self.environment.total_obs()

    def step(self, action):
        self.environment.step( env= "multiagent", actions = action)
        return self.environment.total_obs(), self.environment.total_rewards(), self.environment.total_dones(), {}