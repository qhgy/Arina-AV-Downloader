#!/usr/bin/env python3
"""
Alternative GUI with forced sky blue background everywhere
"""

import sys
import os
from pathlib import Path
import threading
import time

try:
    from PyQt6.QtWidgets import *
    from PyQt6.QtCore import *
    from PyQt6.QtGui import *
    PYQT_AVAILABLE = True
except ImportError:
    try:
        from PySide6.QtWidgets import *
        from PySide6.QtCore import *
        from PySide6.QtGui import *
        PYQT_AVAILABLE = True
    except ImportError:
        PYQT_AVAILABLE = False

class SkyBlueWidget(QWidget):
    """Widget with forced sky blue background"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.set_sky_blue_background()
    
    def set_sky_blue_background(self):
        """Set sky blue gradient background"""
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #87CEEB, stop:0.3 #B0E0E6, stop:0.7 #E0F6FF, stop:1 #F0F8FF);
                border: none;
            }
        """)

def apply_sky_blue_to_all_widgets(widget):
    """Recursively apply sky blue background to all widgets"""
    if isinstance(widget, QWidget):
        # Don't override specific styled widgets like buttons, input fields
        if not isinstance(widget, (QPushButton, QLineEdit, QTextEdit, QGroupBox, QProgressBar)):
            widget.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #87CEEB, stop:0.3 #B0E0E6, stop:0.7 #E0F6FF, stop:1 #F0F8FF);
                border: none;
            """)
    
    # Apply to all children
    for child in widget.findChildren(QWidget):
        if not isinstance(child, (QPushButton, QLineEdit, QTextEdit, QGroupBox, QProgressBar)):
            child.setStyleSheet("""
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #87CEEB, stop:0.3 #B0E0E6, stop:0.7 #E0F6FF, stop:1 #F0F8FF);
                border: none;
            """)

if __name__ == '__main__':
    if not PYQT_AVAILABLE:
        print("PyQt6/PySide6 not available")
        exit(1)
    
    app = QApplication(sys.argv)
    
    # Import the main GUI
    try:
        from gui_downloader import ModernVideoDownloader
        window = ModernVideoDownloader()
        
        # Force apply sky blue background everywhere
        window.setStyleSheet("""
            * {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #87CEEB, stop:0.3 #B0E0E6, stop:0.7 #E0F6FF, stop:1 #F0F8FF);
            }
            QGroupBox, QPushButton, QLineEdit, QTextEdit, QProgressBar {
                /* Keep original styling for these */
            }
        """)
        
        # Apply to all children after a short delay
        QTimer.singleShot(100, lambda: apply_sky_blue_to_all_widgets(window))
        
        window.show()
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"Failed to import GUI: {e}")
        exit(1)