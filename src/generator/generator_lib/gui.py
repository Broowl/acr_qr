import os
import sys
from pathlib import Path
from typing import Callable, Optional
from datetime import date

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

    def _set_key_path(self, key_path: str) -> None:
        self.config.private_key_path = Path(key_path)
        if self.key_path_listener is not None:
            self.key_path_listener(self.config.private_key_path)

    def _on_event_name_set(self) -> None:
        self.config.event_name = self.event_name_edit.text()
        self._enable_button()

    def _on_event_date_set(self) -> None:
        set_date = self.event_date_edit.date()
        self.config.event_date = date(
            set_date.year(), set_date.month(), set_date.day())

    def _on_num_qr_codes_set(self) -> None:
        self.config.num_qr_codes = int(self.num_qr_codes_edit.text())
        self._enable_button()

    def _on_start_button_pressed(self) -> None:
        self.start_button.setEnabled(False)
        if self.callback is not None:
            self.callback(self.config)

    def _on_select_out_dir_menu_triggered(self) -> None:
        selected_out_dir = Path(self.out_dir_dialog.getExistingDirectory())
        if len(selected_out_dir.name) != 0:
            self.config.out_dir = selected_out_dir
            self.progress_indicator.out_dir = self.config.out_dir
            if self.out_dir_listener is not None:
                self.out_dir_listener(self.config.out_dir)

    def _on_open_key_dir_menu_triggered(self) -> None:
        open_folder(self.config.private_key_path.parent)

    def _on_open_online_help_menu_triggered(self) -> None:
        git_hub_url = QtCore.QUrl("https://github.com/Broowl/acr_qr")
        QtGui.QDesktopServices.openUrl(git_hub_url)

    def _on_open_license_menu_triggered(self) -> None:
        license_path = QtCore.QUrl("LICENSE")
        QtGui.QDesktopServices.openUrl(license_path)

    def _on_open_about_menu_triggered(self) -> None:
        self.about_box.show()

    def _on_generate_key_button_pressed(self)-> None:
        if self.key_writer is not None:
            self.key_writer(self.config.private_key_path)

    def _init_file_menu(self) -> None:
        file_menu = self.menuBar().addMenu("Datei")
        file_menu.addAction("Key Ordner öffnen").triggered.connect(
            self._on_open_key_dir_menu_triggered)
        file_menu.addAction("Ausgabeordner wählen").triggered.connect(
            self._on_select_out_dir_menu_triggered)

    def _init_event_name_edit(self) -> None:
        self.event_name_edit = QtWidget.QLineEdit('')
        self.event_name_edit.setText(self.config.event_name)
        self.event_name_edit.editingFinished.connect(self._on_event_name_set)
        self.widget_layout.addWidget(self.event_name_edit)

    def _init_event_date_edit(self) -> None:
        self.event_date_edit = QtWidget.QDateEdit()
        default_date = QtCore.QDate(
            self.config.event_date.year, self.config.event_date.month, self.config.event_date.day)
        self.event_date_edit.setDate(default_date)
        self.event_date_edit.editingFinished.connect(self._on_event_date_set)
        self.widget_layout.addWidget(self.event_date_edit)

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

    def _init_out_dir_dialog(self) -> None:
        self.out_dir_dialog = QtWidget.QFileDialog(
            directory=str(self.config.out_dir))

    def _init_key_dir_dialog(self) -> None:
        self.key_dir_dialog = QtWidget.QFileDialog(
            directory=str(self.config.private_key_path))

    def _init_key_import_dialog(self) -> None:
        self.key_import_dialog = QtWidget.QFileDialog(
            directory=str(os.path.dirname(self.config.private_key_path)),
            filter="*.pem")
        self.key_import_dialog.fileSelected.connect(self._set_key_path)
        self.key_dir_dialog.setWindowTitle("Wähle prive key")

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
        self.about_box.setText("Autor: Daniel Krieger<br>Version: 0.9.2")
        self.about_box.setWindowTitle("Über ACR QR-Code Generator")

    def _init_welcome_box(self) -> None:
        self.welcome_box = QtWidget.QMessageBox()
        self.welcome_box.setWindowTitle("ACR QR-Code Generator")
        self.welcome_box.setText("Es wurde keine private key Datei gefunden.")
        generate_button = QtWidget.QPushButton()
        generate_button.setText("Neu generieren")
        generate_button.clicked.connect(self._on_generate_key_button_pressed)
        self.welcome_box.addButton(
            generate_button, QtWidget.QMessageBox.ButtonRole.ActionRole)
        import_button = QtWidget.QPushButton()
        import_button.clicked.connect(self.key_import_dialog.show)
        import_button.setText("Importieren")
        self.welcome_box.addButton(
            import_button, QtWidget.QMessageBox.ButtonRole.ActionRole)
        if not os.path.exists(self.config.private_key_path):
            self.welcome_box.show()

    def __init__(self, default_config: Config):
        super().__init__()

        self.callback: Optional[Callable[[Config], None]] = None
        self.key_writer: Optional[Callable[[Path], None]] = None
        self.out_dir_listener: Optional[Callable[[Path], None]] = None
        self.key_path_listener: Optional[Callable[[Path], None]] = None
        self.config: Config = default_config

        self.setWindowTitle("ACR QR-Code Generator")
        self.widget_layout = QtWidget.QVBoxLayout()
        self._init_file_menu()
        self.widget_layout.addWidget(QtWidget.QLabel('Veranstaltungsname'))
        self._init_event_name_edit()
        self.widget_layout.addWidget(QtWidget.QLabel('Veranstaltungsdatum'))
        self._init_event_date_edit()
        self.widget_layout.addWidget(QtWidget.QLabel('Anzahl QR-Codes'))
        self._init_num_qr_codes_edit()
        self._init_start_button()
        self._init_progress_bar()
        self._init_out_dir_dialog()
        self._init_help_menu()
        self._init_about_message_box()
        self.progress_indicator = ProgressIndicator(
            self.progress_bar, self.start_button, self.config.out_dir)
        self._init_key_dir_dialog()
        self._init_key_import_dialog()
        self._init_welcome_box()

        widget = QtWidget.QWidget()
        widget.setLayout(self.widget_layout)

        self.setCentralWidget(widget)
        self.setFixedSize(QtCore.QSize(
            int(self.size().width()*1.3), int(self.size().height() * 0.8)))
        self.setWindowIcon(QtGui.QIcon("assets/generator.ico"))

    def set_generator(self, generator: Callable[[Config], None]) -> None:
        self.callback = generator

    def set_key_writer(self, writer: Callable[[Path],None])->None:
        self.key_writer = writer

    def get_progress_indicator(self) -> ProgressIndicator:
        return self.progress_indicator

    def set_out_dir_listener(self, listener: Callable[[Path], None]) -> None:
        self.out_dir_listener = listener

    def set_key_path_listener(self, listener: Callable[[Path], None]) -> None:
        self.key_path_listener = listener


class GeneratorGui:
    """Class representing the generic interface the GUI must provide"""

    def __init__(self, default_config: Config) -> None:
        self.app = QtWidget.QApplication(sys.argv)
        self.window = GeneratorQtMainWindow(default_config)

    def set_generator(self, generator: Callable[[Config], None]) -> None:
        self.window.set_generator(generator)

    def set_key_writer(self, writer: Callable[[Path],None])->None:
        self.window.set_key_writer(writer)

    def get_progress_indicator(self) -> ProgressIndicator:
        return self.window.get_progress_indicator()

    def set_out_dir_listener(self, listener: Callable[[Path], None]) -> None:
        self.window.set_out_dir_listener(listener)

    def set_key_path_listener(self, listener: Callable[[Path], None]) -> None:
        self.window.set_key_path_listener(listener)

    def run(self) -> None:
        self.window.show()
        self.app.exec()
