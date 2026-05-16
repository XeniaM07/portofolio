#ifndef BOARD_H
#define BOARD_H

#include "Animal.h"
#include "Move.h"
#include "Constants.h"

void printBoardWithFences(
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int currentLevel
);

bool addVerticalFence(
    bool verticalFences[ROWS][COLS - 1],
    int row,
    int col
);

bool addHorizontalFence(
    bool horizontalFences[ROWS - 1][COLS],
    int row,
    int col
);

void undoMove(
    Move moves[],
    int& moveCount,
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
);

void resetFences(
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
);

bool canMove(
    int x1,
    int y1,
    int x2,
    int y2,
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
);

bool checkSolution(
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
);

#endif