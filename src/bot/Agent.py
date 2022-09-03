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
        while abs(xdif) > 0.7 or abs(xdif) < 0.3 or abs(zdif) > 0.7 or abs(zdif) < 0.3:

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

        # equipped item shows which item does the bot hold in the main hand.
        equipped_item = self.obs['equipped_items']['mainhand']['type']
        # have_space shows whether the bot has stone pickaxes in its inventory.
        have_s_pickaxes = self.obs['inventory']['stone_pickaxe'] > 0

        step = 0
        while self.obs['inventory'][item] < item_number and not done:
            # If bot's current stone pickaxe is broken, he must equip a new one from his inventory.
            if equipped_item != 'stone_pickaxe' and mode == UNDERGROUND_MODE and have_s_pickaxes:
                print("")
                print("")
                print("")
                print("Stone pickaxe is broken")
                env = env.unwrapped
                equip_pickaxe = normalize_actions({'equip': {'stone_pickaxe': 1}}, env)
                self.obs, reward, done, info = env.step(equip_pickaxe)
                env = ActionShaper(env, mode)
                print("")
                print("")
                print("")

            # Normalize agent's POV, so it could be fed to the model
            pov = (self.obs['pov'].astype(np.float) / 255.0).reshape(1, 64, 64, 3)
            # Call the model to predict the actions given the point of view
            action_probabilities = np.array(self.brain(pov)).squeeze()
            # Apply the probabilities to the action list and choose an action
            action = np.random.choice(a=action_list, p=action_probabilities)

            self.obs, reward, done, info = env.step(action)
            self.monitor.record(action, mode)
            step += 1

            if step % 200 == 0:
                print("")
                print("")
                print(f'step: {step}')
                print("")
                print(f'inventory: {self.obs["inventory"]}')
                print("")
                print(f'equipped item: {equipped_item}')
                print("")
                print(f'have stone pickaxes: {have_s_pickaxes}')
