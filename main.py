import minerl
import gym
import numpy as np
import tensorflow as tf

from minerl.data import BufferedBatchIter
from keras import layers, models, optimizers, losses, callbacks


# This function gets the dictionary of actions and returns a numpy array of active actions during each step
def normalize_actions(actions, batch_size):
    camera_actions = actions["camera"].squeeze()
    forward_actions = actions["forward"].squeeze()
    jump_actions = actions["jump"].squeeze()
    attack_actions = actions["attack"].squeeze()

    # List of all actions (numpy array) for the batch
    action_batch = np.zeros((batch_size,), dtype=np.int)

    # Enumerate all actions in the batch according to their priority
    for i in range(batch_size):
        if camera_actions[i][0] < 0:
            action_batch[i] = 4
        elif camera_actions[i][0] > 0:
            action_batch[i] = 5
        elif camera_actions[i][1] > 0:
            action_batch[i] = 6
        elif camera_actions[i][1] < 0:
            action_batch[i] = 7
        elif attack_actions[i] == 1:
            action_batch[i] = 1
        elif forward_actions[i] == 1:
            if jump_actions[i] == 0:
                action_batch[i] = 1
            else:
                action_batch[i] = 2
        elif jump_actions[i] == 1:
            action_batch[i] = 3
        else:
            action_batch[i] = -1

    return action_batch


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
        layers.Dense(units=8, activation='softmax')
    ])

    model.summary()

    # Model's parameters
    optimizer = optimizers.Adam(learning_rate=1e-3)  # How fast the model learns
    loss = losses.SparseCategoricalCrossentropy(from_logits=True)  # How to calculate the loss
    training_metrics = ['accuracy']  # What metrics to track during training

    # Data loader
    data = minerl.data.make('MineRLObtainDiamond-v0')
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
    model.save_weights('./weights/adam-v0')

    # Use the model to fucking predict the actions
    env = gym.make('MineRLObtainDiamond-v0')


if __name__ == '__main__':
    main()
