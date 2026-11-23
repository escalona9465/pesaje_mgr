############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from PySide6.QtWidgets import (QWidget, QVBoxLayout,QHBoxLayout,QPushButton)
from PySide6.QtGui import (QCursor)
from PySide6 import QtCore
from PySide6.QtCore import QRect,QSize,Qt,QPoint
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineSettings
#from components.imports.bobinas import *


from PySide6.QtWidgets import QLabel
import tkinter as tk
import math

class Responsive():
    def __init__(self):
        self.scale = 1.0
        # Those init pixels are fixed.
        self.initWidth = 361 
        self.initHeight = 203
        self.initWidthPixels = 1366
        self.initHeightPixels = 768

        self.tkObject = tk.Tk()

        self.currentWidth = self.tkObject.winfo_screenmmwidth()
        self.currentHeight = self.tkObject.winfo_screenmmheight()
        self.currentWidthPixels = self.tkObject.winfo_screenwidth()
        self.currentHeightPixels = self.tkObject.winfo_screenheight()

    def scaleFont(self,fontPixels):
        num = math.sqrt(math.pow(self.currentHeightPixels,2) + math.pow(self.currentWidthPixels,2))
        den = math.sqrt(math.pow(self.initHeightPixels,2) + math.pow(self.initWidthPixels,2))
        return int( fontPixels*(num/den) )

    def scaleFontStr(self,fontPixels):
        return (str(self.scaleFont(fontPixels)) + "px")

    def scalePixelsWidth(self,widthInPx):
        return int( (self.currentWidthPixels/self.initWidthPixels)*widthInPx )

    def scalePixelsStrX(self,widthInPx):
        return (str(self.scalePixelsWidth(widthInPx)) + "px")

    def scalePixelsHeight(self,heightInPx):
        return int( (self.currentHeightPixels/self.initHeightPixels)*heightInPx )

    def scalePixelsStrY(self,widthInPy):
        return (str(self.scalePixelsHeight(widthInPy)) + "px")

    def scaleMMWidth(self,widthInMM ):
        return int( (self.currentWidth/self.initWidth)*widthInMM )

    def scaleMMWHeight(self,heightInMM):
        return int( (self.currentWidth/self.initWidth)*heightInMM)

    def sizeScaled(self,width,height):
        return self.scalePixelsWidth(width),self.scalePixelsHeight(height)

    def qSizeScaled(self,width,height):
        return QSize(self.scalePixelsWidth(width),self.scalePixelsHeight(height))

    def qRectScaled(self,x,y,width,height):
        return QRect(self.scalePixelsWidth(x),self.scalePixelsHeight(y),self.scalePixelsWidth(width),self.scalePixelsHeight(height))

    def setCurrentPixelsX(self,pixels):
        self.currentWidthPixels = pixels #self.tkObject.winfo_screenwidth()

    def setCurrentPixelsY(self,pixels):
        self.currentHeightPixels = pixels #self.tkObject.winfo_screenheight()

    def getPosToCenter(self,width,height):
        w = self.currentWidthPixels
        h = self.currentHeightPixels
        #print("w:",w,"h:",h)
        pos_x = int(w/2) - int(width/2)
        pos_y = int(h/2) - int(height/2)
        #print("positions=> x: ",pos_x," y:",pos_y)
        return pos_x,pos_y

class Action():

    def __init__(self,id,obj) -> None:
        self.id = id
        self.obj = obj
        self.mode = ""

    def setId(self,id):
        self.id = id

    def setMode(self,mode):
        self.mode = mode

