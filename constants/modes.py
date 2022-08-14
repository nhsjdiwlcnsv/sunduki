VERTICAL_ANGLE = 6
HORIZONTAL_ANGLE = 9

OVERGROUND_MODE = [
        [('attack', 1)],

        [('forward', 1)],
        [('forward', 1), ('jump', 1)],
        [('forward', 1), ('attack', 1)],
        [('forward', 1), ('jump', 1), ('sprint', 1)],

        [('camera', [0, -HORIZONTAL_ANGLE])],
        [('camera', [0, HORIZONTAL_ANGLE])],
        [('camera', [-VERTICAL_ANGLE, 0])],
        [('camera', [VERTICAL_ANGLE, 0])],

        [('camera', [-VERTICAL_ANGLE, 0]), ('attack', 1)],
        [('camera', [VERTICAL_ANGLE, 0]), ('attack', 1)],

        [('camera', [0, -HORIZONTAL_ANGLE]), ('forward', 1)],
        [('camera', [0, HORIZONTAL_ANGLE]), ('forward', 1)],

        [('back', 1)],
]

UNDERGROUND_MODE = [
        [('attack', 1)],

        [('forward', 1)],
        [('forward', 1), ('jump', 1)],
        [('forward', 1), ('attack', 1)],

        [('place', 'torch')],

        [('camera', [0, -HORIZONTAL_ANGLE])],
        [('camera', [0, HORIZONTAL_ANGLE])],
        [('camera', [-VERTICAL_ANGLE, 0])],
        [('camera', [VERTICAL_ANGLE, 0])],

        [('camera', [0, -HORIZONTAL_ANGLE]), ('attack', 1)],
        [('camera', [0, HORIZONTAL_ANGLE]), ('attack', 1)],

        [('camera', [-VERTICAL_ANGLE, 0]), ('forward', 1)],
        [('camera', [VERTICAL_ANGLE, 0]), ('forward', 1)],

        [('back', 1)],
        [('left', 1)],
        [('right', 1)],
]
