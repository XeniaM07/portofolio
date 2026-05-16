#ifndef ANIMAL_H
#define ANIMAL_H

enum Animal {
    EMPTY,
    COW,
    SHEEP,
    PIG,
    HORSE
};

char animalToChar(Animal animal);
Animal charToAnimal(char ch);

#endif