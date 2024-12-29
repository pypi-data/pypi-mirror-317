
# import subprocess
import sys

def caller(args = sys.argv):
  if args[1] == "-h":
    print("Hello World")
  else:
    print("Okay")
