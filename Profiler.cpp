//
// Created by s41m0n on 05/09/19.
//
#include "Profiler.h"

Profiler::Profiler() {
  for (int i = 0; i < WARM_UP; i++) {
    tick();
  }
  results.clear();
}

void Profiler::store() {
  std::ofstream outputFile;
  outputFile.open(OUTPUT_FILE, std::ios::out);
  std::for_each(results.begin(), results.end(), [this, &outputFile](auto &res) -> void {
      outputFile << res.first.first << "," << res.first.second << ":" << res.second.time_since_epoch().count() << std::endl;
  });
  outputFile.close();
  results.clear();
}

void Profiler::tick(const char *filename, unsigned line_number) {
  results.emplace_back(
          std::make_pair(std::make_pair(filename, line_number), std::chrono::high_resolution_clock::now()));
}
