import gym

from src.Adam import Adam
from src.Agent import Agent
from src.normalizers import normalize_actions
from constants.actions import CRAFT_WOODEN_PICKAXE, MINE_DOWN, CRAFT_STONE_PICKAXE, CRAFT_FURNACE
from constants.limits import LOGS_TO_CHOP, COBBLESTONE_TO_MINE, IRON_TO_MINE
from constants.modes import OVERGROUND_MODE, UNDERGROUND_MODE


def main():
    # Create the environment to perform the actions on. Currently, the bot uses MineRLObtainDiamond-v0 env
    # because it is the closest env to the original conditions of player in Minecraft survival mode
    env = gym.make('MineRLObtainDiamond-v0')
    env.seed(203)

    # Start Minecraft by resetting the environment
    obs = env.reset()

    # Create the model and pass it to MineRL agent, and load the weights from the given path
    model = Adam((64, 64, 3), 11)
    agent = Agent(model, obs)

    # Load the weights from the given path and gather some wood. Shape the env to reduce the number of actions
    agent.load_brain("weights/adam-v2.2/adam-v2.2.ckpt")
    agent.gather_items('log', LOGS_TO_CHOP, env, OVERGROUND_MODE)

    # Perform the actions above and acquire a wooden pickaxe
    # Then rotate the camera to look at the ground and mine down some blocks.
    craft_wooden_pickaxe = normalize_actions(CRAFT_WOODEN_PICKAXE, env)
    mine_down = normalize_actions(MINE_DOWN, env)
    agent.carry_out(craft_wooden_pickaxe + mine_down, env)

    agent.load_brain("weights/adam-v2.2.0/adam-v2.2.0.ckpt")
    agent.gather_items('cobblestone', COBBLESTONE_TO_MINE, env, UNDERGROUND_MODE)

    # Craft a stone pickaxe and a furnace. Prepare for mining iron ore.
    craft_stone_pickaxe = normalize_actions(CRAFT_STONE_PICKAXE, env)
    craft_furnace = normalize_actions(CRAFT_FURNACE, env)
    agent.carry_out(craft_stone_pickaxe + craft_furnace, env)

    print(agent.obs['inventory'])

    # Wrap the environment, load the weights for underground actions and find some iron ore.
    agent.gather_items('iron_ore', IRON_TO_MINE, env, UNDERGROUND_MODE)

    print(agent.obs['inventory'])


if __name__ == '__main__':
    main()
