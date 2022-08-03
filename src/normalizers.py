import numpy as np
import re


# This function gets the gym.spaces.Dict of actions and returns a numpy array of active actions during each step
# Each element of the array is a number that corresponds to the index of the action in the action space
def numerize_actions(actions, batch_size, vertical_padding=7.5, horizontal_padding=5):
    camera_actions = actions["camera"].squeeze()
    attack_actions = actions["attack"].squeeze()
    forward_actions = actions["forward"].squeeze()
    sprint_actions = actions["sprint"].squeeze()
    back_actions = actions["back"].squeeze()
    left_actions = actions["left"].squeeze()
    right_actions = actions["right"].squeeze()
    jump_actions = actions["jump"].squeeze()

    actions = np.zeros((batch_size,), dtype=np.int4)

    for i in range(len(camera_actions)):
        # Moving camera has the highest priority
        if camera_actions[i][0] < -horizontal_padding:
            actions[i] = 7
        elif camera_actions[i][0] > horizontal_padding:
            actions[i] = 8
        elif camera_actions[i][1] > vertical_padding:
            actions[i] = 9
        elif camera_actions[i][1] < -vertical_padding:
            actions[i] = 10

        # Then jump with/without moving forward
        elif jump_actions[i] and forward_actions[i]:
            if sprint_actions[i]:
                actions[i] = 5
            else:
                actions[i] = 6

        # Just move forward if there is no jumping action
        elif forward_actions[i]:
            actions[i] = 4

        # Then other navigation actions
        elif back_actions[i]:
            actions[i] = 1
        elif left_actions[i]:
            actions[i] = 2
        elif right_actions[i]:
            actions[i] = 3

        # Attacking has the lowest priority
        elif attack_actions[i]:
            actions[i] = 0
        else:
            # No reasonable mapping (will be ignored after applying a mask)
            actions[i] = -1

    return actions


# This function gets an array of actions and returns a normalized (for the unwrapped env) sequence of action samples
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
