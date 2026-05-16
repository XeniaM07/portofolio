#include "Solver.h"
#include "Board.h"

void placeFenceByIndex(
    int index,
    bool value,
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
) {
    int verticalCount = ROWS * (COLS - 1);

    if (index < verticalCount) {
        int row = index / (COLS - 1);
        int col = index % (COLS - 1);
        verticalFences[row][col] = value;
    } else {
        int newIndex = index - verticalCount;
        int row = newIndex / COLS;
        int col = newIndex % COLS;
        horizontalFences[row][col] = value;
    }
}

bool solveBacktrackingOptimal(
    int index,
    int usedFences,
    int targetFences,
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
) {
    int totalFences = ROWS * (COLS - 1) + (ROWS - 1) * COLS;

    if (usedFences > targetFences) {
        return false;
    }

    if (index == totalFences) {
        return usedFences == targetFences &&
               checkSolution(board, verticalFences, horizontalFences);
    }

    placeFenceByIndex(index, true, verticalFences, horizontalFences);

    if (solveBacktrackingOptimal(
        index + 1,
        usedFences + 1,
        targetFences,
        board,
        verticalFences,
        horizontalFences
    )) {
        return true;
    }

    placeFenceByIndex(index, false, verticalFences, horizontalFences);

    if (solveBacktrackingOptimal(
        index + 1,
        usedFences,
        targetFences,
        board,
        verticalFences,
        horizontalFences
    )) {
        return true;
    }

    return false;
}

bool solveLevel(
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int& moveCount,
    int maxAllowedFences
) {
    int totalFences = ROWS * (COLS - 1) + (ROWS - 1) * COLS;

    int limit = maxAllowedFences;

    if (limit > totalFences) {
        limit = totalFences;
    }

    for (int targetFences = 0; targetFences <= limit; targetFences++) {
        resetFences(verticalFences, horizontalFences);
        moveCount = 0;

        if (solveBacktrackingOptimal(
            0,
            0,
            targetFences,
            board,
            verticalFences,
            horizontalFences
        )) {
            moveCount = targetFences;
            return true;
        }
    }

    resetFences(verticalFences, horizontalFences);
    moveCount = 0;

    return false;
}