import os
import minerl
import numpy as np
import tensorflow as tf

from minerl.data import BufferedBatchIter
from keras import layers, optimizers, losses
from src.normalizers import numerize_actions


class Adam:
    def __init__(self, input_shape, output_shape):
        # Define the model as a Sequential that takes an array of Keras layers
        self.model = tf.keras.Sequential([
            # First convolutional layer
            layers.Conv2D(filters=64, kernel_size=(5, 5), activation='relu', input_shape=input_shape),  # Performs a 2D convolution over the input.
            layers.MaxPooling2D((2, 2)),  # Reduces the size of the input by a factor of 2. This is useful for downsampling the image.

            # Second convolutional layer
            layers.Conv2D(filters=128, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),

            # Third convolutional layer
            layers.Conv2D(filters=256, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            # Dropout is a regularization technique that randomly drops out units in a neural network. It is used to prevent overfitting.
            # It disables some units in the network with a rate of p. And thus, it generalizes the output.
            layers.Dropout(0.175),

            # Fourth convolutional layer
            layers.Conv2D(filters=512, kernel_size=(3, 3), activation='relu', padding='same'),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(0.15),

            # After performing the convolutional layers, the input is flattened to a 1D array and passed to the dense layers.
            layers.Flatten(),
            layers.Dense(units=1024, activation='relu'),
            layers.Dense(units=output_shape, activation='softmax')
        ])

        # Get model's parameters to compile it with the optimizer and loss function. The metrics are used to track the training progress.
        self.optimizer = optimizers.Adam(1e-3)  # How fast and how accurate the model is trained
        self.loss = losses.SparseCategoricalCrossentropy()  # The loss function used to train the model
        self.training_metrics = ['accuracy']  # The metrics used to track the training progress

    # Call the model to predict the actions given the point of view
    def __call__(self, pov):
        return self.model(pov, training=False)

    # Summarize the model's architecture
    def summary(self):
        self.model.summary()

    def compile(self):
        self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=self.training_metrics)

    def train(self, dataset_name, params, batch_size=16384, num_batches=3):
        # Load the dataset and create a batch iterator
        data = minerl.data.make(dataset_name)
        iterator = BufferedBatchIter(data)

        # Get the checkpoint directory to save the model's weights using callback
        checkpoint_path, checkpoint_dir, cp_callback = params

        # While iterating through the data, iterator feeds the model with the batches of data in order to train it
        for state, actions, _, _, _ in iterator.buffered_batch_iter(batch_size=batch_size, num_batches=num_batches):
            # Normalize both the observations and the actions
            obs = state['pov'].squeeze().astype(np.float) / 255.0
            actions = numerize_actions(actions, len(obs))

            # Apply the mask to the observations and actions to make sure the model only sees the relevant data
            mask = actions != -1
            actions = actions[mask]
            obs = obs[mask]

            self.model.fit(obs, actions, batch_size=256, epochs=10, verbose=1, callbacks=[cp_callback])

            print("")

    # Load the pre-trained model's weights
    def load_weights(self, path):
        checkpoint_dir = os.path.dirname(path)
        latest = tf.train.latest_checkpoint(checkpoint_dir)
        self.model.load_weights(latest)
