import sys
from pathlib import Path
from typing import Callable, Optional

import PyQt5.QtWidgets as QtWidget
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui

from .config import Config


def open_folder(folder: Path) -> None:
    url = str(folder.absolute())
    QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(url))


class ProgressIndicator:
    """Class which can be used to indicate progress"""

    def __init__(self, progress_bar: QtWidget.QProgressBar, start_button: QtWidget.QPushButton, out_dir: Path):
        self.progress_bar = progress_bar
        self.start_button = start_button
        self.out_dir = out_dir
        self._init_message_box()

    def _init_message_box(self) -> None:
        self.box = QtWidget.QMessageBox()
        self.box.setText("Ich habe fertig")
        button = QtWidget.QPushButton()
        button.clicked.connect(lambda: open_folder(self.out_dir))
        button.setText("Ordner öffnen")
        self.box.setWindowTitle("Info")
        self.box.addButton(QtWidget.QMessageBox.StandardButton.Ok)
        self.box.addButton(button, QtWidget.QMessageBox.ButtonRole.ActionRole)

    def set_maximum(self, progress_max: int) -> None:
        self.progress_bar.setMaximum(progress_max)

    def set_progress(self, progress: int) -> None:
        self.progress_bar.setValue(progress + 1)
        if self.progress_bar.value() == self.progress_bar.maximum():
            self.box.show()
            self.start_button.setEnabled(True)


class GeneratorQtMainWindow(QtWidget.QMainWindow):
    """Class representing the QT GUI window"""

    def _enable_button(self) -> None:
        if (len(self.config.event_name) > 0 and self.config.num_qr_codes > 0):
            self.start_button.setEnabled(True)

    def _set_out_dir(self, file: str) -> None:
        self.config.out_dir = Path(file)

    def _on_event_name_set(self) -> None:
        self.config.event_name = self.event_name_edit.text()
        self._enable_button()

    def _on_num_qr_codes_set(self) -> None:
        self.config.num_qr_codes = int(self.num_qr_codes_edit.text())
        self._enable_button()

    def _on_start_button_pressed(self) -> None:
        self.start_button.setEnabled(False)
        if self.callback is not None:
            self.callback(self.config)

    def _on_select_output_folder_menu_triggered(self) -> None:
        self._set_out_dir(self.output_folder_menu.getExistingDirectory())

    def _on_open_key_folder_menu_triggered(self) -> None:
        open_folder(self.config.key_dir)

    def _init_file_menu(self) -> None:
        file_menu = self.menuBar().addMenu("Datei")
        file_menu.addAction("Key Ordner öffnen").triggered.connect(
            self._on_open_key_folder_menu_triggered)
        file_menu.addAction("Ausgabeordner wählen").triggered.connect(
            self._on_select_output_folder_menu_triggered)

    def _init_event_name_edit(self) -> None:
        self.event_name_edit = QtWidget.QLineEdit('')
        self.event_name_edit.setText(self.config.event_name)
        self.event_name_edit.editingFinished.connect(self._on_event_name_set)
        self.widget_layout.addWidget(self.event_name_edit)

    def _init_num_qr_codes_edit(self) -> None:
        self.num_qr_codes_edit = QtWidget.QLineEdit('')
        self.num_qr_codes_edit.setText(str(self.config.num_qr_codes))
        self.num_qr_codes_edit.editingFinished.connect(
            self._on_num_qr_codes_set)
        self.widget_layout.addWidget(self.num_qr_codes_edit)

    def _init_start_button(self) -> None:
        self.start_button = QtWidget.QPushButton('Start')
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self._on_start_button_pressed)
        self.widget_layout.addWidget(self.start_button)

    def _init_progress_bar(self) -> None:
        self.progress_bar = QtWidget.QProgressBar()
        self.widget_layout.addWidget(self.progress_bar)

    def _init_output_folder_menu(self) -> None:
        self.output_folder_menu = QtWidget.QFileDialog(
            directory=str(self.config.out_dir))

    def __init__(self, default_config: Config):
        super().__init__()

        self.callback: Optional[Callable[[Config], None]] = None
        self.config: Config = default_config

        self.setWindowTitle("ACR QR-Code Generator")
        self.widget_layout = QtWidget.QVBoxLayout()
        self._init_file_menu()
        self.widget_layout.addWidget(QtWidget.QLabel('Veranstaltungsname'))
        self._init_event_name_edit()
        self.widget_layout.addWidget(QtWidget.QLabel('Anzahl QR-Codes'))
        self._init_num_qr_codes_edit()
        self._init_start_button()
        self._init_progress_bar()
        self._init_output_folder_menu()

        widget = QtWidget.QWidget()
        widget.setLayout(self.widget_layout)

        self.setCentralWidget(widget)
        self.setFixedSize(QtCore.QSize(600, 300))

    def set_generator(self, generator: Callable[[Config], None]) -> None:
        self.callback = generator

    def get_progress_indicator(self) -> ProgressIndicator:
        return ProgressIndicator(
            self.progress_bar, self.start_button, self.config.out_dir)


class GeneratorGui:
    """Class representing the generic interface the GUI must provide"""

    def __init__(self, default_config: Config) -> None:
        self.app = QtWidget.QApplication(sys.argv)
        self.window = GeneratorQtMainWindow(default_config)

    def set_generator(self, generator: Callable[[Config], None]) -> None:
        self.window.set_generator(generator)

    def get_progress_indicator(self) -> ProgressIndicator:
        return self.window.get_progress_indicator()

    def run(self) -> None:
        self.window.show()
        self.app.exec()
