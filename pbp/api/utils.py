from typing import List

from api.models import Phase


def get_seasons(season: str) -> List[str]:
    if ',' in season:
        return season.split(',')
    return [season]


def get_phases(phase: Phase) -> List[Phase]:
    if phase == Phase.all:
        return [phase.regular_season, phase.playoffs]
    return [phase]