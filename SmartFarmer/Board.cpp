#include <iostream>

#include "Board.h"

using namespace std;

void printBoardWithFences(
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int currentLevel
) {
    cout << "\nNivel curent: " << currentLevel << "\n";
    cout << "\nTabla jocului cu garduri:\n\n";

    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            cout << animalToChar(board[i][j]);

            if (j < COLS - 1) {
                cout << (verticalFences[i][j] ? "|" : " ");
            }
        }

        cout << endl;

        if (i < ROWS - 1) {
            for (int j = 0; j < COLS; j++) {
                cout << (horizontalFences[i][j] ? "-" : " ");

                if (j < COLS - 1) {
                    cout << " ";
                }
            }

            cout << endl;
        }
    }
}

bool addVerticalFence(
    bool verticalFences[ROWS][COLS - 1],
    int row,
    int col
) {
    if (row < 0 || row >= ROWS || col < 0 || col >= COLS - 1) {
        cout << "Pozitie invalida pentru gard vertical.\n";
        return false;
    }

    if (verticalFences[row][col]) {
        cout << "Exista deja gard vertical acolo.\n";
        return false;
    }

    verticalFences[row][col] = true;
    return true;
}

bool addHorizontalFence(
    bool horizontalFences[ROWS - 1][COLS],
    int row,
    int col
) {
    if (row < 0 || row >= ROWS - 1 || col < 0 || col >= COLS) {
        cout << "Pozitie invalida pentru gard orizontal.\n";
        return false;
    }

    if (horizontalFences[row][col]) {
        cout << "Exista deja gard orizontal acolo.\n";
        return false;
    }

    horizontalFences[row][col] = true;
    return true;
}

void undoMove(
    Move moves[],
    int& moveCount,
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
) {
    if (moveCount == 0) {
        cout << "Nu exista mutari pentru undo.\n";
        return;
    }

    moveCount--;

    Move lastMove = moves[moveCount];

    if (lastMove.type == 'V') {
        verticalFences[lastMove.row][lastMove.col] = false;
    } else if (lastMove.type == 'H') {
        horizontalFences[lastMove.row][lastMove.col] = false;
    }

    cout << "Ultima mutare a fost stearsa.\n";
}

void resetFences(
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
) {
    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS - 1; j++) {
            verticalFences[i][j] = false;
        }
    }

    for (int i = 0; i < ROWS - 1; i++) {
        for (int j = 0; j < COLS; j++) {
            horizontalFences[i][j] = false;
        }
    }
}

bool canMove(
    int x1,
    int y1,
    int x2,
    int y2,
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
) {
    if (x2 < 0 || x2 >= ROWS || y2 < 0 || y2 >= COLS) {
        return false;
    }

    if (x1 == x2) {
        if (y1 < y2) {
            return !verticalFences[x1][y1];
        } else {
            return !verticalFences[x1][y2];
        }
    }

    if (y1 == y2) {
        if (x1 < x2) {
            return !horizontalFences[x1][y1];
        } else {
            return !horizontalFences[x2][y1];
        }
    }

    return false;
}

bool checkSolution(
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
) {
    bool visited[ROWS][COLS] = {};

    int dx[] = {-1, 1, 0, 0};
    int dy[] = {0, 0, -1, 1};

    for (int startX = 0; startX < ROWS; startX++) {
        for (int startY = 0; startY < COLS; startY++) {
            if (visited[startX][startY]) {
                continue;
            }

            Animal foundAnimal = EMPTY;

            int queueX[100];
            int queueY[100];

            int left = 0;
            int right = 0;

            queueX[right] = startX;
            queueY[right] = startY;
            right++;

            visited[startX][startY] = true;

            while (left < right) {
                int x = queueX[left];
                int y = queueY[left];
                left++;

                if (board[x][y] != EMPTY) {
                    if (foundAnimal == EMPTY) {
                        foundAnimal = board[x][y];
                    } else if (foundAnimal != board[x][y]) {
                        return false;
                    }
                }

                for (int dir = 0; dir < 4; dir++) {
                    int nx = x + dx[dir];
                    int ny = y + dy[dir];

                    if (
                        nx >= 0 &&
                        nx < ROWS &&
                        ny >= 0 &&
                        ny < COLS &&
                        !visited[nx][ny] &&
                        canMove(x, y, nx, ny, verticalFences, horizontalFences)
                    ) {
                        visited[nx][ny] = true;

                        queueX[right] = nx;
                        queueY[right] = ny;

                        right++;
                    }
                }
            }
        }
    }

    return true;
}