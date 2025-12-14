#include "primefactors.h"

#include <math.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdlib.h>

#define DIVIDE_REPEATED(factor)         \
    {                                   \
        if (num % factor == 0) {        \
            (*out)[cIdx++] = factor;    \
            while (num % factor == 0) { \
                num /= factor;          \
            }                           \
        }                               \
    }

size_t primeFactors(unsigned int num, int** out) {
    // product of first 13 prime factor 2..41 is larger than 2^32-1
    *out = (int*)malloc(sizeof(int) * 13);
    if (*out == NULL) return 0;
    int cIdx = 0;

    DIVIDE_REPEATED(2);

    for (int i = 3; (unsigned long long)(i * i) <= num; i += 2) {
        DIVIDE_REPEATED(i);
    }

    if (num > 1) {
        (*out)[cIdx++] = num;
    }

    return cIdx;
}