import gym

from src.env.ActionShaper import ActionShaper


class Recorder:
    def __init__(self, seed):
        self.env = gym.make('RecorderEnv-v0')
        self.env = gym.wrappers.Monitor(self.env, './public/videos', force=True)
        self.env.seed(seed)
        self.env.reset()

    def record(self, action, mode=None):
        draft_env = ActionShaper(self.env, mode) if mode else self.env
        act = draft_env.new_action_space[action] if mode else action

        obs, _, _, _ = self.env.step(act)

        self.env.render()
