from constants.limits import *


def place(block, optional=None) -> dict:
    return {
        **(optional if optional else {}),
        'jump': {'1': 10},
        'place': {block: 1},
    }


def craft_on_crafting_table(item, optional=None) -> dict:
    return {
        **(optional if optional else {}),
        **PLACE_CRAFTING_TABLE,
        'nearbyCraft': {item: 1},
        **REMOVE_BLOCK,
        'equip': {item: 1} if item != 'furnace' else {},
    }


def dig_down(steps) -> dict:
    return {
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

REMOVE_BLOCK = dig_down(20)
MINE_DOWN = dig_down(500)

PLACE_CRAFTING_TABLE = place('crafting_table', REMOVE_BLOCK)
PLACE_FURNACE = place('furnace', REMOVE_BLOCK)

CRAFT_W_PICKAXE = craft_on_crafting_table('wooden_pickaxe', CRAFT_BASIC_TOOLS)
CRAFT_S_PICKAXE = craft_on_crafting_table('stone_pickaxe')
CRAFT_FURNACE = craft_on_crafting_table('furnace')
