from backend.models.tba.event import Event
from backend.models.tba.match import Match


def filter_events(events: list[Event]) -> list[Event]:

    events = [
        event
        for event in events
        if event.event_type
        not in ["Offseason", "Preseason", "Unlabeled", "Unknown", "Remote", "--"]
    ]

    events = [
        event
        for event in events
        if event.key
        not in [
            "2020dar",
            "2020carv",
            "2020gal",
            "2020hop",
            "2020new",
            "2020roe",
            "2020tur",
        ]
    ]

    return events


def filter_matches(matches: list[Match]) -> list[Match]:
    teams_blacklist: list[str] = [
        "frc0",
        "frc9970",
        "frc9971",
        "frc9972",
        "frc9973",
        "frc9974",
        "frc9975",
        "frc9976",
        "frc9977",
        "frc9978",
        "frc9979",
        "frc9980",
        "frc9981",
        "frc9982",
        "frc9983",
        "frc9984",
        "frc9985",
        "frc9986",
        "frc9987",
        "frc9988",
        "frc9989",
        "frc9990",
        "frc9991",
        "frc9992",
        "frc9993",
        "frc9994",
        "frc9995",
        "frc9996",
        "frc9997",
        "frc9998",
        "frc9999",
    ]
    filtered_matches = []

    for match in matches:
        for alliance in match.alliances:
            alliance.teams = [
                team for team in alliance.teams if team.team_key not in teams_blacklist
            ]
        filtered_matches.append(match)

    return filtered_matches
