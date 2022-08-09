import gym

from src.bot.Adam import Adam
from src.bot.Agent import Agent
from src.env.normalizers import normalize_actions
from src.env.env_specs import CustomMineRLEnv
from constants.actions import *
from constants.limits import *
from constants.modes import *


def main():
    # Create the environment to perform the actions on. Currently, the bot uses MineRLObtainDiamond-v0 env
    # because it is the closest env to the original conditions of player in Minecraft survival mode
    abs_env = CustomMineRLEnv()
    abs_env.register()
    env = gym.make('CustomMineRLEnv-v0')
    print("")
    print(env.action_space)
    env.seed(720)
    # Start Minecraft by resetting the environment
    obs = env.reset()
    print("")
    print(obs)

    # Create the model and pass it to MineRL agent
    model = Adam((64, 64, 3), 11)
    agent = Agent(model, obs)

    # Load the weights from the given path and gather some wood acting in the overground mode
    agent.load_brain("weights/adam-v2.2/adam-v2.2.ckpt")
    agent.gather_items('log', LOGS_TO_CHOP, env, OVERGROUND_MODE)

    # Perform the actions below and acquire a wooden pickaxe
    # Then rotate the camera to look at the ground and prepare the area for mining
    craft_wooden_pickaxe = normalize_actions(CRAFT_WOODEN_PICKAXE, env)
    mine_down = normalize_actions(MINE_DOWN, env)
    agent.carry_out(craft_wooden_pickaxe + mine_down, env)

    agent.load_brain("weights/adam-v2.2.0/adam-v2.2.0.ckpt")
    agent.gather_items('cobblestone', COBBLESTONE_TO_MINE, env, UNDERGROUND_MODE)

    # Craft a stone pickaxe and a furnace. Prepare for mining iron ore.
    craft_stone_pickaxe = normalize_actions(CRAFT_STONE_PICKAXE, env)
    craft_furnace = normalize_actions(CRAFT_FURNACE, env)
    agent.carry_out(craft_stone_pickaxe + craft_furnace, env)

    # After the bot acquired some torches to light up the territory it is time to find some iron ore.
    agent.gather_items('iron_ore', IRON_TO_MINE, env, UNDERGROUND_MODE)

    print(agent.obs['inventory'])


if __name__ == '__main__':
    main()
