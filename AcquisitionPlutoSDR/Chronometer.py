import sys
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QObject

class Chronometer(QObject):
    time_updated = pyqtSignal(int, int, int)

    def __init__(self, count_up=True, start_time=(0, 0, 0)):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.hours, self.minutes, self.seconds = start_time
        self.running = False
        self.count_up = count_up  # True for count up, False for count down

    def start_timer(self):
        if not self.running:
            self.timer.start(1000)
            self.running = True

    def stop_timer(self):
        if self.running:
            self.timer.stop()
            self.running = False

    def reset_timer(self, start_time=(0, 0, 0)):
        self.timer.stop()
        self.running = False
        self.hours, self.minutes, self.seconds = start_time
        self.time_updated.emit(self.hours, self.minutes, self.seconds)

    def update_timer(self):
        if self.count_up:
            self.seconds += 1
            if self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
                if self.minutes == 60:
                    self.minutes = 0
                    self.hours += 1
        else:
            self.seconds -= 1
            if self.seconds < 0:
                self.seconds = 59
                self.minutes -= 1
                if self.minutes < 0:
                    self.minutes = 59
                    self.hours -= 1
                    if self.hours < 0:
                        self.stop_timer()
                        self.hours, self.minutes, self.seconds = 0, 0, 0 # Reset to 0
        self.time_updated.emit(self.hours, self.minutes, self.seconds)

class ChronometerThread(QThread):
    def __init__(self):
        super().__init__()
        self.chronometer = Chronometer()
        self.chronometer.moveToThread(self)

    def run(self):
        self.exec_()

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)

    chronometer_thread = ChronometerThread()
    chronometer_thread.start()  # Démarrer le thread

    chronometer = chronometer_thread.chronometer
    chronometer.start_timer()  # Démarrer le chronomètre

    def print_time(hours, minutes, seconds):
        print(f'{hours:02}:{minutes:02}:{seconds:02}')

    chronometer.time_updated.connect(print_time)

    sys.exit(app.exec_())
