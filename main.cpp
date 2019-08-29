#include "Profiler.h"

int main(int argc, char **argv) {

  //Benchmarking
  for(int i=0; i<100; i++) {
    CHECKPOINT("A");
  }
  ENDPOINT("C");

  return 0;
}