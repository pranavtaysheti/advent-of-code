// inspired from go slices

// Exit/ Return error codes
// 1 -> malloc failed
// 2 -> size of elem to add to list does not match
// 3 -> invalid position

#include "VLA.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int makeVLA(size_t elemSize, int initCap, VLA* out) {
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
int add(VLA* vla, void* elem) {
    if (vla->len == vla->cap) {
        void* newArray = realloc(vla->array, (vla->cap * 2) * (vla->elemSize));
        if (newArray == NULL) {
            fprintf(stderr, "add: malloc for newArray failed.");
            return 1;
        }

        int newCap = (vla->cap == 0) ? 1 : vla->cap * 2;
        vla->cap = newCap;
        vla->array = newArray;
    }

    char* base = (char*)vla->array;
    memcpy(base + (vla->len * vla->elemSize), elem, vla->elemSize);
    vla->len++;
    return 0;
}

int insert(VLA* vla, int idx, void* elem) {
    if (vla->len <= idx || idx < 0) {
        fprintf(stderr, "insert: Index out of bound.");
        return 3;
    }

    char* base = (char*)vla->array;
    memcpy(base + (vla->elemSize * idx), elem, vla->elemSize);
    return 0;
}

int at(VLA* vla, int idx, void* out) {
    if (idx >= vla->len) {
        fprintf(stderr, "at: Index out of bound.");
        return 3;
    }

    char* base = (char*)vla->array;
    memcpy(out, base + (vla->elemSize * idx), vla->elemSize);
    return 0;
}

void del(VLA* vla) {
    free(vla->array);
    vla->array = NULL;
    vla->len = 0;
    vla->cap = 0;
}