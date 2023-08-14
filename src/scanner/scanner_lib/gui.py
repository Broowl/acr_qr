import os
import sys
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Optional, List
from datetime import date, datetime
import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from scanner_lib.event_characteristics import EventCharacteristics
from .config import Config


class ImagePainter:
    """Class which can be used to paint images in the GUI"""

    def __init__(self, label: QtWidget.QLabel) -> None:
        self.label = label
        self.lock = Lock()
        self.image: Optional[QtGui.QImage] = None

    def paint(self, frame: Any) -> None:
        height, width, _ = frame.shape
        bytes_per_line = 3 * width
        image = QtGui.QImage(frame.data, width, height,
                             bytes_per_line, QtGui.QImage.Format_BGR888)
        with self.lock:
            self.image = image

    def do_paint(self) -> None:
        with self.lock:
            if self.image is not None:
                scaled_image = self.image.scaled(
                    self.label.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
                self.label.setPixmap(QtGui.QPixmap(scaled_image))


class StartWindow(QtWidget.QWidget):
    """Startup menu class"""

    def _init_event_name_edit(self) -> None:
        self.event_name_edit = QtWidget.QLineEdit('')
        self.event_name_edit.editingFinished.connect(self._on_event_name_set)
        self.widget_layout.addWidget(self.event_name_edit)

    def _init_event_date_edit(self) -> None:
        self.event_date_edit = QtWidget.QDateEdit()
        event_date = self.event_characteristics.date
        default_date = QtCore.QDate(
            event_date.year, event_date.month, event_date.day)
        self.event_date_edit.setDate(default_date)
        self.event_date_edit.editingFinished.connect(self._on_event_date_set)
        self.widget_layout.addWidget(self.event_date_edit)

    def _init_ok_button(self) -> None:
        self.start_button = QtWidget.QPushButton('Ok')
        self.start_button.setEnabled(True)
        self.start_button.clicked.connect(self._on_ok_button_pressed)
        self.widget_layout.addWidget(self.start_button)

    def __init__(self, on_accepted_callback: Callable[[EventCharacteristics], None], on_closed_callback: Callable[[], None]) -> None:
        super().__init__()
        self.event_characteristics = EventCharacteristics(
            "", datetime.today().date())
        self.setWindowTitle("ACR QR-Code Scanner")
        self.widget_layout = QtWidget.QVBoxLayout()
        self.widget_layout.addWidget(QtWidget.QLabel('Veranstaltungsname'))
        self._init_event_name_edit()
        self.widget_layout.addWidget(QtWidget.QLabel('Veranstaltungsdatum'))
        self._init_event_date_edit()
        self.on_accepted_callback = on_accepted_callback
        self.on_closed_callback = on_closed_callback
        self._init_ok_button()
        self.setLayout(self.widget_layout)

    def _on_ok_button_pressed(self) -> None:
        if self.on_accepted_callback is not None:
            self.on_accepted_callback(self.event_characteristics)
        self.hide()

    def _on_event_name_set(self) -> None:
        self.event_characteristics.name = self.event_name_edit.text()

    def _on_event_date_set(self) -> None:
        set_date = self.event_date_edit.date()
        self.event_characteristics.date = date(
            set_date.year(), set_date.month(), set_date.day())

    # pylint: disable=invalid-name
    def closeEvent(self, close_event: QtGui.QCloseEvent) -> None:
        self.on_closed_callback()
        return super().closeEvent(close_event)


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

    def _on_camera_selected(self, camera: int) -> None:
        if self.camera_listener is not None:
            self.camera_listener(camera)

    def _on_open_online_help_menu_triggered(self) -> None:
        git_hub_url = QtCore.QUrl("https://github.com/Broowl/acr_qr")
        QtGui.QDesktopServices.openUrl(git_hub_url)

    def _on_open_license_menu_triggered(self) -> None:
        license_path = QtCore.QUrl("LICENSE")
        QtGui.QDesktopServices.openUrl(license_path)

    def _on_open_about_menu_triggered(self) -> None:
        self.about_box.show()

    def _on_start_menu_accepted(self, characteristics: EventCharacteristics) -> None:
        if self.event_name_listener is not None:
            self.event_name_listener(characteristics)
        self.timer.start()
        self.show()

    def _on_start_menu_closed(self) -> None:
        self.close()

    def _init_file_menu(self) -> None:
        file_menu = self.menuBar().addMenu("Datei")
        file_menu.addAction("Wähle Key Datei").triggered.connect(
            self._on_select_key_path_menu_triggered)
        file_menu.addAction("Ausgabeordner wählen").triggered.connect(
            self._on_select_log_folder_menu_triggered)

    def _init_config_menu(self) -> None:
        config_menu = self.menuBar().addMenu("Konfiguration")
        camera_menu = config_menu.addMenu("Kamera ändern")
        for camera in self.camera_list:
            camera_menu.addAction(f"{camera}").triggered.connect(
                lambda _, c=camera: self._on_camera_selected(c))

    def _init_log_folder_menu(self) -> None:
        self.log_folder_menu = QtWidget.QFileDialog(
            directory=str(self.config.log_dir.absolute()))

    def _init_key_path_menu(self) -> None:
        self.key_path_menu = QtWidget.QFileDialog(
            directory=str(os.path.dirname(self.config.key_path)))
        self.key_path_menu.fileSelected.connect(self._set_key_path)

    def _init_image_frame(self) -> None:
        image_label = QtWidget.QLabel()
        image_label.setMinimumSize(4 * 40, 3 * 40)
        self.frame_painter = ImagePainter(image_label)
        self.widget_layout.addWidget(image_label)

    def _notify_timer_listener(self) -> None:
        self.frame_painter.do_paint()
        if self.timer_listener is not None:
            self.timer_listener()

    def _init_help_menu(self) -> None:
        help_menu = self.menuBar().addMenu("Hilfe")
        help_menu.addAction("Online Hilfe").triggered.connect(
            self._on_open_online_help_menu_triggered)
        help_menu.addAction("Lizenz").triggered.connect(
            self._on_open_license_menu_triggered)
        help_menu.addAction("Über").triggered.connect(
            self._on_open_about_menu_triggered)

    def _init_about_message_box(self) -> None:
        self.about_box = QtWidget.QMessageBox()
        self.about_box.setText("Autor: Daniel Krieger<br>Version: 1.0.0")
        self.about_box.setWindowTitle("Über ACR QR-Code Generator")

    def __init__(self, default_config: Config, camera_list: List[int]):
        super().__init__()

        self.timer_listener: Optional[Callable[[], None]] = None
        self.key_path_changed_listener: Optional[Callable[[Path], None]] = None
        self.log_dir_changed_listener: Optional[Callable[[Path], None]] = None
        self.camera_listener: Optional[Callable[[int], None]] = None
        self.event_name_listener: Optional[Callable[[
            EventCharacteristics], None]] = None
        self.config: Config = default_config
        self.camera_list = camera_list

        self.setWindowTitle("ACR QR-Code Scanner")
        self.widget_layout = QtWidget.QVBoxLayout()
        self._init_file_menu()
        self._init_log_folder_menu()
        self._init_key_path_menu()
        self._init_config_menu()
        self._init_image_frame()
        self._init_help_menu()
        self._init_about_message_box()

        widget = QtWidget.QWidget()
        widget.setLayout(self.widget_layout)

        self.resize(650, 550)
        self.setCentralWidget(widget)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(33)
        self.timer.timeout.connect(self._notify_timer_listener)
        self.hide()
        self.start_menu = StartWindow(
            self._on_start_menu_accepted, self._on_start_menu_closed)

    def set_timer_listener(self, timer_listener: Callable[[], None]) -> None:
        self.timer_listener = timer_listener

    def set_key_path_changed_listener(self, key_path_changed_listener: Callable[[Path], None]) -> None:
        self.key_path_changed_listener = key_path_changed_listener

    def set_log_dir_changed_listener(self, log_dir_changed_listener: Callable[[Path], None]) -> None:
        self.log_dir_changed_listener = log_dir_changed_listener

    def set_configuration_finished_listener(self, event_name_listener: Callable[[EventCharacteristics], None]) -> None:
        self.event_name_listener = event_name_listener

    def get_painter(self) -> ImagePainter:
        return self.frame_painter

    def set_camera_listener(self, listener:  Callable[[int], None]) -> None:
        self.camera_listener = listener

    def show_start_menu(self) -> None:
        self.start_menu.show()


class ScannerGui:
    """Class representing the generic interface the GUI must provide"""

    def __init__(self, default_config: Config, camera_list: List[int]) -> None:
        self.app = QtWidget.QApplication(sys.argv)
        self.window = ScannerQtMainWindow(default_config, camera_list)

    def get_painter(self) -> ImagePainter:
        return self.window.get_painter()

    def set_timer_listener(self, timer_listener: Callable[[], None]) -> None:
        self.window.set_timer_listener(timer_listener)

    def set_key_path_changed_listener(self, key_path_changed_listener: Callable[[Path], None]) -> None:
        self.window.set_key_path_changed_listener(key_path_changed_listener)

    def set_log_dir_changed_listener(self, log_dir_changed_listener: Callable[[Path], None]) -> None:
        self.window.set_log_dir_changed_listener(log_dir_changed_listener)

    def set_camera_listener(self, camera_listener:  Callable[[int], None]) -> None:
        self.window.set_camera_listener(camera_listener)

    def set_configuration_finished_listener(self, event_name_listener: Callable[[EventCharacteristics], None]) -> None:
        self.window.set_configuration_finished_listener(event_name_listener)

    def run(self) -> None:
        self.window.show_start_menu()
        self.app.exec()
