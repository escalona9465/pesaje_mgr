# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'loginWLZFar.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from components.imports.login import *
from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout
from components.functions import absPath
import sys
from PySide6 import QtCore

class UiLoginWindow(object):

    def setupUi(self, MainWindow, objmgr):
        self.objmgr = objmgr
        responsive = objmgr.getResponsive()
        #responsive.setCurrentPixelsX(1680)
        #responsive.setCurrentPixelsY(1050)
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        width,height = responsive.sizeScaled(1347,920)
        #print("scaled => width:",width," height:",height)
        MainWindow.resize(width, height) # 1347, 920

        icon = QIcon()
        icon.addFile("components/recursos/balanza.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(STYLES_LOGIN)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.frameLogin = QFrame(self.centralwidget)
        self.frameLogin.setObjectName(u"frameLogin")
        self.frameLogin.setEnabled(True)
        self.frameLogin.setGeometry(responsive.qRectScaled(750,160,461,361)) #QRect(750, 160, 461, 361)
        self.frameLogin.setFrameShape(QFrame.StyledPanel)
        self.frameLogin.setFrameShadow(QFrame.Raised)

        self.botonLogin = QPushButton(self.frameLogin)
        self.botonLogin.clicked.connect(self.login)
        self.botonLogin.setObjectName(u"botonLogin")
        self.botonLogin.setGeometry(responsive.qRectScaled(150,250,241,41)) #QRect(150, 250, 241, 41)
        self.botonLogin.setCursor(QCursor(Qt.PointingHandCursor))

        font = QFont()
        font.setBold(True)

        self.botonLogin.setFont(font)

        self.lineUser = QLineEdit(self.frameLogin)
        self.lineUser.setObjectName(u"lineUser")
        self.lineUser.setGeometry(responsive.qRectScaled(150,120,241,41)) #QRect(150, 120, 241, 41)

        font1 = QFont()

        self.lineUser.setFont(font1)
        self.lineUser.setAlignment(Qt.AlignCenter)
        self.linePass = QLineEdit(self.frameLogin)
        self.linePass.setObjectName(u"linePass")
        self.linePass.setGeometry(responsive.qRectScaled(150,180,241,41)) #QRect(150, 180, 241, 41)
        self.linePass.setFont(font1)
        self.linePass.setEchoMode(QLineEdit.Password)
        self.linePass.setAlignment(Qt.AlignCenter)

        self.iconMgr = QToolButton(self.frameLogin)
        self.iconMgr.setObjectName(u"iconMgr")
        self.iconMgr.setGeometry(responsive.qRectScaled(200,10,151,91)) #QRect(200, 10, 151, 91)

        icon1 = QIcon()
        icon1.addFile(u"components/recursos/MGR.png", QSize(), QIcon.Normal, QIcon.Off)

        self.iconMgr.setIcon(icon1)
        self.iconMgr.setIconSize(responsive.qSizeScaled(100,100)) # QSize(100,100)

        self.iconUser = QFrame(self.frameLogin)
        self.iconUser.setObjectName(u"iconUser")
        self.iconUser.setGeometry(responsive.qRectScaled(160,130,31,31)) #QRect(160, 130, 31, 31)
        self.iconUser.setFrameShape(QFrame.StyledPanel)
        self.iconUser.setFrameShadow(QFrame.Raised)

        self.iconUser_2 = QFrame(self.frameLogin)
        self.iconUser_2.setObjectName(u"iconUser_2")
        self.iconUser_2.setGeometry(responsive.qRectScaled(160,190,31,31)) #QRect(160, 190, 31, 31)
        self.iconUser_2.setFrameShape(QFrame.StyledPanel)
        self.iconUser_2.setFrameShadow(QFrame.Raised)

        self.recuperardatosLink = QCommandLinkButton(self.frameLogin)
        self.recuperardatosLink.clicked.connect(self.clickedRecuperar)
        self.recuperardatosLink.setObjectName(u"recuperardatosLink")
        self.recuperardatosLink.setGeometry(responsive.qRectScaled(224,310,211,41)) #QRect(224, 310, 211, 41)
        self.recuperardatosLink.setLayoutDirection(Qt.RightToLeft)
        self.recuperardatosLink.setCursor(QCursor(Qt.PointingHandCursor))

        self.lineUser.raise_()

        self.linePass.raise_()

        self.iconMgr.raise_()

        self.iconUser.raise_()

        self.iconUser_2.raise_()

        self.recuperardatosLink.raise_()

        self.botonLogin.raise_()

        self.iconBalanza = QToolButton(self.centralwidget)
        self.iconBalanza.setObjectName(u"iconBalanza")
        self.iconBalanza.setGeometry(responsive.qRectScaled(0,200,591,411)) #QRect(0, 200, 591, 411)

        icon2 = QIcon()
        icon2.addFile(u"components/recursos/Logo degradao.png", QSize(), QIcon.Normal, QIcon.Off)

        self.iconBalanza.setIcon(icon2)
        self.iconBalanza.setIconSize(responsive.qSizeScaled(400,400)) #QSize(400, 400)

        self.labelTitulo = QLabel(self.centralwidget)
        self.labelTitulo.setObjectName(u"labelTitulo")
        self.labelTitulo.setGeometry(responsive.qRectScaled(60,170,681,201)) #QRect(60, 170, 681, 201)

        font2 = QFont()
        font2.setPointSize(72)
        font2.setBold(True)

        self.labelTitulo.setFont(font2)

        self.labelTitulo2 = QLabel(self.centralwidget)
        self.labelTitulo2.setObjectName(u"labelTitulo2")
        self.labelTitulo2.setGeometry(responsive.qRectScaled(80,350,631,131)) #QRect(80, 350, 631, 131)
        self.labelTitulo2.setFont(font2)

        self.labelExtra2 = QLabel(self.centralwidget)
        self.labelExtra2.setObjectName(u"labelExtra2")
        self.labelExtra2.setGeometry(responsive.qRectScaled(460,670,381,41)) #QRect(460, 670, 381, 41)

        font3 = QFont()
        font3.setPointSize(12)
        font3.setBold(False)

        self.labelExtra2.setFont(font3)
        self.labelExtra2.setAlignment(Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)

        self.iconBalanza.raise_()

        self.frameLogin.raise_()

        self.labelTitulo2.raise_()

        self.labelTitulo.raise_()

        self.labelExtra2.raise_()

        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(responsive.qRectScaled(0,0,1347,22)) #QRect(0, 0, 1347, 22)

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def keyPressEvent(self,event):
        print(f"Tipo de evento: {event.type()}")
        print(f"Tecla presionada: {event.key()}")
        print(f"Texto de la tecla: {event.text()}")
        if event.key() == QtCore.Qt.Key_Return:
        #if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            print("Enter presionado2")

    def clickedRecuperar(self): 
        self.objmgr.restorePassword()
        pass

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Sistema de Pesaje MGR", None))

        self.botonLogin.setText(QCoreApplication.translate("MainWindow", u"Ingresar", None))

        self.lineUser.setPlaceholderText(QCoreApplication.translate("MainWindow", u"USUARIO", None))
        
        self.linePass.setPlaceholderText(QCoreApplication.translate("MainWindow", u"CONTRASE\u00d1A", None))
        
        self.iconMgr.setText(QCoreApplication.translate("MainWindow", u"...", None))
        
        self.recuperardatosLink.setText(QCoreApplication.translate("MainWindow", u"Recuperar datos", None))
        
        self.iconBalanza.setText(QCoreApplication.translate("MainWindow", u"...", None))

        self.labelTitulo.setText(QCoreApplication.translate("MainWindow", u"SISTEMA DE PESAJE", None))

        self.labelTitulo2.setText(QCoreApplication.translate("MainWindow", u"MONTANA GRAFICA", None))

        self.labelExtra2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Digitalizaci\u00f3n Industrial, Corimon C.A. 2020</p></body></html>", None))
    # retranslateUi

    def login(self):
        user = self.lineUser.text()
        password = self.linePass.text()
        credentials = (user,password)
        access_granted = self.objmgr.login(credentials)
        if access_granted :
            self.objmgr.set_productUI()
            self.objmgr.changeView(1)
            self.objmgr.loadMenu()
            self.objmgr.pesajeWidget.campos_segun_usuario()
        else:
            mensajes = Dialogo()
            mensajes.exec_()
            self.clearUser()
            print("the username or password doesn't match")

    def clearUser(self):
        self.lineUser.setText("")
        self.linePass.setText("")
        pass

    def checkName():
        pass

    def checkEmail():
        pass

class LoginUi(QMainWindow, UiLoginWindow):
    # Heredamos de QMainWindow y de la interfaz

    def __init__(self, objmgr):

        # Llamamos al constructor de la superclase
        super().__init__()

        # Ejecutamos el método setupUi heredado del diseño,
        # gracias al cual se generará la interfaz gráfica
        self.setupUi(self,objmgr)

class Dialogo(QDialog):
    def __init__(self):
        super().__init__()
        self.resize(240, 120)
        icon = QIcon("logo.ico")
        self.setWindowIcon(icon)
        self.setWindowTitle("Error en los datos introducidos")

        # creamos un layout y lo establecemos en el widget
        layout = QVBoxLayout()
        self.setLayout(layout)

        # podemos añadir una etiqueta
        info = QLabel("Usuario o contraseña\n         inválidos.")
        info.setStyleSheet("""
                            
                                color:#04336B;
                                font-weight:500;
                                font-size:30px;
                                """
                           )
        
        layout.addWidget(info)