from constants.limits import *


def place(block, optional=None) -> dict:
    return {
        **(optional if optional else {}),
        'jump': {'1': 15},
        'place': {block: 1},
    }


def craft_on_crafting_table(item, quant=1, equip=False, optional=None) -> dict:
    return {
        **(optional if optional else {}),
        **PLACE_CRAFTING_TABLE,
        'nearbyCraft': {item: quant},
        **REMOVE_CRAFTING_TABLE,
        'equip': {item: 1} if equip else {},
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

REMOVE_CRAFTING_TABLE = dig_down(100)
REMOVE_BLOCK = dig_down(20)
MINE_DOWN = dig_down(350)

PLACE_CRAFTING_TABLE = place('crafting_table', REMOVE_BLOCK)
PLACE_FURNACE = place('furnace', REMOVE_BLOCK)

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
