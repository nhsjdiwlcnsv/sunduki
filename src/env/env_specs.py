from minerl.herobraine.env_specs.simple_embodiment import SimpleEmbodimentEnvSpec
from minerl.herobraine.hero.handler import Handler
from typing import List
from abc import ABC

import minerl.herobraine.hero.handlers as handlers

ENV_DOC = """
    The environment is a simple embodiment of the hero's actions.
    The hero is able to move around in the environment and pick up items.
    """

ENV_LENGTH = 150000

none = 'none'
other = 'other'


class CustomMineRLEnv(SimpleEmbodimentEnvSpec, ABC):
    def __init__(self, *args, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = 'CustomMineRLEnv-v0'

        super().__init__(*args, max_episode_steps=ENV_LENGTH, reward_threshold=100.0, **kwargs)

    def create_server_world_generators(self) -> List[Handler]:
        return [handlers.DefaultWorldGenerator()]

    def create_agent_start(self) -> List[Handler]:
        return [handlers.SimpleInventoryAgentStart([dict(type="coal", quantity=5)])]

    def create_rewardables(self) -> List[Handler]:
        return [
            handlers.RewardForCollectingItemsOnce([
                dict(type="log", amount=1, reward=1),
                dict(type="planks", amount=1, reward=2),
                dict(type="stick", amount=1, reward=4),
                dict(type="crafting_table", amount=1, reward=4),
                dict(type="wooden_pickaxe", amount=1, reward=8),
                dict(type="cobblestone", amount=1, reward=16),
                dict(type="furnace", amount=1, reward=32),
                dict(type="stone_pickaxe", amount=1, reward=32),
                dict(type="iron_ore", amount=1, reward=64),
                dict(type="iron_ingot", amount=1, reward=128),
                dict(type="iron_pickaxe", amount=1, reward=256),
                dict(type="diamond", amount=1, reward=1024)
            ]),
        ]

    def create_agent_handlers(self) -> List[Handler]:
        return [handlers.AgentQuitFromPossessingItem([dict(type="diamond", amount=1)])]

    def create_actionables(self) -> List[Handler]:
        return super().create_actionables() + [
            handlers.PlaceBlock([none, 'dirt', 'stone', 'cobblestone', 'crafting_table', 'furnace', 'torch'], _other=none, _default=none),
            handlers.EquipAction([none, 'air', 'wooden_pickaxe', 'stone_pickaxe', 'iron_pickaxe'], _other=none, _default=none),
            handlers.CraftAction([none, 'torch', 'stick', 'planks', 'crafting_table'], _other=none, _default=none),
            handlers.CraftNearbyAction([none, 'wooden_pickaxe', 'stone_pickaxe', 'iron_pickaxe', 'furnace'], _other=none, _default=none),
            handlers.SmeltItemNearby([none, 'iron_ingot', 'coal'], _other=none, _default=none),
        ]

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
            handlers.POVObservation((64, 64)),
            handlers.CompassObservation(),
            handlers.ObservationFromCurrentLocation()
        ]

    def create_server_initial_conditions(self) -> List[Handler]:
        return [
            handlers.TimeInitialCondition(True, 0),
            handlers.SpawningInitialCondition(False),
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
        return CustomMineRLEnv

