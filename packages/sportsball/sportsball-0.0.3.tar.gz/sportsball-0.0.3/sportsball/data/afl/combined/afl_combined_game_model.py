"""AFL combined game model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Type, Union

from ...combined.combined_game_model import CombinedGameModel
from ...combined.combined_team_model import CombinedTeamModel
from ...combined.combined_venue_model import CombinedVenueModel
from ..afltables.afl_afltables_game_model import AFLAFLTablesGameModel
from .afl_combined_team_model import AFLCombinedTeamModel
from .afl_combined_venue_model import AFLCombinedVenueModel


class AFLCombinedGameModel(CombinedGameModel):
    """AFL combined implementation of the game model."""

    @classmethod
    def _combined_team_model_class(cls) -> Type[CombinedTeamModel]:
        return AFLCombinedTeamModel

    @classmethod
    def _combined_venue_model_class(cls) -> Type[CombinedVenueModel]:
        return AFLCombinedVenueModel

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **AFLAFLTablesGameModel.urls_expire_after(),
            **AFLCombinedTeamModel.urls_expire_after(),
            **AFLCombinedVenueModel.urls_expire_after(),
        }
