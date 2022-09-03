import gym

from src.env.ActionShaper import ActionShaper


# This class is used to record videos of bot's performance.
# It creates a gym environment and copies all the action, creating a full copy of bot's behavior on a higher resolution env.
class Recorder:
    def __init__(self, seed):
        self.env = gym.make('RecorderEnv-v0')
        self.env = gym.wrappers.Monitor(self.env, './public/videos', video_callable=False, force=True)
        self.env.seed(seed)
        self.env.reset()

    def record(self, action, mode=None):
        # Unfortunately, due to the fact that the original env is being wrapped and unwrapped many times for many
        # purposes, we need to first create a fake env in order to get the action space of original env, and then
        # adjust our action to its shape.
        draft_env = ActionShaper(self.env, mode) if mode else self.env
        act = draft_env.new_action_space[action] if mode else action

        obs, _, _, _ = self.env.step(act)

        self.env.render()
