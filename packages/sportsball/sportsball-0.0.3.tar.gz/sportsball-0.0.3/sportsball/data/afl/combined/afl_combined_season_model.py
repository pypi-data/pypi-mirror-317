"""AFL combined season model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Type, Union

from ...combined.combined_game_model import CombinedGameModel
from ...combined.combined_season_model import CombinedSeasonModel
from ..afltables.afl_afltables_season_model import AFLAFLTablesSeasonModel
from .afl_combined_game_model import AFLCombinedGameModel


class AFLCombinedSeasonModel(CombinedSeasonModel):
    """The class implementing the AFL combined season model."""

    @classmethod
    def _combined_game_model_class(cls) -> Type[CombinedGameModel]:
        return AFLCombinedGameModel

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **AFLAFLTablesSeasonModel.urls_expire_after(),
            **AFLCombinedGameModel.urls_expire_after(),
        }
