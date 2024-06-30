import PyQt5.QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets
from GUI.GUI import Ui_MainWindow
from GUI.Chronometer import ChronometerThread
from PlutoSetup import CustomSDR
from acquisition import AcquisitionThread
from unzip import convert_parquet_to_csv_and_delete
from SpectrumAnalyzer import SpectrumAnalyzer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout,
    QLabel, QLineEdit, QMessageBox, QPushButton, QTabWidget, QGridLayout
)
import numpy as np

import sys


class MyGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.setupUi(self)

        # Lier les boutons aux routines d'acquisition
        self.ConnectButton.clicked.connect(self.on_connectButton_click)
        self.AcquireButton.clicked.connect(self.on_acquisitionButton_click)
        self.STOPbutton.clicked.connect(self.on_stopButton_click)

        #Lier les boutons aux routines pour enregistrer les données
        self.ScheduleButton.clicked.connect(self.on_scheduleButton_click)
        self.UnzipButton.clicked.connect(self.on_unzipButton_click)
        self.ImmediateRecordingButton.clicked.connect(self.on_immediateRecordingButton_click)

        # Initialiser les chronomètres Up/Down
        self.upChronometerThread = ChronometerThread(count_up=True)
        self.downChronometerThread = ChronometerThread(count_up=False)
        self.upChronometer = self.upChronometerThread.chronometer
        self.downChronometer = self.downChronometerThread.chronometer

        # Ajout du SpectrumAnalyzer au notebook
        self.analyzer = SpectrumAnalyzer()
        self.Notebook.insertTab(1, self.analyzer, "Spectrum Analyzer")
        self.sampling_rate = 30e6 # Pour l'instant on fixe le taux d'échantillonnage à 30 MHz

        # Initialiser le dictionnaire pour stocker les données reçues
        self.data = {}

########################################################################################################################

    """Les fonctions évenementielles de l'interface graphique"""

    def on_connectButton_click(self):
        '''Create Radios'''
        try:
            if hasattr(self, 'my_sdr'):
                self.log("Déjà connecté au PlutoSDR", color='red')
                return

            # Récupérer l'adresse IP du PlutoSDR
            uri = 'ip:' + self.ip_input.text()

            # Afficher que la connexion au Pluto à fonctionnée
            self.my_sdr = CustomSDR(uri=uri)
            self.my_sdr.configure_rx_properties()
            self.my_sdr.configure_tx_properties()
            self.my_sdr.configure_sampling_properties()

            # Prévenir avec le log que la connexion au PlutoSDR a réussie
            self.log("Connexion au PlutoSDR réussie", color='green')

        except Exception as e:

            # Afficher dans le log l'erreur
            self.log("Erreur lors de la connexion au PlutoSDR", color='red')
            self.log(str(e), color='red')

########################################################################################################################
    # Initialiser le thread d'acquisition
    def on_acquisitionButton_click(self):

        # Si le sdr est vide, on ne peut pas lancer l'acquisition
        if not hasattr(self, 'my_sdr'):
            self.log("Veuillez d'abord vous connecter au PlutoSDR", color='red')
            return

        # Lancer le thread d'acquisition
        self.acquisition_thread = AcquisitionThread(self.my_sdr)
        self.log("Acquisition en cours ...", color='green')

        # Définir un slot pour stocker les données reçues
        def on_data_received(rx0, rx1):
            self.data['Rx0'] = rx0
            self.data['Rx1'] = rx1
            self.analyzer.update_signal_data(rx0, self.sampling_rate)
            print("Data received:")
            print("Rx_0:", self.data['Rx0'])
            print("Rx_1:", self.data['Rx1'])

        # Connecter le signal data_received au slot on_data_received
        self.acquisition_thread.data_received.connect(on_data_received)

        # Démarrer le thread d'acquisition
        self.acquisition_thread.start()

########################################################################################################################
    def on_stopButton_click(self):

        # Arrêter le thread d'acquisition
        if hasattr(self, 'acquisition_thread'):
            self.acquisition_thread.stop()
            self.acquisition_thread.wait()
            del self.acquisition_thread
            self.log("Acquisition arrêtée", color='green')

        else:
            self.log("Aucune acquisition en cours", color='red')

