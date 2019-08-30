#include "Profiler.h"

#define N_ITER 100

int main(int argc, char **argv) {

  //Benchmarking
  for(int i=0; i<N_ITER; i++) {
    CHECKPOINT("A")
  }
  ENDPOINT("A")

  return 0;
}