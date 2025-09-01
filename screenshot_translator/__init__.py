#!/usr/bin/env python3

from .config import *
from .screenshot import take_screenshot, cleanup_screenshot
from .translator import translate_image, create_client

__version__ = "1.0.0"
__all__ = [
    "take_screenshot", 
    "cleanup_screenshot",
    "translate_image", 
    "create_client",
    "API_KEY",
    "BASE_URL", 
    "MODEL",
    "TEMP_FILE_PATH",
    "CLI_PROMPT",
    "GUI_PROMPT"
]
