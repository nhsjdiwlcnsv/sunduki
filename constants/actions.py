from constants.limits import LOGS_TO_CHOP


CRAFT_WOODEN_PICKAXE = []
CRAFT_WOODEN_PICKAXE += ['craft:planks'] * LOGS_TO_CHOP
CRAFT_WOODEN_PICKAXE += ['craft:stick'] * 1
CRAFT_WOODEN_PICKAXE += ['craft:crafting_table'] * 1
CRAFT_WOODEN_PICKAXE += ['place:crafting_table'] * 2
CRAFT_WOODEN_PICKAXE += ['nearbyCraft:wooden_pickaxe']
CRAFT_WOODEN_PICKAXE += ['equip:wooden_pickaxe']

LOOK_DOWN = ['camera:[15,5]'] * 20
