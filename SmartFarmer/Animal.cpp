#include "Animal.h"

char animalToChar(Animal animal) {
    switch (animal) {
        case COW: return 'C';
        case SHEEP: return 'S';
        case PIG: return 'P';
        case HORSE: return 'H';
        default: return '.';
    }
}

Animal charToAnimal(char ch) {
    switch (ch) {
        case 'C': return COW;
        case 'S': return SHEEP;
        case 'P': return PIG;
        case 'H': return HORSE;
        default: return EMPTY;
    }
}