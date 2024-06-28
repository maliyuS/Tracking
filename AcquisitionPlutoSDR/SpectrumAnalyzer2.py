import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton
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

        self.markers = []

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

        layout.addLayout(control_layout)

        # Marker control buttons
        marker_control_layout = QHBoxLayout()

        add_marker_btn = QPushButton("Add Marker")
        add_marker_btn.clicked.connect(self.add_marker)
        marker_control_layout.addWidget(add_marker_btn)

        remove_marker_btn = QPushButton("Remove Marker")
        remove_marker_btn.clicked.connect(self.remove_marker)
        marker_control_layout.addWidget(remove_marker_btn)

        layout.addLayout(marker_control_layout)

        self.plot_spectrum()

    def update_parameters(self):
        """Update the spectrum plot parameters."""
        try:
            self.central_freq = float(self.central_freq_input.text())
            self.span = float(self.span_input.text())
            self.plot_spectrum()
        except ValueError:
            self.show_error("Invalid input for frequency or span.")

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

        # Re-add markers
        for marker in self.markers:
            self.plot_item.addItem(marker)

    def add_marker(self):
        """Add a new marker at the center frequency."""
        marker = pg.InfiniteLine(pos=self.central_freq, angle=90, movable=True, pen=pg.mkPen('r', width=2))
        marker.sigPositionChanged.connect(self.update_marker_text)
        self.markers.append(marker)
        self.plot_item.addItem(marker)
        self.update_marker_text()

    def remove_marker(self):
        """Remove the last added marker."""
        if self.markers:
            marker = self.markers.pop()
            self.plot_item.removeItem(marker)
            self.update_marker_text()

    def update_marker_text(self):
        """Update the text display for marker positions."""
        marker_positions = [f"{marker.value():.2f} MHz" for marker in self.markers]
        self.setWindowTitle(f"Spectrum Analyzer - Markers: {', '.join(marker_positions)}")

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
