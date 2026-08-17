import pytest
from app import app, CURRENT
import sudoku_logic


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def count_empty(board):
    return sum(1 for row in board for v in row if v == sudoku_logic.EMPTY)


def test_new_game_sets_current_and_returns_puzzle(client):
    resp = client.get('/new?clues=30')
    assert resp.status_code == 200
    data = resp.get_json()
    assert 'puzzle' in data
    puzzle = data['puzzle']
    assert len(puzzle) == sudoku_logic.SIZE
    assert CURRENT['solution'] is not None
    empties = count_empty(puzzle)
    assert empties == sudoku_logic.SIZE * sudoku_logic.SIZE - 30


def test_check_solution_no_game(client):
    # clear current
    CURRENT['solution'] = None
    resp = client.post('/check', json={'board': sudoku_logic.create_empty_board()})
    assert resp.status_code == 400
    data = resp.get_json()
    assert 'error' in data


def test_check_solution_correct_and_incorrect(client):
    puzzle, solution = sudoku_logic.generate_puzzle(clues=35)
    CURRENT['solution'] = solution
    # correct board
    resp = client.post('/check', json={'board': solution})
    data = resp.get_json()
    assert data['incorrect'] == []
    # incorrect board: change one cell
    bad = sudoku_logic.deep_copy(solution)
    bad[0][0] = (bad[0][0] % 9) + 1  # ensure different number
    resp = client.post('/check', json={'board': bad})
    data = resp.get_json()
    assert [0, 0] in data['incorrect']
