#define PROFILER

#include "Profiler.h"

#define N_ITER 100

int main(int argc, char **argv) {

  //Benchmarking
  for(auto i=0; i<N_ITER; i++) {
    CHECKPOINT
  }

  STOREPOINT
  return 0;
}