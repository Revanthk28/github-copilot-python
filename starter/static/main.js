const SIZE = 9;

const SCORE_STORAGE_KEY = 'sudokuTop10';
const DARK_MODE_KEY = 'sudokuDarkMode';

let puzzle = [];
let timerInterval = null;
let elapsedSeconds = 0;
let hintsUsed = 0;
let gameCompleted = false;


// ========================================
// DARK MODE
// ========================================

function initializeDarkMode() {

    const savedMode =
        localStorage.getItem(DARK_MODE_KEY);

    if (savedMode === 'dark') {
        document.body.classList.add('dark-mode');
    }

    updateDarkModeButton();
}


function toggleDarkMode() {

    document.body.classList.toggle('dark-mode');

    const isDark =
        document.body.classList.contains('dark-mode');

    localStorage.setItem(
        DARK_MODE_KEY,
        isDark ? 'dark' : 'light'
    );

    updateDarkModeButton();
}


function updateDarkModeButton() {

    const button =
        document.getElementById('dark-mode-toggle');

    if (!button) {
        return;
    }

    const isDark =
        document.body.classList.contains('dark-mode');

    if (isDark) {
        button.innerText = '☀️ Light Mode';
    } else {
        button.innerText = '🌙 Dark Mode';
    }
}


// ========================================
// TIMER
// ========================================

function startTimer() {

    stopTimer();

    elapsedSeconds = 0;

    updateTimer();

    timerInterval = setInterval(() => {

        elapsedSeconds++;

        updateTimer();

    }, 1000);
}


function stopTimer() {

    if (timerInterval !== null) {

        clearInterval(timerInterval);

        timerInterval = null;
    }
}


