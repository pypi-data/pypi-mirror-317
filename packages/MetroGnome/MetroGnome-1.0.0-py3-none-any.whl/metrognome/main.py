#!/usr/bin/env python3
"""
main.py
Entry point for the Metrognome application.
"""

import sys
from importlib.resources import files
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication
from .metrognome_window import MetrognomeWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("metrognome")
    app.setWindowIcon(QIcon(str(files("metrognome.resources") / "icon.svg")))

    window = MetrognomeWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
