# Smart Farmer 2D

Smart Farmer 2D is a C++ implementation of the Smart Farmer logic puzzle game, inspired by the original board game from SmartGames.

This project was initially developed during the first year of university as part of a faculty assignment.  
After the academic project was completed, the codebase was refactored and extended in order to improve the architecture, add new features, and create a cleaner and more polished version of the game.

## Project Features

- Full playable Smart Farmer game
- Graphical interface using SFML
- Animal textures and visual game board
- Multiple custom levels loaded from files
- Automatic optimal solver using backtracking
- Undo functionality
- Timer and score system
- Saved scores using files
- Level selection panel
- Console logging for debugging and verification
- Progressive difficulty system

## Technologies Used

- C++
- SFML 2.6.1
- CMake

## Game Rules

The objective of the game is to place fences in such a way that:
- animals of the same type remain together;
- different animal types are separated into different regions.

## Solver

The automatic solver uses an optimal backtracking approach.

Instead of stopping at the first valid solution, the algorithm searches incrementally:
- first with 0 fences;
- then with 1 fence;
- then with 2 fences;
- etc.

The first valid solution found is guaranteed to use the minimum possible number of fences.

## Project Structure

```text
assets/             -> textures and font
Board.*             -> board logic and validation
Solver.*            -> automatic optimal solver
LevelManager.*      -> level loading
GuiGame.*           -> graphical interface
Game.*              -> console game logic