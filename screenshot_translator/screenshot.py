#!/usr/bin/env python3

import subprocess
import os
from .config import TEMP_FILE_PATH


def take_screenshot(temp_path=None):
    """Take a screenshot using KDE Spectacle with area selection."""
    if temp_path is None:
        temp_path = TEMP_FILE_PATH
    
    result = subprocess.Popen(f'spectacle -r -b -n -o {temp_path}', shell=True)
    result.wait()
    
    if result.returncode != 0:
        return None
    
    return temp_path


def cleanup_screenshot(file_path):
    """Remove screenshot file if it exists."""
    if file_path and os.path.exists(file_path):
        os.unlink(file_path)
