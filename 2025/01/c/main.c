#include <stdio.h>

#include "libaoc/VLA.h"

const int DIAL_LEN = 100;

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
    int curr = 50;
    for (int i = 0; i < data->len; i++) {
        Ins cIns;
        at(data, i, &cIns);

        switch (cIns.dir) {
        case dRight:
            curr += cIns.rot;
            break;
        case dLeft:
            curr -= cIns.rot;
            break;
        }

        curr = ((curr % DIAL_LEN) + DIAL_LEN) % DIAL_LEN;
        out[i] = curr;
    }

    return 0;
}

int main() {
    VLA data;
    parse(&data);

    int rotEnds[data.len];
    rotateDial(&data, rotEnds);

    int P1 = 0;
    for (int i = 0; i < data.len; i++) {
        if (rotEnds[i] == 0) {
            P1++;
        }
    }

    printf("P1: %d \n", P1);

    int P2 = 0;
    for (int i = 0; i < data.len - 1; i++) {
        if (rotEnds[i] * rotEnds[i + 1] <= 0) {
            P2++;
        }
    }

    printf("P2: %d \n", P2);

    return 0;
}