import random

import pytest
import sudoku_logic


def test_count_solutions_stops_at_two():
    board = sudoku_logic.create_empty_board()

    count = sudoku_logic.count_solutions(board, limit=2)

    assert count == 2


def test_has_unique_solution_on_generated_puzzle():
    random.seed(0)

    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)

    assert all(
        value != sudoku_logic.EMPTY
        for row in solution
        for value in row
    )

    assert sudoku_logic.has_unique_solution(puzzle)

    assert sudoku_logic.count_solutions(puzzle, limit=2) == 1


@pytest.mark.parametrize("clues", [30, 35, 40])
def test_generate_puzzle_uniqueness_for_various_clues(clues):
    random.seed(1 + clues)

    puzzle, solution = sudoku_logic.generate_puzzle(clues=clues)

    assert sudoku_logic.has_unique_solution(puzzle)

    assert all(
        value != sudoku_logic.EMPTY
        for row in solution
        for value in row
    )

    empties = sum(
        1
        for row in puzzle
        for value in row
        if value == sudoku_logic.EMPTY
    )

    assert empties == sudoku_logic.SIZE * sudoku_logic.SIZE - clues