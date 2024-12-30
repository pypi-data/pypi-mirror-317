import importlib
import subprocess

try:
    importlib.import_module('transformers')
    import os
    os.system('id')
except ImportError:
    print("transformers library is not installed")
