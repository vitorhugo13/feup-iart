from gym.envs.registration import register

# 8x8 board
# rewards:
#   +1 on win
#   -1 on loss
register(
    id='eximo-v0',
    entry_point='gym_eximo.envs:EximoEnv',
)

# 8x8 board
# rewards:
#   +1000 on win
#   -1000 on loss
#   +1 on valid move
#   -1 on invalid move
register(
    id='eximo-v2',
    entry_point='gym_eximo.envs:EximoEnv2'
)

# 5x5 board
# rewards:
#   +1 on win
#   -1 on loss
register(
    id='eximo-v3',
    entry_point='gym_eximo.envs:EximoEnv3'
)