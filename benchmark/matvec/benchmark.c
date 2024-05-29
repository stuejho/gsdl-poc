#include "benchmark.h"
#include "constants.h"

void benchmark(float *A, float *x, float *y) {
for (int ii_231 = 0; ii_231 < 0 + 4; ii_231 += 1) {
    for (int jj_163 = 0; jj_163 < 0 + 4; jj_163 += 1) {
        for (int j = jj_163; j < jj_163 + 1; j++) {
            for (int i = ii_231; i < ii_231 + 1; i++) {
                y[i] += A[i * N + j * 1] * x[j];
            }
        }
    }
}
}
