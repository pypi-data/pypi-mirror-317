# When dropping python 3.10, we can replace "timezone", and "timezone.utc", with "UTC"
from datetime import datetime, timezone
from importlib import import_module

CURRENT_TIME = datetime.now(timezone.utc)
MOST_RECENT_DECEMBER_YEAR = CURRENT_TIME.year if CURRENT_TIME.month == 12 else CURRENT_TIME.year - 1

__all__ = []

for year in range(2015, MOST_RECENT_DECEMBER_YEAR+1):
    try:
        import_module(f'.year_{year}', package='advent_of_code_explainer.puzzles')
        __all__.append(f'year_{year}')
    except ModuleNotFoundError:
        # Dynamically import them if they exist, as they are added, but don't worry
        # if they don't yet exist. They should all be tested for once they exist.
        pass
