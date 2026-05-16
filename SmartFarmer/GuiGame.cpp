#include <SFML/Graphics.hpp>
#include <iostream>
#include <ctime>
#include <string>
#include <fstream>
#include <vector>
#include <cmath>

#include "GuiGame.h"
#include "Animal.h"
#include "Board.h"
#include "Solver.h"
#include "LevelManager.h"
#include "Constants.h"
#include "Move.h"

using namespace std;

const int WINDOW_WIDTH = 850;
const int WINDOW_HEIGHT = 560;

const float CELL_SIZE = 120.f;
const float BOARD_X = 70.f;
const float BOARD_Y = 90.f;
const float FENCE_THICKNESS = 10.f;

struct Button {
    sf::RectangleShape shape;
    sf::Text text;
};

Button createButton(
    const string& label,
    sf::Font& font,
    float x,
    float y,
    float width,
    float height
) {
    Button button;

    button.shape.setSize(sf::Vector2f(width, height));
    button.shape.setPosition(x, y);
    button.shape.setFillColor(sf::Color(230, 230, 230));
    button.shape.setOutlineColor(sf::Color::Black);
    button.shape.setOutlineThickness(2.f);

    button.text.setFont(font);
    button.text.setString(label);
    button.text.setCharacterSize(18);
    button.text.setFillColor(sf::Color::Black);

    sf::FloatRect textBounds = button.text.getLocalBounds();

    button.text.setPosition(
        x + (width - textBounds.width) / 2.f - textBounds.left,
        y + (height - textBounds.height) / 2.f - textBounds.top
    );

    return button;
}

bool isButtonClicked(Button& button, int mouseX, int mouseY) {
    return button.shape.getGlobalBounds().contains(
        static_cast<float>(mouseX),
        static_cast<float>(mouseY)
    );
}

void drawButton(sf::RenderWindow& window, Button& button) {
    window.draw(button.shape);
    window.draw(button.text);
}

vector<string> loadScoresForGui() {
    vector<string> scores;
    ifstream fin("scores.txt");

    if (!fin) {
        scores.push_back("Nu exista scoruri salvate.");
        return scores;
    }

    string line;

    while (getline(fin, line)) {
        if (!line.empty()) {
            scores.push_back(line);
        }
    }

    fin.close();

    if (scores.empty()) {
        scores.push_back("Nu exista scoruri salvate.");
    }

    return scores;
}

void drawScoresPanel(
    sf::RenderWindow& window,
    sf::Font& font,
    const vector<string>& scores
) {
    sf::RectangleShape overlay(sf::Vector2f(WINDOW_WIDTH, WINDOW_HEIGHT));
    overlay.setFillColor(sf::Color(0, 0, 0, 120));
    overlay.setPosition(0.f, 0.f);
    window.draw(overlay);

    sf::RectangleShape panel(sf::Vector2f(650.f, 420.f));
    panel.setFillColor(sf::Color(245, 245, 245));
    panel.setOutlineColor(sf::Color::Black);
    panel.setOutlineThickness(3.f);
    panel.setPosition(100.f, 70.f);
    window.draw(panel);

    sf::Text title;
    title.setFont(font);
    title.setString("Scoruri salvate");
    title.setCharacterSize(28);
    title.setFillColor(sf::Color::Black);
    title.setPosition(320.f, 90.f);
    window.draw(title);

    sf::Text closeText;
    closeText.setFont(font);
    closeText.setString("Apasa ESC pentru inchidere");
    closeText.setCharacterSize(16);
    closeText.setFillColor(sf::Color::Black);
    closeText.setPosition(300.f, 455.f);
    window.draw(closeText);

    float y = 135.f;
    int startIndex = 0;

    if (scores.size() > 10) {
        startIndex = static_cast<int>(scores.size()) - 10;
    }

    for (int i = startIndex; i < static_cast<int>(scores.size()); i++) {
        sf::Text scoreText;
        scoreText.setFont(font);
        scoreText.setString(scores[i]);
        scoreText.setCharacterSize(15);
        scoreText.setFillColor(sf::Color::Black);
        scoreText.setPosition(130.f, y);

        window.draw(scoreText);

        y += 28.f;
    }
}

