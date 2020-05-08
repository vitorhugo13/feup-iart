from gym.envs.registration import register

register(
    id='eximo-v0',
    entry_point='gym_eximo.envs:EximoEnv',
)
# register(
#     id='foo-extrahard-v0',
#     entry_point='gym_foo.envs:FooExtraHardEnv',
# )