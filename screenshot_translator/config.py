#!/usr/bin/env python3

import os

API_KEY = os.getenv('TRANSLATOR_API_KEY', '')
BASE_URL = os.getenv('TRANSLATOR_BASE_URL', 'https://lpzgncibqfos.ap-southeast-1.clawcloudrun.com/v1')
MODEL = os.getenv('TRANSLATOR_MODEL', 'gemini-2.5-flash')
TEMP_FILE_PATH = os.getenv('TRANSLATOR_TEMP_PATH', '/tmp/screenshot_translator_capture.png')

CLI_PROMPT = "Please OCR all text in this image and translate any English text to Chinese. Return the Chinese translation."

GUI_PROMPT = "请识别图片中的所有文本，并将英文翻译成中文。保持原文的排版格式，如果是LaTeX公式，请使用MathJax兼容的语法：行内公式用$公式$，独立公式用$$公式$$。只返回翻译后的中文结果，不要包含原文。"
