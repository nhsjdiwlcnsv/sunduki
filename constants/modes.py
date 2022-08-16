from enum import Enum


# Angles for rotating the camera that are used in below function.
VERTICAL_ANGLE = 6
HORIZONTAL_ANGLE = 9


# There are two modes that define the actions the bot can take during the session: overground and underground.
# In the overground mode the bot can only chop trees and in the underground mode the bot can only perform mining actions.
# There is also a third mode that is used to perform the actions for which the neural network doesn't fit. Crafting, for instance.
class Modes(Enum):
    overground = 'overground'
    underground = 'underground'


# The function below returns an array of actions depending on the mode. It is reasonable to use sprinting and jumping in the overground mode,
# but in the underground mode it is better to use such actions as placing torches, for example.
def form_mode(mode: Modes):
    return [
        [('attack', 1)],

        [('forward', 1)],
        [('forward', 1), ('jump', 1)],
        [('forward', 1), ('attack', 1)],
        [('forward', 1), ('jump', 1), ('sprint', 1)] if mode == Modes.overground else [('place', 'torch')],

        [('camera', [0, -HORIZONTAL_ANGLE])],
        [('camera', [0, HORIZONTAL_ANGLE])],
        [('camera', [-VERTICAL_ANGLE, 0])],
        [('camera', [VERTICAL_ANGLE, 0])],

        [('camera', [-VERTICAL_ANGLE, 0]), ('attack', 1)],
        [('camera', [VERTICAL_ANGLE, 0]), ('attack', 1)],

        [('camera', [0, -HORIZONTAL_ANGLE]), ('forward', 1)],
        [('camera', [0, HORIZONTAL_ANGLE]), ('forward', 1)],

        [('back', 1)],
    ] + ([[('left', 1)], [('right', 1)]] if mode == Modes.underground else [])


OVERGROUND_MODE = form_mode(Modes.overground)
UNDERGROUND_MODE = form_mode(Modes.underground)
