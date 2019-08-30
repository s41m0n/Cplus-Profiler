import sys
import re

checkpoints = []
duration = []
pattern = '(.*):(\\d+)'

def readFile(filename):
  try:
    lines = open(filename, 'r').readlines()
    if len(lines) == 0:
        raise IOError()
  except IOError:
    print('Error: no such file \'' + sys.argv[1] + '\' or empty')
    exit()
  first = True
  previous = 0
  counter = 1
  for line in lines:
    match = re.match(pattern, line, flags=0)
    # Ha matchato l'inizio del benchmark
    if match:
      if first is True:
        first = False
      else:
        duration.append(int(match.group(2)) - previous)
      newCheckpoint = match.group(1)[match.group(1).rfind('/')+1:]
      #Loop detector
      if len(checkpoints) != 0 and newCheckpoint == checkpoints[-1][:len(newCheckpoint)]:
        newCheckpoint += ", " + str(counter)
        counter += 1
      else:
        counter = 1
        newCheckpoint += ", 0"
      checkpoints.append(newCheckpoint)
      previous = int(match.group(2))
    else:
      print('File badly formatted (\'<CHECKPOINTNAME>\':<timestamp>)')
      exit()


def showUsage():
  print("compute.py <filename>")
  print("\t-h/--help: show the usage menu")
  print("\t--show-each: show duration between checkpoints")

def main():
  if len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help":
    showUsage()
    exit()

  readFile(sys.argv[1])
  print("Max execution time: " + str(max(duration)))
  print("Min execution time: " + str(min(duration)))
  print("Avg execution time: " + str(sum(duration)/len(duration)))
  if len(sys.argv) >= 3 and sys.argv[2] == "--show-each":
    for count, item in enumerate(checkpoints[:-1]):
      print("Checkpoint(" + item + ") to Checkpoint(" + checkpoints[count+1] + "): " + str(duration[count]) + " ns")

if __name__== '__main__':
  main()