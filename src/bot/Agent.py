import math
import numpy as np

from constants.actions import CRAFT_S_PICKAXE
from constants.env import SEED
from constants.modes import *
from src.env.ActionShaper import ActionShaper
from src.env.normalizers import normalize_actions
from src.recorder.recorder import Recorder


class Agent:
    def __init__(self, agent_brain, obs, monitor):
        self.brain = agent_brain
        self.brain.compile()

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

    def stand_still(self, env):
        env = ActionShaper(env, OVERGROUND_MODE)
        xpos, zpos = self.obs['location_stats']['xpos'], self.obs['location_stats']['zpos']
        xdif, zdif = xpos - math.floor(xpos), zpos - math.floor(zpos)

        while abs(xdif) > 0.7 or abs(zdif) > 0.7:
            self.obs, reward, done, info = env.step(1)
            self.obs, reward, done, info = env.step(10)
            self.monitor.record(1, OVERGROUND_MODE)
            self.monitor.record(10, OVERGROUND_MODE)

            xpos, zpos = self.obs['location_stats']['xpos'], self.obs['location_stats']['zpos']
            xdif, zdif = xpos - math.floor(xpos), zpos - math.floor(zpos)

    def gather_items(self, item, item_number, env, mode):
        # Wrap the env so the bot could use only relevant actions
        env = ActionShaper(env, mode)

        # Get the number of possible actions and form a list of action indices
        actions_number = env.action_space.n
        action_list = np.arange(actions_number)
        done = False

        equipped_item = self.obs['equipped_items']['mainhand']['type']
        have_s_pickaxes = self.obs['inventory']['stone_pickaxe'] > 0

        while self.obs['inventory'][item] < item_number and not done:

            if equipped_item != 'stone_pickaxe' and mode == UNDERGROUND_MODE and have_s_pickaxes:
                self.carry_out(normalize_actions({'equip': {'stone_pickaxe': 1}}, env), env)

            # Normalize agent's POV, so it could be fed to the model
            pov = (self.obs['pov'].astype(np.float) / 255.0).reshape(1, 64, 64, 3)
            # Call the model to predict the actions given the point of view
            action_probabilities = np.array(self.brain(pov)).squeeze()
            # Apply the probabilities to the action list and choose an action
            action = np.random.choice(a=action_list, p=action_probabilities)

            self.obs, reward, done, info = env.step(action)
            self.monitor.record(action, mode)
