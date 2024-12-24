"""ESPN odds model."""

import datetime
from typing import Any, Dict, Optional, Pattern, Union

import requests

from ..bookie_model import BookieModel
from ..team_model import OddsModel
from .espn_bookie_model import ESPNBookieModel

MONEYLINE_KEY = "moneyLine"


class ESPNOddsModel(OddsModel):
    """ESPN implementation of the odds model."""

    def __init__(
        self,
        session: requests.Session,
        odds: Dict[str, Any],
        bookie: BookieModel,
    ) -> None:
        super().__init__(session)
        self._odds_val = 0.0
        moneyline = odds[MONEYLINE_KEY]
        if moneyline > 0:
            self._odds_val = (float(moneyline) / 100.0) + 1.0
        elif moneyline < 0:
            self._odds_val = (100.0 / float(abs(moneyline))) + 1.0
        self._bookie = bookie

    @property
    def odds(self) -> float:
        """Return the odds."""
        return self._odds_val

    @property
    def bookie(self) -> BookieModel:
        """Return the bookie."""
        return self._bookie

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return the URL cache rules."""
        return ESPNBookieModel.urls_expire_after()
