# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './GUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1120, 849)
        MainWindow.setIconSize(QtCore.QSize(5, 30))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Notebook = QtWidgets.QTabWidget(self.centralwidget)
        self.Notebook.setObjectName("Notebook")
        self.Acquisition = QtWidgets.QWidget()
        self.Acquisition.setObjectName("Acquisition")
        self.gridLayout = QtWidgets.QGridLayout(self.Acquisition)
        self.gridLayout.setObjectName("gridLayout")
        self.recording = QtWidgets.QGridLayout()
        self.recording.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.recording.setObjectName("recording")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_5.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.recording.addLayout(self.horizontalLayout_5, 0, 3, 1, 1)
        self.frame_5 = QtWidgets.QFrame(self.Acquisition)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.recording.addWidget(self.frame_5, 0, 0, 1, 1)
        self.frame_6 = QtWidgets.QFrame(self.Acquisition)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.recording.addWidget(self.frame_6, 0, 4, 1, 1)
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setContentsMargins(20, 20, 20, 20)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.Acquisition)
        self.label_6.setMinimumSize(QtCore.QSize(30, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_7.addWidget(self.label_6)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem2)
        self.inputTimer_minute = QtWidgets.QSpinBox(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputTimer_minute.sizePolicy().hasHeightForWidth())
        self.inputTimer_minute.setSizePolicy(sizePolicy)
        self.inputTimer_minute.setMinimumSize(QtCore.QSize(150, 30))
        self.inputTimer_minute.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.inputTimer_minute.setFont(font)
        self.inputTimer_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.inputTimer_minute.setObjectName("inputTimer_minute")
        self.horizontalLayout_7.addWidget(self.inputTimer_minute)
        self.gridLayout_4.addLayout(self.horizontalLayout_7, 2, 0, 1, 1)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label = QtWidgets.QLabel(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(10, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_6.addWidget(self.label)
        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.inputTimer_heure = QtWidgets.QSpinBox(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputTimer_heure.sizePolicy().hasHeightForWidth())
        self.inputTimer_heure.setSizePolicy(sizePolicy)
        self.inputTimer_heure.setMinimumSize(QtCore.QSize(0, 30))
        self.inputTimer_heure.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.inputTimer_heure.setFont(font)
        self.inputTimer_heure.setAlignment(QtCore.Qt.AlignCenter)
        self.inputTimer_heure.setProperty("value", 3)
        self.inputTimer_heure.setObjectName("inputTimer_heure")
        self.horizontalLayout_6.addWidget(self.inputTimer_heure)
        self.gridLayout_4.addLayout(self.horizontalLayout_6, 1, 0, 1, 1)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_7 = QtWidgets.QLabel(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_8.addWidget(self.label_7)
        spacerItem4 = QtWidgets.QSpacerItem(30, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.inputTimer_seconde = QtWidgets.QSpinBox(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inputTimer_seconde.sizePolicy().hasHeightForWidth())
        self.inputTimer_seconde.setSizePolicy(sizePolicy)
        self.inputTimer_seconde.setMinimumSize(QtCore.QSize(150, 30))
        self.inputTimer_seconde.setMaximumSize(QtCore.QSize(150, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.inputTimer_seconde.setFont(font)
        self.inputTimer_seconde.setAlignment(QtCore.Qt.AlignCenter)
        self.inputTimer_seconde.setObjectName("inputTimer_seconde")
        self.horizontalLayout_8.addWidget(self.inputTimer_seconde)
        self.gridLayout_4.addLayout(self.horizontalLayout_8, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.Acquisition)
        self.label_3.setMinimumSize(QtCore.QSize(0, 30))
        self.label_3.setStyleSheet("color: blue;")
        self.label_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_3.setObjectName("label_3")
        self.gridLayout_4.addWidget(self.label_3, 0, 0, 1, 1)
        self.ScheduleButton = QtWidgets.QPushButton(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ScheduleButton.sizePolicy().hasHeightForWidth())
        self.ScheduleButton.setSizePolicy(sizePolicy)
        self.ScheduleButton.setMinimumSize(QtCore.QSize(25, 50))
        self.ScheduleButton.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ScheduleButton.setFont(font)
        self.ScheduleButton.setObjectName("ScheduleButton")
        self.gridLayout_4.addWidget(self.ScheduleButton, 4, 0, 1, 1)
        self.UnzipButton = QtWidgets.QPushButton(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UnzipButton.sizePolicy().hasHeightForWidth())
        self.UnzipButton.setSizePolicy(sizePolicy)
        self.UnzipButton.setMinimumSize(QtCore.QSize(25, 50))
        self.UnzipButton.setMaximumSize(QtCore.QSize(500, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.UnzipButton.setFont(font)
        self.UnzipButton.setObjectName("UnzipButton")
        self.gridLayout_4.addWidget(self.UnzipButton, 7, 0, 1, 1)
        self.ImmediateRecordingButton = QtWidgets.QPushButton(self.Acquisition)
        self.ImmediateRecordingButton.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ImmediateRecordingButton.setFont(font)
        self.ImmediateRecordingButton.setObjectName("ImmediateRecordingButton")
        self.gridLayout_4.addWidget(self.ImmediateRecordingButton, 5, 0, 1, 1)
        self.recording.addLayout(self.gridLayout_4, 1, 3, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_9 = QtWidgets.QLabel(self.Acquisition)
        self.label_9.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_9.setText("")
        self.label_9.setObjectName("label_9")
        self.horizontalLayout.addWidget(self.label_9)
        self.outputTimer_heure = QtWidgets.QLabel(self.Acquisition)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.outputTimer_heure.setFont(font)
        self.outputTimer_heure.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outputTimer_heure.setAlignment(QtCore.Qt.AlignCenter)
        self.outputTimer_heure.setObjectName("outputTimer_heure")
        self.horizontalLayout.addWidget(self.outputTimer_heure)
        self.label_4 = QtWidgets.QLabel(self.Acquisition)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAccessibleName("")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        self.outputTimer_minute = QtWidgets.QLabel(self.Acquisition)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.outputTimer_minute.setFont(font)
        self.outputTimer_minute.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outputTimer_minute.setAlignment(QtCore.Qt.AlignCenter)
        self.outputTimer_minute.setObjectName("outputTimer_minute")
        self.horizontalLayout.addWidget(self.outputTimer_minute)
        self.label_5 = QtWidgets.QLabel(self.Acquisition)
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setIndent(0)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout.addWidget(self.label_5)
        self.outputTimer_seconde = QtWidgets.QLabel(self.Acquisition)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.outputTimer_seconde.setFont(font)
        self.outputTimer_seconde.setFocusPolicy(QtCore.Qt.NoFocus)
        self.outputTimer_seconde.setAlignment(QtCore.Qt.AlignCenter)
        self.outputTimer_seconde.setObjectName("outputTimer_seconde")
        self.horizontalLayout.addWidget(self.outputTimer_seconde)
        self.label_8 = QtWidgets.QLabel(self.Acquisition)
        self.label_8.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.recording.addLayout(self.horizontalLayout, 0, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ConnectButton = QtWidgets.QPushButton(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ConnectButton.sizePolicy().hasHeightForWidth())
        self.ConnectButton.setSizePolicy(sizePolicy)
        self.ConnectButton.setMinimumSize(QtCore.QSize(0, 0))
        self.ConnectButton.setMaximumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.ConnectButton.setFont(font)
        self.ConnectButton.setObjectName("ConnectButton")
        self.horizontalLayout_2.addWidget(self.ConnectButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.AcquireButton = QtWidgets.QPushButton(self.Acquisition)
        self.AcquireButton.setMinimumSize(QtCore.QSize(0, 0))
        self.AcquireButton.setMaximumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.AcquireButton.setFont(font)
        self.AcquireButton.setObjectName("AcquireButton")
        self.horizontalLayout_3.addWidget(self.AcquireButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.recording.addLayout(self.verticalLayout, 1, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(40, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.recording.addItem(spacerItem5, 0, 1, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.horizontalLayout_4.addItem(spacerItem6)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem7)
        self.recording.addLayout(self.horizontalLayout_4, 2, 3, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.Log1 = QtWidgets.QPlainTextEdit(self.Acquisition)
        self.Log1.setMinimumSize(QtCore.QSize(500, 0))
        self.Log1.setObjectName("Log1")
        self.gridLayout_2.addWidget(self.Log1, 0, 0, 1, 1)
        self.recording.addLayout(self.gridLayout_2, 2, 2, 1, 1)
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(10, -1, 10, -1)
        self.gridLayout_5.setSpacing(20)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem8)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_3.addItem(spacerItem9)
        self.gridLayout_5.addLayout(self.verticalLayout_3, 0, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.Acquisition)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_5.addWidget(self.label_2, 0, 1, 1, 1)
        self.ip_input = QtWidgets.QLineEdit(self.Acquisition)
        self.ip_input.setMinimumSize(QtCore.QSize(0, 40))
        self.ip_input.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.ip_input.setFont(font)
        self.ip_input.setAlignment(QtCore.Qt.AlignCenter)
        self.ip_input.setObjectName("ip_input")
        self.gridLayout_5.addWidget(self.ip_input, 0, 2, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem10, 0, 0, 1, 1)
        self.recording.addLayout(self.gridLayout_5, 1, 2, 1, 1)
        self.gridLayout_6 = QtWidgets.QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.STOPbutton = QtWidgets.QPushButton(self.Acquisition)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.STOPbutton.sizePolicy().hasHeightForWidth())
        self.STOPbutton.setSizePolicy(sizePolicy)
        self.STOPbutton.setMinimumSize(QtCore.QSize(200, 100))
        self.STOPbutton.setMaximumSize(QtCore.QSize(200, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.STOPbutton.setFont(font)
        self.STOPbutton.setObjectName("STOPbutton")
        self.gridLayout_6.addWidget(self.STOPbutton, 0, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_6.addItem(spacerItem11, 1, 0, 1, 1)
        self.recording.addLayout(self.gridLayout_6, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.recording, 0, 0, 3, 2)
        self.Notebook.addTab(self.Acquisition, "")
        self.Spectrum = QtWidgets.QWidget()
        self.Spectrum.setObjectName("Spectrum")
        self.Notebook.addTab(self.Spectrum, "")
        self.Monitoring = QtWidgets.QWidget()
        self.Monitoring.setObjectName("Monitoring")
        self.Notebook.addTab(self.Monitoring, "")
        self.gridLayout_3.addWidget(self.Notebook, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.Notebook.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_6.setText(_translate("MainWindow", "Minute:"))
        self.label.setText(_translate("MainWindow", "Heure:"))
        self.label_7.setText(_translate("MainWindow", "Seconde:"))
        self.label_3.setText(_translate("MainWindow", "Recordings"))
        self.ScheduleButton.setText(_translate("MainWindow", "Schedule"))
        self.UnzipButton.setText(_translate("MainWindow", "Unzip"))
        self.ImmediateRecordingButton.setText(_translate("MainWindow", "Immediate"))
        self.outputTimer_heure.setText(_translate("MainWindow", "HH"))
        self.label_4.setText(_translate("MainWindow", ":"))
        self.outputTimer_minute.setText(_translate("MainWindow", "MM"))
        self.label_5.setText(_translate("MainWindow", ":"))
        self.outputTimer_seconde.setText(_translate("MainWindow", "SS"))
        self.ConnectButton.setText(_translate("MainWindow", "Connect"))
        self.AcquireButton.setText(_translate("MainWindow", "Acquire"))
        self.label_2.setText(_translate("MainWindow", "IP:"))
        self.ip_input.setText(_translate("MainWindow", "192.168.2.1"))
        self.STOPbutton.setText(_translate("MainWindow", "STOP"))
        self.Notebook.setTabText(self.Notebook.indexOf(self.Acquisition), _translate("MainWindow", "Acquisition"))
        self.Notebook.setTabText(self.Notebook.indexOf(self.Spectrum), _translate("MainWindow", "Spectrum"))
        self.Notebook.setTabText(self.Notebook.indexOf(self.Monitoring), _translate("MainWindow", "SDR monitoring"))
