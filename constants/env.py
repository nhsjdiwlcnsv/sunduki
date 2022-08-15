from src.env.env_specs import CustomMineRLEnv
from src.recorder.rec_specs import RecorderEnv

SEED = 203

ABS_ENV = CustomMineRLEnv()
ABS_ENV.register()

ABS_REC = RecorderEnv()
ABS_REC.register()
