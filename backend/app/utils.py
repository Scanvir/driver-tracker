from datetime import datetime, time


def parse_hhmm(value: str) -> time:
    return datetime.strptime(value.strip(), "%H:%M").time()
