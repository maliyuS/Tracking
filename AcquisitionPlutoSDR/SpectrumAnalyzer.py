import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator
import pyqtgraph as pg


class SpectrumAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spectrum Analyzer")
        self.setGeometry(100, 100, 800, 600)

        self.central_freq = 100  # Central frequency in MHz
        self.span = 20  # Span in MHz

        self.initUI()

    def initUI(self):
        """Initialize the user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Plot area
        self.plot_widget = pg.PlotWidget()
        self.plot_item = self.plot_widget.getPlotItem()
        self.plot_item.setLabel('bottom', 'Frequency', units='MHz')
        self.plot_item.setLabel('left', 'Amplitude', units='dB')
        self.plot_item.showGrid(x=True, y=True, alpha=0.3)  # Adding grids
        layout.addWidget(self.plot_widget)

        # Controls
        control_layout = QHBoxLayout()

        # Central frequency control
        control_layout.addWidget(QLabel("Center Frequency (MHz):"))
        self.central_freq_input = QLineEdit(str(self.central_freq))
        self.central_freq_input.setValidator(QDoubleValidator(0, 10 ** 6, 2))
        self.central_freq_input.setReadOnly(False)
        self.central_freq_input.returnPressed.connect(self.update_parameters)
        control_layout.addWidget(self.central_freq_input)

        # Span control
        control_layout.addWidget(QLabel("Span (MHz):"))
        self.span_input = QLineEdit(str(self.span))
        self.span_input.setValidator(QDoubleValidator(0, 10 ** 6, 2))
        self.span_input.setReadOnly(False)
        self.span_input.returnPressed.connect(self.update_parameters)
        control_layout.addWidget(self.span_input)

        # Marker
        control_layout.addWidget(QLabel("Marker (MHz):"))
        self.marker_pos = QLineEdit("")
        self.marker_pos.setValidator(QDoubleValidator(0, 10 ** 6, 2))
        self.marker_pos.setReadOnly(False)
        self.marker_pos.returnPressed.connect(self.update_parameters)
        control_layout.addWidget(self.marker_pos)

        layout.addLayout(control_layout)

        self.plot_spectrum()

    def update_parameters(self):
        """Update the spectrum plot parameters."""
        try:
            self.central_freq = float(self.central_freq_input.text())
            self.span = float(self.span_input.text())
            self.plot_spectrum()
        except ValueError:
            self.show_error("Invalid input for frequency or span.")

        if self.marker_pos.text():
            try:
                marker_freq = float(self.marker_pos.text())
                self.update_marker(marker_freq)
            except ValueError:
                self.show_error("Invalid input for marker frequency.")

    def plot_spectrum(self):
        """Plot the spectrum based on the current parameters."""
        central_freq_hz = self.central_freq * 1e6  # Convert to Hz
        span_hz = self.span * 1e6  # Convert to Hz

        freqs = np.linspace(central_freq_hz - span_hz / 2, central_freq_hz + span_hz / 2, 1000)
        signal = np.sinc((freqs - central_freq_hz) / 1e6)  # Example signal

        self.plot_item.clear()
        self.plot_item.plot(freqs / 1e6, 20 * np.log10(np.abs(signal)),
                            pen=pg.mkPen('b', width=2))  # Convert Hz to MHz for plotting

        # Update axis range
        self.plot_item.setXRange(self.central_freq - self.span / 2, self.central_freq + self.span / 2)
        self.plot_item.setYRange(-100, 0)  # Example range for dB

    def update_marker(self, marker_freq):
        """Update the marker position on the plot."""
        marker_freq_hz = marker_freq * 1e6  # Convert to Hz
        marker_amp = 20 * np.log10(np.abs(np.sinc((marker_freq_hz - self.central_freq * 1e6) / 1e6)))
        self.plot_item.plot([marker_freq], [marker_amp], pen=None, symbol='o', symbolBrush='r',
                            symbolSize=10)  # Larger marker

    def show_error(self, message):
        """Show an error message dialog."""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    analyzer = SpectrumAnalyzer()
    analyzer.show()
    sys.exit(app.exec_())
