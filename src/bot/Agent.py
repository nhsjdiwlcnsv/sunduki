import math
import numpy as np

from constants.modes import *
from src.env.ActionShaper import ActionShaper
from src.env.normalizers import normalize_actions


class Agent:
    def __init__(self, agent_brain, observation):
        self.brain = agent_brain
        self.brain.compile()
        self.brain.summary()

        self.obs = observation

    def load_brain(self, path):
        self.brain.load_weights(path)

    def carry_out(self, actions, env):
        # Unwrap the environment, so it could support the actions that are not available in the shaped environment
        env = env.unwrapped
        # Perform given actions and acquire the item
        for action in actions:
            env.render()
            self.obs, reward, done, info = env.step(action)

    def stand_still(self, env):
        env = ActionShaper(env, OVERGROUND_MODE)
        xpos, zpos = self.obs['location_stats']['xpos'], self.obs['location_stats']['zpos']
        xdif, zdif = xpos - math.floor(xpos), zpos - math.floor(zpos)

        while abs(xdif) > 0.7 or abs(zdif) > 0.7:

            self.obs, reward, done, info = env.step(1)
            self.obs, reward, done, info = env.step(10)

            xpos, zpos = self.obs['location_stats']['xpos'], self.obs['location_stats']['zpos']
            xdif, zdif = xpos - math.floor(xpos), zpos - math.floor(zpos)

            env.render()

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

            env.render()
