# The TPZ Company by Seb
# For a new traget instalaltion: install first Python then install PySide6 like this:pip install PySide6
# Installer dans un CMD en admin : pip install pyadi-iio
# Installer dans un CMD en admin : pip install pyadi-iio[jesd]
# Do an install : pip install matplotlib
# Do an install : pip install pyqtgraph
# Do an install : pip install PyQt5 PyQtWebEngine
# upgrade :python.exe -m pip install --upgrade pip
# Connect a pluto SDR in the USB and check the IP
# Enjoy :-)

import sys
import adi
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
import math
matplotlib.use('Qt5Agg')
import pyqtgraph as pg

#from math import pi

#################################### Binding IMPORT FROM PyQt5

#from PyQt5.QtWidgets import *
#from PyQt5.QtCore import Qt
#from PyQt5.QtGui import *

from pyqtgraph.Qt import QtCore, QtGui, QtWidgets

from PyQt5.QtGui import ( QIcon)

from PyQt5.QtCore import QTime, QTimer, Qt

from PyQt5.QtWidgets import (QApplication, QDialog,
                               QDialogButtonBox,  QGroupBox,
                                QHBoxLayout, QLabel, QLineEdit,
                               QMenu, QMenuBar, QPushButton,
                               QTextEdit, QVBoxLayout, QSizePolicy, QComboBox)


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


#################################### Structure
class Dialog(QDialog):


    def __init__(self, *args, **kwargs):

        super(Dialog, self).__init__(*args, **kwargs)

        # creating graphics layout widget
        self.win = pg.GraphicsLayoutWidget(show=True, size=(500, 500))


        ######### Declaration of fonctions

        self.create_log_window() # start the fonction in object
        self.create_horizontal_settings_RX() # start the fonction in object
        self.create_horizontal_settings_TX() # start the fonction in object
        self.create_horizontal_settings_IP() # start the fonction in object
        self.create_horizontal_app() # start the fonction in object
        self.Clock() # start the fonction in object
        self.show_time() # start the fonction in object
        self.create_graph()# start the fonction in object
        self.Create_button_Cancel()# start the fonction in object

        ########## create the instance in the layout
        main_layout = QVBoxLayout()  # add the main window
        main_layout.addWidget(self._horizontal_settings_IP)# add horizontal_settings_SEND
        main_layout.addWidget(self._horizontal_settings_RX)# add horizontal_settings_RX
        main_layout.addWidget(self._horizontal_settings_TX)# add horizontal_settings_TX
        main_layout.addWidget(self._horizontal_app)# add horizontal_settings_TX
        main_layout.addWidget(self._log_window)# add big_editor
        main_layout.addWidget(self.win) # add plotting layout
        main_layout.addWidget(self._button_Cancel)# add button_box_Cancel
        self.setLayout(main_layout) # display the full layout

        ######## configure the window
        self.setWindowTitle("SDRpluto Interface")
        # setting of the window width & height
        #width = 1500
        # setting  the fixed width of window
        #self.setFixedWidth(width)
        #height= 1000
        #self.setMinimumSize(width, height)
        #self.setFixedHeight(height)
        # opening window in maximized size
        self.showMaximized()
        self.setWindowIcon(QIcon('icon.png'))

    def create_graph(self):
        print ("")

            #self.sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

######################################## IP & Send parameters to Pluto

    def create_horizontal_settings_IP(self):
        self._horizontal_settings_IP = QGroupBox("Send parameters to Pluto")
        layout = QHBoxLayout()
        self._horizontal_settings_IP.setLayout(layout)


        # create label _IP_pluto
        self._IP_pluto = QLabel("IP Pluto: ")
        self._IP_pluto.setAlignment(Qt.AlignLeft)
        layout.addWidget(self._IP_pluto)


        # create _Line_edit_IP_pluto
        self._Line_edit_IP_pluto = QLineEdit()
        self._Line_edit_IP_pluto.setText("192.168.5.1")
        self._Line_edit_IP_pluto.setMinimumWidth(150)
        self._Line_edit_IP_pluto.setMaximumWidth(160)
        self._Line_edit_IP_pluto.setAlignment(Qt.AlignCenter)
        layout.setAlignment(self._Line_edit_IP_pluto, Qt.AlignLeft)
        layout.addWidget(self._Line_edit_IP_pluto)

        # Create a push _Send_Button
        self._Send_Button = QPushButton("Connect and send settings to Pluto", self)
        self._Send_Button.setMinimumWidth(800)
        self._Send_Button.setMaximumWidth(1500)
        self._Send_Button.setStyleSheet("background-color: yellow")
        layout.addWidget(self._Send_Button)
        self._Send_Button.clicked.connect(self.Connect_send_settings)


