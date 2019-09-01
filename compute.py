import sys
import re

previousTimestamp = 0
identifiers = []
checkpoints = []
duration = []
pattern = '(.*):(\\d+)'

def parseMatch(match, number):
  global previousTimestamp, identifiers, checkpoints, duration
  checkpointName = match.group(1)[match.group(1).rfind('/')+1:]
  timestamp = int(match.group(2))
  if number != 0:
    duration.append(timestamp - previousTimestamp)
  identifiers.append(checkpoints.count(checkpointName))
  checkpoints.append(checkpointName)
  previousTimestamp = timestamp

def readFile(filename):
  global identifiers, checkpoints
  try:
    lines = open(filename, 'r').readlines()
    if len(lines) == 0:
        raise IOError()
  except IOError:
    print('Error: no such file \'' + sys.argv[1] + '\' or empty')
    exit()
  for line_number, line in enumerate(lines):
    match = re.match(pattern, line, flags=0)
    if match:
      parseMatch(match, line_number)
  for count, id in enumerate(identifiers):
    checkpoints[count] += "," + str(id)

def showUsage():
  print("compute.py <filename>")
  print("\t-h/--help: show the usage menu")
  print("\t--show-each: show duration between checkpoints")

def main():
  if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    showUsage()
    exit()

  readFile(sys.argv[1])
  if len(sys.argv) >= 3 and sys.argv[2] == "--show-all":
    for count, item in enumerate(checkpoints[:-1]):
      print("Checkpoint(" + item + ") to Checkpoint(" + checkpoints[count+1] + "): " + str(duration[count]) + " ns")

  print("Max execution time: " + str(max(duration)) + " ns")
  print("Min execution time: " + str(min(duration)) + " ns")
  print("Avg execution time: " + str(sum(duration)/len(duration)) + " ns")

if __name__== '__main__':
  main()