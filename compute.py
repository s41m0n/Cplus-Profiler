#!/usr/bin/env python

"""
Utility script to parse output from Profiler framework and print statistics.

This is a script with the aim of printing in a more human-readable format
information previously gathered by the framework.

Usage: profiler_parse.py <filename> [<FLAGS>]
    -h/--help: show the usage menu
    -s/--show-all: show duration between checkpoints
"""

import sys
import re

#Support variables
previousTimestamp = 0
identifiers = []
checkpoints = []
duration = []
#Pattern to match. The framework's output file is: 
#<filename>,<line_of_code>:<timestamp>
pattern = '(\\S+),(\\d+):(\\d+)'

#Function to parse a matched line
def parseMatch(match, number):
  global previousTimestamp, identifiers, checkpoints, duration
  #Used last string from '/' since the __FILE__ macro in C
  #could contain the entire path
  checkpointName = match.group(1)[match.group(1).rfind('/')+1:] + ',' + match.group(2)
  timestamp = int(match.group(3))
  #Skip the first Checkpoint since duration would be meaningless (=0)
  if number != 0:
    duration.append(timestamp - previousTimestamp)
  identifiers.append(checkpoints.count(checkpointName))
  checkpoints.append(checkpointName)
  previousTimestamp = timestamp

#Function to read the specified file
def readFile(filename):
  global identifiers, checkpoints

  try:
    lines = open(filename, 'r').readlines()
    if len(lines) == 0:
        raise IOError()
  except IOError:
    print('Error: no such file \'' + sys.argv[1] + '\' or empty')
    exit()
  #Foreach line read, parse it and update data structures
  for line_number, line in enumerate(lines):
    match = re.match(pattern, line, flags=0)
    if match:
      parseMatch(match, line_number)
    else:
      print("Error while parsing line " + str(line_number) + ": " + line)
      print("Is it compliant with the format <filename>,<line_of_code>:<timestamp> ?")
      exit()

  #Add Checkpoint identifier incrementally calculated.
  #Useful when more Checkpoints/Storepoints in the same Line of code and file
  for count, id in enumerate(identifiers):
    checkpoints[count] += "," + str(id)

#Function to print script usage
def showUsage():
  print("compute.py <filename> [<FLAGS>]")
  print("\t-h/--help: show the usage menu")
  print("\t-s/--show-all: show also duration between checkpoints")

def main():
  global checkpoints, duration

  #Checking arguments
  if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    showUsage()
    exit()

  readFile(sys.argv[1])
  #Checking whether to display all point-to-point distances or not
  if len(sys.argv) >= 3 and (sys.argv[2] == "--show-all" or sys.argv[2] == "-s"):
    for count, item in enumerate(checkpoints[:-1]):
      print("Checkpoint(" + item + ") to Checkpoint(" + checkpoints[count+1] + "): " + str(duration[count]) + " ns")

  #Printing statistics
  print("Max execution time: " + str(max(duration)) + " ns")
  print("Min execution time: " + str(min(duration)) + " ns")
  print("Avg execution time: " + str(sum(duration)/len(duration)) + " ns")

if __name__== '__main__':
  main()