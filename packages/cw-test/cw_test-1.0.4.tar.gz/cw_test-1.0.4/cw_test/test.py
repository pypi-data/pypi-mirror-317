
from pathlib import Path

def print_path():
  this_directory = Path(__file__).parent
  print(this_directory)
