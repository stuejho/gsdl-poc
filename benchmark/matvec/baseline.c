#include "baseline.h"
#include "constants.h"

void base_mat_vec(float *A, float *x, float *y) {
    for (int i = 0; i < M; i++) {
        for (int j = 0; j < N; j++) {
            y[i] += A[i * N + j] * x[j];
        }
    }
}
