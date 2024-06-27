from PyQt5 import QtWidgets
from GUI import Ui_MainWindow
import sys
from Chronometer import ChronometerThread


class MyGUI(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        self.setupUi(self)

        # Appel de la routine lors du click sur le ScheduleButton
        self.ScheduleButton.clicked.connect(self.on_scheduleButton_click)

        self.upChronometerThread = ChronometerThread(count_up=True)
        self.downChronometerThread = ChronometerThread(count_up=False)

        self.upChronometer = self.upChronometerThread.chronometer
        self.downChronometer = self.downChronometerThread.chronometer



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
