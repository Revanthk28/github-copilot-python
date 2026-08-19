from flask import Flask, render_template, jsonify, request
import sudoku_logic

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'difficulty': None
}

# Number of prefilled cells for each difficulty
DIFFICULTY_CLUES = {
    'easy': 45,
    'medium': 35,
    'hard': 30
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    difficulty = request.args.get('difficulty', 'medium').lower()

    # Keep the old ?clues= parameter working
    # so all existing tests continue to pass.
    if 'clues' in request.args:
        clues = int(request.args.get('clues'))
    else:
        if difficulty not in DIFFICULTY_CLUES:
            return jsonify({'error': 'Invalid difficulty'}), 400

        clues = DIFFICULTY_CLUES[difficulty]

    puzzle, solution = sudoku_logic.generate_puzzle(clues)

    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    CURRENT['difficulty'] = difficulty

    return jsonify({
        'puzzle': puzzle,
        'difficulty': difficulty
    })


@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')

    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    incorrect = []

    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])

    return jsonify({'incorrect': incorrect})


if __name__ == '__main__':
    app.run(debug=True)