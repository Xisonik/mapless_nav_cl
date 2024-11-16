from tasks.env_yolo import AlphaBaseEnv
from gymnasium.envs.registration import register
print("register")

register(
     id="AlphaBaseEnv-v0",
     entry_point="tasks.env_yolo:AlphaBaseEnv",
     max_episode_steps=512,
)

register(
     id="AlphaBaseEnv-v1",
     entry_point="tasks.env_with_graph:AlphaBaseEnv",
     max_episode_steps=512,
)
