import sys
import time

import PyQt5
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton, QTabWidget, QGridLayout
)
from PyQt5.QtGui import QDoubleValidator
import pyqtgraph as pg


class SpectrumAnalyzer(QWidget):
    def __init__(self, signal=None, sampling_rate=None, parent=None):
        super().__init__(parent)
        self.central_freq = 0  # Central frequency in kHz
        self.span = 1000  # Span in kHz
        self.signal = signal
        self.sampling_rate = sampling_rate

        self.markers = []
        self.spectrum = None
        self.freqs = None

        self.init_ui()
        self.display_no_data_message()

        # Setup QTimer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_spectrum)
        self.timer.start(100)  # Update every 100 ms

    def init_ui(self):
        """Initialize the user interface components."""
        layout = QVBoxLayout(self)

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

    def display_no_data_message(self):
        """Display a message indicating no data is available."""
        self.plot_item.clear()
        self.plot_item.addItem(pg.TextItem("No Data", anchor=(0.5, 0.5), color='r', border='w'))

    def update_signal_data(self, signal, sampling_rate):
        """Update the spectrum with new signal data."""
        self.signal = signal
        self.sampling_rate = sampling_rate

    def update_parameters(self):
        """Update the spectrum plot based on new parameters."""
        try:
            if self.central_freq != float(self.central_freq_input.text()) or self.span != float(self.span_input.text()):
                self.central_freq = float(self.central_freq_input.text())
                self.span = float(self.span_input.text())
                if self.signal is not None and self.sampling_rate is not None:
                    self.plot_spectrum()
                self.update_marker_text()
        except ValueError:
            self.show_error("Invalid input for frequency or span.")

    def plot_spectrum(self):
        """Calculate and plot the frequency spectrum of the signal."""
        if self.signal is None or self.sampling_rate is None:
            self.display_no_data_message()
            return

        windowed_signal = self.signal * np.blackman(len(self.signal))
        self.spectrum = np.fft.fftshift(np.abs(np.fft.fft(windowed_signal)))
        self.spectrum /= np.sum(np.blackman(len(self.signal)))

        self.freqs = np.fft.fftshift(np.fft.fftfreq(len(self.signal), d=1 / self.sampling_rate)) / 1e3
        magnitude_db = 20 * np.log10(self.spectrum + 1e-10)

        self.plot_item.clear()
        self.plot_item.plot(self.freqs, magnitude_db, pen=pg.mkPen('w', width=2))
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

    def update_spectrum(self):
        """Update the spectrum with current signal data."""
        if self.signal is not None and self.sampling_rate is not None:
            self.plot_spectrum()
            self.update_marker_text()

    def show_error(self, message):
        """Display an error message box."""
        QMessageBox.critical(self, "Error", message)


def main():
    app = QApplication(sys.argv)
    window = QTabWidget()

    # Création de la première tab
    first_tab = QWidget()
    window.addTab(first_tab, "Première Tab")

    # Ajout du SpectrumAnalyzer au layout
    analyzer = SpectrumAnalyzer()
    window.addTab(analyzer, "Spectrum Analyzer")

    # Paramètres de la fenêtre
    window.setWindowTitle("Spectrum Analyzer")
    window.resize(800, 600)
    window.show()

    t = np.linspace(0, 1, 1000)
    signals = [
        np.sin(2 * np.pi * 100000 * t),
        np.sin(2 * np.pi * 200000 * t),
        np.cos(2 * np.pi * 300000 * t),
        np.sin(2 * np.pi * 100000 * t) + 0.5 * np.sin(2 * np.pi * 150000 * t),
    ]
    sampling_rate = 1000000

    def update_signal(index=[0]):
        analyzer.update_signal_data(signals[index[0]], sampling_rate)
        index[0] = (index[0] + 1) % len(signals)

    timer = QTimer()
    timer.timeout.connect(update_signal)
    timer.start(1000)  # Change signal every 10 seconds

    sys.exit(app.exec_())
# main()