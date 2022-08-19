import gym

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
    # TODO #1: Пофиксить функцию gather_items(). Проблема в том, что когда у бота ломается каменная кирка, он, по идее, должен брать новую.
    #       Однако насколько я вижу, он не делает этого по непонятным причинам. Если что, в самой функции есть дофига выводов в консоль,
    #       поэтому сначала запусти ее несколько раз и проверь вообще че да как. К слову, кирка ломается примерно на 11000 шагах, так что
    #       нужно слегка подождать.

    # TODO #2: Пофиксить функцию stand_still(). Я вообще не шарю за то, как с точки зрения координат представить тот факт, что бот стоит
    #          ровно на блоке, а не на стыке двух-трех блоков, поэтому тут все надежды на тебя. Благодаря тому, что у нас теперь кастомный
    #          env, ты можешь чекать координаты бота, а значит и становится на блоки ровно, если я правильно понимаю.

    # TODO #3: Добавить в конец main() код для добычи алмазов. Я бы рекомендовал сначала еще раз заюзать MINE_DOWN (потому что алмазы обычно
    #          ведь на довольно низкой высоте появляются), а затем уже gather_items() с соответствующими аргументами.

    # TODO #4: Использовать излишки угля на факелы. Для того, чтобы переплавить все нужное нам железо для кирки нам нужен лишь один уголь.
    #          Поэтому логичнее всего весь уголь, который бот находит в процессе копания под землей, использовать в крафте факелов. Главное
    #          не забудь, что нам нужны 2 палки на железную кирку и желательно еще 2 доп. палки на каменную кирку, если истратив 3 кирки, бот
    #          не найдет железа.

    # TODO #5: Минимально разобраться с нашей нейронкой и в принципе со сверточными нейронными сетями. Это очень важная таска, потому что вполне
    #          возможно, что я не вижу чего-то, что сможешь увидеть ты в контексте тренировки нейронки. Возможно ты придумаешь лучшее
    #          пространство действий, с которым бот будет гораздо лучше себя показывать. Короче, таска в общей сложности про то, чтобы ты разобрался
    #          с нейронной сетью и попробовал ее перетренировать. Таска хоть и необязательная, но было бы прямо очень круто, если бы тебе удалось
    #          как-то улучшить нейронку. Не забывай сохранять весы в новые папки.

    # TODO #6: Видосы. Нужно пару видосов, где бот находит железо, плавит его и начинает, в общем-то, искать алмазы. Эту таску делать только после
    #          того, как бот будет доделан и желательно перетренерован.

    # Register the environments
    env_data.register_envs()

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
    agent.gather_items('log', LOGS_TO_CHOP, env, OVERGROUND_MODE)
    agent.stand_still(env)

    # Perform the actions below and acquire a wooden pickaxe
    # Then rotate the camera to look at the ground and prepare the area for mining cobblestone
    craft_wooden_pickaxe = normalize_actions(CRAFT_W_PICKAXE, env)
    mine_down = normalize_actions(MINE_DOWN, env)
    agent.carry_out(craft_wooden_pickaxe + mine_down, env)

    # Recreate the model, so it can fit to the new action mode (underground in that specific case)
    # and once again pass it to the agent and load new weights.
    model = Adam((64, 64, 3), 16)
    agent = Agent(model, obs, monitor)

    agent.load_brain("weights/adam-v3.5.1/adam-v3.5.1.ckpt")
    agent.gather_items('cobblestone', COBBLESTONE_TO_MINE, env, UNDERGROUND_MODE)

    # Craft a stone pickaxe and a furnace. Prepare for mining iron ore.
    craft_stone_pickaxe = normalize_actions(CRAFT_S_PICKAXE, env)
    craft_furnace = normalize_actions(CRAFT_FURNACE, env)
    mine_straight = normalize_actions(MINE_STRAIGHT, env)
    agent.carry_out(craft_stone_pickaxe + craft_furnace + mine_straight, env)

    agent.gather_items('iron_ore', IRON_TO_MINE, env, UNDERGROUND_MODE)

    smelt_iron = normalize_actions(SMELT_IRON, env)
    craft_iron_pickaxe = normalize_actions(CRAFT_I_PICKAXE, env)
    agent.carry_out(smelt_iron + craft_iron_pickaxe, env)

    print(agent.obs['inventory'])


if __name__ == '__main__':
    main()
