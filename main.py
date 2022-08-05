import gym
import numpy as np
import minerl

from src.Adam import Adam
from src.Agent import Agent
from src.OvergroundActionShaper import OvergroundActionShaper
from src.normalizers import normalize_actions
from constants.actions import CRAFT_WOODEN_PICKAXE, LOOK_DOWN, CRAFT_STONE_PICKAXE, CRAFT_FURNACE
from constants.limits import LOGS_TO_CHOP, COBBLESTONE_TO_MINE, IRON_TO_MINE


def main():
    # Create the environment to perform the actions on. Currently, the bot uses MineRLObtainDiamond-v0 env
    # because it is the closest env to the original conditions of player in Minecraft survival mode
    env = gym.make('MineRLObtainDiamond-v0')
    env = OvergroundActionShaper(env)
    env.seed(203)

    # Start Minecraft by resetting the environment
    obs = env.reset()

    # Create the model and pass it to MineRL agent, and load the weights from the given path
    model = Adam((64, 64, 3), 11)
    agent = Agent(model, obs)
    agent.load_brain("weights/adam-v2.2/adam-v2.2.ckpt")

    # Get the size of the action space and form a list of action indices
    agent.gather_items('log', LOGS_TO_CHOP, env)

    craft_wooden_pickaxe = normalize_actions(CRAFT_WOODEN_PICKAXE, env)
    look_down = normalize_actions(LOOK_DOWN, env)

    # Perform the actions above and acquire a wooden pickaxe
    # Then once again wrap the environment and prepare for mining. Before that, rotate the camera to look at the ground.
    agent.craft_item(craft_wooden_pickaxe + look_down, env)

    env = OvergroundActionShaper(env)

    while obs['inventory']['cobblestone'] < COBBLESTONE_TO_MINE:
        env.render()
        obs, reward, done, info = env.step(0)

    # Unwrap the environment and craft a stone pickaxe
    env = env.unwrapped
    craft_stone_pickaxe = normalize_actions(CRAFT_STONE_PICKAXE, env)
    craft_furnace = normalize_actions(CRAFT_FURNACE, env)

    for action in craft_stone_pickaxe + craft_furnace:
        env.render()
        obs, reward, done, info = env.step(action)

    # Wrap the environment, load new weights and find some iron ore.
    agent.load_brain("weights/adam-v2.2.0/adam-v2.2.0.ckpt")
    agent.gather_items('iron_ore', IRON_TO_MINE, env)

    print(agent.obs['inventory'])


if __name__ == '__main__':
    main()