######################################## RX Settings

    def create_horizontal_settings_RX(self):
        self._horizontal_settings_RX = QGroupBox("RX Settings")
        layout = QHBoxLayout()
        self._horizontal_settings_RX.setLayout(layout)

        # create label _Frequency_RX
        self._Frequency_RX = QLabel("Frequency RX: ")
        self._Frequency_RX.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._Frequency_RX)

        # create _Line_edit_Frequency_RX
        self._Line_edit_Frequency_RX = QLineEdit()
        self._Line_edit_Frequency_RX.setText("2250")
        self._Line_edit_Frequency_RX.setFixedWidth(50)
        self._Line_edit_Frequency_RX.setAlignment(Qt.AlignCenter)
        self._Line_edit_Frequency_RX.setStyleSheet("background-color: lightgreen")
        layout.addWidget(self._Line_edit_Frequency_RX)

        # create label _space
        self._space = QLabel("MHz                                        ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label _Fsampling_RX
        self._Fsampling_RX = QLabel("Fsampling RX: ")
        layout.addWidget(self._Fsampling_RX)

        # create _Line_edit_Fsampling
        self._Line_edit_Fsampling_RX = QLineEdit()
        self._Line_edit_Fsampling_RX.setText("10")
        self._Line_edit_Fsampling_RX.setFixedWidth(50)
        self._Line_edit_Fsampling_RX.setAlignment(Qt.AlignCenter)
        self._Line_edit_Fsampling_RX.setStyleSheet("background-color: lightgreen")
        layout.addWidget(self._Line_edit_Fsampling_RX)

        # create label _space
        self._space = QLabel("MHz                                        ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label _Filter_RX
        self._Filter_RX = QLabel("Filter RX: ")
        layout.addWidget(self._Filter_RX)
        # create _Line_edit_Filter_RX
        self._Line_edit_Filter_RX = QLineEdit()
        self._Line_edit_Filter_RX.setText("1.0")
        self._Line_edit_Filter_RX.setFixedWidth(50)
        self._Line_edit_Filter_RX.setAlignment(Qt.AlignCenter)
        self._Line_edit_Filter_RX.setAlignment(Qt.AlignCenter)
        self._Line_edit_Filter_RX.setStyleSheet("background-color: lightgreen")
        layout.addWidget(self._Line_edit_Filter_RX)

        # create label _space
        self._space = QLabel("MHz                                        ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label _rx0_gain
        self._rx0_gain = QLabel("RX0_gain: ")
        layout.addWidget(self._rx0_gain)
        # create _Line_edit_rx0_gain
        self._Line_edit_rx0_gain = QLineEdit()
        self._Line_edit_rx0_gain.setText("40")
        self._Line_edit_rx0_gain.setFixedWidth(40)
        self._Line_edit_rx0_gain.setAlignment(Qt.AlignCenter)
        self._Line_edit_rx0_gain.setStyleSheet("background-color: lightgreen")
        layout.addWidget(self._Line_edit_rx0_gain)

        # create label _space
        self._space = QLabel("dB                                        ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label _rx1_gain
        self._rx1_gain = QLabel("RX1_gain: ")
        layout.addWidget(self._rx1_gain)

        # create _Line_edit_rx1_gain
        self._Line_edit_rx1_gain = QLineEdit()
        self._Line_edit_rx1_gain.setText("40")
        self._Line_edit_rx1_gain.setFixedWidth(40)
        self._Line_edit_rx1_gain.setAlignment(Qt.AlignCenter)
        self._Line_edit_rx1_gain.setStyleSheet("background-color: lightgreen")
        layout.addWidget(self._Line_edit_rx1_gain)

        # create label _space
        self._space = QLabel("dB                                        ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label CAG
        self._CAG = QLabel("CAG :")
        self._CAG.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._CAG)

        #layout = QHBoxLayout()
        self.CAG = QComboBox()
        self.CAG.addItem("manual")
        self.CAG.addItem("slow_attack")
        self.CAG.setFixedWidth(80)
        self.CAG.setStyleSheet("background-color: lightgreen")
        layout.addWidget(self.CAG)

        # create label _space
        self._space = QLabel("MHz                                        ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label _NumSamples
        self._NumSamples = QLabel("NumSamples: ")
        self._NumSamples.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._NumSamples)

        # create _Line_edit_NumSamples
        self._Line_edit_NumSamples = QLineEdit()
        self._Line_edit_NumSamples.setText("10000")
        self._Line_edit_NumSamples.setFixedWidth(70)
        self._Line_edit_NumSamples.setAlignment(Qt.AlignCenter)
        self._Line_edit_NumSamples.setStyleSheet("background-color: lightgreen")
        layout.addWidget(self._Line_edit_NumSamples)

        # create label _space
        self._space = QLabel("MHz                                      ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

    ######################################## TX Settings

    def create_horizontal_settings_TX(self):
        self._horizontal_settings_TX = QGroupBox("TX Settings")
        layout = QHBoxLayout()
        self._horizontal_settings_TX.setLayout(layout)

        # create label _Frequency_TX
        self._Frequency_TX = QLabel("Frequency TX: ")
        self._Frequency_TX.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._Frequency_TX)

        # create _Line_edit_Frequency_TX
        self._Line_edit_Frequency_TX = QLineEdit()
        self._Line_edit_Frequency_TX.setText("2250")
        self._Line_edit_Frequency_TX.setFixedWidth(50)
        self._Line_edit_Frequency_TX.setAlignment(Qt.AlignCenter)
        self._Line_edit_Frequency_TX.setStyleSheet("background-color: pink")
        layout.addWidget(self._Line_edit_Frequency_TX)

        # create label _space
        self._space = QLabel("MHz                                  ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label _Frequency_SHIFT
        self._Frequency_SHIFT = QLabel("Frequency Shift: ")
        self._Frequency_SHIFT.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._Frequency_SHIFT)

        # create _Line_edit_Frequency_SHIFT
        self._Line_edit_Frequency_SHIFT = QLineEdit()
        self._Line_edit_Frequency_SHIFT.setText("0.1")
        self._Line_edit_Frequency_SHIFT.setFixedWidth(50)
        self._Line_edit_Frequency_SHIFT.setAlignment(Qt.AlignCenter)
        self._Line_edit_Frequency_SHIFT.setStyleSheet("background-color: pink")
        #self._Line_edit_Frequency_SHIFT.setAlignment(PyQt5.Core.AlignmentFlag.AlignCenter)
        layout.addWidget(self._Line_edit_Frequency_SHIFT)

        # create label _space
        self._space = QLabel("KHz                                  ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label _tx_gain
        self._tx_gain = QLabel("TX_gain: ")
        layout.addWidget(self._tx_gain)

        # create _Line_edit_tx_gain
        self._Line_edit_tx_gain = QLineEdit()
        self._Line_edit_tx_gain.setText("-88")
        self._Line_edit_tx_gain.setFixedWidth(40)
        self._Line_edit_tx_gain.setStyleSheet("background-color: pink")
        self._Line_edit_tx_gain.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._Line_edit_tx_gain)

        # create label _space
        self._space = QLabel("dB                                  ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label SPAN
        self._SPAN = QLabel("SPAN : ")
        self._SPAN.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._SPAN)

        # create _SPAN
        self._SPAN = QLineEdit()
        self._SPAN.setText("3")
        self._SPAN.setFixedWidth(50)
        self._SPAN.setAlignment(Qt.AlignCenter)
        self._SPAN.setStyleSheet("background-color: lightblue")
        layout.addWidget(self._SPAN)

        # create label _space
        self._space = QLabel("MHz                                  ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label Title
        self._Title = QLabel("Title : ")
        self._Title.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._Title)

        # create _Title_LineEdit
        self._Title_LineEdit = QLineEdit()
        self._Title_LineEdit.setText("Spectrum:")
        self._Title_LineEdit.setFixedWidth(100)
        self._Title_LineEdit.setAlignment(Qt.AlignCenter)
        self._Title_LineEdit.setStyleSheet("background-color: lightblue")
        layout.addWidget(self._Title_LineEdit)

        # create label _space
        self._space = QLabel("                                  ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)


        # create label Phase_cal
        self._Phase_cal = QLabel("Phase_cal: ")
        self._Phase_cal.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._Phase_cal)

        # create _phase_cal
        self._Phase_cal = QLineEdit()
        self._Phase_cal.setText("0")
        self._Phase_cal.setFixedWidth(50)
        self._Phase_cal.setAlignment(Qt.AlignCenter)
        self._Phase_cal.setStyleSheet("background-color: lightblue")
        layout.addWidget(self._Phase_cal)

        # create label _space
        self._space = QLabel("°                                  ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # create label RPM
        self.RPM = QLabel("Samples speed: ")
        self.RPM.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.RPM)

        # create _RPM
        self._RPM = QLineEdit()
        self._RPM.setText("0.1")
        self._RPM.setFixedWidth(50)
        self._RPM.setAlignment(Qt.AlignCenter)
        self._RPM.setStyleSheet("background-color: lightblue")
        layout.addWidget(self._RPM)

        # create label _space
        self._space = QLabel("                     ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

        # Create a push _Clear_Button
        self._Clear_Button = QPushButton("Clear Graph", self)
        self._Clear_Button.setGeometry(50, 80, 50, 40)  # (x, y, width, height)
        self._Clear_Button.setStyleSheet("background-color: red")
        layout.addWidget(self._Clear_Button)

        self._Clear_Button.clicked.connect(self.Clear_Graph)

        # create label _space
        self._space = QLabel("                                  ")
        self._space.setAlignment(Qt.AlignCenter)
        layout.addWidget(self._space)

    def Clear_Graph(self):
        print("Clear graph")
        self.win.clear()


######################################## Pluto App start

    def create_horizontal_app(self):
        self._horizontal_app = QGroupBox("Start tests or application")
        layout = QHBoxLayout()
        self._horizontal_app.setLayout(layout)

        # Create a push button
        self._button_app1 = QPushButton("Beamforming App (Jon Kraft)", self)
        layout.addWidget(self._button_app1)
        self._button_app1.clicked.connect(self.Start_app1)

        # Create a push button
        self._button_app2 = QPushButton("IQ App (Jon Kraft)", self)
        layout.addWidget(self._button_app2)
        self._button_app2.clicked.connect(self.Start_app2)

        # Create a push button
        self._button_app3 = QPushButton("Spectrum in loop", self)
        layout.addWidget(self._button_app3)
        self._button_app3.clicked.connect(self.Start_app3)

        # Create a push button
        self._button_app4 = QPushButton("RX0 Spectrum", self)
        layout.addWidget(self._button_app4)
        self._button_app4.clicked.connect(self.Start_app4)

        # Create a push button
        self._button_app5 = QPushButton("RX1 Spectrum", self)
        layout.addWidget(self._button_app5)
        self._button_app5.clicked.connect(self.Start_app5)

        # Create a push button
        self._button_app6 = QPushButton("App6", self)
        layout.addWidget(self._button_app6)
        self._button_app6.clicked.connect(self.Start_app6)

################################## Update settings

    def Update_settings(self):
        # neg and pos give the value of span, span is updated with TextEDitbox SPAN
        global neg, pos
        neg= float (-10.00)
        pos= float (10.00)

        self.Date()

        self.IP_pluto= self._Line_edit_IP_pluto.text()
        print("Send to PLuto IP address =>",self.IP_pluto)

        self.rx_lo= float(self._Line_edit_Frequency_RX.text())* 1000000
        print("Send to PLuto rx_lo =>",self.rx_lo)

        self.samp_rate= float(self._Line_edit_Fsampling_RX.text())* 1000000 # must be <=30.72 MHz if both channels are enabled
        print("Send to PLuto samp_rate => ",self.samp_rate)

        self.fc0= float(self._Line_edit_Filter_RX.text())* 1000000
        print("Send to PLuto fc0 => ",self.fc0)

        self.rx_gain0= float(self._Line_edit_rx0_gain.text())
        print("Send to PLuto rx0_gain => ",self.rx_gain0)

        self.rx_gain1= float(self._Line_edit_rx1_gain.text())
        print("Send to PLuto rx1_gain => ",self.rx_gain1)

        self.rx_mode = str(self.CAG.currentText())
        print("rx_mode => ",self.rx_mode)

        self.NumSamples =int(self._Line_edit_NumSamples.text())
        print("NumSamples => ",self.NumSamples)

        self.tx_lo= float(self._Line_edit_Frequency_TX.text())* 1000000
        print("Send to PLuto tx_lo =>",self.tx_lo)

        self.fshift= float(self._Line_edit_Frequency_SHIFT.text())* 1000
        print("Send to PLuto fshift =>",self.fshift)


        self.tx_gain= float(self._Line_edit_tx_gain.text())
        print("Send to PLuto tx_gain => ",self.tx_gain)

        self.SPAN= float(self._SPAN.text())
        neg= (self.SPAN * -1)/2
        pos= (self.SPAN * 1)/2

        print("Send to PLuto Span => ",self.SPAN)

        self.Title= self._Title_LineEdit.text()
        print("Curve Title =>",self.Title)

        self.phase_cal= int(self._Phase_cal.text())
        print("Phase cal => ",self.phase_cal)
        print(" ")

        self.RPM= float(self._RPM.text())
        print("Sampling FFT display => ",self.RPM)
        print(" ")

        self._log_window.append(str(self.dt_string) +" => " +"IP address is: "+ self.IP_pluto + " ..." )
        self._log_window.append(str(self.dt_string) +" => " +"Frequency RX: "+ str(self.rx_lo/1000000) + "MHz" )
        self._log_window.append(str(self.dt_string) +" => " +"Fsampling: "+ str(self.samp_rate/1000000) + "MHz" )
        self._log_window.append(str(self.dt_string) +" => " +"Filter BW: "+ str(self.fc0/1000000) + "MHz" )
        self._log_window.append(str(self.dt_string) +" => " +"rx0_gain: "+ str(self.rx_gain0) + "dB" )
        self._log_window.append(str(self.dt_string) +" => " +"rx1_gain: "+ str(self.rx_gain1) + "dB" )
        self._log_window.append(str(self.dt_string) +" => " +"rx_mode: "+ self.rx_mode )
        self._log_window.append(str(self.dt_string) +" => " +"NumSamples: "+ str(self.NumSamples) )
        self._log_window.append(str(self.dt_string) +" => " +"Frequency TX: "+ str(self.tx_lo/1000000) + "MHz" )
        self._log_window.append(str(self.dt_string) +" => " +"Frequency shift: "+ str(self.fshift/1000) + "KHz" )
        self._log_window.append(str(self.dt_string) +" => " +"tx0_gain: "+ str(self.tx_gain) + "dB" )
        self._log_window.append(str(self.dt_string) +" => " +"SPAN: "+ str(self.SPAN) + "MHz" )
        self._log_window.append(str(self.dt_string) +" => " +"Phase cal: "+ str(self.phase_cal)+ "°" )
        self._log_window.append(str(self.dt_string) +" => " +"Curve Title :"+ self.Title )
        self._log_window.append(str(self.dt_string) +" => " +"RPM Sample speed display: "+ str(self.RPM) )
        self._log_window.append(" ")


########################  Start the Apps

    def Start_app1(self):
        self._log_window.append(str(self.dt_string) +" => " +"Start App1" )
        self._log_window.append(" ")
        self.Track()
        print("Start App1")
        print(" ")


    def Start_app2(self):
        self._log_window.append(str(self.dt_string) +" => " +"Start App2" )
        self._log_window.append(" ")
        self.Spectrum()
        print("Start App2")
        print(" ")

    def Start_app3(self):
        self._log_window.append(str(self.dt_string) +" => " +"Start App3" )
        self._log_window.append(" ")
        self.QT_FFT()
        print("Start App3")
        print(" ")

    def Start_app4(self):
        self._log_window.append(str(self.dt_string) +" => " +"Start App4" )
        self._log_window.append(" ")
        self.QT_FFT_RX0()
        print("Start App4")
        print(" ")

    def Start_app5(self):
        self._log_window.append(str(self.dt_string) +" => " +"Start App5" )
        self._log_window.append(" ")
        self.QT_FFT_RX1()
        print("Start App5")
        print(" ")

    def Start_app6(self):
        self._log_window.append(str(self.dt_string) +" => " +"Start App6" )
        self._log_window.append(" ")
        print("Start App6")
        print(" ")


        ######################################## Connect_Radio
    def Connect_Radio(self):

        self.Date()
        self.Connect_send_settings
        self._log_window.append(str(self.dt_string) + " => " + "Open Pluto Connection")
        self._log_window.append(" ")

        print("Connection to SDRpluto")
        print(" ")
        '''Setup'''
        phase_cal = 16
        num_scans = 200

        ''' Set distance between Rx antennas '''
        d_wavelength = 0.5                  # distance between elements as a fraction of wavelength.  This is normally 0.5
        wavelength = 3E8/self.rx_lo              # wavelength of the RF carrier
        d = d_wavelength*wavelength         # distance between elements in meters
        print("Fréquence RX et TX: ", int(self.rx_lo/1000000), "GHz")
        print("Bande passante : ", int((self.fc0)/1000), "kHz")
        print("Echantillonnage : ", int(self.samp_rate/1000000), "MHz")
        print("Nombre d'échantillons : ", int(self.NumSamples))
        print("Gain RX0 : ", int(self.rx_gain0))
        print("Gain RX1 : ", int(self.rx_gain1))
        print("Gain TX0 : ", int(self.tx_gain))
        print(" ")
        '''Create Radios'''
        IP_ADDRESS_AD9361 = self.IP_pluto
        device_uri = "ip:" + IP_ADDRESS_AD9361
        sdr = adi.ad9361(device_uri)

        self._log_window.append(str(self.dt_string) +" => " +"IP address is: "+ self.IP_pluto )
        print("IP : ",self.IP_pluto)
        print(" ")

        #sdr = adi.ad9361(uri=str(self.IP_pluto))


        '''Configure properties for the Rx Pluto'''
        sdr.rx_enabled_channels = [0, 1]
        sdr.sample_rate = int(self.samp_rate)
        sdr.rx_rf_bandwidth = int(self.fc0)
        sdr.rx_lo = int(self.rx_lo)
        sdr.gain_control_mode = self.rx_mode
        sdr.rx_hardwaregain_chan0 = int(self.rx_gain0)
        sdr.rx_hardwaregain_chan1 = int(self.rx_gain1)
        sdr.rx_buffer_size = int(self.NumSamples)
        sdr._rxadc.set_kernel_buffers_count(1)   # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto
        sdr.tx_rf_bandwidth = int(self.fc0*3)
        sdr.tx_lo = int(self.tx_lo)
        sdr.tx_cyclic_buffer = True
        sdr.tx_hardwaregain_chan0 = int(self.tx_gain)
        sdr.tx_hardwaregain_chan1 = int(self.tx_gain)
        sdr.tx_buffer_size = int(2**18)

######################### App1
    def Track(self):
        print("Connection to SDRpluto")
        print(" ")
        '''Setup'''
        #samp_rate = 2e6    # must be <=30.72 MHz if both channels are enabled
        #NumSamples = 2**12
        #rx_lo = 5e8 #use 2.25e9
        #rx_mode = "manual"  # can be "manual" or "slow_attack"
        #rx_gain0 = 40
        #rx_gain1 = 40
        tx_lo = self.rx_lo
        tx_gain = -3
        #fc0 = int(200e3)
        phase_cal = 16
        num_scans = 200

        ''' Set distance between Rx antennas '''
        d_wavelength = 0.5                  # distance between elements as a fraction of wavelength.  This is normally 0.5
        wavelength = 3E8/self.rx_lo              # wavelength of the RF carrier
        d = d_wavelength*wavelength         # distance between elements in meters
        print("Fréquence RX et TX: ", int(self.rx_lo/1000000), "GHz")
        print("Bande passante : ", int((self.fc0*3)/1000), "kHz")
        print("Echantillonnage : ", int(self.samp_rate/1000000), "MHz")
        print("Nombre d'échantillons : ", int(self.NumSamples))
        print("Distance optimisée entre les deux antennes Rx : ", int(d*1000), "mm")
        print("Start : ", int(self.NumSamples*1000*(self.samp_rate/2+self.fc0/2)/self.samp_rate), "KHz")
        print("Start : ", int(self.NumSamples*1000*(self.samp_rate/2+self.fc0*2)/self.samp_rate), "KHz")
        print("Gain RX0 : ", int(self.rx_gain0))
        print("Gain RX1 : ", int(self.rx_gain1))
        print("Gain TX0 : ", int(tx_gain))
        print(" ")

        '''Create Radios'''
        sdr = adi.ad9361(uri='ip:192.168.5.1')

        '''Configure properties for the Rx Pluto'''
        sdr.rx_enabled_channels = [0, 1]
        sdr.sample_rate = int(self.samp_rate)
        sdr.rx_rf_bandwidth = int(self.fc0*3)
        sdr.rx_lo = int(self.rx_lo)
        sdr.gain_control_mode = self.rx_mode
        sdr.rx_hardwaregain_chan0 = int(self.rx_gain0)
        sdr.rx_hardwaregain_chan1 = int(self.rx_gain1)
        sdr.rx_buffer_size = int(self.NumSamples)
        sdr._rxadc.set_kernel_buffers_count(1)   # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto
        sdr.tx_rf_bandwidth = int(self.fc0*3)
        sdr.tx_lo = int(self.rx_lo)
        sdr.tx_cyclic_buffer = True
        sdr.tx_hardwaregain_chan0 = int(tx_gain)
        sdr.tx_hardwaregain_chan1 = int(-88)
        sdr.tx_buffer_size = int(2**18)

        '''Program Tx and Send Data'''
        fs = int(sdr.sample_rate)
        N = 2**16
        ts = 1 / float(fs)
        t = np.arange(0, N * ts, ts)
        i0 = np.cos(2 * np.pi * t * self.fc0) * 2 ** 14
        q0 = np.sin(2 * np.pi * t * self.fc0) * 2 ** 14
        iq0 = i0 + 1j * q0
        sdr.tx([iq0,iq0])  # Send Tx data.


        # Assign frequency bins and "zoom in" to the fc0 signal on those frequency bins
        xf = np.fft.fftfreq(self.NumSamples, ts)
        xf = np.fft.fftshift(xf)/1e6
        signal_start = int(self.NumSamples*(self.samp_rate/2+self.fc0/2)/self.samp_rate)
        signal_end = int(self.NumSamples*(self.samp_rate/2+self.fc0*2)/self.samp_rate)

        def calcTheta(phase):
            # calculates the steering angle for a given phase delta (phase is in deg)
            # steering angle is theta = arcsin(c*deltaphase/(2*pi*f*d)
            arcsin_arg = np.deg2rad(phase)*3E8/(2*np.pi*self.rx_lo*d)
            arcsin_arg = max(min(1, arcsin_arg), -1)     # arcsin argument must be between 1 and -1, or numpy will throw a warning
            calc_theta = np.rad2deg(np.arcsin(arcsin_arg))
            return calc_theta

        def dbfs(raw_data):
            # function to convert IQ samples to FFT plot, scaled in dBFS
            NumSamples = len(raw_data)
            win = np.hamming(NumSamples)
            y = raw_data * win
            s_fft = np.fft.fft(y) / np.sum(win)
            s_shift = np.fft.fftshift(s_fft)
            s_dbfs = 20*np.log10(np.abs(s_shift)/(2**11))     # Pluto is a signed 12 bit ADC, so use 2^11 to convert to dBFS
            return s_shift, s_dbfs

        def monopulse_angle(array1, array2):
            ''' Correlate the sum and delta signals  '''
            # Since our signals are closely aligned in time, we can just return the 'valid' case where the signals completley overlap
            # We can do correlation in the time domain (probably faster) or the freq domain
            # In the time domain, it would just be this:
            # sum_delta_correlation = np.correlate(delayed_sum, delayed_delta, 'valid')
            # But I like the freq domain, because then I can focus just on the fc0 signal of interest
            sum_delta_correlation = np.correlate(array1[signal_start:signal_end], array2[signal_start:signal_end], 'valid')
            angle_diff = np.angle(sum_delta_correlation)
            return angle_diff

        def scan_for_DOA():
            # go through all the possible phase shifts and find the peak, that will be the DOA (direction of arrival) aka steer_angle
            data = sdr.rx()
            Rx_0=data[0]
            Rx_1=data[1]
            peak_sum = []
            peak_delta = []
            monopulse_phase = []
            delay_phases = np.arange(-180, 180, 2)    # phase delay in degrees
            for phase_delay in delay_phases:
                delayed_Rx_1 = Rx_1 * np.exp(1j*np.deg2rad(phase_delay+phase_cal))
                delayed_sum = Rx_0 + delayed_Rx_1
                delayed_delta = Rx_0 - delayed_Rx_1
                delayed_sum_fft, delayed_sum_dbfs = dbfs(delayed_sum)
                delayed_delta_fft, delayed_delta_dbfs = dbfs(delayed_delta)
                mono_angle = monopulse_angle(delayed_sum_fft, delayed_delta_fft)

                peak_sum.append(np.max(delayed_sum_dbfs))
                peak_delta.append(np.max(delayed_delta_dbfs))
                monopulse_phase.append(np.sign(mono_angle))

            peak_dbfs = np.max(peak_sum)
            peak_delay_index = np.where(peak_sum==peak_dbfs)
            peak_delay = delay_phases[peak_delay_index[0][0]]
            steer_angle = int(calcTheta(peak_delay))

            return delay_phases, peak_dbfs, peak_delay, steer_angle, peak_sum, peak_delta, monopulse_phase

        '''Collect Data'''
        for i in range(20):
            # let Pluto run for a bit, to do all its calibrations
            data = sdr.rx()

        for i in range(2):
            # Create the window
            fig = plt.figure(figsize=(8, 10))
            # do in continue
            plt.ion()
            fig = plt.gcf()

            #fig.canvas.manager.set_window_title('Poursuite SDR')
            #fig.canvas.draw()

        #for i in range(num_scans):
        while(True):

            delay_phases, peak_dbfs, peak_delay, steer_angle, peak_sum, peak_delta, monopulse_phase = scan_for_DOA()

            plt.title("Poursuite auto SDR")

            plt.plot(delay_phases, peak_sum, color='g')
            plt.plot(delay_phases, peak_delta, color='b')
            plt.plot(delay_phases, monopulse_phase, color='y')

            plt.axvline(x=peak_delay, color='r', linestyle=':')

            plt.text(-180, -21, "Dephasage = {} deg".format(round(peak_delay,1)))
            plt.text(-180, -23, "Jaune polarité phase monopulse")
            plt.text(-180, -25, "Vert signal Somme")
            plt.text(-180, -27, "Bleu signal Delta")

            #plt.text(-180, -28, "angle".format(int(d*1000), steer_angle))


            plt.ylim(top=5, bottom=-50)
            plt.xlabel("Linge verticale dephasage en degrès")
            plt.ylabel("Rx0 + Rx1 [dBfs]")
            #plt.draw()
            #plt.show()

            fig.canvas.flush_events()

            time.sleep(0.10)

            #time.sleep(1)
            plt.clf()
            #plt.close()


        sdr.tx_destroy_buffer()

######################################## QT_FFT
    def QT_FFT(self):

        self.timer.stop()

        '''Create Radio'''
        IP_ADDRESS_AD9361 = self.IP_pluto
        device_uri = "ip:" + IP_ADDRESS_AD9361
        sdr = adi.ad9361(device_uri)

        '''Configure properties for the Radio'''
        sdr.rx_enabled_channels = [0, 1]
        sdr.sample_rate = int(self.samp_rate)
        sdr.rx_rf_bandwidth = int(self.fc0)
        sdr.rx_lo = int(self.rx_lo)
        sdr.gain_control_mode = self.rx_mode
        #print (self.rx_mode)
        sdr.rx_hardwaregain_chan0 = int(self.rx_gain0)
        #print (self.rx_gain0)
        sdr.rx_hardwaregain_chan1 = int(self.rx_gain1)
        #print (self.rx_gain1)
        sdr.rx_buffer_size = int(self.NumSamples)
        sdr._rxadc.set_kernel_buffers_count(1)      # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto
        sdr.tx_rf_bandwidth = int(self.fc0*3)
        sdr.tx_lo = int(self.tx_lo)
        sdr.tx_cyclic_buffer = True
        sdr.tx_hardwaregain_chan0 = int(self.tx_gain)
        sdr.tx_hardwaregain_chan1 = int(-88)
        sdr.tx_buffer_size = int(2**18)

        '''Program Tx and Send Data'''
        fs = int(sdr.sample_rate)
        N = 2**16
        ts = 1 / float(fs)
        t = np.arange(0, N * ts, ts)
        i0 = np.cos(2 * np.pi * t * self.fshift) * 2 ** 14
        q0 = np.sin(2 * np.pi * t * self.fshift) * 2 ** 14
        iq0 = i0 + 1j * q0
        sdr.tx([iq0,iq0])                           # Send Tx data.

        xf = np.fft.fftfreq(self.NumSamples, ts)         # Assign frequency bins
        xf = np.fft.fftshift(xf)/1e6

        def dbfs(raw_data):                         # function to convert IQ samples to FFT plot, scaled in dBFS
            NumSamples = len(raw_data)
            win = np.hamming(NumSamples)
            y = raw_data * win
            s_fft = np.fft.fft(y) / np.sum(win)
            s_shift = np.fft.fftshift(s_fft)
            s_dbfs = 20*np.log10(np.abs(s_shift)/(2**11))   # Pluto is a signed 12 bit ADC, so use 2^11 to convert to dBFS
            return s_dbfs

        '''Collect Data'''
        for i in range(20):                         # let Pluto run for a bit, to do all its calibrations, then get a buffer
            data = sdr.rx()

        ''' Set up FFT Window '''
        #self.win = pg.GraphicsLayoutWidget(show=True, size=(1200, 600))
        self.p1 = self.win.addPlot()
        ## Scale of span from the Editbox
        self.p1.setXRange(neg, pos)
        self.p1.setYRange(-100, 0)
        self.p1.setLabel('bottom', 'frequency', '[MHz]', **{'color': '#FFF', 'size': '14pt'})
        self.p1.setLabel('left', self.Title, **{'color': '#FFF', 'size': '14pt'})

        # Curves
        baseCurve = self.p1.plot()

        ''' Rx Data '''
        data = sdr.rx()
        Rx_0 = data[0]
        Rx_1 = data[1]


        self.delay_phases = np.arange(-180, 182, 1)  # phase delay in degrees // genère le tableur des phase de -180 à 181
        self.i = 0 # index for iterating through phases
        #self.phase_cal = 0 # start with 0 to calibrate
        print(self.phase_cal)

        def rotate():

            phase_delay = self.delay_phases[self.i]
            delayed_Rx_1 = Rx_1 * np.exp(1j*np.deg2rad(phase_delay+self.phase_cal))
            delayed_sum = dbfs(Rx_0 + delayed_Rx_1)

            ''' FFT Plot '''
            baseCurve.setData(xf, delayed_sum)


            # Increment through phases - Reset peaks
            self.i=self.i+1
            if (self.i>=len(self.delay_phases)):
                #print(self.delay_phases)

                self.i=0
                rotate()


            elif (self.i<=-1):
                self.i=len(self.delay_phases)-1
                rotate()

            # Control rate of rotation
            time.sleep(self.RPM/1000000)


        timer=QTimer(self)
        timer.timeout.connect(rotate)
        timer.start(0)

        sdr.tx_destroy_buffer()

        print("Spectrum prog: ok!")


######################################## QT_FFT
    def QT_FFT_RX0(self):

        self.timer.stop()

        '''Create Radio'''
        sdr = adi.ad9361(uri='ip:192.168.5.1')

        '''Configure properties for the Radio'''
        #sdr.rx_enabled_channels = [0, 1]
        sdr.sample_rate = int(self.samp_rate)
        sdr.rx_rf_bandwidth = int(self.fc0)
        sdr.rx_lo = int(self.rx_lo)
        sdr.gain_control_mode = self.rx_mode
        sdr.rx_hardwaregain_chan0 = int(self.rx_gain0)
        #sdr.rx_hardwaregain_chan1 = int(self.rx_gain1)
        sdr.rx_buffer_size = int(self.NumSamples)
        sdr._rxadc.set_kernel_buffers_count(1)      # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto
        #sdr.tx_rf_bandwidth = int(self.fc0*3)
        #sdr.tx_lo = int(200e6)
        #sdr.tx_cyclic_buffer = True
        #sdr.tx_hardwaregain_chan0 = int(-88)
        #sdr.tx_hardwaregain_chan1 = int(-88)
        #sdr.tx_buffer_size = int(2**18)

        '''Program Tx and Send Data'''
        fs = int(sdr.sample_rate)
        ts = 1 / float(fs)

        xf = np.fft.fftfreq(self.NumSamples, ts)         # Assign frequency bins
        xf = np.fft.fftshift(xf)/1e6

        '''Collect Data'''
        for i in range(20):                         # let Pluto run for a bit, to do all its calibrations, then get a buffer
            data = sdr.rx()

        def dbfs(raw_data):                         # function to convert IQ samples to FFT plot, scaled in dBFS
            NumSamples = len(raw_data)
            win = np.hamming(NumSamples)
            y = raw_data * win
            s_fft = np.fft.fft(y) / np.sum(win)
            s_shift = np.fft.fftshift(s_fft)
            s_dbfs = 20*np.log10(np.abs(s_shift)/(2**11))   # Pluto is a signed 12 bit ADC, so use 2^11 to convert to dBFS
            return s_dbfs

        ''' Set up FFT Window '''
        #self.win = pg.GraphicsLayoutWidget(show=True, size=(1200, 600))
        self.p1 = self.win.addPlot()
        ## Scale of span from the Editbox
        self.p1.setXRange(neg, pos)
        self.p1.setYRange(-100, 0)
        self.p1.setLabel('bottom', 'frequency', '[MHz]', **{'color': '#FFF', 'size': '14pt'})
        self.p1.setLabel('left', self.Title, **{'color': '#FFF', 'size': '14pt'})


        def trace_RX0():
                #clear the chart
                self.p1.clear()

                '''Collect Data'''
                for i in range(20):                         # let Pluto run for a bit, to do all its calibrations, then get a buffer
                    data = sdr.rx()

                # trace the curves
                baseCurve = self.p1.plot()

                ''' Rx Data '''
                data = sdr.rx()
                Rx_0 = data[0]

                # wait a moment for the display
                time.sleep(self.RPM/100)

                ''' trace FFT Plot '''
                baseCurve.setData(xf, dbfs(Rx_0))
                # destroy the buffer for a new trace
                sdr.tx_destroy_buffer()

        # update trace fonction for update teh spectrum
        self.timer = QTimer(self)
        self.timer.timeout.connect(trace_RX0)
        self.timer.start(100) # time in milliseconds.

        time.sleep(self.RPM/1000)
        #timer = pg.QtCore.QTimer()

        print("Spectrum prog: ok!")

######################################## QT_FFT
    def QT_FFT_RX1(self):

        self.timer.stop()

        '''Create Radio'''
        sdr = adi.ad9361(uri='ip:192.168.5.1')

        '''Configure properties for the Radio'''
        #sdr.rx_enabled_channels = [0,1]
        sdr.sample_rate = int(self.samp_rate)
        sdr.rx_rf_bandwidth = int(self.fc0)
        sdr.rx_lo = int(self.rx_lo)
        sdr.gain_control_mode = self.rx_mode
        sdr.rx_hardwaregain_chan1 = int(self.rx_gain1)
        #sdr.rx_hardwaregain_chan1 = int(self.rx_gain1)
        sdr.rx_buffer_size = int(self.NumSamples)
        sdr._rxadc.set_kernel_buffers_count(1)      # set buffers to 1 (instead of the default 4) to avoid stale data on Pluto
        #sdr.tx_rf_bandwidth = int(self.fc0*3)
        #sdr.tx_lo = int(200e6)
        #sdr.tx_cyclic_buffer = True
        #sdr.tx_hardwaregain_chan0 = int(-88)
        #sdr.tx_hardwaregain_chan1 = int(-88)
        #sdr.tx_buffer_size = int(2**18)

        '''Program Tx and Send Data'''
        fs = int(sdr.sample_rate)
        ts = 1 / float(fs)

        xf = np.fft.fftfreq(self.NumSamples, ts)         # Assign frequency bins
        xf = np.fft.fftshift(xf)/1e6

        '''Collect Data'''
        for i in range(20):                         # let Pluto run for a bit, to do all its calibrations, then get a buffer
            data = sdr.rx()

        def dbfs(raw_data):                         # function to convert IQ samples to FFT plot, scaled in dBFS
            NumSamples = len(raw_data)
            win = np.hamming(NumSamples)
            y = raw_data * win
            s_fft = np.fft.fft(y) / np.sum(win)
            s_shift = np.fft.fftshift(s_fft)
            s_dbfs = 20*np.log10(np.abs(s_shift)/(2**11))   # Pluto is a signed 12 bit ADC, so use 2^11 to convert to dBFS
            return s_dbfs

        ''' Set up FFT Window '''
        #self.win = pg.GraphicsLayoutWidget(show=True, size=(1200, 600))
        self.p1 = self.win.addPlot()
        ## Scale of span from the Editbox
        self.p1.setXRange(neg, pos)
        self.p1.setYRange(-100, 0)
        self.p1.setLabel('bottom', 'frequency', '[MHz]', **{'color': '#FFF', 'size': '14pt'})
        self.p1.setLabel('left', self.Title, **{'color': '#FFF', 'size': '14pt'})


        def trace_RX1():
                #clear the chart
                self.p1.clear()

                '''Collect Data'''
                for i in range(20):                         # let Pluto run for a bit, to do all its calibrations, then get a buffer
                    data = sdr.rx()

                # trace the curves
                baseCurve = self.p1.plot()

                ''' Rx Data '''
                data = sdr.rx()
                Rx_1 = data[1]

                # wait a moment for the display
                time.sleep(self.RPM/100)

                ''' trace FFT Plot '''
                baseCurve.setData(xf, dbfs(Rx_1))
                # destroy the buffer for a new trace
                sdr.tx_destroy_buffer()

        # update trace fonction for update teh spectrum
        self.timer = QTimer(self)
        self.timer.timeout.connect(trace_RX1)
        self.timer.start(100) # time in milliseconds.

        time.sleep(self.RPM/1000)
        #timer = pg.QtCore.QTimer()

        print("Spectrum prog: ok!")

######################################## Connect_send_settings
    def Connect_send_settings(self):
        self.Update_settings()
        print(" ")
        self.Connect_Radio()
        print(" ")


########## create the cancel button
    def Create_button_Cancel(self):
        self._button_Cancel = QDialogButtonBox(QDialogButtonBox.Cancel) # add the cancel button
        self._button_Cancel.accepted.connect(self.accept) # add the cancel button
        self._button_Cancel.rejected.connect(self.reject) # add the cancel button

        ########## Create the LOG window
    def create_log_window(self):    # Create teh log window
        self._log_window = QTextEdit()
        self._log_window.setReadOnly(True)
        self._log_window.setMaximumHeight(120)
        self._log_window.setStyleSheet("background-color: transparent;")
        ######## Update the date and time for LOG
        self.Date() # pickup the date
        ######## app start print the massage in LOG
        self._log_window.append(str(self.dt_string) + " => " + "App Start...Fist click on: Connect and send settings to Pluto ") # display log
        self._log_window.append(" ")

        ######## Send_Time
    def Send_Time(self):
        self.Date()
        self._log_window.append(str(self.dt_string))
        self._log_window.append(" ")

################################################################# Date Clock and Time
    def Date(self):
        from datetime import datetime

        # datetime object containing current date and time
        now = datetime.now()
        #print("now =", now)

        # dd/mm/YY H:M:S
        self.dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        #print("date and time =", self.dt_string)

    def Clock(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)
        self.show_time()

    def show_time(self):
        time = QTime.currentTime()
        self.text = time.toString("hh:mm:ss")
        #print(self.text)
        #self.Send_Time()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dialog = Dialog()
    sys.exit(dialog.exec())

