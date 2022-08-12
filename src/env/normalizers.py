import numpy as np
import re


# This function gets the gym.spaces.Dict of actions and returns a numpy array of active actions during each step
# Each element of the array is a number that corresponds to the index of the action in the action space
def numerize_actions(actions, batch_size, vertical_padding=9, horizontal_padding=7.5) -> np.ndarray:
    camera = actions["camera"].squeeze()
    attack = actions["attack"].squeeze()
    forward = actions["forward"].squeeze()
    back = actions["back"].squeeze() if "back" in actions else np.zeros(batch_size)
    sprint = actions["sprint"].squeeze() if "sprint" in actions else np.zeros(batch_size)
    place = actions["place"].squeeze() if "place" in actions else np.zeros(batch_size)
    left = actions["left"].squeeze() if "left" in actions else np.zeros(batch_size)
    right = actions["right"].squeeze() if "right" in actions else np.zeros(batch_size)
    jump = actions["jump"].squeeze()

    numerized_actions = np.zeros((batch_size,), dtype=np.int64)

    for i in range(batch_size):
        if camera[i][0] <= -horizontal_padding:
            numerized_actions[i] = 9 if attack[i] else 5
        elif camera[i][0] >= horizontal_padding:
            numerized_actions[i] = 10 if attack[i] else 6
        elif camera[i][1] <= -vertical_padding:
            numerized_actions[i] = 11 if forward[i] else 7
        elif camera[i][1] >= vertical_padding:
            numerized_actions[i] = 12 if forward[i] else 8

        elif forward[i] and jump[i]:
            numerized_actions[i] = 4 if sprint[i] else 2

        elif forward[i]:
            numerized_actions[i] = 3 if attack[i] else 1

        elif place[i] == "torch":
            numerized_actions[i] = 4

        elif attack[i]:
            numerized_actions[i] = 0

        elif left[i]:
            numerized_actions[i] = 13
        elif right[i]:
            numerized_actions[i] = 14
        elif back[i]:
            numerized_actions[i] = 15

        else:
            numerized_actions[i] = -1

    return numerized_actions


# This function gets an array of actions and returns a normalized (for the unwrapped env) sequence of action samples
# where each action sample is a dictionary of actions with only one active action
def normalize_actions(actions, env) -> list:
    action_sequence = []

    for action in actions:
        for obj, quantity in actions[action].items():
            action_sample = env.action_space.noop()

            if obj.isnumeric() or re.search("^\[.*]$", obj):
                obj = eval(obj)

            action_sample["craft" if action == "nearbyCraft" else action] = obj
            action_sequence += [action_sample for _ in range(quantity)]

    return action_sequence
