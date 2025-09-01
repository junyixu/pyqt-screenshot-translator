#!/usr/bin/env python3

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, 
    QPushButton, QLabel, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QFont
import markdown

from .screenshot import take_screenshot, cleanup_screenshot
from .translator import translate_image
from .config import GUI_PROMPT


class ScreenshotWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            temp_path = take_screenshot()
            if temp_path is None:
                self.error.emit("Screenshot cancelled or failed")
                return
            
            self.finished.emit(temp_path)
        except Exception as e:
            self.error.emit(f"Screenshot failed: {str(e)}")


class TranslationWorker(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path

    def run(self):
        try:
            translation = translate_image(self.image_path, GUI_PROMPT)
            if not translation or translation.strip() == "":
                self.error.emit("API returned empty response")
                return
                
            self.finished.emit(translation)
            
        except Exception as e:
            self.error.emit(f"Translation failed: {str(e)}")
        finally:
            cleanup_screenshot(self.image_path)


class MarkdownWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(400)

    def set_markdown(self, text):
        html_content = markdown.markdown(text, extensions=['fenced_code', 'tables'])
        
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <script>
                window.MathJax = {{
                    tex: {{
                        inlineMath: [['$', '$'], ['\\(', '\\)']],
                        displayMath: [['$$', '$$'], ['\\[', '\\]']],
                        processEscapes: true,
                        processEnvironments: true
                    }},
                    startup: {{
                        ready: function() {{
                            MathJax.startup.defaultReady();
                            console.log('MathJax loaded successfully');
                        }}
                    }},
                    options: {{
                        skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'],
                        ignoreHtmlClass: 'tex2jax_ignore'
                    }}
                }};
            </script>
            <script id="MathJax-script" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.0/es5/tex-mml-chtml.js"></script>
            <style>
                body {{
                    font-family: 'Noto Sans', 'Segoe UI', Arial, sans-serif;
                    line-height: 1.8;
                    margin: 20px;
                    background-color: #ffffff;
                    color: #333333;
                    font-size: 15px;
                }}
                h1, h2, h3, h4, h5, h6 {{
                    color: #2c3e50;
                    border-bottom: 1px solid #e1e4e8;
                    padding-bottom: 0.3em;
                    margin-top: 24px;
                    margin-bottom: 16px;
                    font-weight: 600;
                }}
                h1 {{ font-size: 2em; }}
                h2 {{ font-size: 1.5em; }}
                h3 {{ font-size: 1.25em; }}
                code {{
                    background-color: #f6f8fa;
                    padding: 2px 4px;
                    border-radius: 3px;
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    color: #d73a49;
                    font-size: 0.9em;
                }}
                pre {{
                    background-color: #f6f8fa;
                    padding: 16px;
                    border-radius: 6px;
                    overflow-x: auto;
                    border-left: 4px solid #0366d6;
                    margin: 16px 0;
                }}
                pre code {{
                    background-color: transparent;
                    padding: 0;
                    color: #24292e;
                }}
                blockquote {{
                    border-left: 4px solid #0366d6;
                    margin: 16px 0;
                    padding-left: 16px;
                    color: #6a737d;
                    font-style: italic;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 16px 0;
                }}
                th, td {{
                    border: 1px solid #dfe2e5;
                    padding: 8px 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #f6f8fa;
                    font-weight: 600;
                    color: #24292e;
                }}
                p {{
                    margin: 16px 0;
                    text-align: justify;
                }}
                .math-display {{
                    margin: 16px 0;
                    text-align: center;
                }}
                .math-inline {{
                    padding: 0 2px;
                }}
                ul, ol {{
                    margin: 16px 0;
                    padding-left: 32px;
                }}
                li {{
                    margin: 8px 0;
                    line-height: 1.6;
                }}
            </style>
        </head>
        <body>
            <div id="content">
                {html_content}
            </div>
            <script>
                setTimeout(function() {{
                    if (typeof MathJax === 'undefined' || !MathJax.typeset) {{
                        console.log('MathJax failed to load, showing raw content');
                        document.getElementById('content').style.opacity = '1';
                    }}
                }}, 5000);
            </script>
        </body>
        </html>
        """
        
        self.setHtml(full_html)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Screenshot Translator")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        title_label = QLabel("Screenshot Translator")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        self.screenshot_btn = QPushButton("Take Screenshot")
        self.screenshot_btn.clicked.connect(self.take_screenshot)
        self.screenshot_btn.setMinimumHeight(40)
        layout.addWidget(self.screenshot_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.markdown_widget = MarkdownWidget()
        layout.addWidget(self.markdown_widget, 1)
        
        self.status_label = QLabel("Ready to take screenshot")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setMaximumHeight(25)
        layout.addWidget(self.status_label)
        
        self.screenshot_worker = None
        self.translation_worker = None

    def take_screenshot(self):
        if self.screenshot_worker and self.screenshot_worker.isRunning():
            return
            
        self.screenshot_btn.setEnabled(False)
        self.status_label.setText("Taking screenshot...")
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        self.screenshot_worker = ScreenshotWorker()
        self.screenshot_worker.finished.connect(self.on_screenshot_finished)
        self.screenshot_worker.error.connect(self.on_error)
        self.screenshot_worker.start()

    def on_screenshot_finished(self, image_path):
        self.status_label.setText("Translating...")
        
        self.translation_worker = TranslationWorker(image_path)
        self.translation_worker.finished.connect(self.on_translation_finished)
        self.translation_worker.error.connect(self.on_error)
        self.translation_worker.start()

    def on_translation_finished(self, translation):
        self.status_label.setText("Translation complete")
        self.markdown_widget.set_markdown(translation)
        self.reset_ui()

    def on_error(self, error_message):
        self.status_label.setText(f"Error: {error_message}")
        self.markdown_widget.set_markdown(f"**Error:** {error_message}")
        self.reset_ui()

    def reset_ui(self):
        self.screenshot_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        if self.screenshot_worker:
            self.screenshot_worker.wait()
        if self.translation_worker:
            self.translation_worker.wait()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Screenshot Translator")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
