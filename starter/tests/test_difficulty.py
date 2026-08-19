import sudoku_logic
from app import app, DIFFICULTY_CLUES


def count_clues(board):
    return sum(
        1
        for row in board
        for value in row
        if value != sudoku_logic.EMPTY
    )


def test_difficulty_clue_order():
    assert DIFFICULTY_CLUES["easy"] > DIFFICULTY_CLUES["medium"]
    assert DIFFICULTY_CLUES["medium"] > DIFFICULTY_CLUES["hard"]


def test_easy_difficulty():
    app.testing = True

    with app.test_client() as client:
        response = client.get("/new?difficulty=easy")

    assert response.status_code == 200

    data = response.get_json()
    puzzle = data["puzzle"]

    assert data["difficulty"] == "easy"
    assert count_clues(puzzle) == 45
    assert sudoku_logic.has_unique_solution(puzzle)


def test_medium_difficulty():
    app.testing = True

    with app.test_client() as client:
        response = client.get("/new?difficulty=medium")

    assert response.status_code == 200

    data = response.get_json()
    puzzle = data["puzzle"]

    assert data["difficulty"] == "medium"
    assert count_clues(puzzle) == 35
    assert sudoku_logic.has_unique_solution(puzzle)


def test_hard_difficulty():
    app.testing = True

    with app.test_client() as client:
        response = client.get("/new?difficulty=hard")

    assert response.status_code == 200

    data = response.get_json()
    puzzle = data["puzzle"]

    assert data["difficulty"] == "hard"
    assert count_clues(puzzle) == 30
    assert sudoku_logic.has_unique_solution(puzzle)


def test_invalid_difficulty():
    app.testing = True

    with app.test_client() as client:
        response = client.get("/new?difficulty=extreme")

    assert response.status_code == 400
    assert "error" in response.get_json()