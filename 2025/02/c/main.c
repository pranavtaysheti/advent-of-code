#include <stdio.h>
#include <stdlib.h>

#include "VLA.h"
#include "hashmap.h"
#include "primefactors.h"

struct IDRange {
    unsigned int start;
    unsigned int end;
};
typedef struct IDRange IDRange;

int digits(unsigned int num) {
    int curr = 1;
    int res = 1;
    while (curr < num) {
        curr *= 10;
        res++;
    }

    return res;
}

int splitRange(IDRange* idr, IDRange** out) {
    int minDigits = digits(idr->start);
    int maxDigits = digits(idr->end);

    *out = (IDRange*)malloc(sizeof(IDRange) * (maxDigits - minDigits + 1));

    int curr = idr->start;
    for (int cDigits = minDigits; cDigits <= maxDigits; cDigits++) {
        int maxNumCurrDigits = 1;
        for (int i = 0; i < cDigits; i++) {
            maxNumCurrDigits *= 10;
        }

        maxNumCurrDigits - 1;

        unsigned int maxCurrRange =
            (maxNumCurrDigits < idr->end) ? maxNumCurrDigits : idr->end;

        size_t oIdx = cDigits - minDigits;
        (*out)[oIdx] = (IDRange){curr, maxCurrRange};

        curr = ++maxCurrRange;
    }

    return 0;
}

int fakeIDs(IDRange* idr, size_t (*lookLenSelector)(int len, VLA* out),
            VLA* out) {
    return 0;
}

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
