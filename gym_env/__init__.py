from gym.envs.registration import register

register(
    id='PreyEnvironment-v0',
    entry_point='gym_env.envs:PreyEnvironment',
)