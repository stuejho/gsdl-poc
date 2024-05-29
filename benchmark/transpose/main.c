#include "benchmark.h"
#include "util.h"

int main(void) {
    check_correctness(benchmark);
    benchmark_impl(benchmark);
    return 0;
}