# Cplus-Profiler
Simple, easy to use and fast C++ class for profiling and benchmark

Author: Simone Magnani - s41m0n

## Usage

In order to gather data, the user is required to insert the macro `CHECKPOINT(<NAME>)` in all the code fragments he wants to measure the execution time.

Once established all the capture points, the macro `ENDPOINT(<NAME>)` not only performs the last measurement, but it also stores the gathered data into a simple file.

```c++
...
CHECKPOINT("A")

someFunctions();

CHECKPOINT("B")

otherFunctions();

ENDPOINT("C")
...
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