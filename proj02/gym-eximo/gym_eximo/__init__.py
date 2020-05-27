from gym.envs.registration import register

register(
    id='eximo-v0',
    entry_point='gym_eximo.envs:EximoEnv',
)

register(
    id='eximo-v2',
    entry_point='gym_eximo.envs:EximoEnv2'
)
# register(
#     id='foo-extrahard-v0',
#     entry_point='gym_foo.envs:FooExtraHardEnv',
# )