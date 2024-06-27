import sys
import time
from PyQt5.QtCore import QThread, pyqtSignal, QCoreApplication, QTimer
from PlutoSetup import CustomSDR

from PlutoSetup import CustomSDR
class AcquisitionThread(QThread):
    data_received = pyqtSignal(object, object)

    def __init__(self, sdr, parent=None):
        super().__init__(parent)
        self.sdr = sdr
        self._running = False

    def run(self):
        self._running = True
        self.sdr.calibrate_rx()
        while self._running:
            data = self.sdr.receive_data()
            self.data_received.emit(data['Rx_0'], data['Rx_1'])

    def stop(self):
        self._running = False

def test_acquisition_thread():
    app = QCoreApplication(sys.argv)

    # Afficher que la connexion au Pluto à fonctionnée
    my_sdr = CustomSDR(uri='ip:192.168.2.1')
    my_sdr.configure_rx_properties()
    my_sdr.configure_tx_properties()
    my_sdr.configure_sampling_properties()

    # Initialiser le thread d'acquisition
    acquisition_thread = AcquisitionThread(my_sdr)

    # Définir un slot pour imprimer les données reçues
    def print_data(rx0, rx1):
        print("Data received:")
        print("Rx_0:", rx0)
        print("Rx_1:", rx1)

    # Connecter le signal data_received au slot print_data
    acquisition_thread.data_received.connect(print_data)

    # Démarrer le thread d'acquisition
    acquisition_thread.start()

    # Utiliser QTimer pour arrêter le thread après 5 secondes
    def stop_thread():
        acquisition_thread.stop()
        acquisition_thread.wait()
        print("Acquisition thread stopped.")
        QCoreApplication.quit()

    QTimer.singleShot(5000, stop_thread)

    # Exécuter application Qt
    sys.exit(app.exec_())

# Appeler la fonction de test
test_acquisition_thread()
