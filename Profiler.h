//
// Created by s41m0n on 30/07/19.
//
#ifdef PROFILER

#ifndef __PROFILER__
#define __PROFILER__


#include <iomanip>
#include <sstream>
#include <string>
#include <vector>
#include <chrono>
#include <algorithm>
#include <fstream>
#include <ctime>

#define WARM_UP 100

#define PROFILER_FILENAME "profile"
#define PROFILER_EXTENSION ".log"


#define CHECKPOINT Profiler::getInstance().tick(__FILE__, __LINE__);
#define STOREPOINT {CHECKPOINT Profiler::getInstance().store();}


/***
 * Profiler Singleton header class to measure execution time of certain functions
 */
class Profiler {

private:
    ///Private class constructor to avoid instantiation, includes a warm-up phase for the timer and cache loading
    Profiler();

    ///Support data structure
    std::vector<std::pair<std::pair<const char *, unsigned>, std::chrono::high_resolution_clock::time_point>> results;

    ///Final filename calculate at execution time
    std::string output_file;

public:
    /**
     * Function to be called before the `objective function` execution to store the initial timestamp
     * @param filename: the name of the file containing the checkpoint
     * @param request : checkpoint number
     */
    void tick(const char *filename = "", unsigned line_number = 0);

    ///Function called to store gathered data into a file
    void store();

    ///Singleton implementation, method to return the instance
    static Profiler &getInstance() {
      static Profiler instance;
      return instance;
    }
};

inline Profiler::Profiler() {
  auto now = time(nullptr);
  auto ltm = localtime(&now);

  output_file = dynamic_cast<std::ostringstream &>(std::ostringstream().seekp(0)
          << PROFILER_FILENAME << "(" << std::setw(4)
          << 1900 + ltm->tm_year << std::setfill('0') << std::setw(2)
          << ltm->tm_mon << std::setfill('0') << std::setw(2)
          << ltm->tm_mday << "_" << std::setfill('0') << std::setw(2)
          << ltm->tm_hour << std::setfill('0') << std::setw(2)
          <<ltm->tm_min << std::setfill('0') << std::setw(2)
          << ltm->tm_sec << ")" << PROFILER_EXTENSION).str();

  for (int i = 0; i < WARM_UP; i++) {
    tick();
  }
  results.clear();
}

inline void Profiler::store() {
  std::ofstream outputFile;
  outputFile.open(output_file, std::ios::app);
  std::for_each(results.begin(), results.end(), [this, &outputFile](auto &res) -> void {
      outputFile << res.first.first << "," << res.first.second << ":" << res.second.time_since_epoch().count() << std::endl;
  });
  outputFile.close();
  results.clear();
}

inline void Profiler::tick(const char *filename, unsigned line_number) {
  results.emplace_back(
          std::make_pair(std::make_pair(filename, line_number), std::chrono::high_resolution_clock::now()));
}


#endif //__PROFILER__

#else

#define CHECKPOINT
#define STOREPOINT

#endif //PROFILER
