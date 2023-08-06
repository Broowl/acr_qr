import os
import sys
from pathlib import Path
from typing import Callable

import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from .config import Config

class MainWindow(QtWidget.QMainWindow):
    """Class representing the GUI window"""


    def _set_log_dir(self, file: str) -> None:
        self.config.log_dir = Path(file)

    def _set_key_path(self, file: str) -> None:
        self.config.key_path = Path(file)

    def _on_select_log_folder_menu_triggered(self) -> None:
        self.log_folder_menu.getExistingDirectory()

    def _on_select_key_path_menu_triggered(self) -> None:
        self.key_path_menu.show()

    def _init_file_menu(self) -> None:
        file_menu = self.menuBar().addMenu("Datei")
        file_menu.addAction("Wähle Key Datei").triggered.connect(
            self._on_select_key_path_menu_triggered)
        file_menu.addAction("Ausgabeordner wählen").triggered.connect(
            self._on_select_log_folder_menu_triggered)

    def _init_log_folder_menu(self) -> None:
        self.log_folder_menu = QtWidget.QFileDialog(
            directory=str(self.config.log_dir.absolute()))
        self.log_folder_menu.fileSelected.connect(self._set_log_dir)

    def _init_key_path_menu(self) -> None:
        self.key_path_menu = QtWidget.QFileDialog(
            directory=str(os.path.dirname(self.config.key_path)))
        self.key_path_menu.fileSelected.connect(self._set_key_path)

    def __init__(self, callback: Callable[[], None], default_config: Config):
        super().__init__()

        self.callback = callback
        self.config: Config = default_config

        self.setWindowTitle("ACR QR-Code Scanner")
        self.widget_layout = QtWidget.QVBoxLayout()
        self._init_file_menu()
        self._init_log_folder_menu()
        self._init_key_path_menu()

        widget = QtWidget.QWidget()
        widget.setLayout(self.widget_layout)
        
        self.setCentralWidget(widget)
        self.setFixedSize(QtCore.QSize(600, 300))
        self.timer = QtCore.QTimer()
        self.timer.setInterval(33)
        self.timer.timeout.connect(self.callback)
        self.timer.start()


def create(callback: Callable[[], None], default_config: Config) -> None:
    app = QtWidget.QApplication(sys.argv)
    window = MainWindow(callback, default_config)
    window.show()
    app.exec()