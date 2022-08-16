from src.env.env_specs import CustomMineRLEnv
from minerl.herobraine.hero.handler import Handler
from typing import List
from abc import ABC

import minerl.herobraine.hero.handlers as handlers


class RecorderEnv(CustomMineRLEnv, ABC):
    def __init__(self, *args, **kwargs):
        if 'name' not in kwargs:
            kwargs['name'] = 'RecorderEnv-v0'

        super().__init__(*args, **kwargs)

    def create_observables(self) -> List[Handler]:
        return [handlers.POVObservation((240, 240))]

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

