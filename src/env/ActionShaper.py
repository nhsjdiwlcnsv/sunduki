import gym

from abc import ABC


# This class is inherited from the abstract class gym.ActionWrapper that is used to filter out the actions that are not relevant
# for the current environment.
class ActionShaper(gym.ActionWrapper, ABC):
    def __init__(self, env, new_actions):
        super().__init__(env)

        # The list of all possible actions the bot can take while being over ground
        self.new_actions = new_actions

        # Gym envs possess a special field – 'action_space'. While 'self.new_actions' is just a list of actions,
        # the action space of environment is an object of gym.spaces.Space (e.g. Dict or Discrete) type, that defines
        # types of actions
        self.new_action_space = []
        for action_pair in self.new_actions:
            # env.action_space.sample() returns a random sample of actions at one time step.
            # env.action_space.noop() returns a sample without active actions.
            act = self.env.action_space.noop()
            for action, value in action_pair:
                act[action] = value
                # 'act' is a sample of action_space where only the required action is active.

            self.new_action_space.append(act)

        self.action_space = gym.spaces.Discrete(len(self.new_action_space))

    # action() is a method that must be overwritten so that step() could work correctly
    def action(self, action):
        return self.new_action_space[action]
