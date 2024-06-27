from PyQt5 import QtWidgets
from GUI import Ui_MainWindow
import sys
from Chronometer import ChronometerThread
from PlutoSetup import CustomSDR
from unzip import convert_parquet_to_csv_and_delete


class MyGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.setupUi(self)

        # Appel des routines lors du click sur chaque ScheduleButton
        self.ScheduleButton.clicked.connect(self.on_scheduleButton_click)
        self.ConnectButton.clicked.connect(self.on_connectButton_click)
        self.UnzipButton.clicked.connect(self.unzipButton_click)

        self.upChronometerThread = ChronometerThread(count_up=True)
        self.downChronometerThread = ChronometerThread(count_up=False)

        self.upChronometer = self.upChronometerThread.chronometer
        self.downChronometer = self.downChronometerThread.chronometer



    def unzipButton_click(self):

        # Décompresser les enregsitrements
        try:
            convert_parquet_to_csv_and_delete('C:\\Users\\DEV\\Desktop\\Samuel\\AcquisitionPlutoSDR\\recordings_temp')
            self.log("Décompression des enregistrements terminée")
        except Exception as e:
            self.log("Erreur lors de la décompression des enregistrements")
            self.log(e)

    def on_connectButton_click(self):

        '''Create Radios'''
        try:
            # Afficher que la connexion au Pluto à fonctionnée
            self.my_sdr = CustomSDR(uri='ip:192.168.2.1')
            self.my_sdr.configure_rx_properties()
            self.my_sdr.configure_tx_properties()
            self.my_sdr.configure_sampling_properties()

            # Prévenir avec le log que la connexion au PlutoSDR a réussie
            self.log("Connexion au PlutoSDR réussie")

        except Exception as e:

            # Afficher dans le log l'erreur
            self.log("Erreur lors de la connexion au PlutoSDR")
            self.log(e)

        # Afficher sur le log un messsage
    def log(self, message):
        self.Log1.setPlainText(message)


    def on_scheduleButton_click(self):

        # Récupérer le contenu de inputTimer_heure, inputTimer_minute et inputTimer_seconde
        hours = int(self.inputTimer_heure.text())
        minutes = int(self.inputTimer_minute.text())
        seconds = int(self.inputTimer_seconde.text())

        # Démarer le Chronometer et le connecter à la méthode update_display
        self.startUpChronometer(hours, minutes, seconds)


    def startUpChronometer(self, hours, minutes, seconds):
        self.downChronometerThread.start()
        self.downChronometer.hours = hours
        self.downChronometer.minutes = minutes
        self.downChronometer.seconds = seconds
        self.downChronometer.time_updated.connect(self.update_display)
        self.downChronometer.start_timer()


    def update_display(self, hours, minutes, seconds):
        # print(f'{hours:02}:{minutes:02}:{seconds:02}')
        self.outputTimer_heure.setText(f'{hours:02}')
        self.outputTimer_minute.setText(f'{minutes:02}')
        self.outputTimer_seconde.setText(f'{seconds:02}')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyGUI()
    window.show()
    sys.exit(app.exec_())
