#ifndef VLA_H_
#define VLA_H_

#include <stddef.h>

enum VLA_Error {
    VLA_OK = 0,
    VLA_MALLOC_FAIL = 1,
    VLA_ELEM_SIZE_MISMATCH = 2,
};
typedef enum VLA_Error VLA_Error;

struct VLA {
    void* array;
    size_t elemSize;
    size_t len;
    size_t cap;
};
typedef struct VLA VLA;

VLA_Error makeVLA(size_t elemSize, size_t initCap, VLA* out);
VLA_Error appendVLA(VLA* vla, void* elem);
VLA_Error extendVLA(VLA* dest, VLA* src);
void delVLA(VLA* vla);

#endif