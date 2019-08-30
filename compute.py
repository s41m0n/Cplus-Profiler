import sys
import re

checkpoints = []
duration = []
pattern = '(.*):(\\d+)'

if len(sys.argv) == 1 or '.txt' not in sys.argv[1]:
   print('Error: need a filename (.txt)')
   exit()

def readFile(filename):
  try:
    lines = open(filename, 'r').readlines()
    if len(lines) == 0:
        raise IOError()
  except IOError:
    print('Error: no such file' + sys.argv[1] + 'or empty')
    exit()
  first = True
  previous = 0
  for line in lines:
    match = re.match(pattern, line, flags=0)
    # Ha matchato l'inizio del benchmark
    if match:
      if first is True:
        first = False
      else:
        duration.append(int(match.group(2)) - previous)
      checkpoints.append(match.group(1))
      previous = int(match.group(2))

def main():
  readFile(sys.argv[1])
  print("Max execution time: " + str(max(duration)))
  print("Min execution time: " + str(min(duration)))
  print("Avg execution time: " + str(sum(duration)/len(duration)))
  for count, item in enumerate(checkpoints[:-1]):
    print(item + "=>" + checkpoints[count+1] + ": " + str(duration[count]) + " ns")

if __name__== '__main__':
  main()