import sys
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton
)
from PyQt5.QtGui import QDoubleValidator
import pyqtgraph as pg

class SpectrumAnalyzer(QMainWindow):
    def __init__(self, signal, sampling_rate):
        super().__init__()
        self.setWindowTitle("Spectrum Analyzer")
        self.setGeometry(100, 100, 800, 600)

        self.central_freq = 0  # Central frequency in kHz
        self.span = 1000  # Span in kHz
        self.signal = signal
        self.sampling_rate = sampling_rate

        self.markers = []
        self.spectrum = None
        self.freqs = None

        self.init_ui()
        self.plot_spectrum()

    def init_ui(self):
        """Initialize the user interface components."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.setup_plot_widget(layout)
        self.setup_control_layout(layout)
        self.setup_marker_controls(layout)

    def setup_plot_widget(self, layout):
        """Setup the plot widget."""
        self.plot_widget = pg.PlotWidget()
        self.plot_item = self.plot_widget.getPlotItem()
        self.plot_item.setLabel('bottom', 'Frequency', units='kHz')
        self.plot_item.setLabel('left', 'Amplitude', units='dB')
        self.plot_item.showGrid(x=True, y=True, alpha=0.3)
        layout.addWidget(self.plot_widget)

    def setup_control_layout(self, layout):
        """Setup control layout for frequency and span inputs."""
        control_layout = QHBoxLayout()

        control_layout.addWidget(QLabel("Center Frequency (kHz):"))
        self.central_freq_input = QLineEdit(str(self.central_freq))
        self.central_freq_input.setValidator(QDoubleValidator(-1e6, 1e6, 2))
        self.central_freq_input.returnPressed.connect(self.update_parameters)
        control_layout.addWidget(self.central_freq_input)

        control_layout.addWidget(QLabel("Span (kHz):"))
        self.span_input = QLineEdit(str(self.span))
        self.span_input.setValidator(QDoubleValidator(0, 1e6, 2))
        self.span_input.returnPressed.connect(self.update_parameters)
        control_layout.addWidget(self.span_input)

        layout.addLayout(control_layout)

    def setup_marker_controls(self, layout):
        """Setup marker control buttons."""
        marker_control_layout = QHBoxLayout()

        add_marker_btn = QPushButton("Add Marker")
        add_marker_btn.clicked.connect(self.add_marker)
        marker_control_layout.addWidget(add_marker_btn)

        remove_marker_btn = QPushButton("Remove Marker")
        remove_marker_btn.clicked.connect(self.remove_marker)
        marker_control_layout.addWidget(remove_marker_btn)

        layout.addLayout(marker_control_layout)

        self.marker_info_layout = QHBoxLayout()
        layout.addLayout(self.marker_info_layout)

    def update_parameters(self):
        """Update the spectrum plot based on new parameters."""
        try:
            self.central_freq = float(self.central_freq_input.text())
            self.span = float(self.span_input.text())
            self.plot_spectrum()
            self.update_marker_text()
        except ValueError:
            self.show_error("Invalid input for frequency or span.")

    def plot_spectrum(self):
        """Calculate and plot the frequency spectrum of the signal."""
        windowed_signal = self.signal * np.blackman(len(self.signal))
        self.spectrum = np.fft.fftshift(np.abs(np.fft.fft(windowed_signal)))
        self.spectrum /= np.sum(np.blackman(len(self.signal)))

        self.freqs = np.fft.fftshift(np.fft.fftfreq(len(self.signal), d=1 / self.sampling_rate)) / 1e3
        magnitude_db = 20 * np.log10(self.spectrum + 1e-10)

        self.plot_item.clear()
        self.plot_item.plot(self.freqs, magnitude_db, pen=pg.mkPen('b', width=2))
        self.plot_item.setXRange(self.central_freq - self.span / 2, self.central_freq + self.span / 2)
        self.plot_item.setYRange(-100, 50)

        for marker in self.markers:
            self.plot_item.addItem(marker)
        self.update_marker_text()

    def add_marker(self):
        """Add a movable marker to the plot."""
        if len(self.markers) < 2:
            marker = pg.InfiniteLine(pos=self.central_freq, angle=90, movable=True, pen=pg.mkPen('r', width=2))
            marker.sigPositionChanged.connect(self.update_marker_text)
            self.markers.append(marker)
            self.plot_item.addItem(marker)
            self.update_marker_text()

    def remove_marker(self):
        """Remove the most recently added marker."""
        if self.markers:
            marker = self.markers.pop()
            self.plot_item.removeItem(marker)
            self.update_marker_text()

    def update_marker_text(self):
        """Update text labels for markers showing frequency and amplitude."""
        for i in reversed(range(self.marker_info_layout.count())):
            self.marker_info_layout.itemAt(i).widget().setParent(None)

        if len(self.markers) == 2:
            marker_info = []
            for i, marker in enumerate(self.markers):
                freq = marker.value()
                idx = np.abs(self.freqs - freq).argmin()
                amplitude_db = 20 * np.log10(self.spectrum[idx] + 1e-10)
                marker_info.append(f"M{i + 1}: {freq:.2f} kHz, {amplitude_db:.2f} dB")
                self.marker_info_layout.addWidget(QLabel(marker_info[-1]))

            delta_freq = abs(self.markers[1].value() - self.markers[0].value())
            delta_amp = abs(
                float(marker_info[1].split(', ')[1].split()[0]) -
                float(marker_info[0].split(', ')[1].split()[0])
            )
            delta_label = QLabel(f"ΔF: {delta_freq:.2f} kHz, ΔA: {delta_amp:.2f} dB")
            self.marker_info_layout.addWidget(delta_label)

    def show_error(self, message):
        """Display an error message box."""
        QMessageBox.critical(self, "Error", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = np.linspace(0, 1, 1000)  # 1 second period
    example_signal = np.sin(2 * np.pi * 100000 * t)  # 100 kHz sine wave
    sampling_rate = 1000000  # 1 MHz sampling rate
    analyzer = SpectrumAnalyzer(example_signal, sampling_rate)
    analyzer.show()
    sys.exit(app.exec_())
