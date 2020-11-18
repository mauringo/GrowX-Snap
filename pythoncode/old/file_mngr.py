import os

# from pathlib import Path
# import importlib
# import json

def pl_find(payload):
    """Helps finding the current directory of files"""

    payload = payload + ".json"
    for root, _, files in os.walk(".", topdown=False):
        for name in files:
            if name == payload:
                    return os.path.join(root, name)