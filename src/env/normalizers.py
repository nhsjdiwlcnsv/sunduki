import numpy as np
import re


# This function gets the gym.spaces.Dict of actions and returns a numpy array of active actions during each step
# Each element of the array is a number that corresponds to the index of the action in the action space
def numerize_actions(actions, batch_size, vertical_padding=5, horizontal_padding=5):
    camera = actions["camera"].squeeze()
    attack = actions["attack"].squeeze()
    forward = actions["forward"].squeeze()
    back = actions["sneak"].squeeze()
    sprint = actions["sprint"].squeeze() if "sprint" in actions else np.zeros(batch_size)
    sneak = actions["sneak"].squeeze() if "sneak" in actions else np.zeros(batch_size)
    place = actions["place"].squeeze() if "place" in actions else np.zeros(batch_size)
    left = actions["left"].squeeze()
    right = actions["right"].squeeze()
    jump = actions["jump"].squeeze()

    actions = np.zeros((batch_size,), dtype=np.int64)

    for i in range(len(camera)):
        if camera[i][1] < -vertical_padding:
            actions[i] = 0
        elif camera[i][1] > vertical_padding:
            actions[i] = 1
        elif camera[i][0] < -horizontal_padding:
            actions[i] = 2
        elif camera[i][0] > horizontal_padding:
            actions[i] = 3

        elif place[i] == "torch":
            actions[i] = 5

        elif jump[i] and forward[i]:
            if sprint[i]:
                actions[i] = 5
            else:
                actions[i] = 6

        elif forward[i]:
            actions[i] = 4

        elif back[i] or sneak[i]:
            actions[i] = 1
        elif left[i]:
            actions[i] = 2
        elif right[i]:
            actions[i] = 3

        # Attacking has the lowest priority
        elif attack[i]:
            actions[i] = 0

        else:
            # No reasonable mapping (will be ignored after applying a mask)
            actions[i] = -1

    return actions


# This function gets an array of actions and returns a normalized (for the unwrapped env) sequence of action samples
# where each action sample is a dictionary of actions with only one active action
def normalize_actions(action_array, env):
    action_sequence = []

    for item in action_array:
        act, obj = item.split(':')
        action_sample = env.action_space.noop()

        if obj.isnumeric() or re.search("^\[.*]$", obj):
            obj = eval(obj)

        for action in action_sample:
            if action == act:
                action_sample[action] = obj

        action_sequence.append(action_sample)

    return action_sequence
