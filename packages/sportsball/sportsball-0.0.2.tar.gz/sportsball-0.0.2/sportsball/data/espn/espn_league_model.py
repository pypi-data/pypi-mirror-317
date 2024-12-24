"""ESPN league model."""

import datetime
from typing import Any, Dict, Iterator, Optional, Pattern, Union

import requests

from ..league import League
from ..league_model import LeagueModel
from ..season_model import SeasonModel
from .espn_season_model import ESPNSeasonModel


class ESPNLeagueModel(LeagueModel):
    """ESPN implementation of the league model."""

    def __init__(
        self, start_url: str, league: League, session: requests.Session
    ) -> None:
        super().__init__(league, session)
        self._start_url = start_url

    @property
    def seasons(self) -> Iterator[SeasonModel]:
        page = 1
        while True:
            response = self.session.get(self._start_url + f"&page={page}")
            seasons = response.json()
            for item in seasons["items"]:
                season_response = self.session.get(item["$ref"])
                season_response.raise_for_status()
                season_json = season_response.json()

                for season_item in season_json["types"]["items"]:
                    season_type_response = self.session.get(season_item["$ref"])
                    season_type_response.raise_for_status()
                    season_type_json = season_type_response.json()
                    yield ESPNSeasonModel(self.session, season_type_json)

            if page >= seasons["pageCount"]:
                break
            page += 1

    @staticmethod
    def urls_expire_after() -> (
        Dict[
            Union[str, Pattern[Any]],
            Optional[Union[int, float, str, datetime.datetime, datetime.timedelta]],
        ]
    ):
        """Return any URL cache rules."""
        return {
            **ESPNSeasonModel.urls_expire_after(),
        }
