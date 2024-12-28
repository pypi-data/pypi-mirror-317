from importlib import import_module
import os

YEAR_MODULE = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]

__all__ = []

for day in range(1, 26):
    try:
        import_module(f'.day_{day}', package=f'advent_of_code_explainer.puzzles.{YEAR_MODULE}')
        __all__.append(f'day_{day}')
    except ModuleNotFoundError:
        # Dynamically import them if they exist, as they are added, but don't worry
        # if they don't yet exist. They should all be tested for once they exist.
        pass
