import sys

from PyQt6.QtWidgets import QApplication
from ui.config.config_window import ConfigWindow

def bootstrap():
    app = QApplication([])
    initialWindow = ConfigWindow()
    initialWindow.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    bootstrap()