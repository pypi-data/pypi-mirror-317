# import pytest
import advent_of_code_explainer as aoce


def test_function():
    assert aoce.__version__ == "0.0.1"
    assert aoce.puzzles.year_2024.day_1.solve_two(0) == 2
    assert aoce.puzzles.year_2024.day_2.solve_two(0) == 4
    assert aoce.puzzles.year_2023.day_1.solve_two(0) == 2
    assert aoce.puzzles.year_2023.day_2.solve_two(0) == 4
