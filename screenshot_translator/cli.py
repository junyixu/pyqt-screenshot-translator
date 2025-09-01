#!/usr/bin/env python3

import subprocess
import os
from .screenshot import take_screenshot, cleanup_screenshot
from .translator import translate_image
from .config import CLI_PROMPT


def show_notification(title, message, timeout=0):
    """Show notification using kdialog (Qt/KDE native)"""
    if timeout == 0:
        # For permanent notifications, use a very long timeout
        timeout = 86400  # 24 hours
    subprocess.run([
        'kdialog', '--title', title, '--passivepopup', message, str(timeout)
    ])


def main():
    screenshot_path = take_screenshot()
    if not screenshot_path:
        show_notification('Screenshot cancelled or failed', '')
        return

    try:
        translation = translate_image(screenshot_path, CLI_PROMPT)
        show_notification('Translation Result', translation)
    except Exception as e:
        show_notification('Translation failed', str(e))
    finally:
        cleanup_screenshot(screenshot_path)


if __name__ == "__main__":
    main()
