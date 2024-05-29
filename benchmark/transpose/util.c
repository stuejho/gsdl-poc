#include <malloc.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#include "baseline.h"
#include "constants.h"
#include "util.h"

#define TIMER_INIT_COUNTERS(_start_, _stop_) \
  struct timeval _start_;                    \
  struct timeval _stop_;
#define TIMER_GET_CLOCK(_counter_) gettimeofday(&_counter_, NULL);
#define TIMER_GET_DIFF(_start_, _stop_, _diff_) _diff_ = ((_stop_.tv_sec - _start_.tv_sec) * 1e6 + _stop_.tv_usec - _start_.tv_usec); //* 1000 // <-- TODO: this 1000 should actually be derived like it is in memory mountatin

#define TIMER_WARMUP(_start_, _stop_) \
  {                                   \
    TIMER_GET_CLOCK(_start_);         \
    TIMER_GET_CLOCK(_stop_);          \
    TIMER_GET_CLOCK(_start_);         \
    TIMER_GET_CLOCK(_stop_);          \
    TIMER_GET_CLOCK(_start_);         \
    TIMER_GET_CLOCK(_stop_);          \
    TIMER_GET_CLOCK(_start_);         \
    TIMER_GET_CLOCK(_stop_);          \
  }

void flush_cache() {
    int size = 1024 * 1024 * 8;

    int *buff = (int *) malloc(sizeof(int) * size);
    int i, result = 0;
    volatile int sink;
    for (i = 0; i < size; i++)
        result += buff[i];
    sink = result; /* So the compiler doesn't optimize away the loop */

    free(buff);
}

void init_arr_index(float *arr, int num_elems) {
    for (int i = 0; i < num_elems; i++) {
        arr[i] = i;
    }
}

void init_arr_value(float *arr, int num_elems, float value) {
    for (int i = 0; i < num_elems; i++) {
        arr[i] = value;
    }
}

void print_mat(float *mat, int num_rows, int num_cols) {
    for (int i = 0; i < num_rows; i++) {
        print_vec(&mat[i * num_cols], num_cols);
    }
}

void print_vec(float *vec, int num_elems) {
    for (int i = 0; i < num_elems; i++) {
        printf("%f ", vec[i]);
    }
    printf("\n");
}

void check_correctness(void (*transpose_func)(float *, float *))
{
    int mat_row_size = M;
    int mat_col_size = N;
    int x_size = N;
    int y_size = M;

    // Baseline
    float *A_base = malloc(sizeof(float) * (mat_row_size * mat_col_size));
    float *B_base = malloc(sizeof(float) * (mat_row_size * mat_col_size));

    init_arr_index(A_base, mat_row_size * mat_col_size);
    init_arr_value(B_base, mat_row_size * mat_col_size, 0);

    base_transpose(A_base, B_base);

    // Benchmark
    float *A_bench = malloc(sizeof(float) * (mat_row_size * mat_col_size));
    float *B_bench = malloc(sizeof(float) * (mat_row_size * mat_col_size));

    init_arr_index(A_bench, mat_row_size * mat_col_size);
    init_arr_value(B_bench, mat_row_size * mat_col_size, 0);

    transpose_func(A_bench, B_bench);

    // Check
    int passed = 1;
    for (int i = 0; i < M; i++)
    {
        for (int j = 0; j < N; j++)
        {
            int idx = i * N + j;
            float diff = fabs(B_base[idx] - B_bench[idx]);
            if (diff > THRESHOLD)
            {
                fprintf(stderr, "Error: B_base[%d][%d] = %f != B_bench[%d][%d] = %f\n", i, j, B_base[idx], i, j, B_bench[idx]);
                passed = 0;
            }
        }
    }

    free(A_base);
    free(B_base);

    free(A_bench);
    free(B_bench);

    if (passed == 0)
    {
        exit(1);
    }
    fprintf(stderr, "PASS!\n");
}

void benchmark_impl(void (*transpose_func)(float *, float *)) {
    int mat_row_size = M;
    int mat_col_size = N;

    float *A = malloc(sizeof(float) * (mat_row_size * mat_col_size));
    float *B = malloc(sizeof(float) * (mat_row_size * mat_col_size));

    init_arr_index(A, mat_row_size * mat_col_size);
    init_arr_value(B, mat_row_size * mat_col_size, 0);

    // Initialize the start and stop variables.
    TIMER_INIT_COUNTERS(stop, start);

    // Click the timer a few times so the subsequent measurements are more accurate
    TIMER_WARMUP(stop, start);

    // flush the cache
    flush_cache();

    unsigned long long int total_time = 0LL;
    for (int i = 0; i < NUM_RUNS; i++) {
        init_arr_value(B, mat_row_size * mat_col_size, 0);

        // Start timer
        TIMER_GET_CLOCK(start);

        transpose_func(A, B);

        // Stop timer
        TIMER_GET_CLOCK(stop);

        long diff;
        TIMER_GET_DIFF(start, stop, diff);
        total_time += diff;
    }

    fprintf(stderr, "Total (ns),Average (ns)\n");
    printf("\"%llu\",\"%f\"\n", total_time, (float) total_time / NUM_RUNS);

    free(A);
    free(B);
}
