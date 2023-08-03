import PyQt5.QtWidgets as Qt
import sys


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
        if (len(self.event_name) > 0 and self.num_qr_codes > 0):
            self.start_button.setEnabled(True)

    def _on_event_name_set(self):
        self.event_name = self.event_name_edit.text()
        self._enable_button()

    def _on_num_qr_codes_set(self):
        self.num_qr_codes = int(self.num_qr_codes_edit.text())
        self._enable_button()

    def _on_start_button_pressed(self):
        self.start_button.setEnabled(False)
        self.progress_bar.setMaximum(self.num_qr_codes)
        self.callback(self.event_name, self.num_qr_codes, ProgressIndicator(
            self.progress_bar, self.start_button))

    def __init__(self, callback):
        super().__init__()

        self.callback = callback
        self.event_name = ""
        self.num_qr_codes = 0

        self.setWindowTitle("ACR QR-Code Generator")

        layout = Qt.QVBoxLayout()
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


def create(callback):
    app = Qt.QApplication(sys.argv)
    window = MainWindow(callback)
    window.show()

    app.exec()
