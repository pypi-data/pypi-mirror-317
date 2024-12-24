"""
This is the current version of TorchServe
"""
import os
from pathlib import Path

version_path = os.path.join(Path(__file__).resolve().parent, 'version.txt')
__version__ = open(version_path, 'r').read().strip()
