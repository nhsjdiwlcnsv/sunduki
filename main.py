import gym
import logging
import constants.env as env_data

from src.bot.Adam import Adam
from src.bot.Agent import Agent
from src.recorder.recorder import Recorder
from src.env.normalizers import normalize_actions
from constants.actions import *
from constants.limits import *
from constants.modes import *
from constants.env import SEED


def main():
    # Register the environments
    env_data.register_envs()
    logging.basicConfig(level=logging.DEBUG)

    env = gym.make('CustomMineRLEnv-v0')
    env.seed(SEED)

    # Start Minecraft by resetting the environment
    obs = env.reset()

    # Create the monitor to record videos
    monitor = Recorder(SEED)

    # Create the model and pass it to MineRL agent
    model = Adam((64, 64, 3), 14)
    agent = Agent(model, obs, monitor)

    # Load the weights from the given path and gather some wood acting in the overground mode
    agent.load_brain("weights/adam-v3.5/adam-v3.5.ckpt")
    agent.carry_out(normalize_actions(EQUIP_D_AXE, env), env)
    agent.gather_items('log', LOGS_TO_CHOP, env, OVERGROUND_MODE)
    agent.stand_still(env)

    # Perform the actions below and acquire a wooden pickaxe
    # Then rotate the camera to look at the ground and prepare the area for mining cobblestone
    craft_wooden_pickaxe = normalize_actions(CRAFT_W_PICKAXE, env)
    mine_down = normalize_actions(MINE_DOWN, env)
    place_torch = normalize_actions(PLACE_TORCH, env)
    mine_straight = normalize_actions(MINE_STRAIGHT, env)
    agent.carry_out(craft_wooden_pickaxe + mine_down + place_torch + mine_straight, env)

    # Recreate the model, so it can fit to the new action mode (underground in that specific case)
    # and once again pass it to the agent and load new weights.
    model = Adam((64, 64, 3), 16)
    agent = Agent(model, obs, monitor)

    agent.load_brain("weights/adam-v3.5.1/adam-v3.5.1.ckpt")
    agent.gather_items('cobblestone', COBBLESTONE_TO_MINE, env, UNDERGROUND_MODE)

    # Craft a stone pickaxe and a furnace. Prepare for mining iron ore.
    craft_stone_pickaxe = normalize_actions(CRAFT_S_PICKAXE, env)
    craft_furnace = normalize_actions(CRAFT_FURNACE, env)
    agent.carry_out(craft_stone_pickaxe + craft_furnace, env)
    agent.carry_out(normalize_actions(EQUIP_D_PICKAXE, env), env)

    agent.gather_items('iron_ore', IRON_TO_MINE, env, UNDERGROUND_MODE)

    smelt_iron = normalize_actions(SMELT_IRON, env)
    craft_iron_pickaxe = normalize_actions(CRAFT_I_PICKAXE, env)
    agent.carry_out(smelt_iron + craft_iron_pickaxe, env)

    agent.gather_items('diamond', DIAMONDS_TO_MINE, env, UNDERGROUND_MODE)

    print(agent.obs['inventory'])


if __name__ == '__main__':
    main()
