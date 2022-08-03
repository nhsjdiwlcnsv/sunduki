from constants.limits import LOGS_TO_CHOP, COBBLESTONE_TO_MINE

CRAFT_WOODEN_PICKAXE = []
CRAFT_WOODEN_PICKAXE += ['craft:planks'] * (LOGS_TO_CHOP - 1)
CRAFT_WOODEN_PICKAXE += ['craft:stick'] * 3
CRAFT_WOODEN_PICKAXE += ['craft:crafting_table'] * 2
CRAFT_WOODEN_PICKAXE += ['place:crafting_table'] * 2
CRAFT_WOODEN_PICKAXE += ['nearbyCraft:wooden_pickaxe']
CRAFT_WOODEN_PICKAXE += ['equip:wooden_pickaxe']

LOOK_DOWN = []
LOOK_DOWN += ['camera:[15,0]'] * 30

CRAFT_STONE_PICKAXE = []
CRAFT_STONE_PICKAXE += ['jump:1'] * 20
CRAFT_STONE_PICKAXE += ['place:crafting_table'] * 2
CRAFT_STONE_PICKAXE += ['camera:[-1,0]']
CRAFT_STONE_PICKAXE += ['nearbyCraft:stone_pickaxe'] * 2
CRAFT_STONE_PICKAXE += ['equip:stone_pickaxe']

CRAFT_FURNACE = []
CRAFT_FURNACE += ['nearbyCraft:furnace']
CRAFT_FURNACE += ['camera:[1,0]']
CRAFT_FURNACE += ['attack:1'] * 20

CRAFT_TORCH = []
CRAFT_TORCH += ['jump:1'] * 20
CRAFT_TORCH += ['place:furnace'] * 2
CRAFT_TORCH += ['camera:[72,91]']
CRAFT_TORCH += ['nearbySmelt:coal']
CRAFT_TORCH += ['craft:torch']