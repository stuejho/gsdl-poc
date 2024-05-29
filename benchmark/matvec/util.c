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

void check_correctness(void (*mat_vec_func)(float *, float *, float *))
{
    int mat_row_size = M;
    int mat_col_size = N;
    int x_size = N;
    int y_size = M;

    // Baseline
    float *A_base = malloc(sizeof(float) * (mat_row_size * mat_col_size));
    float *x_base = malloc(sizeof(float) * (x_size));
    float *y_base = malloc(sizeof(float) * (y_size));

    init_arr_index(A_base, mat_row_size * mat_col_size);
    init_arr_value(x_base, x_size, 1);
    init_arr_value(y_base, y_size, 0);

    base_mat_vec(A_base, x_base, y_base);

    // Benchmark
    float *A_bench = malloc(sizeof(float) * (mat_row_size * mat_col_size));
    float *x_bench = malloc(sizeof(float) * (x_size));
    float *y_bench = malloc(sizeof(float) * (y_size));

    init_arr_index(A_bench, mat_row_size * mat_col_size);
    init_arr_value(x_bench, x_size, 1);
    init_arr_value(y_bench, y_size, 0);

    mat_vec_func(A_bench, x_bench, y_bench);

    // Check
    int passed = 1;
    for (int i = 0; i < y_size; i++)
    {
        float diff = fabs(y_base[i] - y_bench[i]);
        if (diff > THRESHOLD)
        {
            fprintf(stderr, "Error: y_base[%d] = %f != y_bench[%d] = %f\n", i, y_base[i], i, y_bench[i]);
            passed = 0;
        }
    }

    free(A_base);
    free(x_base);
    free(y_base);

    free(A_bench);
    free(x_bench);
    free(y_bench);

    if (passed == 0)
    {
        exit(1);
    }
    fprintf(stderr, "PASS!\n");
}

void benchmark_impl(void (*mat_vec_func)(float *, float *, float *)) {
    int mat_row_size = M;
    int mat_col_size = N;
    int x_size = N;
    int y_size = M;

    float *A = malloc(sizeof(float) * (mat_row_size * mat_col_size));
    float *x = malloc(sizeof(float) * (x_size));
    float *y = malloc(sizeof(float) * (y_size));

    init_arr_index(A, mat_row_size * mat_col_size);
    init_arr_value(x, x_size, 1);
    init_arr_value(y, y_size, 0);

    // Initialize the start and stop variables.
    TIMER_INIT_COUNTERS(stop, start);

    // Click the timer a few times so the subsequent measurements are more accurate
    TIMER_WARMUP(stop, start);

    // flush the cache
    flush_cache();

//    printf("A initial\n");
//    print_mat(A, mat_row_size, mat_col_size);
//    printf("x initial\n");
//    print_vec(x, y_size);
//    printf("y initial\n");
//    print_vec(y, y_size);

    unsigned long long int total_time = 0LL;
    for (int i = 0; i < NUM_RUNS; i++) {
        init_arr_value(y, y_size, 0);

        // Start timer
        TIMER_GET_CLOCK(start);

        mat_vec_func(A, x, y);

        // Stop timer
        TIMER_GET_CLOCK(stop);

        long diff;
        TIMER_GET_DIFF(start, stop, diff);
        total_time += diff;

    }

    fprintf(stderr, "Total (ns),Average (ns)\n");
    printf("\"%llu\",\"%f\"\n", total_time, (float) total_time / NUM_RUNS);

    free(A);
    free(x);
    free(y);
}
