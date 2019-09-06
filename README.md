# Cplus-Profiler
Simple, easy to use and fast C++ header class for profiling and benchmark.

Author: Simone Magnani - s41m0n

## Introduction

This framework is born to accomplish an efficient measurement of user's programs. More in detail, there already are hundreds of tools (especially in Linux) to perform benchmarks and profiling, but I noticed that they sometimes are too hard to learn and they may not meet users' needs.

A worth-mentioning tool is [perf](https://perf.wiki.kernel.org/index.php/Main_Page). Perf is a Linux profiling tool with performance counters which helps users to understand at low-level how not only the program, but also the hardware behaves. As the wiki reports, this tool not only is quite complex to learn, but it also produces deep information that users may not use or that they have to aggregate them to achieve a readable result. Moreover, perf refers to different types of event (ex. I/O disk) users may not be interested in.

CPlus-Profiler provides a simple to use method not only to run a whole program benchmark, but also to measure single code-fragments performance.

## How it works

The framework defines two different main components:

* Check-point: `CHECKPOINT`
* Store-point: `STOREPOINT`

A check-point is a point of the code where we simply want to take a measure (timestamp).
A store-point is a specialized check-point which not only acts like it, but it also manages the data storing into a file.

While the usage of a check-point leads to a negligible overhead (\~60 nanoseconds), it is suggested to use wisely the store-points, since the I/O operation on file are more expensive.

Each measure is characterized by:

* filename: the name of the file which contains the check-point;
* line of code: the line of code where the check-point has been inserted;
* timestamp: the measure in *nanoseconds* taken.

Accordingly, the format used to store check-points is: `<filename>,<line_of_code>:<timestamp>`.

## Usage

The framework is activated by defining `#define PROFILER` in your code (wherever the user wants) but **before** the library inclusion. Without this definition, the framework will be automatically turned off for all the execution.

Possible operations:
* to insert Check-points, the user have just to insert the MACRO `CHECKPOINT`.
* to insert Store-points, insert the MACRO `STOREPOINT`.
* to remove them, comment the apposite line or remove it.

An interesting feature is that in case the user deactivates the framework, it is not required to remove every checkpoints he had previously inserted in the code: the framework will handle it by replacing them with an empty line!

## Example 

In this simple program we want to measure the performance of our function to compute the square of a number. We insert two check-points between the functions call and a final store-point at the end.

```c++
#define PROFILER

#include "Profiler.h"

int main(int argc, char **argv) {

  CHECKPOINT 				//line 7
  computeSquare(1);
  CHECKPOINT   			//line 9
  computeSquare(2);
  STOREPOINT 				//line 11
  return 0;
}
```

After the execution, we obtain the following `profile(Sep  2 2019,18:18:47)` file:

```txt
main.cpp,7:1567333232104876595
main.cpp,9:1567333232104876666
main.cpp,11:1567333232104876737
```

Since the stored timestamps refer to the start of the epoch, to beautify the data and print some statistics we use our script `compute.py`:

```bash
$ python compute.py profiler_result.txt --show-all

Checkpoint(main.cpp,7,0) to Checkpoint(main.cpp,9,0): 71 ns
Checkpoint(main.cpp,9,0) to Checkpoint(main.cpp,11,0): 71 ns
Max execution time: 71 ns
Min execution time: 71 ns
Avg execution time: 71.0 ns
```

The format `Checkpoint(main.cpp,7,0)` means that the point has been inserted in the file main.cpp at line 7. The third element is an identifier, given appositely by the python script to distinguish check-points inserted in the same line of code (ex. in a loop).

## Performance analysis

For this analysis, tests have been run on a Dell Xps 9570. Please consider that results are different depending on your processors and the available CPU.

I used the `main.cpp` file in this project which creates consecutively 100 check-points and a final store-point. The check-points are inserted inside a loop and there is not any other function call except for the check-points themselves. The aim of this program is to measure the time taken by each `CHECKPOINT` to perform and save the single measurement. The final store-points has not been taken into account in the performance analysis result, since the BPU (branch predictor unit) of our processors would probably fail the prediction of the last loop cycle (which has to exit the loop), leading to some small delay due to the exit from the loop.

```bash
Max execution time: 69 ns
Min execution time: 46 ns
Avg execution time: 49.515151515151516 ns
```

These results are really significant and they prove that the overhead added by the framework is completely small and do not interfere with the performance of our programs.
