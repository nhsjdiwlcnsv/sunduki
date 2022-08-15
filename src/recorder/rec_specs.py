from src.env.env_specs import CustomMineRLEnv
from minerl.herobraine.hero.handler import Handler
from typing import List
from abc import ABC

import minerl.herobraine.hero.handlers as handlers

REC_DOC = """
    This env is just a higher resolution version of the CustomMineRLEnv
    that allows us to record bot's progress.
    """

REC_LENGTH = 150000

none = 'none'
other = 'other'


class RecorderEnv(CustomMineRLEnv, ABC):
    def __init__(self, *args, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = 'RecorderEnv-v0'

        super().__init__(*args, **kwargs)

    def create_observables(self) -> List[Handler]:
        return [
            handlers.FlatInventoryObservation([
                'dirt',
                'coal',
                'torch',
                'log',
                'planks',
                'stick',
                'crafting_table',
                'wooden_pickaxe',
                'stone',
                'cobblestone',
                'furnace',
                'stone_pickaxe',
                'iron_ore',
                'iron_ingot',
                'iron_pickaxe'
            ]),
            handlers.EquippedItemObservation(
                ['air', 'wooden_pickaxe', 'stone_pickaxe', 'iron_pickaxe', none, other],
                _default='air',
                _other=other
            ),
            handlers.POVObservation((360, 360)),
            handlers.CompassObservation(),
            handlers.ObservationFromCurrentLocation()
        ]

    def create_server_quit_producers(self):
        return []

    def create_server_decorators(self) -> List[Handler]:
        return []

    # the episode can terminate when this is True
    def determine_success_from_rewards(self, rewards: list) -> bool:
        return sum(rewards) >= self.reward_threshold

    def is_from_folder(self, folder: str) -> bool:
        return folder == 'env'

    def get_docstring(self):
        return RecorderEnv