void drawLevelsPanel(
    sf::RenderWindow& window,
    sf::Font& font,
    bool playedLevels[NUMBER_OF_LEVELS],
    int currentLevel
) {
    sf::RectangleShape overlay(sf::Vector2f(WINDOW_WIDTH, WINDOW_HEIGHT));
    overlay.setFillColor(sf::Color(0, 0, 0, 120));
    overlay.setPosition(0.f, 0.f);
    window.draw(overlay);

    sf::RectangleShape panel(sf::Vector2f(680.f, 430.f));
    panel.setFillColor(sf::Color(245, 245, 245));
    panel.setOutlineColor(sf::Color::Black);
    panel.setOutlineThickness(3.f);
    panel.setPosition(85.f, 60.f);
    window.draw(panel);

    sf::Text title;
    title.setFont(font);
    title.setString("Alege nivelul");
    title.setCharacterSize(28);
    title.setFillColor(sf::Color::Black);
    title.setPosition(330.f, 80.f);
    window.draw(title);

    float startX = 130.f;
    float startY = 130.f;
    float buttonSize = 48.f;
    float gap = 12.f;

    for (int i = 0; i < NUMBER_OF_LEVELS; i++) {
        int row = i / 10;
        int col = i % 10;

        float x = startX + col * (buttonSize + gap);
        float y = startY + row * (buttonSize + gap);

        sf::RectangleShape levelBox(sf::Vector2f(buttonSize, buttonSize));
        levelBox.setPosition(x, y);

        if (i + 1 == currentLevel) {
            levelBox.setFillColor(sf::Color(255, 220, 120));
        } else if (playedLevels[i]) {
            levelBox.setFillColor(sf::Color(140, 220, 140));
        } else {
            levelBox.setFillColor(sf::Color(230, 230, 230));
        }

        levelBox.setOutlineColor(sf::Color::Black);
        levelBox.setOutlineThickness(2.f);
        window.draw(levelBox);

        sf::Text numberText;
        numberText.setFont(font);
        numberText.setString(to_string(i + 1));
        numberText.setCharacterSize(18);
        numberText.setFillColor(sf::Color::Black);

        sf::FloatRect bounds = numberText.getLocalBounds();

        numberText.setPosition(
            x + (buttonSize - bounds.width) / 2.f - bounds.left,
            y + (buttonSize - bounds.height) / 2.f - bounds.top
        );

        window.draw(numberText);
    }

    sf::Text info;
    info.setFont(font);
    info.setString("Verde = jucat/rezolvat | Galben = nivel curent | ESC = inchide");
    info.setCharacterSize(16);
    info.setFillColor(sf::Color::Black);
    info.setPosition(175.f, 455.f);
    window.draw(info);
}

int getClickedLevelFromPanel(int mouseX, int mouseY) {
    float startX = 130.f;
    float startY = 130.f;
    float buttonSize = 48.f;
    float gap = 12.f;

    for (int i = 0; i < NUMBER_OF_LEVELS; i++) {
        int row = i / 10;
        int col = i % 10;

        float x = startX + col * (buttonSize + gap);
        float y = startY + row * (buttonSize + gap);

        if (
            mouseX >= x &&
            mouseX <= x + buttonSize &&
            mouseY >= y &&
            mouseY <= y + buttonSize
        ) {
            return i + 1;
        }
    }

    return -1;
}

void drawBoard(
    sf::RenderWindow& window,
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    sf::Texture& cowTexture,
    sf::Texture& sheepTexture,
    sf::Texture& pigTexture,
    sf::Texture& horseTexture
) {
    sf::RectangleShape cell(sf::Vector2f(CELL_SIZE, CELL_SIZE));
    cell.setFillColor(sf::Color(90, 180, 90));
    cell.setOutlineColor(sf::Color::Black);
    cell.setOutlineThickness(2.f);

    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS; j++) {
            float x = BOARD_X + j * CELL_SIZE;
            float y = BOARD_Y + i * CELL_SIZE;

            cell.setPosition(x, y);
            window.draw(cell);

            sf::Sprite animalSprite;

            if (board[i][j] == COW) {
                animalSprite.setTexture(cowTexture);
            } else if (board[i][j] == SHEEP) {
                animalSprite.setTexture(sheepTexture);
            } else if (board[i][j] == PIG) {
                animalSprite.setTexture(pigTexture);
            } else if (board[i][j] == HORSE) {
                animalSprite.setTexture(horseTexture);
            } else {
                continue;
            }

            sf::FloatRect bounds = animalSprite.getLocalBounds();

            animalSprite.setScale(
                80.f / bounds.width,
                80.f / bounds.height
            );

            animalSprite.setPosition(
                x + 20.f,
                y + 20.f
            );

            window.draw(animalSprite);
        }
    }

    sf::RectangleShape fence;
    fence.setFillColor(sf::Color(120, 70, 20));

    for (int i = 0; i < ROWS; i++) {
        for (int j = 0; j < COLS - 1; j++) {
            if (verticalFences[i][j]) {
                fence.setSize(sf::Vector2f(FENCE_THICKNESS, CELL_SIZE));
                fence.setPosition(
                    BOARD_X + (j + 1) * CELL_SIZE - FENCE_THICKNESS / 2,
                    BOARD_Y + i * CELL_SIZE
                );
                window.draw(fence);
            }
        }
    }

    for (int i = 0; i < ROWS - 1; i++) {
        for (int j = 0; j < COLS; j++) {
            if (horizontalFences[i][j]) {
                fence.setSize(sf::Vector2f(CELL_SIZE, FENCE_THICKNESS));
                fence.setPosition(
                    BOARD_X + j * CELL_SIZE,
                    BOARD_Y + (i + 1) * CELL_SIZE - FENCE_THICKNESS / 2
                );
                window.draw(fence);
            }
        }
    }
}

