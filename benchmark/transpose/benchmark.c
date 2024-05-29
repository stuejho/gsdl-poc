#include "benchmark.h"
#include "constants.h"

void benchmark(float *src, float *dest) {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            dest[j * M + i] = src[i * N + j];
        }
    }
}
