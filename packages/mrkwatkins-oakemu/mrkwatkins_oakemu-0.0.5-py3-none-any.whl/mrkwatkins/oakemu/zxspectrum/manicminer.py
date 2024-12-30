from enum import IntEnum

from MrKWatkins.OakEmu import StateSerializer as DotNetStateSerializer  # noqa
from MrKWatkins.OakEmu.Machines.ZXSpectrum.Games import ManicMiner as DotNetManicMiner  # noqa

from mrkwatkins.oakemu.zxspectrum.game import Game


class ManicMinerAction(IntEnum):
    NONE = 0
    MOVE_LEFT = 1
    MOVE_RIGHT = 2
    JUMP_UP = 3
    JUMP_LEFT = 4
    JUMP_RIGHT = 5


class ManicMiner(Game):
    def __init__(self):
        self._manic_miner = DotNetManicMiner()
        super().__init__(self._manic_miner, ManicMinerAction)

    @property
    def cavern(self) -> int:
        return self._manic_miner.Cavern

    @cavern.setter
    def cavern(self, value: int):
        self._manic_miner.Cavern = value

    @property
    def cavern_name(self) -> str:
        return self._manic_miner.CavernName

    @property
    def lives(self) -> int:
        return self._manic_miner.Lives

    @lives.setter
    def lives(self, value: int):
        self._manic_miner.Lives = value

    @property
    def air_supply(self) -> int:
        return int(self._manic_miner.AirSupply)

    def start_episode(self, cavern: int = 0) -> None:
        self._game.StartEpisode(cavern)

    def __getstate__(self):
        state = {
            "_manic_miner": bytes(DotNetStateSerializer.Save(self._manic_miner)),
        }
        return state

    def __setstate__(self, state):
        self._manic_miner = DotNetManicMiner()
        DotNetStateSerializer.Restore[DotNetManicMiner](self._manic_miner, state["_manic_miner"])

        super().__init__(self._manic_miner, ManicMinerAction, False)
