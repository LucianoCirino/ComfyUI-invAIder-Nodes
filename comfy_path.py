import sys
import os

# Get the absolute path of various directories
my_dir = os.path.dirname(os.path.abspath(__file__))
comfy_dir = os.path.abspath(os.path.join(my_dir, '..', '..'))

# Append comfy_dir to sys.path & import files
sys.path.append(comfy_dir)