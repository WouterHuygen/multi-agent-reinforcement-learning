import ray
from ray import tune
from ray.rllib.models import ModelCatalog
from src.dqn import dqn_predator_policy, dqn_prey_policy, DQNTrainer, dqn_prey_model, dqn_predator_model
from src import PreyEnvironment, PredatorEnvironment, MultiagentEnvironment



def create_prey_env(env_config):
    return PreyEnvironment.PreyEnv()

def create_predator_env(env_config):
    return PredatorEnvironment.PredatorEnv()

def create_multiagent_env(env_config):
    return MultiagentEnvironment.MAEnvironment()


if __name__ == "__main__":
    ray.init()
    env = tune.register_env("MAEnv-v0", create_multiagent_env)
    ModelCatalog.register_custom_model("DQNPredatorModel", dqn_predator_model.DQNPredatorModel)
    ModelCatalog.register_custom_model("DQNPreyModel", dqn_prey_model.DQNPreyModel)

    policy_config = {
        "predator_policy_config": {
            "no_done_at_end": True,
            "num_gpus": 0,
            "num_workers": 1,
            "framework": "torch",
            # "sample_batch_size": 50,
            "env": "MAEnv-v0",
            "dqn_model": {
                "custom_model": "DQNPredatorModel",
                "custom_model_config": {
                    "network_size": [32, 64, 32],
                },  # extra options to pass to your model
            },

            ########################################
            # Parameters Agent
            ########################################
            "lr": 4e-3,
            # "lr": tune.grid_search([5e-3, 2e-3, 1e-3, 5e-4]),
            "gamma": 0.985,
            # "gamma": tune.grid_search([0.983, 0.985, 0.986, 0.987, 0.988, 0.989]),
            "epsilon": 1,
            "epsilon_decay": 0.99998,
            "epsilon_min": 0.01,
            "buffer_size": 20000,
            "batch_size": 2000,

            ########################################
            # Envaluation parameters
            ########################################
            "evaluation_interval": 100, # based on training iterations
            "evaluation_num_episodes": 100,
            "evaluation_config": {
                "epsilon": -1,
            },
        },
        "prey_policy_config": {
            "no_done_at_end": True,
            "num_gpus": 0,
            "num_workers": 1,
            "framework": "torch",
            # "sample_batch_size": 50,
            "env": "MAEnv-v0",
            "dqn_model": {
                "custom_model": "DQNPreyModel",
                "custom_model_config": {
                    "network_size": [32, 64, 32],
                },  # extra options to pass to your model
            },

            ########################################
            # Parameters Agent
            ########################################
            "lr": 4e-3,
            # "lr": tune.grid_search([5e-3, 2e-3, 1e-3, 5e-4]),
            "gamma": 0.985,
            # "gamma": tune.grid_search([0.983, 0.985, 0.986, 0.987, 0.988, 0.989]),
            "epsilon": 1,
            "epsilon_decay": 0.99998,
            "epsilon_min": 0.01,
            "buffer_size": 20000,
            "batch_size": 2000,

            ########################################
            # Envaluation parameters
            ########################################
            "evaluation_interval": 100, # based on training iterations
            "evaluation_num_episodes": 100,
            "evaluation_config": {
                "epsilon": -1,
            },
        }
    }

    MAE = MultiagentEnvironment.MAEnvironment()
    policies = {"predator": (dqn_predator_policy.DQNPredatorPolicy,
                           MAE.observation_space_predator,
                           MAE.action_space_predator,
                           policy_config["predator_policy_config"]),
                "prey": (dqn_prey_policy.DQNPreyPolicy,
                         MAE.observation_space_prey,
                         MAE.action_space_prey,
                         policy_config["prey_policy_config"])}


    def policy_mapping_fn(agent_id):
        if "predator" in agent_id:
            return "predator"
        else:
            return "prey"


    tune.run(
        DQNTrainer,

        # checkpoint_freq=10,
        checkpoint_at_end=True,
        stop={"timesteps_total": 2000000},
        config={
            "no_done_at_end": True,
            "num_gpus": 0,
            "num_workers": 1,
            "framework": "torch",
            # "sample_batch_size": 50,
            "env": "MAEnv-v0",

            ########################################
            # Parameters Agent
            ########################################
            "lr": 4e-3,
            # "lr": tune.grid_search([5e-3, 2e-3, 1e-3, 5e-4]),
            "gamma": 0.985,
            # "gamma": tune.grid_search([0.983, 0.985, 0.986, 0.987, 0.988, 0.989]),
            "epsilon": 1,
            "epsilon_decay": 0.99998,
            "epsilon_min": 0.01,
            "buffer_size": 20000,
            "batch_size": 2000,

            "multiagent": {
                "policy_mapping_fn": policy_mapping_fn,
                "policies": policies,
                "policies_to_train": policies
            },

            ########################################
            # Envaluation parameters
            ########################################
            "evaluation_interval": 100, # based on training iterations
            "evaluation_num_episodes": 100,
            "evaluation_config": {
                "epsilon": -1,
            },
        }


    )
