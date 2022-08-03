import gym
import numpy as np

from src.Adam import Adam
from src.OvergroundActionShaper import OvergroundActionShaper
from src.normalizers import normalize_actions
from constants.actions import CRAFT_WOODEN_PICKAXE, LOOK_DOWN, CRAFT_STONE_PICKAXE, CRAFT_FURNACE, CRAFT_TORCH
from constants.limits import LOGS_TO_CHOP, COBBLESTONE_TO_MINE


def main():
    # Create and compile the model
    model = Adam((64, 64, 3), 11)
    model.summary()
    model.compile()

    # Load the model's weights
    model.load_weights("weights/adam-v2.2/adam-v2.2.ckpt")

    # Create the environment to perform the actions on. Currently, the bot uses MineRLObtainDiamond-v0 env
    # because it is the closest env to the original conditions of player in Minecraft survival mode
    env = gym.make('MineRLObtainDiamond-v0')
    env = OvergroundActionShaper(env)
    env.seed(203)

    # Start Minecraft by resetting the environment
    obs = env.reset()

    # Get the size of the action space and form a list of action indices
    actions_number = env.action_space.n
    action_list = np.arange(actions_number)

    while obs['inventory']['log'] < LOGS_TO_CHOP:
        env.render()

        pov = (obs['pov'].astype(np.float) / 255.0).reshape(1, 64, 64, 3)
        # Call the model to predict the actions given the point of view
        action_probabilities = model(pov)
        # Apply the probabilities to the action list and sample an action
        action = np.random.choice(action_list, p=action_probabilities.numpy().squeeze())

        obs, reward, done, info = env.step(action)

    # Unwrap the environment and craft a wooden pickaxe
    env = env.unwrapped
    craft_wooden_pickaxe = normalize_actions(CRAFT_WOODEN_PICKAXE, env)
    look_down = normalize_actions(LOOK_DOWN, env)

    # Perform the actions above and acquire a wooden pickaxe
    # Then once again wrap the environment and prepare for mining. Before that, rotate the camera to look at the ground.
    for action in craft_wooden_pickaxe + look_down:
        env.render()
        obs, reward, done, info = env.step(action)

    env = OvergroundActionShaper(env)

    while obs['inventory']['cobblestone'] < COBBLESTONE_TO_MINE:
        env.render()
        obs, reward, done, info = env.step(0)

    # Unwrap the environment and craft a stone pickaxe
    env = env.unwrapped
    craft_stone_pickaxe = normalize_actions(CRAFT_STONE_PICKAXE, env)
    craft_furnace = normalize_actions(CRAFT_FURNACE, env)
    craft_torch = normalize_actions(CRAFT_TORCH, env)

    print("")
    print(obs['inventory'])

    for action in craft_stone_pickaxe + craft_furnace:
        env.render()
        obs, reward, done, info = env.step(action)

    print("")
    print(obs['inventory'])

    for action in craft_torch:
        if obs['inventory']['crafting_table']:
            print("")
            print(obs['inventory'])
        env.render()
        obs, reward, done, info = env.step(action)

    print("")
    print(obs['inventory'])


if __name__ == '__main__':
    main()
