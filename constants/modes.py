OVERGROUND_MODE = [
        [('attack', 1)],
        [('back', 1)],
        [('left', 1)],
        [('right', 1)],
        [('forward', 1)],
        [('forward', 1), ('jump', 1), ('sprint', 1)],
        [('forward', 1), ('jump', 1)],
        [('camera', [-20, 0])],
        [('camera', [20, 0])],
        [('camera', [0, 7.5])],
        [('camera', [0, -7.5])],
]

UNDERGROUND_MODE = [
        [('attack', 1)],
        [('sneak', 1)],
        [('left', 1)],
        [('right', 1)],
        [('forward', 1)],
        [('forward', 1), ('sneak', 1)],
        [('forward', 1), ('jump', 1)],
        [('camera', [-10, 0])],
        [('camera', [10, 0])],
        [('camera', [0, 5])],
        [('camera', [0, -5])],
]
