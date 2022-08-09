OVERGROUND_MODE = [
        [('attack', 1)],
        [('back', 1)],
        [('left', 1)],
        [('right', 1)],
        [('forward', 1)],
        [('forward', 1), ('jump', 1), ('sprint', 1)],
        [('forward', 1), ('jump', 1)],
        [('camera', [-5, 0])],
        [('camera', [7.5, 0])],
        [('camera', [0, 5])],
        [('camera', [0, -5])],
]

UNDERGROUND_MODE = [
        [('attack', 1)],
        [('sneak', 1)],
        [('left', 1)],
        [('right', 1)],
        [('forward', 1)],
        [('place', 'torch')],
        [('forward', 1), ('jump', 1)],
        [('camera', [-2.5, 0])],
        [('camera', [5, 0])],
        [('camera', [0, 2.5])],
        [('camera', [0, -2.5])],
]
