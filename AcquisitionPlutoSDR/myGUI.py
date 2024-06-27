from asyncio import sleep

from PyQt6 import QtWidgets
from GUI import Ui_MainWindow
from Chronometer import ChronometerThread
import sys


class myGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(myGUI, self).__init__()
        self.setupUi(self)

        self.chronometer_thread = ChronometerThread()
        self.chronometer_thread.start()

        self.chronometer = self.chronometer_thread.chronometer
        self.chronometer.time_updated.connect(self.update_display)

        # Déclencher le chronomètre lors de l'appuie sur le bouton Schedule
        self.ScheduleButton.clicked.connect(self.on_scheduleButton_click)


    def on_scheduleButton_click(self):
        # récupérer le contenu de inputTimer_heure, inputTimer_minute et inputTimer_seconde
        hours = int(self.inputTimer_heure.text())
        minutes = int(self.inputTimer_minute.text())
        seconds = int(self.inputTimer_seconde.text())

        # Compte à rebours à partir de l'heure, minute et seconde récupérées
        self.chronometer_thread.start()  # Démarrer le thread
        self.chronometer.start_timer()  # Démarrer le chronomètre

        sleep(1000)

        seconde = self.chronometer.seconds
        print(seconde)

    def updated(self):
        minute = self.chronometer.minutes
        print(minute)




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = myGUI()

    window.show()
    sys.exit(app.exec())
