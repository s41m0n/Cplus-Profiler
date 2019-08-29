# Cplus-Profiler
Simple, easy to use and fast C++ class for profiling and benchmark

Author: Simone Magnani - s41m0n

## Usage

In order to gather data, the user is required to insert the macro `CHECKPOINT(<NAME>);` in all the code fragments he wants to measure the execution time.

Once established all the capture points, the macro `ENDPOINT(<NAME>)` not only performs the last measurement, but it also stores the gathered data into a simple file.

```c++
...
CHECKPOINT("A");

someFunctions();

CHECKPOINT("B");

otherFunctions();

ENDPOINT("C");
...
```

Since the stored timestamp refers to the start of the epoch, to beautify the data and print some statistics the user can use `compute.py <result_file_name>`.