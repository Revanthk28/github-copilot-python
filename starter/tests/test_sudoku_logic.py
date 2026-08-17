import sudoku_logic


def count_empty(board):
    return sum(1 for row in board for v in row if v == sudoku_logic.EMPTY)


def test_create_empty_board():
    b = sudoku_logic.create_empty_board()
    assert len(b) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in b)
    assert all(v == sudoku_logic.EMPTY for row in b for v in row)


def test_deep_copy_independence():
    b = sudoku_logic.create_empty_board()
    b2 = sudoku_logic.deep_copy(b)
    b2[0][0] = 1
    assert b[0][0] == sudoku_logic.EMPTY


def test_fill_board_produces_valid_solution():
    b = sudoku_logic.create_empty_board()
    result = sudoku_logic.fill_board(b)
    assert result is True
    # rows contain 1..9
    for row in b:
        assert set(row) == set(range(1, sudoku_logic.SIZE + 1))
    # columns
    for c in range(sudoku_logic.SIZE):
        col = [b[r][c] for r in range(sudoku_logic.SIZE)]
        assert set(col) == set(range(1, sudoku_logic.SIZE + 1))
    # 3x3 boxes
    for br in range(0, sudoku_logic.SIZE, 3):
        for bc in range(0, sudoku_logic.SIZE, 3):
            box = []
            for i in range(3):
                for j in range(3):
                    box.append(b[br + i][bc + j])
            assert set(box) == set(range(1, sudoku_logic.SIZE + 1))


def test_generate_puzzle_has_correct_counts():
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
    assert len(puzzle) == sudoku_logic.SIZE
    # solution fully filled
    assert all(v != sudoku_logic.EMPTY for row in solution for v in row)
    # puzzle has exactly 81-35 empties
    empties = count_empty(puzzle)
    assert empties == sudoku_logic.SIZE * sudoku_logic.SIZE - 35