bool handleMouseClickOnBoard(
    int mouseX,
    int mouseY,
    Move moves[],
    int& moveCount,
    int maxAllowedFences,
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS]
) {
    if (moveCount >= maxAllowedFences) {
        return false;
    }

    float x = static_cast<float>(mouseX);
    float y = static_cast<float>(mouseY);

    if (
        x < BOARD_X ||
        x > BOARD_X + COLS * CELL_SIZE ||
        y < BOARD_Y ||
        y > BOARD_Y + ROWS * CELL_SIZE
    ) {
        return false;
    }

    for (int col = 0; col < COLS - 1; col++) {
        float fenceX = BOARD_X + (col + 1) * CELL_SIZE;

        if (fabs(x - fenceX) <= 8.f) {
            int row = static_cast<int>((y - BOARD_Y) / CELL_SIZE);

            if (addVerticalFence(verticalFences, row, col)) {
                moves[moveCount].type = 'V';
                moves[moveCount].row = row;
                moves[moveCount].col = col;
                moveCount++;
                return true;
            }
        }
    }

    for (int row = 0; row < ROWS - 1; row++) {
        float fenceY = BOARD_Y + (row + 1) * CELL_SIZE;

        if (fabs(y - fenceY) <= 8.f) {
            int col = static_cast<int>((x - BOARD_X) / CELL_SIZE);

            if (addHorizontalFence(horizontalFences, row, col)) {
                moves[moveCount].type = 'H';
                moves[moveCount].row = row;
                moves[moveCount].col = col;
                moveCount++;
                return true;
            }
        }
    }

    return false;
}

