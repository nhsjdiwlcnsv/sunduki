from constants.limits import LOGS_TO_CHOP, COBBLESTONE_TO_MINE

CRAFT_WOODEN_PICKAXE = []
CRAFT_WOODEN_PICKAXE += ['craft:planks'] * LOGS_TO_CHOP
CRAFT_WOODEN_PICKAXE += ['craft:stick'] * round(((LOGS_TO_CHOP * 4) - 7) / 4)
CRAFT_WOODEN_PICKAXE += ['craft:crafting_table']
CRAFT_WOODEN_PICKAXE += ['camera:[180,0]']
CRAFT_WOODEN_PICKAXE += ['forward:1'] * 60
CRAFT_WOODEN_PICKAXE += ['attack:1'] * 20
CRAFT_WOODEN_PICKAXE += ['jump:1'] * 20
CRAFT_WOODEN_PICKAXE += ['place:crafting_table']
CRAFT_WOODEN_PICKAXE += ['craft:wooden_pickaxe']
CRAFT_WOODEN_PICKAXE += ['equip:wooden_pickaxe']

CRAFT_TORCH = []
CRAFT_TORCH += ['craft:torch'] * 2
CRAFT_TORCH += ['attack:1'] * 20

MINE_DOWN = []
MINE_DOWN += ['attack:1'] * 500

CRAFT_STONE_PICKAXE = []
CRAFT_STONE_PICKAXE += ['camera:[180,0]']
CRAFT_STONE_PICKAXE += ['jump:1'] * 20
CRAFT_STONE_PICKAXE += ['place:crafting_table']
CRAFT_STONE_PICKAXE += ['craft:stone_pickaxe'] * round((COBBLESTONE_TO_MINE - 8) / 3)
CRAFT_STONE_PICKAXE += ['equip:stone_pickaxe']

CRAFT_FURNACE = []
CRAFT_FURNACE += ['craft:furnace']
