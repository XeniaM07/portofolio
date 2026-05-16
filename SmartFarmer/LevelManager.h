#ifndef LEVEL_MANAGER_H
#define LEVEL_MANAGER_H

#include "Animal.h"
#include "Constants.h"

bool loadLevel(
    int levelNumber,
    Animal board[ROWS][COLS],
    int& maxAllowedFences
);

void saveScore(
    int level,
    int fencesUsed,
    int elapsedSeconds
);

void displayScores();

#endif