# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5 import QtCore, QtGui, QtWidgets
import requests

elenco_docker= ["1","2","3"]
docker_selected = ""
SERVER_IP = 'http://192.168.1.70:8000/'


data = {
    "action": "TurnOn",
    "DockerID": "1",
}

RSP_1_active = [""]
RSP_2_active = [""]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 30, 671, 41))
        self.label.setFont(QFont('Arial', 25))
        self.label.setObjectName("label")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(60, 90, 671, 351))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 669, 349))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.radioButton = []
        i=0
        for item in elenco_docker :
            self.radioButton.append(QtWidgets.QRadioButton(self.scrollAreaWidgetContents))
            self.radioButton[i].setGeometry(QtCore.QRect(30, 40 + i*30, 112, 23))
            self.radioButton[i].setObjectName("radioButton")
            self.radioButton[i].clicked.connect(self.check)

            i=i+1

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.turnonButton = QtWidgets.QPushButton(self.centralwidget)
        self.turnonButton.setGeometry(QtCore.QRect(160, 490, 201, 51))
        self.turnonButton.setObjectName("turnonButton")
        self.turnonButton.clicked.connect(self.turnon)
        self.turnofButton = QtWidgets.QPushButton(self.centralwidget)
        self.turnofButton.setGeometry(QtCore.QRect(440, 490, 201, 51))
        self.turnofButton.setObjectName("turnofButton")
        self.turnofButton.clicked.connect(self.turnoff)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow","LIST OF DOCKERS"))
        i=0
        for item in elenco_docker :
            self.radioButton[i].setText(_translate("MainWindow","docker"+ item))
            i=i+1
        self.turnonButton.setText(_translate("MainWindow", "Turn ON"))
        self.turnofButton.setText(_translate("MainWindow", "Turn OFF"))

  
    # method called by radio button
    def check(self):

        global docker_selected

        for radio_button in self.radioButton : 
            # checking if it is checked
            if radio_button.isChecked():
                
                # changing docker_selected
                docker_selected = radio_button.text()
    
    # method called by Turn On button
    def turnon(self):

        global docker_selected

        print("Richiesta TURN ON docker : " + docker_selected)
        data["action"] = "TurnOn"
        data["DockerID"] = docker_selected.replace("docker","")

        r = requests.post(SERVER_IP,json=data)



    # method called by Turn Off button
    def turnoff(self):

        global docker_selected

        print("Richiesta TURN OFF docker : " + docker_selected)
        data["action"] = "TurnOff"
        data["DockerID"] = docker_selected.replace("docker","")

        r = requests.post(SERVER_IP,json=data)

    
    
        
