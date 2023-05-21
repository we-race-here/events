from apps.event.models import RaceSeries

"""

"""


def individual_points(raceseries: RaceSeries) -> dict:
    """
    Person identification priority: User, License, Name
    return a dict of points for each person
    """
    pass


def club_points(raceseries: RaceSeries) -> dict:
    """
    club identification priority/identification: Organization, usac, Name
    return a dict of points for each team
    Notes:
    - Try to add a club to the result record before calculating points
    - Club must be a CURRENT club at EBC
    - CURRENT probably means they have paid club dues and have a club admin
    - Results should be grouped by category
    """