function updateTimer() {

    const minutes =
        Math.floor(elapsedSeconds / 60);

    const seconds =
        elapsedSeconds % 60;

    const timer =
        document.getElementById('timer');

    if (timer) {

        timer.innerText =
            `Time: ${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
}


// ========================================
// FORMAT TIME
// ========================================

function formatTime(totalSeconds) {

    const minutes =
        Math.floor(totalSeconds / 60);

    const seconds =
        totalSeconds % 60;

    return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}


// ========================================
// CREATE SUDOKU BOARD
// ========================================

function createBoardElement() {

    const boardDiv =
        document.getElementById('sudoku-board');

    boardDiv.innerHTML = '';

    for (let i = 0; i < SIZE; i++) {

        const rowDiv =
            document.createElement('div');

        rowDiv.className =
            'sudoku-row';

        for (let j = 0; j < SIZE; j++) {

            const input =
                document.createElement('input');

            input.type = 'text';

            input.maxLength = 1;

            input.className =
                'sudoku-cell';

            input.dataset.row = i;
            input.dataset.col = j;

            input.setAttribute(
                'aria-label',
                `Row ${i + 1}, Column ${j + 1}`
            );

            input.addEventListener(
                'input',
                (event) => {

                    const value =
                        event.target.value
                            .replace(/[^1-9]/g, '');

                    event.target.value =
                        value;
                }
            );

            rowDiv.appendChild(input);
        }

        boardDiv.appendChild(rowDiv);
    }
}


// ========================================
// RENDER PUZZLE
// ========================================

function renderPuzzle(puz) {

    puzzle = puz;

    createBoardElement();

    const inputs =
        document
            .getElementById('sudoku-board')
            .getElementsByTagName('input');

    for (let i = 0; i < SIZE; i++) {

        for (let j = 0; j < SIZE; j++) {

            const index =
                i * SIZE + j;

            const value =
                puzzle[i][j];

            const input =
                inputs[index];

            if (value !== 0) {

                input.value =
                    value;

                input.disabled =
                    true;

                input.className =
                    'sudoku-cell prefilled';

            } else {

                input.value = '';

                input.disabled =
                    false;

                input.className =
                    'sudoku-cell';
            }
        }
    }
}


// ========================================
// NEW GAME
// ========================================

async function newGame() {

    const difficultySelect =
        document.getElementById('difficulty');

    const difficulty =
        difficultySelect
            ? difficultySelect.value
            : 'medium';

    try {

        const response =
            await fetch(
                `/new?difficulty=${difficulty}`
            );

        if (!response.ok) {

            throw new Error(
                'Unable to start game'
            );
        }

        const data =
            await response.json();

        renderPuzzle(
            data.puzzle
        );

        hintsUsed = 0;

        gameCompleted = false;

        updateHintCount();

        const message =
            document.getElementById('message');

        message.innerText = '';

        message.style.color =
            '';

        startTimer();

    } catch (error) {

        document.getElementById(
            'message'
        ).innerText =
            'Unable to start a new game.';
    }
}


// ========================================
// HINT
// ========================================

async function useHint() {

    if (gameCompleted) {
        return;
    }

    try {

        const response =
            await fetch('/hint', {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/json'
                }
            });

        const data =
            await response.json();

        const message =
            document.getElementById(
                'message'
            );

        if (data.error) {

            message.style.color =
                '#d32f2f';

            message.innerText =
                data.error;

            return;
        }

        const inputs =
            document
                .getElementById(
                    'sudoku-board'
                )
                .getElementsByTagName(
                    'input'
                );

        const index =
            data.row * SIZE +
            data.col;

        const input =
            inputs[index];

        input.value =
            data.value;

        input.disabled =
            true;

        input.className =
            'sudoku-cell prefilled hint-cell';

        puzzle[data.row][data.col] =
            data.value;

        hintsUsed =
            data.hints;

        updateHintCount();

        message.style.color =
            '#1976d2';

        message.innerText =
            `Hint used. Hints: ${hintsUsed}`;

    } catch (error) {

        document.getElementById(
            'message'
        ).innerText =
            'Unable to use hint.';
    }
}


function updateHintCount() {

    const hintCount =
        document.getElementById(
            'hint-count'
        );

    if (hintCount) {

        hintCount.innerText =
            `Hints: ${hintsUsed}`;
    }
}


// ========================================
// CHECK SOLUTION
// ========================================

async function checkSolution() {

    if (gameCompleted) {
        return;
    }

    const inputs =
        document
            .getElementById(
                'sudoku-board'
            )
            .getElementsByTagName(
                'input'
            );

    const board = [];

    for (let i = 0; i < SIZE; i++) {

        board[i] = [];

        for (let j = 0; j < SIZE; j++) {

            const index =
                i * SIZE + j;

            const value =
                inputs[index].value;

            board[i][j] =
                value
                    ? parseInt(
                        value,
                        10
                    )
                    : 0;
        }
    }

    try {

        const response =
            await fetch('/check', {
                method: 'POST',
                headers: {
                    'Content-Type':
                        'application/json'
                },
                body: JSON.stringify({
                    board: board
                })
            });

        const data =
            await response.json();

        const message =
            document.getElementById(
                'message'
            );

        if (data.error) {

            message.style.color =
                '#d32f2f';

            message.innerText =
                data.error;

            return;
        }

        const incorrect =
            new Set(
                data.incorrect.map(
                    cell =>
                        cell[0] * SIZE +
                        cell[1]
                )
            );

        for (
            let index = 0;
            index < inputs.length;
            index++
        ) {

            const input =
                inputs[index];

            if (input.disabled) {
                continue;
            }

            input.className =
                'sudoku-cell';

            if (incorrect.has(index)) {

                input.className =
                    'sudoku-cell incorrect';
            }
        }

        if (incorrect.size === 0) {

            stopTimer();

            gameCompleted = true;

            message.style.color =
                '#388e3c';

            message.innerText =
                'Congratulations! You solved it!';

            saveCompletedGame();

        } else {

            message.style.color =
                '#d32f2f';

            message.innerText =
                'Some cells are incorrect.';
        }

    } catch (error) {

        document.getElementById(
            'message'
        ).innerText =
            'Unable to check the solution.';
    }
}


// ========================================
// TOP 10 SCOREBOARD
// ========================================

function getScores() {

    try {

        const storedScores =
            localStorage.getItem(
                SCORE_STORAGE_KEY
            );

        if (!storedScores) {
            return [];
        }

        const scores =
            JSON.parse(
                storedScores
            );

        return Array.isArray(scores)
            ? scores
            : [];

    } catch (error) {

        return [];
    }
}


function saveScores(scores) {

    localStorage.setItem(
        SCORE_STORAGE_KEY,
        JSON.stringify(scores)
    );
}


function saveCompletedGame() {

    const playerInput =
        document.getElementById(
            'player-name'
        );

    let playerName =
        playerInput.value.trim();

    if (!playerName) {
        playerName = 'Player';
    }

    const difficulty =
        document.getElementById(
            'difficulty'
        ).value;

    const newScore = {

        player: playerName,

        time: elapsedSeconds,

        difficulty: difficulty,

        hints: hintsUsed
    };

    let scores =
        getScores();

    scores.push(
        newScore
    );

    scores.sort(
        (a, b) => {

            if (a.time !== b.time) {
                return a.time - b.time;
            }

            return a.hints - b.hints;
        }
    );

    scores =
        scores.slice(0, 10);

    saveScores(scores);

    renderScores();

    const message =
        document.getElementById(
            'message'
        );

    message.innerText =
        `Congratulations! Score saved: ${formatTime(elapsedSeconds)}`;
}


function renderScores() {

    const scoreList =
        document.getElementById(
            'score-list'
        );

    const noScores =
        document.getElementById(
            'no-scores'
        );

    const scores =
        getScores();

    scoreList.innerHTML = '';

    if (scores.length === 0) {

        noScores.style.display =
            'block';

        return;
    }

    noScores.style.display =
        'none';

    scores.forEach(
        (score, index) => {

            const row =
                document.createElement(
                    'tr'
                );

            row.innerHTML = `
                <td>${index + 1}</td>
                <td>${escapeHtml(score.player)}</td>
                <td>${formatTime(score.time)}</td>
                <td>${capitalize(score.difficulty)}</td>
                <td>${score.hints}</td>
            `;

            scoreList.appendChild(row);
        }
    );
}


function clearScores() {

    const confirmed =
        window.confirm(
            'Are you sure you want to clear all Top 10 scores?'
        );

    if (!confirmed) {
        return;
    }

    localStorage.removeItem(
        SCORE_STORAGE_KEY
    );

    renderScores();
}


function escapeHtml(value) {

    const div =
        document.createElement(
            'div'
        );

    div.textContent =
        value;

    return div.innerHTML;
}


function capitalize(value) {

    if (!value) {
        return '';
    }

    return value.charAt(0).toUpperCase() +
        value.slice(1);
}


// ========================================
// INITIALIZE
// ========================================

window.addEventListener(
    'load',
    () => {

        initializeDarkMode();

        document
            .getElementById(
                'dark-mode-toggle'
            )
            .addEventListener(
                'click',
                toggleDarkMode
            );

        document
            .getElementById(
                'new-game'
            )
            .addEventListener(
                'click',
                newGame
            );

        document
            .getElementById(
                'hint'
            )
            .addEventListener(
                'click',
                useHint
            );

        document
            .getElementById(
                'check-solution'
            )
            .addEventListener(
                'click',
                checkSolution
            );

        document
            .getElementById(
                'clear-scores'
            )
            .addEventListener(
                'click',
                clearScores
            );

        const difficultySelect =
            document.getElementById(
                'difficulty'
            );

        if (difficultySelect) {

            difficultySelect.addEventListener(
                'change',
                newGame
            );
        }

        renderScores();

        newGame();
    }
);