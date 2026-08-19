# Sudoku Project Instructions

## Project Context

This project is a Flask-based Sudoku game developed as part of the Udacity GitHub Copilot project.

The application contains:
- Flask backend
- Sudoku puzzle generation and validation
- HTML templates
- Plain CSS
- JavaScript frontend
- Pytest test suite

## Coding Standards

- Use clear, readable Python, JavaScript, HTML, and CSS.
- Keep functions small and reusable.
- Avoid unnecessary changes to existing working functionality.
- Add comments where logic is not immediately obvious.
- Use consistent naming conventions.
- Handle invalid user input safely.
- Do not introduce unnecessary dependencies.

## Sudoku Requirements

The application must:
- Generate valid Sudoku puzzles.
- Ensure generated puzzles have exactly one solution.
- Support Easy, Medium, and Hard difficulty levels.
- Keep prefilled cells locked.
- Detect incorrect answers.
- Provide visual feedback for incorrect entries.
- Display a congratulatory message when the puzzle is solved.

## Interactive Features

The application should support:
- New Game
- Check Solution
- Hint
- Timer
- Difficulty selection
- Dark mode
- Top 10 completed-game scores

## Score Requirements

Completed games should store:
- Player name
- Completion time
- Difficulty
- Number of hints used

The scoreboard must keep only the top 10 scores using browser localStorage.

## Testing Requirements

- Use pytest for backend and Sudoku logic tests.
- Existing tests must continue to pass after changes.
- New functionality must include appropriate tests.
- Run tests from the `starter` directory using:

python -m pytest -q

## Copilot Guidelines

Before modifying code:
1. Inspect the existing implementation.
2. Explain which files need modification.
3. Make the smallest reasonable changes.
4. Preserve existing functionality.
5. Add or update tests for new behavior.
6. Run the test suite after implementation.

Do not make unrelated changes.

When a Copilot suggestion could introduce unnecessary complexity, security issues, broken functionality, or violate these instructions, evaluate the suggestion and reject or modify it.