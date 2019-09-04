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

#endif //__PROFILER__
