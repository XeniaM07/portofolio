#include <iostream>
#include <ctime>

#include "Game.h"
#include "Animal.h"
#include "Board.h"
#include "Solver.h"
#include "LevelManager.h"
#include "Constants.h"
#include "Move.h"

using namespace std;

void showMenu() {
    cout << "\nAlege actiunea:\n";
    cout << "1 - Adauga gard vertical\n";
    cout << "2 - Adauga gard orizontal\n";
    cout << "3 - Undo ultima mutare\n";
    cout << "4 - Verifica solutia\n";
    cout << "5 - Nivel urmator\n";
    cout << "6 - Restart nivel\n";
    cout << "7 - Rezolvare automata\n";
    cout << "8 - Afiseaza scoruri\n";
    cout << "0 - Iesire\n";
    cout << "Optiune:";
}

void resetCurrentLevel(
    int currentLevel,
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int& moveCount,
    int& maxAllowedFences,
    time_t& levelStartTime
) {
    loadLevel(currentLevel, board, maxAllowedFences);
    resetFences(verticalFences, horizontalFences);
    moveCount = 0;
    levelStartTime = time(0);
}

bool goToNextLevel(
    int& currentLevel,
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int& moveCount,
    int& maxAllowedFences,
    time_t& levelStartTime
) {
    if (currentLevel >= NUMBER_OF_LEVELS) {
        cout << "Nu mai exista niveluri.\n";
        return false;
    }

    currentLevel++;

    resetCurrentLevel(
        currentLevel,
        board,
        verticalFences,
        horizontalFences,
        moveCount,
        maxAllowedFences,
        levelStartTime
    );

    cout << "Ai trecut la nivelul "
         << currentLevel
         << ".\n";

    return true;
}

void handleVerticalFence(
    Move moves[],
    int& moveCount,
    bool verticalFences[ROWS][COLS - 1],
    int maxAllowedFences
) {
    if (moveCount >= maxAllowedFences) {
        cout << "Ai folosit toate gardurile disponibile pentru acest nivel.\n";
        return;
    }

    int row;
    int col;

    cout << "\nRand:";
    cin >> row;

    cout << "\nColoana:";
    cin >> col;

    if (addVerticalFence(verticalFences, row, col)) {
        moves[moveCount].type = 'V';
        moves[moveCount].row = row;
        moves[moveCount].col = col;

        moveCount++;
    }
}

void handleHorizontalFence(
    Move moves[],
    int& moveCount,
    bool horizontalFences[ROWS - 1][COLS],
    int maxAllowedFences
) {
    if (moveCount >= maxAllowedFences) {
        cout << "Ai folosit toate gardurile disponibile pentru acest nivel.\n";
        return;
    }

    int row;
    int col;

    cout << "\nRand:";
    cin >> row;

    cout << "\nColoana:";
    cin >> col;

    if (addHorizontalFence(horizontalFences, row, col)) {
        moves[moveCount].type = 'H';
        moves[moveCount].row = row;
        moves[moveCount].col = col;

        moveCount++;
    }
}

void handleCheckSolution(
    int& currentLevel,
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int& moveCount,
    int& maxAllowedFences,
    time_t& levelStartTime
) {
    if (checkSolution(board, verticalFences, horizontalFences)) {
        int elapsedSeconds = time(0) - levelStartTime;

        cout << "\nSolutia este corecta!\n";
        cout << "Ai folosit " << moveCount << " garduri.\n";
        cout << "Timp: " << elapsedSeconds << " secunde.\n";

        saveScore(currentLevel, moveCount, elapsedSeconds);

        if (currentLevel < NUMBER_OF_LEVELS) {
            cout << "Se incarca nivelul urmator...\n";

            goToNextLevel(
                currentLevel,
                board,
                verticalFences,
                horizontalFences,
                moveCount,
                maxAllowedFences,
                levelStartTime
            );
        } else {
            cout << "\nFelicitari! Ai terminat toate nivelurile!\n";
        }
    } else {
        cout << "\nSolutia NU este corecta.\n";
    }
}

void runGame() {
    Animal board[ROWS][COLS];

    int currentLevel = 1;
    int maxAllowedFences = 0;
    time_t levelStartTime = time(0);

    if (!loadLevel(currentLevel, board, maxAllowedFences)) {
        return;
    }

    bool verticalFences[ROWS][COLS - 1] = {};
    bool horizontalFences[ROWS - 1][COLS] = {};

    Move moves[MAX_MOVES];
    int moveCount = 0;

    int option;

    do {
        printBoardWithFences(
            board,
            verticalFences,
            horizontalFences,
            currentLevel
        );

        cout << "\nGarduri folosite: "
             << moveCount
             << "/"
             << maxAllowedFences
             << "\n";

        showMenu();
        cin >> option;

        if (option == 1) {
            handleVerticalFence(
                moves,
                moveCount,
                verticalFences,
                maxAllowedFences
            );
        } else if (option == 2) {
            handleHorizontalFence(
                moves,
                moveCount,
                horizontalFences,
                maxAllowedFences
            );
        } else if (option == 3) {
            undoMove(
                moves,
                moveCount,
                verticalFences,
                horizontalFences
            );
        } else if (option == 4) {
            handleCheckSolution(
                currentLevel,
                board,
                verticalFences,
                horizontalFences,
                moveCount,
                maxAllowedFences,
                levelStartTime
            );
        } else if (option == 5) {
            goToNextLevel(
                currentLevel,
                board,
                verticalFences,
                horizontalFences,
                moveCount,
                maxAllowedFences,
                levelStartTime
            );
        } else if (option == 6) {
            resetCurrentLevel(
                currentLevel,
                board,
                verticalFences,
                horizontalFences,
                moveCount,
                maxAllowedFences,
                levelStartTime
            );

            cout << "Nivelul a fost restartat.\n";
        } else if (option == 7) {
            if (solveLevel(
                board,
                verticalFences,
                horizontalFences,
                moveCount,
                maxAllowedFences
            )) {
                cout << "Solverul a gasit o solutie.\n";
                cout << "Garduri folosite: " << moveCount << "\n";
            } else {
                cout << "Solverul nu a gasit nicio solutie.\n";
            }
        } else if (option == 8) {
            displayScores();
        }

    } while (option != 0);
}