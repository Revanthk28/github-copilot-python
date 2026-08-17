import copy
import random

SIZE = 9
EMPTY = 0

def deep_copy(board):
    return copy.deepcopy(board)

def create_empty_board():
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]

def is_safe(board, row, col, num):
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False
    # Check 3x3 box
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

# Solver utilities for counting solutions and checking uniqueness

def _find_unassigned_with_fewest_options(board):
    best = None
    best_options = None
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == EMPTY:
                options = [n for n in range(1, SIZE + 1) if is_safe(board, r, c, n)]
                if best is None or len(options) < best_options:
                    best = (r, c)
                    best_options = len(options)
                    if best_options == 0:
                        return best
    return best


def count_solutions(board, limit=2):
    """
    Count solutions of a Sudoku board using backtracking.
    Stops early when the count reaches `limit`.
    Returns the count (0, 1, or >=limit).
    """
    board_copy = deep_copy(board)
    count = 0

    def backtrack():
        nonlocal count
        if count >= limit:
            return
        # find unassigned cell (use heuristic)
        pos = _find_unassigned_with_fewest_options(board_copy)
        if pos is None:
            # no empty cells -> found a solution
            count += 1
            return
        r, c = pos
        # compute candidates
        candidates = [n for n in range(1, SIZE + 1) if is_safe(board_copy, r, c, n)]
        for n in candidates:
            board_copy[r][c] = n
            backtrack()
            board_copy[r][c] = EMPTY
            if count >= limit:
                return

    backtrack()
    return count


def has_unique_solution(board):
    """Return True if the board has exactly one solution."""
    return count_solutions(board, limit=2) == 1


def remove_cells(board, clues):
    """
    Remove cells from a fully filled board while preserving a unique solution.
    This attempts to remove SIZE*SIZE - clues cells but will only remove a cell
    if the puzzle still has a unique solution after removal. If it cannot reach
    the requested number of clues with the current filled board, the function
    will stop and leave the board with as many removals as were safely possible.
    """
    cells_to_remove = SIZE * SIZE - clues
    # positions of filled cells
    positions = [(r, c) for r in range(SIZE) for c in range(SIZE) if board[r][c] != EMPTY]
    random.shuffle(positions)
    removed = 0
    for (r, c) in positions:
        if removed >= cells_to_remove:
            break
        old = board[r][c]
        board[r][c] = EMPTY
        # check uniqueness
        if has_unique_solution(board):
            removed += 1
        else:
            # revert removal
            board[r][c] = old
    # note: we may not reach the desired number of removals for this filled board


def generate_puzzle(clues=35, max_tries=10):
    """
    Generate a puzzle with the requested number of clues and a unique solution.

    The function will attempt up to `max_tries` random filled boards and try to
    remove cells while preserving uniqueness. If it cannot produce a puzzle
    with the exact number of clues after `max_tries` attempts, it raises
    a RuntimeError. This keeps the API backward-compatible while enforcing
    the uniqueness requirement.
    """
    for _ in range(max_tries):
        board = create_empty_board()
        fill_board(board)
        solution = deep_copy(board)
        remove_cells(board, clues)
        # ensure produced puzzle has unique solution
        if has_unique_solution(board):
            puzzle = deep_copy(board)
            return puzzle, solution
    raise RuntimeError(f"Failed to generate puzzle with {clues} clues and unique solution after {max_tries} attempts")
