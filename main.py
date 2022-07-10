from abc import ABC

import minerl
import gym
import numpy as np
import tensorflow as tf

from minerl.data import BufferedBatchIter
from keras import layers, models, optimizers, losses


class ActionShaper(gym.ActionWrapper, ABC):
    def __init__(self, env, camera_angle=20):
        super().__init__(env)

        self.camera_angle = camera_angle
        self.dataset_actions = [
            [('attack', 1)],
            [('forward', 1)],
            [('back', 1)],
            [('left', 1)],
            [('right', 1)],
            [('jump', 1)],
            [('forward', 1), ('jump', 1)],
            # [('forward', 1), ('attack', 1)],
            [('camera', [-self.camera_angle, 0])],
            [('camera', [self.camera_angle, 0])],
            [('camera', [0, self.camera_angle])],
            [('camera', [0, -self.camera_angle])],
        ]

        self.actions = []
        for actions in self.dataset_actions:
            act = self.env.action_space.noop()
            for a, v in actions:
                act[a] = v

            self.actions.append(act)

        self.action_space = gym.spaces.Discrete(len(self.actions))

    def action(self, action):
        return self.actions[action]


# This function gets the dictionary of actions and returns a numpy array of active actions during each step
def normalize_actions(actions, batch_size):
    camera_actions = actions["camera"].squeeze()
    attack_actions = actions["attack"].squeeze()
    forward_actions = actions["forward"].squeeze()
    back_actions = actions["back"].squeeze()
    left_actions = actions["left"].squeeze()
    right_actions = actions["right"].squeeze()
    jump_actions = actions["jump"].squeeze()
    batch_size = len(camera_actions)
    actions = np.zeros((batch_size,), dtype=np.int)

    for i in range(len(camera_actions)):
        # Moving camera has the highest priority
        if camera_actions[i][0] < -5:
            actions[i] = 7
        elif camera_actions[i][0] > 5:
            actions[i] = 8
        elif camera_actions[i][1] > 5:
            actions[i] = 9
        elif camera_actions[i][1] < -5:
            actions[i] = 10

        # Then moving forward with/without jump
        elif forward_actions[i] == 1:
            if jump_actions[i] == 1:
                actions[i] = 6
            else:
                actions[i] = 1

        # Then other navigation actions
        elif back_actions[i] == 1:
            actions[i] = 2
        elif left_actions[i] == 1:
            actions[i] = 3
        elif right_actions[i] == 1:
            actions[i] = 4

        elif jump_actions[i] == 1:
            actions[i] = 5

        # Attacking has the lowest priority
        elif attack_actions[i] == 1:
            actions[i] = 0
        else:
            # No reasonable mapping (will be ignored after applying a mask)
            actions[i] = -1
    return actions


# Тут допущена ошибка. Правильно было бы написать "deaf main", что означало бы, что главный глухой.
def main():
    model = models.Sequential([

        # First convolutional layer
        layers.Conv2D(filters=64, kernel_size=(5, 5), activation='relu', input_shape=(64, 64, 3)),
        layers.MaxPooling2D((2, 2)),

        # Second convolutional layer
        layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),

        # Third convolutional layer
        layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),

        layers.Flatten(),
        layers.Dense(units=1024, activation='relu'),
        layers.Dense(units=11, activation='softmax')
    ])

    model.summary()

    # Model's parameters
    optimizer = optimizers.Adam(learning_rate=1e-3)  # How fast the model learns
    loss = losses.SparseCategoricalCrossentropy(from_logits=True)  # How to calculate the loss
    training_metrics = ['accuracy']  # What metrics to track during training

    data = minerl.data.make('MineRLTreechop-v0')
    iterator = BufferedBatchIter(data)

    model.compile(optimizer=optimizer, loss=loss, metrics=training_metrics)

    # While iterating through the data, iterator feeds the model with the batches of data in order to train it
    for state, actions, reward, next_state, done in iterator.buffered_batch_iter(batch_size=16384, num_batches=5):
        obs = state['pov'].squeeze().astype(np.float) / 255.0
        actions = normalize_actions(actions, len(obs))

        # Apply the mask to the observations and actions to make sure the model only sees the relevant data
        mask = actions != -1
        actions = actions[mask]
        obs = obs[mask]

        model.fit(obs, actions, batch_size=256, epochs=10, verbose=1)

        print("")

    # Save the model's weights
    # model.save_weights('./weights/adam-v0')

    # Use the model to fucking predict the actions
    env = gym.make('MineRLObtainDiamond-v0')
    env = ActionShaper(env)

    obs = env.reset()

    total_reward = 0
    actions_number = env.action_space.n
    action_list = np.arange(actions_number)

    for step in range(18000):
        env.render()

        pov = (obs['pov'].squeeze().astype(np.float) / 255.0).reshape((1, 64, 64, 3))
        action_probabilities = model(pov, training=False)

        action = np.random.choice(action_list, p=action_probabilities.numpy()[0])

        obs, reward, done, info = env.step(action)
        total_reward += reward

        print("Step: {} Reward: {}".format(step, total_reward))
        print("")
        print("Inventory:", obs['inventory']['logs'])

        if done:
            break

    print("Total reward:", total_reward)


if __name__ == '__main__':
    main()
