import sys
import re

checkpoints = []
timestamps = []
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
        checkpoints.append(match.group(1))
        timestamps.append(int(match.group(2)) - previous)
      previous = int(match.group(2))

def main():
  readFile(sys.argv[1])
  print("Max execution time: " + str(max(timestamps)))
  print("Min execution time: " + str(min(timestamps)))
  print("Avg execution time: " + str(sum(timestamps)/len(timestamps)))

if __name__== '__main__':
  main()