########################################################################################################################
    def on_scheduleButton_click(self):

        # Vérification de l'existence de l'attribut après suppression
        if not hasattr(self, 'acquisition_thread'):
            self.log("Impossible de programmer un enregistrement: aucune acquisition en cours !", color='red')
            return

        # Récupérer le contenu de inputTimer_heure, inputTimer_minute et inputTimer_seconde
        hours = int(self.inputTimer_heure.text())
        minutes = int(self.inputTimer_minute.text())
        seconds = int(self.inputTimer_seconde.text())

        self.log('Enregistrement programmé dans : ' + f'{hours:02}:{minutes:02}:{seconds:02}', color='green')

        # Démarer le Chronometer et le connecter à la méthode on_timeUpdated
        self.startUpChronometer(hours, minutes, seconds)

    def on_immediateRecordingButton_click(self):

        # Vérification de l'existence de l'attribut après suppression
        if not hasattr(self, 'acquisition_thread'):
            self.log("Veuillez d'abord lancer l'acquisition !", color='red')
            return

        self.acquisition_thread._ImmediateSaving = True

        self.log("Enregistrement d'une séquence d'acquisition ...", color='green')

########################################################################################################################
    def on_unzipButton_click(self):

        if hasattr(self, 'acquisition_thread'):
            self.log("Veuillez d'abord arrêter l'acquisition avant de décompresser les enregistrements", color='red')
            return

        # Décompresser les enregsitrements
        try:
            convert_parquet_to_csv_and_delete('C:\\Users\\DEV\\Desktop\\Samuel\\AcquisitionPlutoSDR2\\recordings_temp')
            self.log("Décompression des enregistrements terminée", color='green')

        except Exception as e:
            self.log("Erreur lors de la décompression des enregistrements", color='red')
            self.log(e, color='red')

########################################################################################################################

    """ Gérer les chronomètres Up/Down"""
    def startUpChronometer(self, hours, minutes, seconds):
        self.downChronometerThread.start()
        self.downChronometer.time_updated.connect(self.on_timeUpdated)
        self.downChronometer.start_timer(hours, minutes, seconds)
        self.changeColor("red")

########################################################################################################################
    def on_timeUpdated(self, hours, minutes, seconds):

        # Vérification de l'existence de l'attribut après suppression
        if not hasattr(self, 'acquisition_thread'):
            self.log("Attention: L'enregistrement à été déprogrammé !", color='orange')
            self.downChronometer.stop_timer()
            self.downChronometerThread.quit()
            self.outputTimer_heure.setText("00")
            self.outputTimer_minute.setText("00")
            self.outputTimer_seconde.setText("00")
            return

        # print(f'{hours:02}:{minutes:02}:{seconds:02}')
        self.outputTimer_heure.setText(f'{hours:02}')
        self.outputTimer_minute.setText(f'{minutes:02}')
        self.outputTimer_seconde.setText(f'{seconds:02}')


        # Si le chronomètre est terminé, arrêter le thread et démarrer l'enregistrement
        if hours == 0 and minutes == 0 and seconds == 0:
            # Arrêter le chronomètre
            self.downChronometer.stop_timer()
            self.downChronometerThread.quit()
            self.log("Chronomètre terminé", color='green')

            # Démarrer l'enregistrement
            self.log("Démarrage des enregistrements...", color='green')
            self.acquisition_thread._scheduleSaving = True

########################################################################################################################
    def changeColor(self, color):
        self.outputTimer_heure.setStyleSheet(f"color: {color}")
        self.outputTimer_minute.setStyleSheet(f"color: {color}")
        self.outputTimer_seconde.setStyleSheet(f"color: {color}")

########################################################################################################################

    """Méthode pour afficher un message dans le log"""
    def log(self, message, color='black'):
        # Utilisation de HTML pour définir la couleur du texte
        self.Log1.appendHtml(f"<span style='color: {color};'>{message}</span>")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyGUI()
    window.show()
    sys.exit(app.exec_())