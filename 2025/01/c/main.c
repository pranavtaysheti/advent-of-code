#include <stdio.h>
#include <stdlib.h>

#include "libaoc/VLA.h"

const int DIAL_LEN = 100;
const int DIAL_START = 50;

enum Dir { dNone, dRight, dLeft };
typedef enum Dir Dir;

struct Ins {
    Dir dir;
    int rot;
};
typedef struct Ins Ins;

int parse(VLA* out) {
    makeVLA(sizeof(Ins), 10, out);

    Dir cDir = dNone;
    int cRot = 0;
    int cCol = 0;
    char cChar;

    while ((cChar = getchar()) != EOF) {
        if (cChar == '\n') {
            add(out, &(Ins){cDir, cRot});

            cRot = 0;
            cDir = dNone;
            cCol = 0;
            continue;
        }

        if (cCol == 0) {
            switch (cChar) {
            case 'R':
                cDir = dRight;
                break;

            case 'L':
                cDir = dLeft;
                break;
            }
        } else {
            cRot *= 10;
            cRot += cChar - 48;
        }

        cCol++;
    }

    return 0;
}

int rotateDial(VLA* data, int* out) {
    int curr = DIAL_START;
    for (int i = 0; i < data->len; i++) {
        Ins cIns = ((Ins*)data->array)[i];

        switch (cIns.dir) {
        case dRight:
            curr += cIns.rot;
            break;
        case dLeft:
            curr -= cIns.rot;
            break;
        }

        out[(i + 1) * 2 + 1] = curr;
        curr = ((curr % DIAL_LEN) + DIAL_LEN) % DIAL_LEN;
        out[(i + 1) * 2] = curr;
    }

    return 0;
}

int main() {
    VLA data;
    parse(&data);

    int* rotEnds = malloc(sizeof(int) * ((data.len + 1) * 2));
    rotEnds[0] = DIAL_START;
    rotEnds[1] = DIAL_START;

    rotateDial(&data, rotEnds);

    int P1 = 0;
    for (int i = 0; i < data.len; i++) {
        if (rotEnds[i * 2] == 0) {
            P1++;
        }
    }

    printf("P1: %d \n", P1);

    int P2 = P1;
    for (int i = 0; i < data.len; i++) {
        int nach = rotEnds[(i + 1) * 2 + 1];
        int vor = rotEnds[i * 2];

        Dir cDir = ((Ins*)data.array)[i].dir;
        switch (cDir) {
        case dRight:
            P2 += (nach - 1) / DIAL_LEN - vor / DIAL_LEN;
            break;
        case dLeft:
            P2 += (vor - 1 + 100 * DIAL_LEN) / DIAL_LEN -
                  (nach + 100 * DIAL_LEN) / DIAL_LEN;
            break;
        }
    }

    printf("P2: %d \n", P2);
    return 0;
}