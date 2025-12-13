#ifndef VLA_H_
#define VLA_H_

#include <stddef.h>

struct VLA {
    void* array;
    size_t elemSize;
    int len;
    int cap;
};
typedef struct VLA VLA;

int makeVLA(size_t elemSize, int initCap, VLA* out);
int appendVLA(VLA* vla, void* elem);
int insert(VLA* vla, int pos, void* elem);
int at(VLA* vla, int idx, void* out);
void del(VLA* vla);

#endif