#ifndef SOLVER_H
#define SOLVER_H

#include "Animal.h"
#include "Constants.h"

bool solveLevel(
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int& moveCount,
    int maxAllowedFences
);

#endif