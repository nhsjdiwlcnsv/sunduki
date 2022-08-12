VERTICAL_ANGLE = 4.5
HORIZONTAL_ANGLE = 7.5

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
]  # 14

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

        [('left', 1)],
        [('right', 1)],
        [('back', 1)],
]  # 16
