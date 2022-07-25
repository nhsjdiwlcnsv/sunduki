# This function gets an array of actions and returns a normalized (for the current env) sequence of action samples
def normalize_actions(action_array, env):
    action_sequence = []

    for item in action_array:
        act = item.split(':')[0]
        obj = item.split(':')[1]
        action_sample = env.action_space.noop()
        odd_actions = ['attack', 'camera', 'forward', 'back', 'left', 'right', 'jump', 'sneak', 'sprint']

        for action in action_sample:
            if action != act and action not in odd_actions:
                action_sample[action] = 'none'
            elif action == act:
                action_sample[action] = obj

        action_sequence.append(action_sample)

    return action_sequence
