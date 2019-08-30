//
// Created by s41m0n on 30/07/19.
//
#ifndef __PROFILER__
#define __PROFILER__

#include <vector>
#include <chrono>
#include <algorithm>
#include <fstream>

#define WARM_UP 100
#define OUTPUT_FILE "profiler_result.txt"

#ifdef PROFILER
#define CHECKPOINT(X) Profiler::getInstance().tick(X);
#define STOREPOINT(X) {CHECKPOINT(X) Profiler::getInstance().store();}
#else
#define CHECKPOINT(X)
#define STOREPOINT(X)
#endif

/***
 * Profiler Singleton header class to measure execution time of certain functions
 */
class Profiler {

private:
    ///Private class constructor to avoid instantiation, includes a warm-up phase for the timer and cache loading
    Profiler();

    ///Support data structure
    std::vector<std::pair<unsigned int, std::chrono::high_resolution_clock::time_point>> results;

public:
    /**
     * Function to be called before the `objective function` execution to store the initial timestamp
     * @param request : checkpoint number
     */
    void tick(unsigned int checkpoint_number = 0);

    ///Function called to store gathered data into a file
    void store();

#ifdef PROFILER
    ///Singleton implementation, method to return the instance
    static Profiler &getInstance() {
      static Profiler instance;
      return instance;
    }

#endif
};

inline Profiler::Profiler() {
  for (int i = 0; i < WARM_UP; i++) {
    tick();
  }
  results.clear();
}

inline void Profiler::store() {
  std::ofstream outputFile;
  outputFile.open(OUTPUT_FILE, std::ios::out);
  std::for_each(results.begin(), results.end(), [this, &outputFile](auto &res) -> void {
      outputFile << "'" << res.first << "':" << res.second.time_since_epoch().count() << std::endl;
  });
  outputFile.close();
  results.clear();
}

inline void Profiler::tick(unsigned int checkpoint_number) {
  results.emplace_back(std::make_pair(checkpoint_number, std::chrono::high_resolution_clock::now()));
}


#endif //__PROFILER__
