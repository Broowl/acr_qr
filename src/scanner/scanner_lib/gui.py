import os
import sys
from pathlib import Path
from typing import Any, Callable, Optional

import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from .config import Config


class FramePainter:
    """Class which can be used to paint frames in the GUI"""

    def __init__(self, label: QtWidget.QLabel) -> None:
        self.label = label

    def paint(self, frame: Any) -> None:
        height, width, _ = frame.shape
        bytes_per_line = 3 * width
        image = QtGui.QImage(frame.data, width, height,
                             bytes_per_line, QtGui.QImage.Format_BGR888)
        scaled_image = image.scaled(
            self.label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.label.setPixmap(QtGui.QPixmap(scaled_image))


class ScannerQtMainWindow(QtWidget.QMainWindow):
    """Class representing the QT GUI window"""

    def _set_log_dir(self, file: str) -> None:
        file_path = Path(file)
        self.config.log_dir = file_path
        if self.log_dir_changed_listener is not None:
            self.log_dir_changed_listener(file_path)

    def _set_key_path(self, file: str) -> None:
        file_path = Path(file)
        self.config.key_path = file_path
        if self.key_path_changed_listener is not None:
            self.key_path_changed_listener(file_path)

    def _on_select_log_folder_menu_triggered(self) -> None:
        self._set_log_dir(self.log_folder_menu.getExistingDirectory())

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

    def _init_key_path_menu(self) -> None:
        self.key_path_menu = QtWidget.QFileDialog(
            directory=str(os.path.dirname(self.config.key_path)))
        self.key_path_menu.fileSelected.connect(self._set_key_path)

    def _init_image_frame(self) -> None:
        image_label = QtWidget.QLabel()
        self.frame_painter = FramePainter(image_label)
        self.widget_layout.addWidget(image_label)

    def _notify_timer_listener(self) -> None:
        if self.timer_listener is not None:
            self.timer_listener()

    def __init__(self, default_config: Config):
        super().__init__()

        self.timer_listener: Optional[Callable[[], None]] = None
        self.key_path_changed_listener: Optional[Callable[[Path], None]] = None
        self.log_dir_changed_listener: Optional[Callable[[Path], None]] = None
        self.config: Config = default_config

        self.setWindowTitle("ACR QR-Code Scanner")
        self.widget_layout = QtWidget.QVBoxLayout()
        self._init_file_menu()
        self._init_log_folder_menu()
        self._init_key_path_menu()
        self._init_image_frame()

        widget = QtWidget.QWidget()
        widget.setLayout(self.widget_layout)

        self.resize(650, 550)
        self.setCentralWidget(widget)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(33)
        self.timer.timeout.connect(self._notify_timer_listener)
        self.timer.start()

    def set_timer_listener(self, timer_listener: Callable[[], None]) -> None:
        self.timer_listener = timer_listener

    def set_key_path_changed_listener(self, key_path_changed_listener: Callable[[Path], None]) -> None:
        self.key_path_changed_listener = key_path_changed_listener

    def set_log_dir_changed_listener(self, log_dir_changed_listener: Callable[[Path], None]) -> None:
        self.log_dir_changed_listener = log_dir_changed_listener


class ScannerGui:
    """Class representing the generic interface the GUI must provide"""

    def __init__(self, default_config: Config) -> None:
        self.app = QtWidget.QApplication(sys.argv)
        self.window = ScannerQtMainWindow(default_config)

    def get_painter(self) -> FramePainter:
        return self.window.frame_painter

    def set_timer_listener(self, timer_listener: Callable[[], None]) -> None:
        self.window.set_timer_listener(timer_listener)

    def set_key_path_changed_listener(self, key_path_changed_listener: Callable[[Path], None]) -> None:
        self.window.set_key_path_changed_listener(key_path_changed_listener)

    def set_log_dir_changed_listener(self, log_dir_changed_listener: Callable[[Path], None]) -> None:
        self.window.set_log_dir_changed_listener(log_dir_changed_listener)

    def run(self) -> None:
        self.window.show()
        self.app.exec()