class Alert():
    
    def __init__(self,frame,alertText) -> None:
        self.alertText = alertText
        self.lineNotify = QLabel(frame)
        self.lineNotify.setStyleSheet("""
            QLabel#lineNotify{
                background-color:#ff0000;
                border-radius:5px;
                font-weight:700;
                color:white;
                text-align:center;
            }        
        """)
        self.lineNotify.setGeometry(QRect(20, 205, 840, 25))
        self.lineNotify.setAlignment(Qt.AlignCenter)
        self.lineNotify.setObjectName(u"lineNotify")
        self.lineNotify.hide()
        self.timer = QtCore.QTimer()

    def showNotification(self,text):
        self.alertText = text
        self.lineNotify.setText(self.alertText)
        self.lineNotify.show()
        self.blink()

    def blink(self):
        self.timer.singleShot(500,self.lineNotify.hide)
        self.timer.singleShot(1000,self.lineNotify.show)
        self.timer.singleShot(1500,self.lineNotify.hide)
        self.timer.singleShot(2000,self.lineNotify.show)
        self.timer.singleShot(2500,self.lineNotify.hide)
        self.timer.singleShot(3000,self.lineNotify.show)
        self.timer.singleShot(3500,self.lineNotify.hide)
        self.timer.singleShot(4000,self.lineNotify.show)
        self.timer.singleShot(4500,self.lineNotify.hide)
        self.timer.singleShot(5000,self.lineNotify.show)
        self.timer.singleShot(5500,self.lineNotify.hide)

    def setText(self,text):
        self.alertText = text

    def setLocation(self,location):
        self.lineNotify.setGeometry(location)

    def setMode(self,mode):
        if mode == "SUCCESS":
            self.lineNotify.setStyleSheet("""
                QLabel#lineNotify{
                    background-color:#4c4cff;
                    border-radius:5px;
                    font-weight:700;
                    color:white;
                    text-align:center;
                }        
                """)
        elif mode == "FAILURE":
            self.lineNotify.setStyleSheet("""
                QLabel#lineNotify{
                    background-color:#ff0000;
                    border-radius:5px;
                    font-weight:700;
                    color:white;
                    text-align:center;
                }        
            """)

class WebView(QWidget):
    def __init__(self):
        #super(webView, self).__init__()
        super().__init__()
        self.layout = QVBoxLayout(self)

        self.webV = QWebEngineView()
        self.width_ = 0
        self.height_ = 0
        self.fileName = ""

    def loadView(self):
        self.webV.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        #self.fileDir = QtCore.QFileInfo("test.html").absoluteFilePath()
        self.fileDir = QtCore.QFileInfo(self.fileName).absoluteFilePath()
        print(self.fileDir) #file:///C:/Users/elrodriguez/Desktop/pesaje_mgr_PC_16_06_2022_L1/tempPdf.pdf
        #url = "https://doc.qt.io/qtforpython-6/PySide6/QtWebEngineWidgets/QWebEngineView.html"
        #url_path = QtCore.QUrl.fromLocalFile(self.fileDir)
        #url_path = QtCore.QUrl.fromLocalFile("file:///C:/Users/elrodriguez/Desktop/pesaje_mgr_PC_16_06_2022_L1/tempHtml.html")
        url_path = QtCore.QUrl.fromUserInput("file:///" + self.fileDir)
        print(url_path)
        self.webV.load( url_path )#QtCore.QUrl("file:///" + self.fileDir))
        #self.webV.load(QtCore.QUrl(url))
        self.layout.addWidget(self.webV)

    def setFileName(self,filename):
        self.fileName = filename
        print("setting file name",self.fileName)
        pass

    def setSize(self,width,height):
        self.width_ = width
        self.height_ = height
        self.resize(QSize(width,height))
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)

    def getWebView(self):
        return self.webV

