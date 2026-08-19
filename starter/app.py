from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Number of prefilled cells for each difficulty level.
DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 30
}

# Keep a simple in-memory store for the current game.
CURRENT = {
    'puzzle': None,
    'solution': None,
    'hints': 0
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty')

    # Backward compatibility with the original /new?clues=35 API.
    clues_parameter = request.args.get('clues')

    if clues_parameter is not None:
        try:
            clues = int(clues_parameter)
        except ValueError:
            return jsonify({
                'error': 'Clues must be a valid number'
            }), 400

        if clues < 1 or clues > sudoku_logic.SIZE * sudoku_logic.SIZE:
            return jsonify({
                'error': 'Clues must be between 1 and 81'
            }), 400

        selected_difficulty = 'custom'

    else:
        # Difficulty is required for the new difficulty-based API.
        if difficulty is None:
            difficulty = 'medium'

        if difficulty not in DIFFICULTY_CLUES:
            return jsonify({
                'error': 'Invalid difficulty. Choose Easy, Medium, or Hard.'
            }), 400

        clues = DIFFICULTY_CLUES[difficulty]
        selected_difficulty = difficulty

    puzzle, solution = sudoku_logic.generate_puzzle(
        clues=clues
    )

    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['hints'] = 0

    return jsonify({
        'puzzle': puzzle,
        'difficulty': selected_difficulty,
        'clues': clues
    })


@app.route('/hint', methods=['POST'])
def hint():
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')

    if puzzle is None or solution is None:
        return jsonify({
            'error': 'No game in progress'
        }), 400

    # Find the first empty cell and fill it with
    # the correct value from the solution.
    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):

            if puzzle[row][col] == sudoku_logic.EMPTY:

                value = solution[row][col]

                puzzle[row][col] = value
                CURRENT['hints'] += 1

                return jsonify({
                    'row': row,
                    'col': col,
                    'value': value,
                    'hints': CURRENT['hints']
                })

    return jsonify({
        'error': 'No empty cells remaining'
    }), 400


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json

    if not data or 'board' not in data:
        return jsonify({
            'error': 'Invalid board data'
        }), 400

    board = data.get('board')
    solution = CURRENT.get('solution')

    if solution is None:
        return jsonify({
            'error': 'No game in progress'
        }), 400

    incorrect = []

    for row in range(sudoku_logic.SIZE):
        for col in range(sudoku_logic.SIZE):

            if board[row][col] != solution[row][col]:
                incorrect.append([row, col])

    return jsonify({
        'incorrect': incorrect
    })


if __name__ == '__main__':
    app.run(debug=True)