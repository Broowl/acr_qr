import PyQt5.QtWidgets as Qt
from PyQt5.QtCore import QSize
import sys
from pathlib import Path
from config import Config


class ProgressIndicator:
    def __init__(self, progress_bar: Qt.QProgressBar, start_button: Qt.QPushButton):
        self.progress_bar = progress_bar
        self.start_button = start_button

    def set_progress(self, progress: int):
        self.progress_bar.setValue(progress + 1)
        if (self.progress_bar.value() == self.progress_bar.maximum()):
            self.start_button.setEnabled(True)


class MainWindow(Qt.QMainWindow):
    def _enable_button(self):
        if (len(self.config.event_name) > 0 and self.config.num_qr_codes > 0):
            self.start_button.setEnabled(True)

    def _on_event_name_set(self):
        self.config.event_name = self.event_name_edit.text()
        self._enable_button()

    def _on_num_qr_codes_set(self):
        self.config.num_qr_codes = int(self.num_qr_codes_edit.text())
        self._enable_button()

    def _on_start_button_pressed(self):
        self.start_button.setEnabled(False)
        self.progress_bar.setMaximum(self.config.num_qr_codes)
        self.callback(self.config, ProgressIndicator(
            self.progress_bar, self.start_button))

    def _on_select_output_folder_menu_triggered(self):
        self.output_folder_menu = Qt.QFileDialog(directory=str(Path.home()))
        self.output_folder_menu.fileSelected.connect(
            lambda file: self._set_out_dir(file))
        self.output_folder_menu.show()

    def _set_out_dir(self, file: str):
        self.config.out_dir = Path(file)

    def __init__(self, callback, default_config: Config):
        super().__init__()

        self.callback = callback
        self.config: Config = default_config

        self.setWindowTitle("ACR QR-Code Generator")
        layout = Qt.QVBoxLayout()
        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction("Open key folder")
        fileMenu.addAction("Select output folder").triggered.connect(
            lambda: self._on_select_output_folder_menu_triggered())
        layout.addWidget(Qt.QLabel('Veranstaltungsname'))
        self.event_name_edit = Qt.QLineEdit('')
        self.event_name_edit.editingFinished.connect(
            lambda: self._on_event_name_set())
        layout.addWidget(self.event_name_edit)
        layout.addWidget(Qt.QLabel('Anzahl QR-Codes'))
        self.num_qr_codes_edit = Qt.QLineEdit('')
        self.num_qr_codes_edit.editingFinished.connect(
            lambda: self._on_num_qr_codes_set())
        layout.addWidget(self.num_qr_codes_edit)
        self.start_button = Qt.QPushButton('Start')
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(
            lambda: self._on_start_button_pressed())
        layout.addWidget(self.start_button)
        self.progress_bar = Qt.QProgressBar()
        layout.addWidget(self.progress_bar)

        widget = Qt.QWidget()
        widget.setLayout(layout)

        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)
        self.setFixedSize(QSize(600, 300))


def create(callback, default_config: Config):
    app = Qt.QApplication(sys.argv)
    window = MainWindow(callback, default_config)
    window.show()

    app.exec()
