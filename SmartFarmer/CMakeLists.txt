cmake_minimum_required(VERSION 4.2)
project(SmartFarmer)

set(CMAKE_CXX_STANDARD 20)
set(SFML_DIR "D:/Fisiere/CLion 2026.1.1/SFML-2.6.1/lib/cmake/SFML")

find_package(SFML 2.6 COMPONENTS graphics window system REQUIRED)

add_executable(SmartFarmer main.cpp
        Constants.h
        Animal.cpp
        Animal.h
        Move.h
        LevelManager.cpp
        LevelManager.h
        Board.cpp
        Board.h
        Solver.cpp
        Solver.h
        Game.cpp
        Game.h
        GuiGame.cpp
        GuiGame.h
)

target_link_libraries(SmartFarmer
        sfml-graphics
        sfml-window
        sfml-system
)