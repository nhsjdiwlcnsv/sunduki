import numpy as np

from constants.modes import *
from constants.limits import *
from src.env.ActionShaper import ActionShaper
from src.env.normalizers import normalize_actions


class Agent:
    def __init__(self, agent_brain, obs, monitor):
        self.brain = agent_brain
        self.brain.compile()

        # Monitor is used to record the bot's progress into videos. Its method record() gets an action,
        # then it executes it in his high resolution environment and records the result. Using this technique,
        # we can get a more appealing video than the one produced by the gym's default environment.
        self.monitor = monitor
        self.obs = obs

    def load_brain(self, path):
        self.brain.load_weights(path)

    def carry_out(self, actions, env):
        # Unwrap the environment, so it could support the actions that are not available in the shaped environment
        env = env.unwrapped
        # Perform given actions and acquire the item
        for action in actions:
            self.obs, reward, done, info = env.step(action)
            self.monitor.record(action)

    # This method is used to correct the bot's situation after he has gathered all the logs.
    # It is vitally important because the bot needs to stand right on a block, which will allow
    # him to mine down under himself.
    def stand_still(self, env):
        env = ActionShaper(env, UNDERGROUND_MODE)
        # Calculate bot's position in the world by getting the coordinates he is standing on
        # and then calculate the difference between the bot's position and the nearest whole number.
        xpos, zpos = self.obs['location_stats']['xpos'], self.obs['location_stats']['zpos']
        xdif, zdif = xpos - math.floor(xpos), zpos - math.floor(zpos)

        # If the difference is greater than 0.7 (once again, empiric method), the bot must move
        # forward and right (if needed) to stand on the block.
        while abs(xdif) > 0.8 or abs(xdif) < 0.2 or abs(zdif) > 0.8 or abs(zdif) < 0.2:
            self.obs, reward, done, info = env.step(1)
            self.obs, reward, done, info = env.step(15)
            self.monitor.record(1, UNDERGROUND_MODE)
            self.monitor.record(15, UNDERGROUND_MODE)

            xpos, zpos = self.obs['location_stats']['xpos'], self.obs['location_stats']['zpos']
            xdif, zdif = xpos - math.floor(xpos), zpos - math.floor(zpos)

    def gather_items(self, item, item_number, env, mode):
        # Wrap the env so the bot could use only relevant actions
        env = ActionShaper(env, mode)

        # Get the number of possible actions and form a list of action indices
        actions_number = env.action_space.n
        action_list = np.arange(actions_number)
        done = False

        while self.obs['inventory'][item] < item_number and not done:
            # Normalize agent's POV, so it could be fed to the model
            pov = (self.obs['pov'].astype(np.float) / 255.0).reshape(1, 64, 64, 3)
            # Call the model to predict the actions given the point of view
            action_probabilities = np.array(self.brain(pov)).squeeze()
            # Apply the probabilities to the action list and choose an action
            action = np.random.choice(a=action_list, p=action_probabilities)

            self.obs, reward, done, info = env.step(action)
            self.monitor.record(action, mode)
