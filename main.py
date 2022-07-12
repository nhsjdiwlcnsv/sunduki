import os
import minerl
import gym
import numpy as np
import tensorflow as tf

from minerl.data import BufferedBatchIter
from keras import layers, models, optimizers, losses
from abc import ABC


# This class is inherited from the abstract class gym.ActionWrapper that is used to filter out the actions that are not relevant
# for the current environment.
class ActionShaper(gym.ActionWrapper, ABC):
    def __init__(self, env, vertical_camera_angle=7.5, horizontal_camera_angle=20):
        super().__init__(env)

        self.vertical_camera_angle = vertical_camera_angle
        self.horizontal_camera_angle = horizontal_camera_angle
        self.dataset_actions = [
            [('attack', 1)],
            [('back', 1)],
            [('left', 1)],
            [('right', 1)],
            [('forward', 1)],
            [('forward', 1), ('jump', 1), ('sprint', 1)],
            [('forward', 1), ('jump', 1)],
            [('camera', [-self.horizontal_camera_angle, 0])],
            [('camera', [self.horizontal_camera_angle, 0])],
            [('camera', [0, self.vertical_camera_angle])],
            [('camera', [0, -self.vertical_camera_angle])],
        ]

        self.actions = []
        for actions in self.dataset_actions:
            act = self.env.action_space.noop()
            for action, value in actions:
                act[action] = value

            self.actions.append(act)

        self.action_space = gym.spaces.Discrete(len(self.actions))

    def action(self, action):
        return self.actions[action]


# This function gets the dictionary of actions and returns a numpy array of active actions during each step
def normalize_actions(actions, batch_size, vertical_camera_padding=7.5, horizontal_camera_padding=5):
    camera_actions = actions["camera"].squeeze()
    attack_actions = actions["attack"].squeeze()
    forward_actions = actions["forward"].squeeze()
    sprint_actions = actions["sprint"].squeeze()
    back_actions = actions["back"].squeeze()
    left_actions = actions["left"].squeeze()
    right_actions = actions["right"].squeeze()
    jump_actions = actions["jump"].squeeze()

    actions = np.zeros((batch_size,), dtype=np.int)

    for i in range(len(camera_actions)):
        # Moving camera has the highest priority
        if camera_actions[i][0] < -horizontal_camera_padding:
            actions[i] = 7
        elif camera_actions[i][0] > horizontal_camera_padding:
            actions[i] = 8
        elif camera_actions[i][1] > vertical_camera_padding:
            actions[i] = 9
        elif camera_actions[i][1] < -vertical_camera_padding:
            actions[i] = 10

        # Then moving forward with/without jump
        elif jump_actions[i] == 1:
            if forward_actions[i] == 1 and sprint_actions[i] == 1:
                actions[i] = 5
            elif forward_actions[i] == 1 and sprint_actions[i] == 0:
                actions[i] = 6

        elif forward_actions[i] == 1:
            actions[i] = 4

        # Then other navigation actions
        elif back_actions[i] == 1:
            actions[i] = 1
        elif left_actions[i] == 1:
            actions[i] = 2
        elif right_actions[i] == 1:
            actions[i] = 3

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
        layers.Conv2D(filters=64, kernel_size=(5, 5), activation='relu', input_shape=(64, 64, 3)),  # Performs a 2D convolution over the input.
        layers.MaxPooling2D((2, 2)),  # Reduces the size of the input by a factor of 2. This is useful for downsampling the image.

        # Second convolutional layer
        layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),

        # Third convolutional layer
        layers.Conv2D(filters=256, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        # Dropout is a regularization technique that randomly drops out units in a neural network. It is used to prevent overfitting.
        # It disables some units in the network with a rate of p. And thus, it generalizes the output.
        layers.Dropout(0.2),

        # Fourth convolutional layer
        layers.Conv2D(filters=512, kernel_size=(3, 3), activation='relu', padding='same'),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.2),

        # After performing the convolutional layers, the input is flattened to a 1D array and passed to the dense layers.
        layers.Flatten(),
        layers.Dense(units=1024, activation='relu'),
        layers.Dense(units=11, activation='softmax')
    ])

    model.summary()

    # Model's parameters
    optimizer = optimizers.Adam(learning_rate=1e-3)  # How fast the model learns
    loss = losses.SparseCategoricalCrossentropy()  # The loss function
    training_metrics = ['accuracy']  # What metrics to track during training
    checkpoint_path = "weights/adam-v1/adam-v1.ckpt"  # Path to save the weights of the model
    checkpoint_dir = os.path.dirname(checkpoint_path)  # Directory to later load the weights from
    cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_path, save_weights_only=True, verbose=1)

    # Load the MineRLTreechop-v0 dataset and create a batch iterator
    # data = minerl.data.make('MineRLTreechop-v0')
    # iterator = BufferedBatchIter(data)

    model.compile(optimizer=optimizer, loss=loss, metrics=training_metrics)

    # While iterating through the data, iterator feeds the model with the batches of data in order to train it
    # for state, actions, reward, next_state, done in iterator.buffered_batch_iter(batch_size=16384, num_batches=3):
    #     obs = state['pov'].squeeze().astype(np.float) / 255.0
    #     actions = normalize_actions(actions, len(obs))
    #
    #     # Apply the mask to the observations and actions to make sure the model only sees the relevant data
    #     mask = actions != -1
    #     actions = actions[mask]
    #     obs = obs[mask]
    #
    #     model.fit(obs, actions, batch_size=256, epochs=10, verbose=1, callbacks=[cp_callback])
    #
    #     print("")

    # Load the model's weights
    latest = tf.train.latest_checkpoint(checkpoint_dir)
    model.load_weights(latest)

    # Use the model to fucking predict the actions
    env = gym.make('MineRLObtainDiamond-v0')
    reduced_env = ActionShaper(env)

    obs = env.reset()

    actions_number = reduced_env.action_space.n
    action_list = np.arange(actions_number)
    done = False

    while obs['inventory']['log'] <= 10 and not done:
        reduced_env.render()

        pov = (obs['pov'].squeeze().astype(np.float) / 255.0).reshape((1, 64, 64, 3))
        action_probabilities = model(pov, training=False)
        action = np.random.choice(action_list, p=action_probabilities.numpy()[0])

        obs, reward, done, _ = reduced_env.step(action)


if __name__ == '__main__':
    main()
