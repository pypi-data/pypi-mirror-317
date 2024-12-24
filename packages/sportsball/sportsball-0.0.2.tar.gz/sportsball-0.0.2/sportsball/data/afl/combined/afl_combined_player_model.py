"""AFL combined player model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

from ...combined.combined_player_model import CombinedPlayerModel
from ..afltables.afl_afltables_player_model import AFLAFLTablesPlayerModel


class AFLCombinedPlayerModel(CombinedPlayerModel):
    """AFL combined implementation of the player model."""

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return {
            **AFLAFLTablesPlayerModel.urls_expire_after(),
        }
