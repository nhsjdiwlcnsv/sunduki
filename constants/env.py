# Seed that is used to generate the world.
SEED = 46353

# The maximum number of steps the bot can take during each session.
MAX_STEPS = 150_000

# These are default handlers for actions and observations.
other = 'other'
none = 'none'


def register_envs():
    from src.env.env_specs import CustomMineRLEnv
    from src.recorder.rec_specs import RecorderEnv
    # For using custom environments gym requires that the environment is registered as a gym environment.
    # ABS_ENV is a custom env with 64x64 resolution in which the bot actually performs the actions.
    abs_env = CustomMineRLEnv()
    abs_env.register()

    # ABS_REC is a custom env with 360x360 resolution used only for recording the bot's progress into videos.
    abs_rec = RecorderEnv()
    abs_rec.register()
