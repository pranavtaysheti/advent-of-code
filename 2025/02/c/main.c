#include <stdio.h>
#include <stdlib.h>

#include "VLA.h"
#include "primefactors.h"

struct IDRange {
    int start;
    int end;
};
typedef struct IDRange IDRange;

int parse(VLA* out) {
    makeVLA(sizeof(IDRange), 10, out);

    IDRange cIDRange;
    while (scanf("%d-%d,", &cIDRange.start, &cIDRange.end) == 2) {
        appendVLA(out, &cIDRange);
    }

    return 0;
}

int main() {
    VLA data;
    parse(&data);

    return 0;
}
