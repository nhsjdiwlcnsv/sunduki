import minerl
import gym
import numpy as np

from model.Adam import Adam
from wrappers.OvergroundActionShaper import OvergroundActionShaper
from wrappers.Unwrapped import normalize_actions


def main():
    model = Adam((64, 64, 3), 11)

    model.summary()
    model.compile()

    # Load the model's weights
    model.load_weights("weights/adam-v2.2/adam-v2.2.ckpt")

    # Use the model to chop trees
    env = gym.make('MineRLObtainDiamond-v0')
    env = OvergroundActionShaper(env)
    env.seed(720)

    # Start Minecraft by resetting the environment
    obs = env.reset()

    # Get the size of the action space and form a list of action indices
    actions_number = env.action_space.n
    action_list = np.arange(actions_number)

    while obs['inventory']['log'] < 5:
        env.render()

        pov = (obs['pov'].astype(np.float) / 255.0).reshape(1, 64, 64, 3)
        # Call the model to predict the actions given the point of view
        action_probabilities = model(pov)
        # Apply the probabilities to the action list and sample an action
        action = np.random.choice(action_list, p=action_probabilities.numpy().squeeze())

        obs, reward, done, info = env.step(action)

    # Unwrap the environment and craft a wooden pickaxe
    env = env.unwrapped

    action_sequence = normalize_actions([
        'craft:planks',
        'craft:planks',
        'craft:planks',
        'craft:planks',
        'craft:stick',
        'craft:crafting_table',
        'craft:crafting_table',
        'place:crafting_table',
        'place:crafting_table',
        'nearbyCraft:wooden_pickaxe',
        'equip:wooden_pickaxe',
    ], env)

    for action in action_sequence:
        env.render()
        obs, reward, done, info = env.step(action)

    # Once again wrap the environment and prepare for mining. Make a few steps back and rotate the camera to look at the ground.
    env = OvergroundActionShaper(env)

    for step in range(1000):
        env.render()

        if step < 50:
            action = 1
        elif step < 100:
            action = 8
        elif step < 150:
            action = 9
        else:
            action = 0

        obs, reward, done, info = env.step(action)

    print(obs['inventory'])


if __name__ == '__main__':
    main()
