#ifndef UTIL_H
#define UTIL_H

void flush_cache();

void init_arr_index(float *arr, int num_elems);

void init_arr_value(float *arr, int num_elems, float value);

void print_mat(float *mat, int num_rows, int num_cols);

void print_vec(float *vec, int num_elems);

void check_correctness(void (*mat_vec_func)(float *, float *, float *));

void benchmark_impl(void (*mat_vec_func)(float *, float *, float *));

#endif