void restartLevel(
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

void goNextLevelGui(
    int& currentLevel,
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int& moveCount,
    int& maxAllowedFences,
    time_t& levelStartTime,
    string& message
) {
    if (currentLevel < NUMBER_OF_LEVELS) {
        currentLevel++;

        restartLevel(
            currentLevel,
            board,
            verticalFences,
            horizontalFences,
            moveCount,
            maxAllowedFences,
            levelStartTime
        );

        message = "Nivelul urmator a fost incarcat.";
    } else {
        message = "Nu mai exista niveluri.";
    }
}

void printGuiStateToConsole(
    const string& action,
    int currentLevel,
    Animal board[ROWS][COLS],
    bool verticalFences[ROWS][COLS - 1],
    bool horizontalFences[ROWS - 1][COLS],
    int moveCount,
    int maxAllowedFences
) {
    cout << "\n==============================\n";
    cout << "Actiune GUI: " << action << "\n";
    cout << "Nivel: " << currentLevel << "\n";
    cout << "Garduri folosite: " << moveCount << "/" << maxAllowedFences << "\n";

    printBoardWithFences(
        board,
        verticalFences,
        horizontalFences,
        currentLevel
    );

    cout << "==============================\n";
}

void runGuiGame() {
    sf::RenderWindow window(
        sf::VideoMode(WINDOW_WIDTH, WINDOW_HEIGHT),
        "Smart Farmer 2D"
    );

    Animal board[ROWS][COLS];

    int currentLevel = 1;
    int maxAllowedFences = 0;
    int moveCount = 0;

    time_t levelStartTime = time(0);
    bool levelSolved = false;
    int finalElapsedSeconds = 0;

    bool verticalFences[ROWS][COLS - 1] = {};
    bool horizontalFences[ROWS - 1][COLS] = {};

    Move moves[MAX_MOVES];

    if (!loadLevel(currentLevel, board, maxAllowedFences)) {
        return;
    }

    bool playedLevels[NUMBER_OF_LEVELS] = {};
    playedLevels[currentLevel - 1] = true;

    printGuiStateToConsole(
        "Joc pornit",
        currentLevel,
        board,
        verticalFences,
        horizontalFences,
        moveCount,
        maxAllowedFences
    );

    sf::Texture cowTexture;
    sf::Texture sheepTexture;
    sf::Texture pigTexture;
    sf::Texture horseTexture;

    if (!cowTexture.loadFromFile("assets/cow.png") ||
        !sheepTexture.loadFromFile("assets/sheep.png") ||
        !pigTexture.loadFromFile("assets/pig.png") ||
        !horseTexture.loadFromFile("assets/horse.png")) {
        cout << "Eroare la incarcarea imaginilor din folderul assets.\n";
        return;
    }

    sf::Font font;

    if (!font.loadFromFile("assets/arial.ttf")) {
        cout << "Eroare la incarcarea fontului assets/arial.ttf.\n";
        return;
    }

    Button checkButton = createButton("Check", font, 560.f, 55.f, 210.f, 36.f);
    Button undoButton = createButton("Undo", font, 560.f, 98.f, 210.f, 36.f);
    Button restartButton = createButton("Restart", font, 560.f, 141.f, 210.f, 36.f);
    Button solveButton = createButton("Solve", font, 560.f, 184.f, 210.f, 36.f);
    Button nextButton = createButton("Next Level", font, 560.f, 227.f, 210.f, 36.f);
    Button levelsButton = createButton("Levels", font, 560.f, 270.f, 210.f, 36.f);
    Button scoresButton = createButton("Scores", font, 560.f, 313.f, 210.f, 36.f);
    Button exitButton = createButton("Exit", font, 560.f, 356.f, 210.f, 36.f);

    string message = "Click intre celule pentru a pune garduri.";

    bool showScoresPanel = false;
    bool showLevelsPanel = false;
    vector<string> guiScores;

    while (window.isOpen()) {
        sf::Event event;

        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                cout << "\nActiune GUI: Fereastra inchisa.\n";
                window.close();
            }

            if (
                event.type == sf::Event::MouseButtonPressed &&
                event.mouseButton.button == sf::Mouse::Left
            ) {
                int mouseX = event.mouseButton.x;
                int mouseY = event.mouseButton.y;

                cout << "\nClick mouse la pozitia: x = "
                     << mouseX << ", y = " << mouseY << "\n";

                if (showLevelsPanel) {
                    int selectedLevel = getClickedLevelFromPanel(mouseX, mouseY);

                    if (selectedLevel != -1) {
                        currentLevel = selectedLevel;

                        restartLevel(
                            currentLevel,
                            board,
                            verticalFences,
                            horizontalFences,
                            moveCount,
                            maxAllowedFences,
                            levelStartTime
                        );

                        levelSolved = false;
                        finalElapsedSeconds = 0;
                        playedLevels[currentLevel - 1] = true;

                        message = "Nivelul " + to_string(currentLevel) + " a fost incarcat.";
                        showLevelsPanel = false;

                        printGuiStateToConsole(
                            "Nivel ales din panoul Levels",
                            currentLevel,
                            board,
                            verticalFences,
                            horizontalFences,
                            moveCount,
                            maxAllowedFences
                        );
                    }

                    continue;
                }

                if (isButtonClicked(checkButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Check\n";

                    if (checkSolution(board, verticalFences, horizontalFences)) {
                        if (!levelSolved) {
                            finalElapsedSeconds =
                                static_cast<int>(time(0) - levelStartTime);

                            saveScore(
                                currentLevel,
                                moveCount,
                                finalElapsedSeconds
                            );

                            levelSolved = true;
                            playedLevels[currentLevel - 1] = true;
                        }

                        message = "Solutie corecta! Scor salvat. Apasa Next Level.";

                        cout << "Rezultat verificare: solutie corecta.\n";
                        cout << "Timp final: "
                             << finalElapsedSeconds
                             << " secunde.\n";
                    } else {
                        message = "Solutia NU este corecta.";
                        cout << "Rezultat verificare: solutie incorecta.\n";
                    }

                    printGuiStateToConsole(
                        "Buton Check apasat",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                } else if (isButtonClicked(undoButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Undo\n";

                    undoMove(
                        moves,
                        moveCount,
                        verticalFences,
                        horizontalFences
                    );

                    levelSolved = false;
                    finalElapsedSeconds = 0;
                    levelStartTime = time(0);

                    message = "Ultima mutare a fost anulata. Timpul a fost resetat.";

                    printGuiStateToConsole(
                        "Buton Undo apasat",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                } else if (isButtonClicked(restartButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Restart\n";

                    restartLevel(
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences,
                        levelStartTime
                    );

                    levelSolved = false;
                    finalElapsedSeconds = 0;
                    playedLevels[currentLevel - 1] = true;

                    message = "Nivelul a fost restartat.";

                    printGuiStateToConsole(
                        "Buton Restart apasat",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                } else if (isButtonClicked(solveButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Solve\n";

                    if (levelSolved) {
                        message = "Nivel deja rezolvat. Apasa Next Level.";
                        cout << "Solver ignorat: nivelul este deja rezolvat.\n";
                    } else if (solveLevel(
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    )) {
                        message = "Solverul a gasit o solutie.";
                        playedLevels[currentLevel - 1] = true;
                        cout << "Solver: solutie gasita.\n";
                    } else {
                        message = "Solverul nu a gasit nicio solutie.";
                        cout << "Solver: nu a gasit solutie.\n";
                    }

                    printGuiStateToConsole(
                        "Buton Solve apasat",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                } else if (isButtonClicked(nextButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Next Level\n";

                    goNextLevelGui(
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences,
                        levelStartTime,
                        message
                    );

                    levelSolved = false;
                    finalElapsedSeconds = 0;
                    playedLevels[currentLevel - 1] = true;

                    printGuiStateToConsole(
                        "Buton Next Level apasat",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                } else if (isButtonClicked(levelsButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Levels\n";

                    showLevelsPanel = true;
                    showScoresPanel = false;
                    message = "Alege un nivel din panou.";
                } else if (isButtonClicked(scoresButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Scores\n";

                    guiScores = loadScoresForGui();
                    showScoresPanel = true;
                    showLevelsPanel = false;
                    message = "Scorurile sunt afisate pe ecran.";

                    displayScores();
                } else if (isButtonClicked(exitButton, mouseX, mouseY)) {
                    cout << "Buton apasat: Exit\n";
                    cout << "Joc inchis.\n";

                    window.close();
                } else {
                    if (levelSolved) {
                        message = "Nivel deja rezolvat. Apasa Next Level.";
                        cout << "Mutare ignorata: nivelul este deja rezolvat.\n";
                    } else {
                        bool added = handleMouseClickOnBoard(
                            mouseX,
                            mouseY,
                            moves,
                            moveCount,
                            maxAllowedFences,
                            verticalFences,
                            horizontalFences
                        );

                        if (added) {
                            message = "Gard adaugat.";
                            playedLevels[currentLevel - 1] = true;

                            printGuiStateToConsole(
                                "Gard adaugat de jucator",
                                currentLevel,
                                board,
                                verticalFences,
                                horizontalFences,
                                moveCount,
                                maxAllowedFences
                            );
                        } else {
                            message = "Click invalid sau limita de garduri atinsa.";
                            cout << "Click invalid sau limita de garduri atinsa.\n";
                        }
                    }
                }
            }

            if (event.type == sf::Event::KeyPressed) {
                if (event.key.code == sf::Keyboard::Escape) {
                    showScoresPanel = false;
                    showLevelsPanel = false;
                    cout << "Tasta apasata: ESC - inchidere panouri.\n";
                }

                if (event.key.code == sf::Keyboard::U) {
                    cout << "Tasta apasata: U - Undo\n";

                    undoMove(
                        moves,
                        moveCount,
                        verticalFences,
                        horizontalFences
                    );

                    levelSolved = false;
                    finalElapsedSeconds = 0;
                    levelStartTime = time(0);

                    message = "Ultima mutare a fost anulata. Timpul a fost resetat.";

                    printGuiStateToConsole(
                        "Tasta U apasata - Undo",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                }

                if (event.key.code == sf::Keyboard::R) {
                    cout << "Tasta apasata: R - Restart\n";

                    restartLevel(
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences,
                        levelStartTime
                    );

                    levelSolved = false;
                    finalElapsedSeconds = 0;
                    playedLevels[currentLevel - 1] = true;

                    message = "Nivelul a fost restartat.";

                    printGuiStateToConsole(
                        "Tasta R apasata - Restart",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                }

                if (event.key.code == sf::Keyboard::C) {
                    cout << "Tasta apasata: C - Check\n";

                    if (checkSolution(board, verticalFences, horizontalFences)) {
                        if (!levelSolved) {
                            finalElapsedSeconds =
                                static_cast<int>(time(0) - levelStartTime);

                            saveScore(
                                currentLevel,
                                moveCount,
                                finalElapsedSeconds
                            );

                            levelSolved = true;
                            playedLevels[currentLevel - 1] = true;
                        }

                        message = "Solutie corecta! Scor salvat. Apasa Next Level.";

                        cout << "Rezultat verificare: solutie corecta.\n";
                        cout << "Timp final: "
                             << finalElapsedSeconds
                             << " secunde.\n";
                    } else {
                        message = "Solutia NU este corecta.";
                        cout << "Rezultat verificare: solutie incorecta.\n";
                    }

                    printGuiStateToConsole(
                        "Tasta C apasata - Check",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                }

                if (event.key.code == sf::Keyboard::S) {
                    cout << "Tasta apasata: S - Solve\n";

                    if (levelSolved) {
                        message = "Nivel deja rezolvat. Apasa Next Level.";
                        cout << "Solver ignorat: nivelul este deja rezolvat.\n";
                    } else if (solveLevel(
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    )) {
                        message = "Solverul a gasit o solutie.";
                        playedLevels[currentLevel - 1] = true;
                        cout << "Solver: solutie gasita.\n";
                    } else {
                        message = "Solverul nu a gasit nicio solutie.";
                        cout << "Solver: nu a gasit solutie.\n";
                    }

                    printGuiStateToConsole(
                        "Tasta S apasata - Solve",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                }

                if (event.key.code == sf::Keyboard::N) {
                    cout << "Tasta apasata: N - Next Level\n";

                    goNextLevelGui(
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences,
                        levelStartTime,
                        message
                    );

                    levelSolved = false;
                    finalElapsedSeconds = 0;
                    playedLevels[currentLevel - 1] = true;

                    printGuiStateToConsole(
                        "Tasta N apasata - Next Level",
                        currentLevel,
                        board,
                        verticalFences,
                        horizontalFences,
                        moveCount,
                        maxAllowedFences
                    );
                }
            }
        }

        int elapsedSeconds = levelSolved
            ? finalElapsedSeconds
            : static_cast<int>(time(0) - levelStartTime);

        window.clear(sf::Color(160, 220, 160));

        drawBoard(
            window,
            board,
            verticalFences,
            horizontalFences,
            cowTexture,
            sheepTexture,
            pigTexture,
            horseTexture
        );

        sf::Text title;
        title.setFont(font);
        title.setString("Smart Farmer 2D");
        title.setCharacterSize(32);
        title.setFillColor(sf::Color::Black);
        title.setPosition(70.f, 15.f);
        window.draw(title);

        sf::Text info;
        info.setFont(font);
        info.setCharacterSize(20);
        info.setFillColor(sf::Color::Black);
        info.setString(
            "Nivel: " + to_string(currentLevel) +
            "   Garduri: " + to_string(moveCount) + "/" +
            to_string(maxAllowedFences) +
            "   Timp: " + to_string(elapsedSeconds) + "s"
        );
        info.setPosition(70.f, 475.f);
        window.draw(info);

        sf::Text messageText;
        messageText.setFont(font);
        messageText.setCharacterSize(18);
        messageText.setFillColor(sf::Color::Black);
        messageText.setString(message);
        messageText.setPosition(70.f, 510.f);
        window.draw(messageText);

        drawButton(window, checkButton);
        drawButton(window, undoButton);
        drawButton(window, restartButton);
        drawButton(window, solveButton);
        drawButton(window, nextButton);
        drawButton(window, levelsButton);
        drawButton(window, scoresButton);
        drawButton(window, exitButton);

        if (showScoresPanel) {
            drawScoresPanel(window, font, guiScores);
        }

        if (showLevelsPanel) {
            drawLevelsPanel(window, font, playedLevels, currentLevel);
        }

        window.display();
    }
}