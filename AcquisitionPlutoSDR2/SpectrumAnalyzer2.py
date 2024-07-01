import numpy as np
import pyqtgraph as pg
from PyQt5.QtCore import QTimer


class SpectrumAnalyzer(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__(show=True, size=(500, 500))

        # Paramètres d'acquisition
        self.numsamples = 2**18
        self.sampling_rate = 30e6
        self.phase_cal = 0
        self.delay_phases = np.arange(-180, 182, 1)  # phase delay in degrees // genère le tableur des phase de -180 à 181

        # Variable d'affichage
        self.span = 1e6 # Span en Hz
        self.y1 = float(-100)
        self.y2 = float(0)

        self.Title = "Amplitude (dB)"  # Ajout de la définition de self.Title

        # Configuration de la fenêtre FFT
        self.setup_fft_window()

        # Timer pour mettre à jour le graphique
        timer = QTimer(self)
        timer.timeout.connect(self.update_plot)
        timer.start(0)

        self.freqs = None
        self.fft_signal_db = None


        ''' Set up FFT Window '''
    def setup_fft_window(self):

        self.p1 = self.addPlot()
        self.p1.showGrid(x=True, y=True)

        ## Scale of span from the Editbox
        self.p1.setXRange(-self.span/2, self.span/2)
        self.p1.setYRange(self.y1, self.y2)
        self.p1.setLabel('bottom', 'frequency', '[KHz]', **{'color': '#FFF', 'size': '14pt'})
        self.p1.setLabel('left', self.Title, **{'color': '#FFF', 'size': '14pt'})

        # Curves
        self.baseCurve = self.p1.plot()


    # Calcul de la FFT

    def compute_fft(self, signal):

        # Calculer le signal fenêtré
        windowed_signal = signal * np.blackman(len(signal))

        # Calculer la FFT
        fft_signal = np.fft.fftshift(np.abs(np.fft.fft(windowed_signal, len(signal))))
        fft_signal /= np.sum(np.blackman(len(signal)))
        self.fft_signal_db = 20 * np.log10(fft_signal + 1e-10)

        # Calculer l'axe des fréquences en kHz
        self.freqs = np.fft.fftshift(np.fft.fftfreq(len(signal), d=1 / len(signal))) / 1e3


# Mise à jour du graphique
    def update_plot(self):
        if self.fft_signal_db is not None and self.freqs is not None:
            self.baseCurve.setData(self.freqs, self.fft_signal_db)
