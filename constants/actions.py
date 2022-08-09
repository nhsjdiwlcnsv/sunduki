from constants.limits import LOGS_TO_CHOP, COBBLESTONE_TO_MINE

CRAFT_WOODEN_PICKAXE = []
CRAFT_WOODEN_PICKAXE += ['craft:planks'] * LOGS_TO_CHOP
CRAFT_WOODEN_PICKAXE += ['craft:stick'] * round(((LOGS_TO_CHOP * 4) - 7) / 4)
CRAFT_WOODEN_PICKAXE += ['craft:crafting_table']
CRAFT_WOODEN_PICKAXE += ['camera:[180,0]']
CRAFT_WOODEN_PICKAXE += ['attack:1'] * 80
CRAFT_WOODEN_PICKAXE += ['jump:1'] * 20
CRAFT_WOODEN_PICKAXE += ['place:crafting_table']
CRAFT_WOODEN_PICKAXE += ['craft:wooden_pickaxe']
CRAFT_WOODEN_PICKAXE += ['equip:wooden_pickaxe']

MINE_DOWN = []
MINE_DOWN += ['camera:[-180,0]']
MINE_DOWN += ['attack:1'] * 250
MINE_DOWN += ['camera:[90,0]']
MINE_DOWN += ['attack:1'] * 250

CRAFT_STONE_PICKAXE = []
CRAFT_STONE_PICKAXE += ['camera:[180,0]']
CRAFT_STONE_PICKAXE += ['jump:1'] * 20
CRAFT_STONE_PICKAXE += ['place:crafting_table']
CRAFT_STONE_PICKAXE += ['camera:[-1,0]']
CRAFT_STONE_PICKAXE += ['craft:stone_pickaxe'] * round((COBBLESTONE_TO_MINE - 8) / 3)
CRAFT_STONE_PICKAXE += ['equip:stone_pickaxe']

CRAFT_FURNACE = []
CRAFT_FURNACE += ['nearbyCraft:furnace']
CRAFT_FURNACE += ['camera:[1,0]']
CRAFT_FURNACE += ['attack:1'] * 80