class Preview(QWidget):
    def __init__(self,obj):
        super().__init__()
        
        self.popupObject = obj
        self.width_ = 0
        self.height_ = 0

        self._zoomInBtn = QPushButton("+")
        self._zoomInBtn.clicked.connect(self.zoomIn)
        self._zoomInBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self._zoomOutBtn = QPushButton("-")
        self._zoomOutBtn.clicked.connect(self.zoomOut)
        self._zoomOutBtn.setCursor(QCursor(Qt.PointingHandCursor))

        if self.popupObject.type == "PALLET":
            self._printBtn = QPushButton("Imprimir")
            self._printBtn.clicked.connect(self.popupObject.printPalletGenerated)
            self._printBtn.setCursor(QCursor(Qt.PointingHandCursor))

            self._returnBtn = QPushButton("Volver")
            self._returnBtn.clicked.connect(self.popupObject.returnToFormPallet)
            self._returnBtn.setCursor(QCursor(Qt.PointingHandCursor))
        if self.popupObject.type == "PLEGADIZO":
            self._printBtn = QPushButton("Imprimir")
            self._printBtn.clicked.connect(self.popupObject.printPlegadizoGenerated)
            self._printBtn.setCursor(QCursor(Qt.PointingHandCursor))

            self._returnBtn = QPushButton("Volver")
            self._returnBtn.clicked.connect(self.popupObject.returnToFormPlegadizo)
            self._returnBtn.setCursor(QCursor(Qt.PointingHandCursor))

        elif self.popupObject.type == "TURN":
            self._printBtn = QPushButton("Imprimir")
            self._printBtn.clicked.connect(self.popupObject.printTurnGenerated)
            self._printBtn.setCursor(QCursor(Qt.PointingHandCursor))

            self._returnBtn = QPushButton("Volver")
            self._returnBtn.clicked.connect(self.popupObject.returnToFormTurn)
            self._returnBtn.setCursor(QCursor(Qt.PointingHandCursor)) 

        elif self.popupObject.type == "HABLADOR":
            self._printBtn = QPushButton("Imprimir")
            self._printBtn.clicked.connect(self.popupObject.printHablGenerated)
            self._printBtn.setCursor(QCursor(Qt.PointingHandCursor))

            self._returnBtn = QPushButton("Volver")
            self._returnBtn.clicked.connect(self.popupObject.returnToFormHabl)
            self._returnBtn.setCursor(QCursor(Qt.PointingHandCursor)) 

        elif self.popupObject.type == "":
            pass

        self._cancelBtn = QPushButton("Cancelar")
        self._cancelBtn.clicked.connect(self.popupObject.close)
        self._cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))

        self.docPreview = WebView()
        #self.docPreview.setSize(300,200)
        
        self.bottomLayout = QHBoxLayout()

        self.bottomLayout.addWidget(self._printBtn)
        self.bottomLayout.addWidget(self._zoomInBtn)
        self.bottomLayout.addWidget(self._zoomOutBtn)
        self.bottomLayout.addWidget(self._returnBtn)
        self.bottomLayout.addWidget(self._cancelBtn)
        
        self.mainLayout = QVBoxLayout()

        self.mainLayout.addWidget(self.docPreview)
        self.mainLayout.addLayout(self.bottomLayout)

        self.zoom = 1.0 # This will be float.
        self.moveToCenter()
        self.setLayout(self.mainLayout)

    def zoomIn(self):
        webPrev = self.getPreview().getWebView()
        self.zoom = self.zoom*1.05
        webPrev.setZoomFactor(self.zoom)

    def zoomOut(self):
        webPrev = self.getPreview().getWebView()
        self.zoom = self.zoom*0.95
        webPrev.setZoomFactor(self.zoom)

    def setZoomOut(self,factor):
        webPrev = self.getPreview().getWebView()
        self.zoom = self.zoom*factor
        webPrev.setZoomFactor(self.zoom)

    def zoomOutDoc(self):
        #open text file in read mode
        #dir = QtCore.QFileInfo("tempHtml.html").absoluteFilePath()

        #file = open(dir, "r")
        #data = file.read()
        #zoom = self.
        #data.replace("","")
        #file.close()

        #print(data)
        pass

    def moveToCenter(self):
        r = Responsive()
        left,right = r.getPosToCenter(self.width_,self.height_)
        point = QPoint(left,right)
        #point.setX(left)
        #point.setY(right)
        self.move(point)

    def setFileName(self,fileName):
        self.docPreview.setFileName(fileName)

    def setSize(self,width,height):
        self.width_ = width
        self.height_ = height
        self.resize(QSize(width,height))
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)
    
    def getPreview(self):
        return self.docPreview
    

 