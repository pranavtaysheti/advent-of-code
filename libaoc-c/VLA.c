// inspired from go slices

// Exit/ Return error codes
// 1 -> malloc failed
// 2 -> size of elem to add to list does not match
// 3 -> invalid position

// In general, this library is VERY Quick and Dirty.
// EXTREMELY unsafe and for this project's use only.

#include "VLA.h"

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

VLA_Error makeVLA(size_t elemSize, size_t initCap, VLA* out) {
    *out = (VLA){
        .elemSize = elemSize,
        .len = 0,
        .cap = initCap,
        .array = NULL,
    };

    void* newArray = malloc(elemSize * initCap);
    if (newArray == NULL) {
        fprintf(stderr, "makeVLA: malloc for newArray failed.");
        return 1;
    }

    out->array = newArray;
    return 0;
}

// Note: the array member of VLA may get reallocated. when element is added
VLA_Error appendVLA(VLA* vla, void* elem) {
    if (vla->len == vla->cap) {
        size_t newCap = (vla->cap == 0) ? 1 : vla->cap * 2;
        void* newArray = realloc(vla->array, newCap * (vla->elemSize));
        if (newArray == NULL) {
            fprintf(stderr, "appendVLA: malloc for newArray failed.");
            return 1;
        }

        vla->cap = newCap;
        vla->array = newArray;
    }

    char* base = (char*)vla->array;
    memcpy(base + (vla->len * vla->elemSize), elem, vla->elemSize);
    vla->len++;
    return 0;
}

// Safety warning: its assumed src->elemSize == dest->elemSize
VLA_Error extendVLA(VLA* dest, VLA* src) {
    if (src->elemSize != dest->elemSize) {
        return 2;
    }

    for (size_t i = 0; i < src->len; i++) {
        int err = appendVLA(dest, (src->array) + (i * src->elemSize));
        if (err > 0) {
            fprintf(stderr, "extendVLA: error appending to dest VLA.");
            return err;
        }
    }

    return 0;
}

void delVLA(VLA* vla) {
    free(vla->array);
    vla->array = NULL;
    vla->len = 0;
    vla->cap = 0;
    vla->elemSize = 0;
}