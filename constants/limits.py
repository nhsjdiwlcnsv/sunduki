import math

# Natural limits defined in empirical tests. For example, the bot must chop 5 logs which is 20 planks.
# 20 planks are converted into 1 crafting table, 1 wooden pickaxe, and the rest is used for sticks.
LOGS_TO_CHOP = 5
# Cobblestone is only used for crafting 3 stone pickaxes (which is 3*3=9 cobblestone)
# and 1 furnace (which is 8 cobblestone).
COBBLESTONE_TO_MINE = 17
# Iron is only used for crafting 1 iron pickaxe. The only iron pickaxe will be later used for mining diamonds.
IRON_TO_MINE = 3

# The number of sticks is calculated as follows:
STICKS_QUANT = math.floor(((LOGS_TO_CHOP * 4) - 7) / 4)
# The number of stone pickaxes is calculated as follows:
S_PICKAXES_QUANT = math.floor((COBBLESTONE_TO_MINE - 8) / 3)
# The total number of coal in bot's starting inventory is 5, but 1 coal should be left for smelting iron,
# so torches should be crafted 4 times.
TORCHES_QUANT = 4
