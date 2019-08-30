# Cplus-Profiler
Simple, easy to use and fast C++ header class for profiling and benchmark

Author: Simone Magnani - s41m0n

## Introduction

## How it works

The framework defines two different main components:

* Check-point: `CHECKPOINT`
* Store-point: `STOREPOINT`

A check-point is a point of the code where we simply want to take a measure (timestamp).
A store-point is a specialized check-point which not only acts like it, but it also manage the data storing into a file.

While the usage of a check-point leads to a negligible overhead(\~60 nanoseconds), it is suggested to wisely use especially the store-points, since the I/O operation on file are more expensive.

Every measure is characterized by the identifier:

* filename
* line of code
* timestamp (nanoseconds)

Thanks to this implementation, the user is not required to name each capture point, since they are clear enough.

## Usage

To insert these points into the code, the user have just to insert their specific MACRO.
To remove them, comment the line or remove it.

In order to gather data, the user is required to insert the macro `CHECKPOINT` in all the code fragments he wants to get the timestamp.

Once decided the place where the user want to permanently save the retrieved data into a file, insert the macro `STOREPOINT`. 


## Example 

```c++
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
```

Example of `result.txt`:

```txt
'A':1567157376902525016
'B':1567157376902525111
'C':1567157376902525272
```

Since the stored timestamps refer to the start of the epoch, to beautify the data and print some statistics the user can use `compute.py <result_file_name>` to achieve the following result:

```python
Max execution time: 161
Min execution time: 95
Avg execution time: 128.0
'A'=>'B': 95 ns
'B'=>'C': 161 ns
```

## Performance analysis


```
1) Add a brief section to the idea behind checkpoints (so, how this feature should be used, to do what). ALso specify the difference between this and "perf" in Linux.
2) Add some performance numbers, as I feel somebody may be upset to see so much C++ code (and classes), unless you show that the overhead is so tiny.
Btw, it is not clear how the overhead increases if we have more checkpoints (do we have to operate on string; are these operations costly if we have so many strings?) (edited) 
```