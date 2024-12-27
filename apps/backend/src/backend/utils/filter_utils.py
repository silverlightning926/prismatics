from backend.models.tba.event import Event


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
