from constants.limits import *


# Actions in this file are represented as dictionaries, where key is an action itself, and its value is another dictionary.
# This very dictionary that represents the value of the action has the objective of the action as a key,
# and for the value it has the number of times the action should be executed.

# These action cannot be performed by the neural network, so they are not included in action modes and are being executed
# manually by the bot using an unwrapped version of the env.

# For example, placing specific blocks (except torches) is not supported by the neural network.
def place(block, optional=None) -> dict:
    return {
        **(optional if optional else {}),
        'jump': {'1': 15},
        'place': {block: 1},
    }


# Crafting actions are nearly the most important ones in the entire project, so they must be implemented
# by the human, not the CNN.
def craft_on_crafting_table(item, quant=1, equip=False, optional=None) -> dict:
    return {
        **(optional if optional else {}),
        **PLACE_CRAFTING_TABLE,
        'nearbyCraft': {item: quant},
        **REMOVE_CRAFTING_TABLE,
        'equip': {item: 1} if equip else {},
    }


# It is fair for digging in specific directions as well. Here, the function takes the amount of steps
# as an argument and digs down for the given amount of steps.
def dig_down(steps) -> dict:
    return {
        # Camera action value is generally a list where the first element is a vertical angle, and the second is a horizontal angle.
        # To move the camera down the angle must be positive.
        'camera': {'[180, 0]': 1},
        'attack': {'1': steps},
    }


CRAFT_BASIC_TOOLS = {
    'craft': {
        'planks': LOGS_TO_CHOP,
        'stick': STICKS_QUANT,
        'torch': TORCHES_QUANT,
        'crafting_table': 1
    },
}

REMOVE_CRAFTING_TABLE = dig_down(150)
REMOVE_BLOCK = dig_down(20)
MINE_DOWN = dig_down(500)

PLACE_CRAFTING_TABLE = place('crafting_table', REMOVE_BLOCK)
PLACE_FURNACE = place('furnace', REMOVE_BLOCK)

# Before crafting any pickaxes, the bot must craft planks, sticks, torches, and crafting table itself.
# After that, the bot can craft a wooden pickaxe and then, after obtaining 17 cobblestone, it will craft
# 3 stone pickaxes and 1 furnace.
# equip=True means that the item will be equipped after crafting.
# quant means the number of times the item will be crafted.
CRAFT_W_PICKAXE = craft_on_crafting_table('wooden_pickaxe', equip=True, optional=CRAFT_BASIC_TOOLS)
CRAFT_S_PICKAXE = craft_on_crafting_table('stone_pickaxe', equip=True, quant=S_PICKAXES_QUANT)
CRAFT_I_PICKAXE = craft_on_crafting_table('iron_pickaxe', equip=True, quant=2)
CRAFT_FURNACE = craft_on_crafting_table('furnace')

MINE_STRAIGHT = {
    'camera': {
        '[180, 0]': 1,
        '[-90, 0]': 1,
    },
    'attack': {'1': 60},
}

SMELT_IRON = {
    **PLACE_FURNACE,
    'nearbySmelt': {'iron_ingot': IRON_TO_MINE},
    **REMOVE_BLOCK
}
