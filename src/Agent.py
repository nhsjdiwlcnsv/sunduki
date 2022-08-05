import numpy as np

from src.OvergroundActionShaper import OvergroundActionShaper


class Agent:
    def __init__(self, agent_brain, observation):
        self.brain = agent_brain
        self.brain.compile()
        self.brain.summary()

        self.obs = observation

    def load_brain(self, path):
        self.brain.load_weights(path)

    def craft_item(self, actions, env):
        # Unwrap the environment, so it could support the actions that are not available in the shaped environment
        env = env.unwrapped
        # Perform given actions and acquire the item
        for action in actions:
            self.obs, reward, done, info = env.step(action)

    def gather_items(self, item, item_number, env):
        # Wrap the env so the bot could use only relevant actions
        env = OvergroundActionShaper(env)

        # Get the number of possible actions and form a list of action indices
        actions_number = env.action_space.n
        action_list = np.arange(actions_number)

        while self.obs['inventory'][item] < item_number:
            env.render()

            # Normalize agent's POV, so it could be fed to the model
            pov = (self.obs['pov'].astype(np.float) / 255.0).reshape(1, 64, 64, 3)
            # Call the model to predict the actions given the point of view
            action_probabilities = self.brain(pov)
            # Apply the probabilities to the action list and choose an action
            action = np.random.choice(action_list, p=action_probabilities.numpy().squeeze())
            self.obs, reward, done, info = env.step(action)

