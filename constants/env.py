from src.env.env_specs import CustomMineRLEnv
from src.recorder.rec_specs import RecorderEnv

# Seed that is used to generate the world.
SEED = 203

# For using custom environments gym requires that the environment is registered as a gym environment.
# ABS_ENV is a custom env with 64x64 resolution in which the bot actually performs the actions.
ABS_ENV = CustomMineRLEnv()
ABS_ENV.register()

# ABS_REC is a custom env with 360x360 resolution used only for recording the bot's progress into videos.
ABS_REC = RecorderEnv()
ABS_REC.register()
