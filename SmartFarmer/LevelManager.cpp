#include <iostream>
#include <fstream>
#include <ctime>
#include <string>

#include "LevelManager.h"

using namespace std;

bool loadLevel(
    int levelNumber,
    Animal board[ROWS][COLS],
    int& maxAllowedFences
) {
    ifstream fin("levels.txt");

    if (!fin) {
        cout << "Fisierul levels.txt nu a fost gasit.\n";
        return false;
    }

    int numberOfLevels;
    fin >> numberOfLevels;

    if (levelNumber < 1 || levelNumber > numberOfLevels) {
        cout << "Nivel invalid.\n";
        return false;
    }

    string line;
    int levelFenceLimit;

    for (int level = 1; level <= numberOfLevels; level++) {
        fin >> levelFenceLimit;

        for (int i = 0; i < ROWS; i++) {
            fin >> line;

            if (level == levelNumber) {
                for (int j = 0; j < COLS; j++) {
                    board[i][j] = charToAnimal(line[j]);
                }

                maxAllowedFences = levelFenceLimit;
            }
        }
    }

    fin.close();
    return true;
}

void saveScore(
    int level,
    int fencesUsed,
    int elapsedSeconds
) {
    ofstream fout("scores.txt", ios::app);

    if (!fout) {
        cout << "Eroare la salvarea scorului.\n";
        return;
    }

    time_t now = time(0);

    fout << "Nivel: " << level
         << " | Garduri folosite: " << fencesUsed
         << " | Timp: " << elapsedSeconds << " secunde"
         << " | Data: " << ctime(&now);

    fout.close();
}

void displayScores() {
    ifstream fin("scores.txt");

    if (!fin) {
        cout << "\nNu exista scoruri salvate momentan.\n";
        return;
    }

    string line;

    cout << "\n===== SCORURI SALVATE =====\n";

    while (getline(fin, line)) {
        cout << line << endl;
    }

    cout << "===========================\n";

    fin.close();
}