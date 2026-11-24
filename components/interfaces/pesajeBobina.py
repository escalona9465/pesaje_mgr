# -*- coding: utf-8 -*-

from components.imports.bobinas import *
from components.functions import getCurrentTime
from components.functions import (getProductFromName, getTotalsForPallet,getLastTicket,getTodayTickets,
getOpFromTable,getNamesFromClients,getNamesFromProducts,getCodeFromClient,
getClientfromId,getCodesFromProducts,getProductFromCode,getTicketsForPallet,getTheSameCoils,
getArrHablador,getLastTicketOp,getTheSameCoilsPallet,getTotalsForOp,lookForTicketOnPallet,countBobinas,
countBobinasPallet,getProductRowByOp,orderByAlphabeth)

from PySide6.QtGui import QIntValidator, QRegularExpressionValidator
from PySide6.QtCore import QRegularExpression
from components.interfaces.dialogos import *
from portCommngmt import disablePort,enablePort

import time
import sys
from datetime import date


"""**********************************************************************************************************
*************************************************************************************************************
*************************** Agregado el 31/10/2023 para el filtrado *****************************************
*************************** dinamico del comboBox Cod. Productos ********************************************
*************************************************************************************************************
*************************************************************************************************************"""

class ExtendedComboBox(QComboBox):
        def __init__(self, parent=None):
            super(ExtendedComboBox, self).__init__(parent)
    
            self.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setEditable(True)
    
            # add a filter model to filter matching items
            self.pFilterModel = QSortFilterProxyModel(self)
            self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
            self.pFilterModel.setSourceModel(self.model())
    
            # add a completer, which uses the filter model
            self.completer = QCompleter(self.pFilterModel, self)
            # always show all (filtered) completions
            self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            self.setCompleter(self.completer)
    
            # connect signals
            self.lineEdit().textEdited[str].connect(self.pFilterModel.setFilterFixedString)
            self.completer.activated.connect(self.on_completer_activated)
    
    
        # on selection of an item from the completer, select the corresponding item from combobox
        def on_completer_activated(self, text):
            if text:
                index = self.findText(text)
                self.setCurrentIndex(index)
                self.activated.emit(self.itemText(index))
    
    
        # on model change, update the models of the filter and completer as well
        def setModel(self, model):
            super(ExtendedComboBox, self).setModel(model)
            self.pFilterModel.setSourceModel(model)
            self.completer.setModel(self.pFilterModel)
    
    
        # on model column change, update the model column of the filter and completer as well
        def setModelColumn(self, column):
            self.completer.setCompletionColumn(column)
            self.pFilterModel.setFilterKeyColumn(column)
            super(ExtendedComboBox, self).setModelColumn(column)

"""**********************************************************************************************************
*************************************************************************************************************"""

class UiPesoWindow(object):
    def setupUi(self, pesoWindow, objmgr):
        self.objmgr = objmgr
        responsive = objmgr.getResponsive()
        if not pesoWindow.objectName():
            pesoWindow.setObjectName(u"pesoWindow")
        pesoWindow.resize(1366, 780)
        icon = QIcon()
        icon.addFile(u"components/recursos/balanza.png", QSize(), QIcon.Normal, QIcon.Off)
        pesoWindow.setWindowIcon(icon)
        pesoWindow.setStyleSheet(BOBINAS_STYLES)
        # Checks area
        self._checkTara = False
        self._checkOp = False
        self._checkMaxWB = False
        self._checkAmt = False
        self._checkBxP = False
        self._checkPallet = False
        self._checkWeight = False
        self._checkGeneral = False

        self.indexOp = 0
        self.lastOp = ""

        self.items = []

        self.currentOps = []
        self.tableOp = []

        self.currentClients = []
        self.tableClients = []

        self.currentProducts = []
        self.tableProducts = []

        self.currentCodes = []
        self.tableCodes = []

        self.isCapturing = True

        self.centralwidget = QWidget(pesoWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.frameDatos = QFrame(self.centralwidget)
        self.frameDatos.setObjectName(u"frameDatos")
        self.frameDatos.setGeometry(responsive.qRectScaled(40, 20, 400, 680)) # QRect(40, 20, 400, 680)
        self.frameDatos.setFrameShape(QFrame.StyledPanel)
        self.frameDatos.setFrameShadow(QFrame.Raised)

        self.labelTitulo = QLabel(self.frameDatos)
        self.labelTitulo.setObjectName(u"labelTitulo")
        self.labelTitulo.setGeometry(responsive.qRectScaled(160, 10, 110, 31)) # QRect(160, 10, 81, 31)

        font = QFont()
        font.setBold(True)
        font.setItalic(False)

        self.labelTitulo.setFont(font)

        self.regex = QRegularExpression(r'\d+')
        self.validador = QRegularExpressionValidator(self.regex)
        
        self.lineOp = ExtendedComboBox(self.frameDatos)
        self.lineOp.setObjectName(u"lineOp")
        self.lineOp.setGeometry(responsive.qRectScaled(170, 50, 111, 30)) # QRect(170, 50, 111, 30)
        self.lineOp.setEditable(True)
        self.lineOp.currentIndexChanged.connect(self.fillOpFromDB)
        self.lineOp.currentTextChanged.connect(self.checkOp)
        #self.lineOp.focusInEvent = 

        self.comboCodigo = ExtendedComboBox(self.frameDatos)
        self.comboCodigo.setObjectName(u"comboCodigo")
        self.comboCodigo.setGeometry(responsive.qRectScaled(170, 90, 171, 30)) # QRect(170, 90, 171, 30)
        self.comboCodigo.setEditable(True)
        self.comboCodigo.currentIndexChanged.connect(self.updateFieldsByCode)

        self.comboBoxProd = QComboBox(self.frameDatos)
        self.comboBoxProd.setObjectName(u"comboBoxProd")
        self.comboBoxProd.setGeometry(responsive.qRectScaled(170, 130, 171, 30)) # QRect(170, 130, 171, 30)
        self.comboBoxProd.currentIndexChanged.connect(self.updateFieldsByProduct)

        self.comboBoxClient = QComboBox(self.frameDatos)
        self.comboBoxClient.setObjectName(u"comboBoxClient")
        self.comboBoxClient.setGeometry(responsive.qRectScaled(170, 170, 171, 30)) # QRect(170, 170, 171, 30)
        self.comboBoxClient.setDisabled(True)
        #self.comboBoxClient.setEditable(False) #
        self.comboBoxClient.setEnabled(False)
        
        self.label = QLabel(self.frameDatos)
        self.label.setObjectName(u"label")
        self.label.setGeometry(responsive.qRectScaled(140, 55, 31, 16)) # QRect(140, 55, 31, 16)

        self.label_2 = QLabel(self.frameDatos)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(responsive.qRectScaled(60, 95, 101, 20)) # QRect(60, 95, 101, 20)
        self.label_2.setFont(font)

        self.label_3 = QLabel(self.frameDatos)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(responsive.qRectScaled(100, 135, 71, 20)) # QRect(100, 135, 71, 20)

        self.label_4 = QLabel(self.frameDatos)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(responsive.qRectScaled(110, 175, 51, 21)) # QRect(110, 175, 51, 21)

        self.lineTara = QLineEdit(self.frameDatos)
        self.lineTara.setObjectName(u"lineTara")
        self.lineTara.setGeometry(responsive.qRectScaled(170, 210, 81, 30)) # QRect(170, 210, 81, 30)
        self.lineTara.setEnabled(True)
        self.lineTara.setAlignment(Qt.AlignCenter)
        self.lineTara.textChanged.connect(self.tareFromLine)

        self.linePesoMax = QLineEdit(self.frameDatos)
        self.linePesoMax.setObjectName(u"linePesoMax")
        self.linePesoMax.setGeometry(responsive.qRectScaled(170, 250, 101, 30)) # QRect(170, 250, 101, 30)
        self.linePesoMax.setAlignment(Qt.AlignCenter)
        self.linePesoMax.setValidator(self.validador)
        self.linePesoMax.textChanged.connect(self.checkWMax)

        self.linePesoMin = QLineEdit(self.frameDatos)
        self.linePesoMin.setObjectName(u"linePesoMax")
        self.linePesoMin.setGeometry(responsive.qRectScaled(170, 290, 101, 30)) # QRect(170, 250, 101, 30)
        self.linePesoMin.setAlignment(Qt.AlignCenter)
        self.linePesoMin.setValidator(self.validador)
        #self.linePesoMin.textChanged.connect(self.checkWMax)

        self.lineCantidad = QLineEdit(self.frameDatos)
        self.lineCantidad.setObjectName(u"lineCantidad")
        self.lineCantidad.setGeometry(responsive.qRectScaled(170, 330, 101, 30)) # QRect(170, 290, 101, 30)
        self.lineCantidad.setAlignment(Qt.AlignCenter)
        self.lineCantidad.setValidator(self.validador)
        self.lineCantidad.textChanged.connect(self.checkAmt)

        self.lineBxP = QLineEdit(self.frameDatos)
        self.lineBxP.setObjectName(u"lineBxP")
        self.lineBxP.setGeometry(responsive.qRectScaled(170, 370, 101, 30)) # QRect(170, 330, 101, 30)
        self.lineBxP.setAlignment(Qt.AlignCenter)
        self.lineBxP.setValidator(self.validador)
        self.lineBxP.textChanged.connect(self.checkBxP)

        self.linePaletaAct = QLineEdit(self.frameDatos)
        self.linePaletaAct.setObjectName(u"linePaletaAct")
        self.linePaletaAct.setGeometry(responsive.qRectScaled(170, 410, 101, 30)) # QRect(170, 370, 101, 30)
        self.linePaletaAct.setAlignment(Qt.AlignCenter)
        self.linePaletaAct.setEnabled(False)
        self.linePaletaAct.textChanged.connect(self.checkPallet)

        self.checkbm = QCheckBox(self.frameDatos)
        self.checkbm.setObjectName(u"checkbm")
        self.checkbm.setGeometry(responsive.qRectScaled(170, 450, 111, 30)) # QRect(170, 400, 111, 30)
        self.checkbm.setCursor(QCursor(Qt.PointingHandCursor))
        self.checkbm.stateChanged.connect(self.checkbmChanged)
        
        self.checkh = QCheckBox(self.frameDatos)
        self.checkh.setObjectName(u"checkh")
        self.checkh.setGeometry(responsive.qRectScaled(170, 478, 81, 30)) # QRect(170, 430, 81, 30)
        self.checkh.setCursor(QCursor(Qt.PointingHandCursor))
        self.checkh.stateChanged.connect(self.checkhChanged)

        self.checktd = QCheckBox(self.frameDatos)
        self.checktd.setObjectName(u"qchecktd")
        self.checktd.setGeometry(responsive.qRectScaled(170, 505, 120, 30)) 

        self.botonIniciar = QPushButton(self.frameDatos)
        self.botonIniciar.setObjectName(u"botonIniciar")
        self.botonIniciar.setGeometry(responsive.qRectScaled(150, 540, 111, 41)) # QRect(150, 460, 111, 41)
        self.botonIniciar.setCursor(QCursor(Qt.PointingHandCursor))
        self.botonIniciar.clicked.connect(self.initWeight)
        self.centralwidget.installEventFilter(self)

        self.botonCaptura = QPushButton(self.frameDatos)
        self.botonCaptura.setObjectName(u"botonCaptura")
        self.botonCaptura.setGeometry(responsive.qRectScaled(150, 565, 111, 41)) # QRect(150, 515, 111, 41)
        self.botonCaptura.setCursor(QCursor(Qt.PointingHandCursor))
        self.botonCaptura.clicked.connect(self.cptWeight)
        self.botonCaptura.setVisible(False)

        self.botonSalir = QPushButton(self.frameDatos)
        self.botonSalir.setObjectName(u"botonSalir")
        self.botonSalir.setGeometry(responsive.qRectScaled(150, 600, 111, 41))
        self.botonSalir.clicked.connect(self.returnToProducts) # If want to logged out return to login
        self.botonSalir.setCursor(QCursor(Qt.PointingHandCursor))


        self.label_5 = QLabel(self.frameDatos)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(responsive.qRectScaled(130, 215, 31, 16)) # QRect(130, 215, 31, 16)

        self.label_6 = QLabel(self.frameDatos)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(responsive.qRectScaled(40, 255, 131, 20)) # QRect(40, 255, 131, 20)

        self.label_6_1 = QLabel(self.frameDatos)
        self.label_6_1.setObjectName(u"label_6_1")
        self.label_6_1.setGeometry(responsive.qRectScaled(42, 295, 121, 20)) # QRect(40, 255, 131, 20)

        self.label_7 = QLabel(self.frameDatos)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(responsive.qRectScaled(45, 335, 121, 20)) # QRect(42, 295, 121, 20)

        self.label_8 = QLabel(self.frameDatos)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(responsive.qRectScaled(45, 375, 101, 20)) # QRect(45, 335, 121, 20)

        self.label_9 = QLabel(self.frameDatos)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(responsive.qRectScaled(70, 415, 101, 20)) # QRect(70, 375, 101, 20)

        self.label_10 = QLabel(self.frameDatos)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(responsive.qRectScaled(260, 215, 21, 21)) # QRect(260, 215, 21, 21)

        self.label_11 = QLabel(self.frameDatos)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(responsive.qRectScaled(280, 255, 47, 16))

        self.label_11_1 = QLabel(self.frameDatos)
        self.label_11_1.setObjectName(u"label_11")
        self.label_11_1.setGeometry(responsive.qRectScaled(280, 295, 47, 16))

        self.label_12 = QLabel(self.frameDatos)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(responsive.qRectScaled(280, 335, 47, 13))

        self.label_13 = QLabel(self.frameDatos)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(responsive.qRectScaled(280, 375, 47, 13))

        self.botonTara = QPushButton(self.frameDatos)
        self.botonTara.setObjectName(u"botonTara")
        self.botonTara.setGeometry(responsive.qRectScaled(290, 210, 75, 30))
        self.botonTara.setCursor(QCursor(Qt.PointingHandCursor))
        self.botonTara.clicked.connect(self.tare)

        self.botonCerrar = QPushButton(self.frameDatos)
        self.botonCerrar.setObjectName(u"botonCerrar")
        self.botonCerrar.setGeometry(responsive.qRectScaled(285, 410, 81, 30))
        self.botonCerrar.setCursor(QCursor(Qt.PointingHandCursor))
        self.botonCerrar.clicked.connect(self.closePallet)

        #self.botonOP = QPushButton(self.frameDatos)
        #self.botonOP.setObjectName(u"botonOP")
        #self.botonOP.setGeometry(responsive.qRectScaled(290, 50, 75, 30))
        #self.botonOP.setCursor(QCursor(Qt.PointingHandCursor))
        #self.botonOP.clicked.connect(self.changeOp)

        self.framePeso = QFrame(self.centralwidget)
        self.framePeso.setObjectName(u"framePeso")
        self.framePeso.setGeometry(responsive.qRectScaled(450, 20, 880, 680)) #width = 921

        self.alert = Alert(self.framePeso,"")
        
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framePeso.sizePolicy().hasHeightForWidth())

        self.framePeso.setSizePolicy(sizePolicy)
        self.framePeso.setCursor(QCursor(Qt.ArrowCursor))
        self.framePeso.setLayoutDirection(Qt.LeftToRight)
        self.framePeso.setFrameShape(QFrame.NoFrame)
        self.framePeso.setFrameShadow(QFrame.Plain)

        self.lcdNumber = QLCDNumber(self.framePeso)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(responsive.qRectScaled(60, 20, 361, 91))
        self.lcdNumber.setMaximumSize(QSize(16777215, 91))
        self.lcdNumber.setFrameShape(QFrame.StyledPanel)
        self.lcdNumber.setFrameShadow(QFrame.Raised)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(6)
        self.lcdNumber.setMode(QLCDNumber.Dec)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setProperty("value", 0.00)
        self.lcdNumber.setStyleSheet("""
            QLCDNumber#lcdNumber{
                background:white;
            }        
        """)

        self.lcdInput = QLineEdit(self.framePeso)
        self.lcdInput.setObjectName(u"lcdInput")
        self.lcdInput.setGeometry(responsive.qRectScaled(60, 20, 361, 91))
        self.lcdInput.setMaximumSize(QSize(16777215, 91))
        self.lcdInput.setProperty("value", 0.00)
        self.lcdInput.setStyleSheet("""
            QLineEdit#lcdInput{
                font-size:40px;
                color:#04336b;
            }
        """)
        self.lcdInput.hide()
        self.lcdInput.textChanged.connect(self.updateManual)

        self.tablaPesaje = QTableWidget(self.framePeso)
        if (self.tablaPesaje.columnCount() < 5):
            self.tablaPesaje.setColumnCount(5)
            self.rowCount = 1
            self.tablaPesaje.setRowCount(self.rowCount)
            self.tablaPesaje.clearContents() 

        #brush = QBrush(QColor(0, 0, 0, 255))
        #brush.setStyle(Qt.SolidPattern)

        font1 = QFont()
        font1.setStyleStrategy(QFont.PreferDefault)

        __qtablewidgetitem = QTableWidgetItem()
        #__qtablewidgetitem.setFont(font1);
        #__qtablewidgetitem.setForeground(brush);

        self.tablaPesaje.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tablaPesaje.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tablaPesaje.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tablaPesaje.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()

        self.tablaPesaje.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tablaPesaje.setObjectName(u"tablaPesaje")
        self.tablaPesaje.setGeometry(responsive.qRectScaled(20, 240, 840, 410))

        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tablaPesaje.sizePolicy().hasHeightForWidth())

        self.tablaPesaje.setSizePolicy(sizePolicy1)
        self.tablaPesaje.setMaximumSize(QSize(881, 16777215))
        self.tablaPesaje.setAutoFillBackground(False)
        self.tablaPesaje.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tablaPesaje.setColumnCount(5)
        self.tablaPesaje.horizontalHeader().setCascadingSectionResizes(False)
        self.tablaPesaje.horizontalHeader().setDefaultSectionSize(210)
        self.tablaPesaje.verticalHeader().setDefaultSectionSize(40)

        headerTabla = self.tablaPesaje.horizontalHeader()       
        self.tablaPesaje.setColumnWidth(0,100)
        self.tablaPesaje.setColumnWidth(1,110)
        self.tablaPesaje.setColumnWidth(2,160)
        headerTabla.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tablaPesaje.setColumnWidth(4,100)

        self.label_14 = QLabel(self.framePeso)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(responsive.qRectScaled(65, 170, 47, 13))

        self.label_15 = QLabel(self.framePeso)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(responsive.qRectScaled(225, 170, 47, 13))

        self.label_bm = QLabel(self.framePeso)
        self.label_bm.setObjectName(u"label_15")
        self.label_bm.setGeometry(responsive.qRectScaled(385, 167, 111, 13))
        self.label_bm.setText("Bobina Matriz")

        self.labelTara = QLabel(self.framePeso)
        self.labelTara.setObjectName(u"labelTara")
        self.labelTara.setGeometry(responsive.qRectScaled(105, 160, 91, 31))
        self.labelTara.setFrameShape(QFrame.StyledPanel)

        self.labelNeto = QLabel(self.framePeso)
        self.labelNeto.setObjectName(u"labelNeto")
        self.labelNeto.setGeometry(responsive.qRectScaled(265, 160, 91, 31))
        self.labelNeto.setFrameShape(QFrame.StyledPanel)

        self.labelBobMatriz = QLineEdit(self.framePeso)
        self.labelBobMatriz.setGeometry(responsive.qRectScaled(495, 160, 91, 31))
        self.labelBobMatriz.setObjectName("editBM")
        self.labelBobMatriz.setStyleSheet("""
        QLineEdit#editBM{
            border:solid;
            border-color:#99AA99;
            border-radius:0px;
            border-width:1px;
        }
        """)
        changeToDisable(self.labelBobMatriz)
        self.labelBobMatriz.setText("")
        self.labelBobMatriz.setDisabled(True)
        self.labelBobMatriz.textChanged.connect(self.updateBobMatriz)
        #self.labelBobMatriz.setFrameShape(QFrame.StyledPanel)

        self.labelTicket = QLabel(self.framePeso)
        self.labelTicket.setObjectName(u"labelTicket")
        self.labelTicket.setGeometry(responsive.qRectScaled(730, 20, 121, 31))
        self.labelTicket.setFrameShape(QFrame.StyledPanel)

        self.comboBoxBal = QComboBox(self.framePeso)
        self.comboBoxBal.addItem("")
        self.comboBoxBal.addItem("")
        self.comboBoxBal.addItem("")
        self.comboBoxBal.setObjectName(u"comboBoxBal")
        self.comboBoxBal.setGeometry(responsive.qRectScaled(250, 120, 101, 22))
        self.comboBoxBal.currentTextChanged.connect(self.changeBal)

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.botonReconectar = QPushButton(self.framePeso)
        self.botonReconectar.setText("Reconectar")
        self.botonReconectar.clicked.connect(lambda: objmgr.reconectar_balanza(self.comboBoxBal.currentText()))
        self.botonReconectar.setGeometry(responsive.qRectScaled(451,120,80,22))
        self.botonReconectar.setObjectName("reconectar")

        self.lineKg = QLineEdit(self.framePeso)
        self.lineKg.setObjectName(u"lineKg")
        self.lineKg.setGeometry(responsive.qRectScaled(430, 20, 81, 91))

        font2 = QFont()
        font2.setBold(False)
        font2.setItalic(False)

        self.lineKg.setFont(font2)
        self.lineKg.setReadOnly(True)

        self.lineTicket = QLineEdit(self.framePeso)
        self.lineTicket.setObjectName(u"lineTicket")
        self.lineTicket.setGeometry(responsive.qRectScaled(575, 20, 150, 31))
        self.lineTicket.setReadOnly(True)
        
        self.label_16 = QLabel(self.framePeso)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(responsive.qRectScaled(80, 120, 161, 20))

        self.labelNBobina = QLabel(self.framePeso)
        self.labelNBobina.setObjectName(u"labelNBobina")
        self.labelNBobina.setGeometry(responsive.qRectScaled(760, 71, 100, 17))

        self.labelNPaleta = QLabel(self.framePeso)
        self.labelNPaleta.setObjectName(u"labelNPaleta")
        self.labelNPaleta.setGeometry(responsive.qRectScaled(760, 94, 100, 17))

        self.label_20 = QLabel(self.framePeso)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(responsive.qRectScaled(580, 71, 100, 17))

        self.label_22 = QLabel(self.framePeso)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(responsive.qRectScaled(580, 94, 100, 17))

        self.label_24 = QLabel(self.framePeso)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(responsive.qRectScaled(580, 117, 180, 17))

        self.labelAcumPaleta = QLabel(self.framePeso)
        self.labelAcumPaleta.setObjectName(u"labelAcumPaleta")
        self.labelAcumPaleta.setGeometry(responsive.qRectScaled(760, 117, 100, 17))

        self.label_26 = QLabel(self.framePeso)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(responsive.qRectScaled(580, 140, 250, 17))

        self.labelAcumOp = QLabel(self.framePeso)
        self.labelAcumOp.setObjectName(u"labelAcumOp")
        self.labelAcumOp.setGeometry(responsive.qRectScaled(760, 140, 100, 17))

        pesoWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(pesoWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(responsive.qRectScaled(0, 0, 1366, 22))

        pesoWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(pesoWindow)
        self.statusbar.setObjectName(u"statusbar")

        pesoWindow.setStatusBar(self.statusbar)
        QMetaObject.connectSlotsByName(pesoWindow)
        QMetaObject.connectSlotsByName(objmgr)
        self.retranslateUi(pesoWindow)

        self.timer = QtCore.QTimer()

        self.updateProductsFromDB()
        self.updateClientsFromDB()

        self.updateOpList()

        self.checkOp()
        if self.objmgr.currentUser["nivel"] == "SUPERVISOR" or self.objmgr.currentUser["nivel"] == "ADMINISTRADOR":
            self.campos_editables()
        else:
            self.campos_no_editables()

    def campos_segun_usuario(self):
        if self.objmgr.currentUser["nivel"] == "SUPERVISOR" or self.objmgr.currentUser["nivel"] == "ADMINISTRADOR":
            self.campos_editables()
        else:
            self.campos_no_editables()

    def campos_no_editables(self):
        self.comboCodigo.setEnabled(False)
        self.comboBoxProd.setEnabled(False)
        self.comboBoxClient.setEnabled(False)
        #self.lineTara.setEnabled(False)
        self.linePesoMax.setEnabled(False)
        self.linePesoMin.setEnabled(False)
        #self.botonTara.setEnabled(False)

    def campos_editables(self):
        self.comboCodigo.setEnabled(True)
        self.comboBoxProd.setEnabled(True)
        self.comboBoxClient.setEnabled(True)
        self.lineTara.setEnabled(True)
        self.linePesoMax.setEnabled(True)
        self.linePesoMin.setEnabled(True)
        self.botonTara.setEnabled(True)


    def updateManual(self):
        strInput = self.lcdInput.text()
        if isFloat(strInput):
            self.objmgr.updateWeight(float(strInput))
            changeToNormal(self.lcdInput)
        else:
            changeToError(self.lcdInput)


    def updateBobMatriz(self):
        try:
            self.objmgr.bobinaMatriz = self.labelBobMatriz.text()
            changeToNormal(self.labelBobMatriz)
            #print("Bobina matriz actualizada =>",self.objmgr.bobinaMatriz)
        except:
            changeToError(self.labelBobMatriz)
        pass

    def updateClientsFromDB(self):
        result,tableClients = self.getTableClients()
        if result:
            self.tableClients = tableClients
            #print("Reading op from db:",self.tableClients)
            self.currentClients = getNamesFromClients(tableClients)
            self.comboBoxClient.clear()
            self.addItemsToClients(self.currentClients)
            #print(self.currentClients)

    def updateProductsFromDB(self):
        self.comboBoxProd.blockSignals(True)
        self.comboCodigo.blockSignals(True)
        result,tableProducts = self.getTableProducts()
        if result:
            self.tableProducts = tableProducts
            #print("Reading op from db:",self.tableProducts)
            self.currentProducts = getNamesFromProducts(self.tableProducts)
            self.currentCodes = getCodesFromProducts(self.tableProducts)
            self.comboCodigo.clear()
            self.comboBoxProd.clear()
            #self.currentCodes = orderByAlphabeth(self.currentCodes,"FM0-")
            self.addItemsToCodes(self.currentCodes)
            self.addItemsToProducts(self.currentProducts)
            self.comboBoxProd.blockSignals(False)
            self.comboCodigo.blockSignals(False)

    def updateFieldsByCode(self):
        op = self.lineOp.currentText()
        opNotExist = len(self.objmgr.getAnOp(op)) <= 0
        # if op doesn't exist you can't fill fiels from manual data.
        # only fill when not are saving data.
        if opNotExist:
            code = self.comboCodigo.currentText()
            success,products = self.objmgr.getProductsOnDB()
            productRow = getProductFromCode(products,code)
            toWriteProduct = productRow[1] # it represents the name of product
            clientId = productRow[3]
            client = self.objmgr.getAnClient(clientId)
            toWriteClient = client[2]
            # update fields here
            self.comboBoxProd.setCurrentText(toWriteProduct)
            self.comboBoxClient.setCurrentText(toWriteClient)
            #print("changin to => ",toWriteProduct,toWriteClient,code)

    def updateFieldsByProduct(self):
        op = self.lineOp.currentText()
        opNotExist = len(self.objmgr.getAnOp(op)) <= 0
        # if op doesn't exist you can't fill fiels from manual data.
        # only fill when not are saving data.
        if opNotExist:
            nameProduct = self.comboBoxProd.currentText()
            success,products = self.objmgr.getProductsOnDB()
            #print("update fields products=>",products)
            productRow = getProductFromName(products,nameProduct)
            #print("Product row=>",productRow)
            toWriteCode = productRow[0] # it represents the name of product
            clientId = productRow[3]
            client = self.objmgr.getAnClient(clientId)
            toWriteClient = client[2]
            # update fields here
            self.comboCodigo.setCurrentText(toWriteCode)
            self.comboBoxClient.setCurrentText(toWriteClient)
            #print("changin to => ",toWriteCode,toWriteClient,nameProduct)

    def updateOpList(self):
        result,self.tableOp = self.getTableBobinas()
        result,self.tableOp_1 = self.getTableBobinas_OP()
        #print(result)
        if result:
            #print("Reading op from db:",self.tableOp_1)
            #print(f"Longitud {len(self.tableOp_1)}")
            #self.currentOps = getOpFromTable(self.tableOp)
            self.currentOps = self.tableOp_1
            #print(self.currentOps)
            #print("1")
            self.addItemsToOp(self.currentOps)
            #print("2")
            self.updateScreenValues()
            #print(self.currentOps)
            #print("OK update OP list")

    def retranslateUi(self, pesoWindow):
        pesoWindow.setWindowTitle(QCoreApplication.translate("pesoWindow", u"MainWindow", None))
        self.labelTitulo.setText(QCoreApplication.translate("pesoWindow", u"Bobinas", None))
        
        self.label.setText(QCoreApplication.translate("pesoWindow", u"O.P.", None))
        self.label_2.setText(QCoreApplication.translate("pesoWindow", u"Cod. Producto", None))
        self.label_3.setText(QCoreApplication.translate("pesoWindow", u"Producto", None))
        self.label_4.setText(QCoreApplication.translate("pesoWindow", u"Cliente", None))

        self.checkbm.setText(QCoreApplication.translate("pesoWindow", u"Bobina Matriz", None))
        self.checkh.setText(QCoreApplication.translate("pesoWindow", u"Hablador", None))
        self.checktd.setText(QCoreApplication.translate("pesoWindow", u"Ticket doble", None))

        self.botonIniciar.setText(QCoreApplication.translate("pesoWindow", u"Iniciar Peso", None))
        self.botonCaptura.setText(QCoreApplication.translate("pesoWindow", u"Capturar Peso", None))

        self.label_5.setText(QCoreApplication.translate("pesoWindow", u"Tara", None))
        self.label_6.setText(QCoreApplication.translate("pesoWindow", u"Peso max. bobina", None))
        self.label_6_1.setText(QCoreApplication.translate("pesoWindow", u"Peso min. bobina", None))
        self.label_7.setText(QCoreApplication.translate("pesoWindow", u"Cantidad Paletas", None))
        self.label_8.setText(QCoreApplication.translate("pesoWindow", u"Bobinas x Paleta", None))
        self.label_9.setText(QCoreApplication.translate("pesoWindow", u"Paleta Actual", None))
        self.label_10.setText(QCoreApplication.translate("pesoWindow", u"Kg", None))
        self.label_11.setText(QCoreApplication.translate("pesoWindow", u"Kg", None))
        self.label_11_1.setText(QCoreApplication.translate("pesoWindow", u"Kg", None))
        self.label_12.setText(QCoreApplication.translate("pesoWindow", u"Unid.", None))
        self.label_13.setText(QCoreApplication.translate("pesoWindow", u"Unid.", None))

        self.botonTara.setText(QCoreApplication.translate("pesoWindow", u"tare", None))
        self.botonCerrar.setText(QCoreApplication.translate("pesoWindow", u"Cerrar Paleta", None))
        #self.botonOP.setText(QCoreApplication.translate("pesoWindow", u"Cambiar", None))
        self.botonSalir.setText(QCoreApplication.translate("pesoWindow", u"Salir", None))

        ___qtablewidgetitem = self.tablaPesaje.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("pesoWindow", u"N Ticket", None));
        ___qtablewidgetitem1 = self.tablaPesaje.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("pesoWindow", u"O.P", None));
        ___qtablewidgetitem2 = self.tablaPesaje.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("pesoWindow", u"Cod. Productos", None));
        ___qtablewidgetitem3 = self.tablaPesaje.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("pesoWindow", u"Descripci\u00f3n Producto", None));
        ___qtablewidgetitem4 = self.tablaPesaje.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("pesoWindow", u"Peso Bruto", None));

        self.label_14.setText(QCoreApplication.translate("pesoWindow", u"Tara", None))
        self.label_15.setText(QCoreApplication.translate("pesoWindow", u"Neto", None))
        self.labelTara.setText("")
        self.labelNeto.setText("")
        self.labelTicket.setText("")
        self.comboBoxBal.setItemText(0, QCoreApplication.translate("pesoWindow", u"BALANZA 1", None))
        self.comboBoxBal.setItemText(1, QCoreApplication.translate("pesoWindow", u"BALANZA 2", None))
        self.comboBoxBal.setItemText(2, QCoreApplication.translate("pesoWindow", u"MANUAL", None))

        self.lineKg.setText(QCoreApplication.translate("pesoWindow", u"Kg", None))
        self.lineTicket.setText(QCoreApplication.translate("pesoWindow", u"N\u00ba Ticket", None))
        self.label_16.setText(QCoreApplication.translate("pesoWindow", u"Seleccionar Balanza", None))
        self.labelNBobina.setText(QCoreApplication.translate("pesoWindow", u"0/0", None))
        self.labelNPaleta.setText(QCoreApplication.translate("pesoWindow", u"0/0", None))
        self.label_20.setText(QCoreApplication.translate("pesoWindow", u"N Bobina", None))
        self.label_22.setText(QCoreApplication.translate("pesoWindow", u"N\u00ba Paleta", None))
        self.label_24.setText(QCoreApplication.translate("pesoWindow", u"Acumulado paleta (Kg)", None))
        self.labelAcumPaleta.setText(QCoreApplication.translate("pesoWindow", u"0.00", None))
        self.label_26.setText(QCoreApplication.translate("pesoWindow", u"Acumulado O.P (Kg)", None))
        self.labelAcumOp.setText(QCoreApplication.translate("pesoWindow", u"0.00", None))

        # Testing functions
        #self.rowCount,self.items,self.tablaPesaje = appendTable(self.rowCount,5,self.items,self.tablaPesaje,dataExampleTableBobinas)
        self.loadTodayTickets()

        #self.fillFields(dataExampleFieldsBobinas)
        #self.fillSelectors(arrExampleProduc,arrExampleCodigo,arrExampleProduc)

    def updateFieldsByOp(self):
        op = self.lineOp.currentText()
        opRow = self.objmgr.getAnOp(op)
        resultProducts,arrProducts = self.objmgr.getProductsOnDB()
        resultClient,arrClient = self.objmgr.getClientsOnDB()

        productRow = getProductRowByOp(opRow,arrProducts,op)
        product = productRow[1] #opRow[] #self.comboBoxProd.currentText()
        client_id = productRow[3]
        clientRow = getClientfromId(arrClient,client_id) #self.comboBoxClient.currentText() # 
        client = clientRow[2] # client name
        codigo = productRow[0] #self.comboCodigo.currentText() # This is the product code.
        tara = str(opRow[1])
        bobXPallet = opRow[3]
        amt = opRow[2]
        actPallet = opRow[4]
        maxWeight = productRow[2]
        minWeight = productRow[4]
        # Update the screen values associated with frame pesaje widget.
        self.comboBoxProd.setCurrentText(product)
        self.comboBoxClient.setCurrentText(client)
        self.comboCodigo.setCurrentText(codigo)
        self.lineTara.setText(  "{:4.2f}".format(float(tara)) )
        self.labelTara.setText( "{:4.2f}".format(float(tara)) )
        self.lineBxP.setText(str(bobXPallet))
        self.lineCantidad.setText(str(amt))
        self.linePaletaAct.setText(str(actPallet))
        self.linePesoMax.setText(str(maxWeight))
        self.linePesoMin.setText(str(minWeight))

    def loadTodayTickets(self):
        # It makes error when op gets deleted from op list and get store theirs tickets
        success,table = self.objmgr.dbMGR.getTableByRow("proceso_bobina","fecha_emision",str(date.today()))
        #print("table for today=>",table)
        if success:
            for i in range(len(table)):
                ticket = table[i][0]
                op = table[i][6]
                #print("op for today=>",op)
                opRow = self.objmgr.getAnOp(op)
                #print("opRow for today=>",opRow)
                productCode = opRow[8]
                productRow = self.objmgr.getAnProduct(productCode)
                productName = productRow[1]
                netWeight = table[i][2]
                data = {
                    "ticket":str(ticket),
                    "op":str(op),
                    "productCode":str(productCode),
                    "description":str(productName),
                    "bruteWeight": "{:4.2f}".format(float(netWeight))
                }
                self.rowCount,self.items,self.tablaPesaje = appendTable(self.rowCount,5,self.items,self.tablaPesaje,data)

    def fillOpFromDB(self):
        self.checkOp()
        self.checkbm.setChecked(False)
        if self._checkGeneral:
            #print("fill fields from database")
            pass
            
    def getCurrentOp(self):
        op = self.lineOp.currentText()
        return op

    def tara_inter(self):
        self.tareFromLine()
        return self.tara_intermediaria

    def tareFromLine(self):
        self.tara_intermediaria = 0.0
        tara = 0.0
        try:
            self.tara_intermediaria = float(self.lineTara.text())
            tara = float(self.lineTara.text())
        except:
            pass
        if self.checkTara(tara):
            self.objmgr.setTara(tara)
            self.labelTara.setText(str(tara))
            self.labelTara.setEnabled(True)
            self.labelNeto.setEnabled(False)
            op = self.lineOp.currentText()
            #print("tara updated:",tara," obj tara:",self.objmgr.getTara())
            self.objmgr.updateTaraOnDB(str(op),str(tara))

    def checkTara(self,tara):
        result = False
        try:
            if isFloat(tara) and tara > 0.00 :#and tara <= 4.00:
                self._checkTara = True
                changeToNormal(self.lineTara)
                result = True
            else:
                changeToError(self.lineTara)
                self._checkTara = False                
        except Exception as e:
            changeToError(self.lineTara)
            self._checkTara = False
            print(e)
        #print(f"Resultado de cheackTara: {result}.")
        return result

    def checkWeight(self):
        try:
            weight = self.objmgr.getWeight()
            if isFloat(weight) and weight > 0.00:
                self._checkWeight = True  
            else:
                self.blinkErrorLCD()
                self._checkWeight = False                
        except Exception as e:
            self.timer.singleShot(600,self.changeToErrorLCD)
            self.timer.singleShot(1500,self.changeToNormalLCD)
            self._checkWeight = False
            print(f"Existe una excepcion: {e}")
        ##################
        #self._checkWeight = True # Use this only for tests.
        ##################
        return self._checkWeight

    def checkWMax(self):
        try:
            pesoMax = float(self.linePesoMax.text())
            if isFloat(pesoMax) and pesoMax > 0.00:
                self._checkWMax = True 
                changeToNormal(self.linePesoMax) 
            else:
                self._checkWMax = False    
                changeToError(self.linePesoMax)            
        except Exception as e:
            self._checkWMax = False
            changeToError(self.linePesoMax)
            #print(e)
        return self._checkWMax

    def blinkErrorLCD(self):
        self.timer.singleShot(500,self.changeToErrorLCD)
        self.timer.singleShot(1000,self.changeToNormalLCD)
        self.timer.singleShot(1500,self.changeToErrorLCD)
        self.timer.singleShot(2000,self.changeToNormalLCD)
        self.timer.singleShot(2500,self.changeToErrorLCD)
        self.timer.singleShot(3000,self.changeToNormalLCD)
        self.timer.singleShot(3500,self.changeToErrorLCD)
        self.timer.singleShot(4000,self.changeToNormalLCD)

    def changeToErrorLCD(self):
        changeToError(self.lcdNumber)

    def changeToNormalLCD(self):
        changeToNormal(self.lcdNumber)

    def getTableBobinas(self):
        return self.objmgr.getTableBobinas()
    
    def getTableBobinas_OP(self):
        return self.objmgr.getTableBobinas_OP()

    def getTableClients(self):
        return self.objmgr.getTableClients()

    def getTableProducts(self):
        return self.objmgr.getTableProducts()

    def addItemsToOp(self,arrTable):
        self.lastOp = self.lineOp.currentText()
        #print("Last op saved =>",self.lastOp)
        self.lineOp.clear()
        #print("OK CLEAR LINE OP")
        """for i in range(len(arrTable)):
            self.lineOp.addItem(arrTable[i])
            print(arrTable[i])"""
        list_op = [str(i) for i in arrTable]
        self.lineOp.addItems(list_op)
        # charge the actual op index to the screen line text.
        #print(" current op", self.currentOps," indexop:",self.indexOp)
        self.lineOp.setCurrentText(self.lastOp)#self.currentOps[self.indexOp])
        #print("OK additemsop")

    def addItemsToClients(self,arrTable):
        self.comboBoxClient.clear()
        for i in range(len(arrTable)):
            self.comboBoxClient.addItem(arrTable[i])

    def addItemsToProducts(self,arrTable):
        self.comboBoxProd.clear()
        self.comboBoxProd.addItems(arrTable)
        """for i in range(len(arrTable)):
            self.comboBoxProd.addItem(arrTable[i])"""

    def addItemsToCodes(self,arrTable):
        self.comboCodigo.clear()
        self.comboCodigo.addItems(arrTable)
        """for i in range(len(arrTable)):
            self.comboCodigo.addItem(arrTable[i])"""

    def updateIndexOp(self):
        for i in range(len(self.tableOp)):
            #print("arr",self.tableOp[i][0],"?",self.lineOp.currentText()," lastOp=>",str(self.lastOp))
            if str(self.tableOp[i][0]) == self.lineOp.currentText() :#str(self.lastOp): # 
                self.indexOp = i
                #print("IndexOp=>",self.indexOp)

    def updateIndexOpLast(self):
        for i in range(len(self.tableOp)):
            #print("arr",self.tableOp[i][0],"?",self.lineOp.currentText()," lastOp=>",str(self.lastOp))
            if str(self.tableOp[i][0]) == str(self.lastOp): # 
                self.indexOp = i
                #print("IndexOp=>",self.indexOp)

    def checkOp(self):
        #self.checkbm.setChecked(False)
        #self.checktd.setChecked(False)
        #self.checkh.setChecked(False)
        
        op = self.lineOp.currentText()
        opExist = not len(self.objmgr.getAnOp(op)) <= 0
        #print(" the op ",op, " exist ?",opExist)
        if opExist:        
            self.lockFields()
            #self.botonTara.setEnabled(False)
            #if containsValue(self.tableOp,self.lineOp.currentText()):
            #print("contains value ",self.lineOp.currentText()," from tableOp")
            self.updateIndexOp()
            #print("index op",self.indexOp)
            if len(self.tableOp)> 0:
                code = str(self.tableOp[self.indexOp][8])
                #print("tableOp result",self.tableOp,"code=>",code,"indexOp=>",self.indexOp)
                #product = getProductFromCode(self.tableProducts,code)
                product = self.objmgr.getProductFromCode(code)
                #print("Product:",product)
                nameProduct = product[1]
                clientId = product[3]
                self.updateClientsFromDB()
                #client = getClientfromId(self.tableClients,clientId)
                client = self.objmgr.getClientfromIDDB(clientId)
                #print("client:",client)
                clientName = client[2]
                tara = str(self.tableOp[self.indexOp][1])
                maxWeightCoils = str(product[2] )# check if there is max weight by coil or other.
                minWeightCoils = str(product[4])
                bxp = str(self.tableOp[self.indexOp][3])
                dataDic = {
                    "op": str(self.tableOp[self.indexOp][0]),
                    "productCode":str(self.tableOp[self.indexOp][8]),
                    "product":nameProduct,
                    "tara": tara,
                    "client":clientName,
                    "maxWeightBob":maxWeightCoils,
                    "minWeightBob":minWeightCoils,
                    "bxp":bxp,
                    "amtPallet":str(self.tableOp[self.indexOp][2]),
                    "actualPallet":str(self.tableOp[self.indexOp][4]),
                }
                #print("dataDict:",dataDic)
                #self.fillFields(dataDic)
                self.updateFieldsByOp()
                self.objmgr.setTara(float(tara))
                #if error_lineOP == True:
                    #self.checkbm.setChecked(False)
        else:
            if self.objmgr.currentUser["nivel"] == "ADMINISTRADOR" or self.objmgr.currentUser["nivel"] == "SUPERVISOR":
                self.unlockFields()
                self.botonTara.setEnabled(True)
                self.linePaletaAct.setText("1")
            #print("tableOp: ",self.tableOp," lineOp: ",self.lineOp.currentText())
        try:
            op = int(self.lineOp.currentText())
            if op != 0 and  check3DigitsOp(int(op)) and len(list(self.lineOp.currentText()))==8:
                self._checkOp = True
                changeToNormal(self.lineOp)
                error_lineOP = False
            else:
                self._checkOp = False
                changeToError(self.lineOp)
                error_lineOP = True
        except:
            self._checkOp = False
            changeToError(self.lineOp)
            error_lineOP = True

        #print("breakpoint at CHECKOP=> ",time.time()-initTime)
        if error_lineOP == True:
            self.checkbm.setChecked(False)
        self.updateScreenValues()
        return self._checkOp

    def checkMaxWB(self):
        return True
        #return self.objmgr.getMaxWeightBobina() > self.objmgr.getWeight()

    def checkBxP(self):
        self._checkBxP = self.checkInt(self.lineBxP)
        if self._checkBxP:
            op = self.lineOp.currentText()
            bxp = self.lineBxP.text()
            self.objmgr.updateBxPOnDB(op,bxp)
        return self._checkBxP
            
    def checkAmt(self):
        self._checkAmt = self.checkInt(self.lineCantidad)
        if self._checkAmt:
            op = self.lineOp.currentText()
            amt = self.lineCantidad.text()
            self.objmgr.updateAmtPalletsOnDB(op,amt)
        return self._checkAmt

    def checkPallet(self):
        self._checkPallet = self.checkInt(self.linePaletaAct)
        return self._checkPallet

    def checkGeneral(self):
        checkPallet = self.checkPallet()
        checkWMax = self.checkWMax()
        checkAmt = self.checkAmt()
        checkBxP = self.checkBxP()
        checkMaxWB = self.checkMaxWB()
        checkOp = self.checkOp()
        checkWeight = self.checkWeight()
        #checkTara = self._checkTara
        #print(self._checkTara,checkWeight,checkPallet,checkWMax,checkAmt,checkBxP,checkMaxWB,checkOp)
        return self._checkTara and checkWeight and checkPallet and checkWMax and checkAmt and checkBxP and checkMaxWB and checkOp

    
    def checkInt(self,object):
        checkNumber = False
        try:
            number = int(object.text())
            if number != 0 :
                checkNumber = True
                changeToNormal(object)
            else:
                self._checkOp = False
                changeToError(object)
        except:
            checkNumber = False
            changeToError(object)
        return checkNumber

    def checkPesoMax(self):
        pass

    def blink(self,obj):
        self.timer.singleShot(500,obj.hide)
        self.timer.singleShot(1000,obj.show)
        self.timer.singleShot(1500,obj.hide)
        self.timer.singleShot(2000,obj.show)
        self.timer.singleShot(2500,obj.hide)
        self.timer.singleShot(3000,obj.show)
        self.timer.singleShot(3500,obj.hide)
        self.timer.singleShot(4000,obj.show)
        self.timer.singleShot(4500,obj.hide)
        self.timer.singleShot(5000,obj.show)
        self.timer.singleShot(5500,obj.hide)

    def getFramePeso(self):
        return self.framePeso
        
    def showNotification(self,alertText):
        responsive = self.objmgr.getResponsive()
        self.lineNotify = QLabel(self.framePeso)
        self.lineNotify.setGeometry(responsive.qRectScaled(20, 205, 840, 25))
        #self.lineNotify.setGeometry(QRect(20, 205, 840, 25))
        self.lineNotify.setAlignment(Qt.AlignCenter)
        self.lineNotify.setObjectName(u"lineNotify")
        self.lineNotify.show()
        self.lineNotify.setText(alertText)
        self.blink(self.lineNotify)

    def changeOp(self):
        self.lineBxP.setText("")
        self.lineCantidad.setText("")
        self.linePesoMax.setText("")
        self.linePesoMin.setText("")
        self.lineTara.setText("")
        self.labelTara.setText("")
        self.linePaletaAct.setText("")
        self.comboCodigo.clear()
        self.comboBoxProd.clear()
        self.comboBoxClient.clear()

    def changeBal(self):
        if self.comboBoxBal.currentText() == "Balanza 1".upper():
            self.lcdNumber.show()
            self.lcdInput.hide()
            self.objmgr.setIndexBalanza(1)
            if self.objmgr.isManual():
                self.objmgr.run()
                self.objmgr.stopManual()
                print("deactivated  manual")
            if self.objmgr.isActiveBalanza2():
                self.objmgr.stopBalanza2()
                self.objmgr.updateWeight(0.0)
                print("deactivated  balanza 2")
            print("status balanza:",self.objmgr.getIndexBalanza())
        elif self.comboBoxBal.currentText() == "Balanza 2".upper():
            self.objmgr.showWaitBalanzaWindow(Action("WAIT_BALANZA",self))
            self.lcdNumber.show()
            self.lcdInput.hide()
            self.objmgr.setIndexBalanza(2)
            if self.objmgr.isManual():
                self.objmgr.run()
                self.objmgr.stopManual()
            if not self.objmgr.isActiveBalanza2():
                self.objmgr.startBalanza2()
                print("Activated  balanza 2")
                print("status balanza:",self.objmgr.getIndexBalanza())

        elif self.comboBoxBal.currentText() == "MANUAL".upper():
            self.lcdNumber.hide()
            self.lcdInput.show()
            self.objmgr.setIndexBalanza(3)
            self.objmgr.stopProvider()
            self.objmgr.setManual()
            if self.objmgr.isActiveBalanza2():
                self.objmgr.stopBalanza2()
            try:
                weight = float(self.lcdInput.text())
                #print("weight",weight)
                self.objmgr.updateWeight(weight)
                changeToNormal(self.lcdInput)
            except:
                self.objmgr.updateWeight(0.00)
                changeToError(self.lcdInput)
        else:
            pass
        pass

    def checkbmChanged(self):
        #print("bm checked=>",self.checkbm.isChecked())
        if self.checkbm.isChecked():
            self.labelBobMatriz.clear()
            changeToNormal(self.labelBobMatriz)
            self.labelBobMatriz.setEnabled(True)
            #print("Enabled")
        else:
            self.labelBobMatriz.clear()
            self.labelBobMatriz.setText("")
            changeToDisable(self.labelBobMatriz)
            self.labelBobMatriz.setDisabled(True)
            #print("Disabled")

        if self.checkh.isChecked:
            self.checkh.setChecked(False)
            #self.checkbm.setChecked(True)
            ##print("you checked bm!")
        
        pass

    def checkhChanged(self):
        if self.checkbm.isChecked:
            self.checkbm.setChecked(False)
            #self.checkh.setChecked(True)
            ##print("you checked bm!")
        pass

    def actionBobina(self):
        pass

    def actionMatriz(self):
        
        pesajeObject = self
        mgrObj = self.objmgr
        try:
            #print("input matriz accepted!!!")
            #mgrObj.bobinaMatriz = int(obj.input.text())
            #print("bobina matriz guardada..., ",mgrObj.bobinaMatriz)

            # Cargo el diccionario actual de la bobina
            bobMatriz = self.labelBobMatriz.text() #mgrObj.bobinaMatriz
            fields = pesajeObject.readFieldsBobina()
            #print("Result reading database \n",fields,"\n setting main coil with ",bobMatriz)
            if len(fields)>0:
                fields["bobMatriz"] = str(bobMatriz)
                mgrObj.setData(fields)
                # Envio la impresion del ticket
                mgrObj.printBobina()

                mgrObj.showPrintingWindow(pesajeObject.actionBobina)
                
                # cierro la ventana emergente de notificacion
                #self.objmgr.closePrintingWindow() #closing with timer
                # make all verifications here...  
            else:
                pass
                #print("some error printing coils....")  

        except Exception as e:
            print(e)
            pass   

    def showHablador(self):
        self.setModePrintHablador(1)
        self.objmgr.showInsertHabladorWindow("",self)

    def actionHablador(self,hablador):
        #print(hablador)
        #self.objmgr.showPrintingWindow(self.actionBobina)
        # Cargo el diccionario actual de la bobina
        dataHablador = getArrHablador(hablador)
        result = self.objmgr.saveHablador(dataHablador)
        if result:
            #self.objmgr.setHablador(hablador)
            ##print("init print hablador")
            self.objmgr.printHablador()
            ##print("end print hablador")

            time.sleep(3)
            
            self.objmgr.setData(self.readFieldsPallet())

            ##print("init print pallet")
            self.objmgr.printPallet()
            ##print("end print pallet")

            # cierro la ventana emergente de notificacion
            self.objmgr.closeInsertHabladorWindow()
            #self.objmgr.closePrintingWindow()
            # make all verifications here... 
              

    def actionReHablador(self,hablador):
        #print(hablador)
        # Cargo el diccionario actual de la bobina
        #self.objmgr.setHablador(hablador)
        self.objmgr.printHablador()
        self.objmgr.closeInsertHabladorWindow()

    def initPrint(self):
        self.objmgr.stopProvider() # fast execution when stoping the provider cycle.
        #inicio_getanopeninitprint=time.time()
        opRow = self.objmgr.getAnOp(self.lineOp.currentText())# Modificado 24/05/2023
        self.objmgr.setEnableOp(len(opRow)>0) # if exist op pass to process!!!
        #tiempo_getanopeninitiprint=time.time()-inicio_getanopeninitprint
        #print(f"tiempo getanop en init print: {tiempo_getanopeninitiprint}")
        if not self.objmgr.isEnableOp():
            if self.objmgr.currentUser["nivel"] == "SUPERVISOR" or self.objmgr.currentUser["nivel"] == "ADMINISTRADOR":
                #self.objmgr.addOp(self.lineOp.currentText())
                pass
            else:
                mensaje = Dialog_msj("permiso_crear_op",self)
                mensaje.setWindowModality(Qt.ApplicationModal)
                mensaje.exec_()
        #print("result creating op",self.objmgr.isEnableOp())
        if self.objmgr.isEnableOp():
            self.objmgr.disableOp() # turn off enter to new op on DB  
            #inicio_checkgeneral=time.time()  
            self._checkGeneral = self.checkGeneral()  
            #tiempo_checkgeneral=time.time()-inicio_checkgeneral
            #print(f"Estado de checkgenral: {self._checkGeneral}")
            #print(f"Check general en init print: {tiempo_checkgeneral}")
            if self._checkGeneral: #if not self.objmgr.isCapturing() and self._checkGeneral: # When you want to check capture weight button first.
                if self.checkbm.isChecked():
                    #print("printing with bobMatriz variable")
                    self.actionMatriz()
                    #self.objmgr.showInsertMatrizWindow(Action("INPUT_MATRIZ",self))
                else:
                    # Cargo el diccionario actual de la bobina
                    #inicio_readfieldsbobina=time.time()
                    fields = self.readFieldsBobina()
                    #tiempo_readfieldbobina=time.time()-inicio_readfieldsbobina
                    #print(f"Tiempo readfieldsbobina en initprint: {tiempo_readfieldbobina}")
                    #inicio_updateoplist=time.time()
                    self.updateOpList()
                    #tiempo_updateoplist=time.time()-inicio_updateoplist
                    #print(f"Tiempo updateoplista en initprint: {tiempo_getanopeninitiprint}")
                    self.objmgr.setData(fields)
                    #inicio_printbobina=time.time()
                    printResult = self.objmgr.printBobina()
                    #tiempo_printbobina=time.time()-inicio_printbobina
                    #print(f"Tiempo printbobina en initprint: {tiempo_printbobina}")
                    if self.checktd.isChecked():
                        printResult = self.objmgr.printBobina()
                        #print("you checked doble print, printing second coil...")
                    #print("\nresult print:",printResult,fields,"\n")
                    # Envio la impresion del ticket
                    #self.objmgr.showPrintingWindow(self.actionBobina)
                    #inicio_updatescreenvalues=time.time()
                    self.updateScreenValues()
                    #tiempo_updatescreenvalues=time.time()-inicio_updatescreenvalues
                    #print(f"Tiempo updatescreenvalues en initprint: {tiempo_updatescreenvalues}")
                #self.unlockFields()
                loadStyles(self,NORMAL)
                self.isCapturing = True
                self.objmgr.setCapturing(True)
            elif not self._checkGeneral:
                print("Some field doesn't match.")
            else:
                print("You have to make capturing before init print and data need to match.")
        else:
            pass
        #inicio_updateindexop=time.time()
        self.updateIndexOp()
        #tiempo_updateindexop=time.time()-inicio_updateindexop
        #print(f"Tiempo en updateindexop en initprint: {tiempo_updateindexop}")
        #inicio_updatescreenvalues2=time.time()
        self.updateScreenValues()
        #tiempo_updatescreenvalues2=time.time()-inicio_updatescreenvalues2
        #print(f"Tiempo updatescreenvalues en initprint: {tiempo_updatescreenvalues2}")
        if self.comboBoxBal.currentText() == "MANUAL".upper():
            pass
        else:
            self.objmgr.run() # start again a new instance op provider.


    def verificar_tara(self):
        if self.lineTara.text() == "0.0" or self.lineTara.text() =="0" or self.lineTara.text() =="" or self.lineTara.text() == " "or self.lineTara.text() == "0.00":
            ventana_agregar_tara = Dialog_msj("agregar_tara",self)
            ventana_agregar_tara.setWindowModality(Qt.ApplicationModal)
            ventana_agregar_tara.exec_()

    def verificar_datos_op(self):
        result = False
        if (self.lineTara.text() == "" or self.linePesoMax.text() == "" or self.linePesoMin.text() == "" or self.linePesoMin.text() == "None" or self.lineCantidad.text() == "" or self.lineBxP.text() == ""):
            result = False
            #print("Hay un campo vacio")
        else:
            result = True
            #print("Todos los campos estan OK")
        return result
    
    def verificar_linePesoMin(self):
        #result = False
        if self.linePesoMin.text() == "" or self.linePesoMin.text() == " " or self.linePesoMin.text() == "0" or self.linePesoMin.text() == "None" or self.linePesoMin.text() == "0.0":
            ventana_agregar_pesomin = DialogVerificacionImpresion(self,"agregar_pesoMin")
            ventana_agregar_pesomin.setWindowModality(Qt.ApplicationModal)
            ventana_agregar_pesomin.exec_()
        else:
            #print("Todo OK")
            pass

    def verificar_limites(self):
        #print(f"Peso Actual: {self.objmgr.weight}")
        self.limites = False
        #print(f"Peso usado: {self.objmgr.weight}")
        if  not (self.objmgr.currentUser["nivel"] == "SUPERVISOR" or self.objmgr.currentUser["nivel"] == "ADMINISTRADOR"):
            self.limites = False
            if (self.objmgr.weight >= float(self.linePesoMin.text().replace(",",".")) and self.objmgr.weight <= float(self.linePesoMax.text().replace(",","."))):
                self.limites = True
            else:
                mensajeError = Dialog_msj("peso_fuera_de_rango",self)
                mensajeError.setWindowModality(Qt.ApplicationModal)
                mensajeError.exec_()
                #result = False
        else:
            #print("eNTRANDO A ELSE")
            self.limites = True
        return self.limites

    def verificar_cliente_nestle(self):
        if (self.comboCodigo.currentText().startswith("FM0-NES") or self.comboCodigo.currentText().startswith("FM0-NET") or self.comboCodigo.currentText().startswith("FM0-ITC")):
            result = True
        else:
            result = False
        return result

    def initWeight(self):
        self.supervisor_aprobador = "N/A"
        inicio_impresion = time.time()
        #print(f"Inicio de impresion: {inicio_impresion}")
        opRow = self.objmgr.getAnOp(self.lineOp.currentText())# Modificado 24/05/2023
        self.objmgr.setEnableOp(len(opRow)>0)
        if not self.objmgr.isEnableOp():
            if self.objmgr.currentUser["nivel"] == "SUPERVISOR" or self.objmgr.currentUser["nivel"] == "ADMINISTRADOR":
                #self.objmgr.addOp(self.lineOp.currentText())
                mensaje = Dialog_msj("op_no_registrada",self)
                mensaje.setWindowModality(Qt.ApplicationModal)
                mensaje.exec_()
            else:
                mensaje = Dialog_msj("permiso_crear_op",self)
                mensaje.setWindowModality(Qt.ApplicationModal)
                mensaje.exec_()
            #self.objmgr.up
        #print("Haz hecho clic!!!!")
        self.verificar_linePesoMin()
        self.verificar_tara()
        #self.verificar_limites()
        if self.verificar_datos_op() and self.verificar_limites():
            if ((self.verificar_cliente_nestle() and self.checkbm.isChecked() and self.labelBobMatriz.text() != "") or (not self.verificar_cliente_nestle())):
                self.botonIniciar.setEnabled(False)
                self.botonIniciar.setDisabled(True)
                op = self.lineOp.currentText()
                #inicio_getAnOp=time.time()
                opRow = self.objmgr.getAnOp(op)
                #tiempo_getanOP=time.time()-inicio_getAnOp
                #print(f"tiempo getanop:{tiempo_getanOP}")
                countMax = 99999
                cuCountBobinas = -1
                if len(opRow) > 0 :
                    countPallet = opRow[4]
                    #inicio_getcoils=time.time()
                    #resultCoils,coils = self.objmgr.getCoilsOnDB()
                    #tiempo_getcoils=time.time()-inicio_getcoils
                    #print(f"tiempo getcoils: {tiempo_getcoils}")
                    #inicio_countbobinas=time.time()
                    cuCountBobinas = len(self.objmgr.countBobinasPalletNew(op,countPallet))
                    #tiempo_countbobinas=time.time()-inicio_countbobinas
                    #print(f"tiempo countbobinas: {tiempo_countbobinas}")
                    countMax = int(opRow[3]) if opRow[3] not in (None, "") else 99999
                #print("countMax=>",countMax," cuCountBobinas=>",cuCountBobinas)
                if countMax <= cuCountBobinas:
                    #print("You area trying to exceed the current amount of coils")
                    #inicio_exceed=time.time()
                    self.objmgr.showExeedBobinaWindow(Action("EXEED_BOBINA",self),countMax)
                    #tiempo_exceed=time.time()-inicio_exceed
                    #print(f"Tiempo Exceed: {tiempo_exceed}")
                else:
                    #print("Keep Printing with out any wait windows!.")
                    #inicio_initprint=time.time()
                    self.initPrint()#Modificado 24/05/2023
                    #tiempo_initprint=time.time()-inicio_initprint
                    #print(f"tiempo initprint: {tiempo_initprint}")
                self.botonIniciar.setDisabled(False)
                self.botonIniciar.setEnabled(True)
                final_impresion = time.time()
                tiempo_total = final_impresion - inicio_impresion
                #print(f"Final de impresion: {final_impresion}")
                #print(f"Tiempo total de impresion: {tiempo_total}")
            else:
                #print("Cliente Nestle, debe marcar la bobina matriz")
                mensajeError = Dialog_msj("cliente_nestle",self)
                mensajeError.setWindowModality(Qt.ApplicationModal)
                mensajeError.exec_()
        else:
            print("Hay campos vacios o el peso está fuera de los límites")

    def cptWeight(self):
        self._checkGeneral = self.checkGeneral() 
        #print("checking returned:",self._checkGeneral, "CAPTURING:",self.isCapturing)
        if self._checkGeneral:
            if self.isCapturing:
                #self.lockFields()
                loadStyles(self,INIT_PESAJE)
                self.objmgr.setCapturing(False)
            else:
                #self.unlockFields()
                loadStyles(self,NORMAL)
                self.objmgr.setCapturing(True)   
                #self.objmgr.updateWeight(0.0)      
        self.isCapturing = not self.isCapturing

    def actionPallet(self):
        self.objmgr.showWaitPrintWindow(Action("CONFIRM_PRINT",self))
    
    def actionPrintPallet(self):
        #print("This pallet has a tiket? ",self.palletHasTicket())
        fields = self.readFieldsPallet()
        #fields[""] = 
        self.objmgr.setData(fields)
        #print(self.readFieldsPallet()
        self.objmgr.printPallet()
        self.updateScreenValues()
        if self.isCapturing == False:
            self.isCapturing = True
            loadStyles(self,NORMAL)
            self.unlockFields()
        #print("updating screen values from the pallet...")

    def closePallet(self):
        mensaje = Dialog_msj("seleccione_paleta_embalaje",self)
        mensaje.setWindowModality(Qt.ApplicationModal)
        mensaje.exec_()

    def setPaletaEmbalaje(self,peso):
        self.objmgr.paletaEmbalaje = peso

    def closePallet_new(self):
        if self.palletHasTicket():
            if self.checkh.isChecked():
                self.objmgr.showClosePalleteWindow(Action("CONFIRM_PALLET_HABLADOR",self))
            else:
                self.objmgr.showClosePalleteWindow(Action("CONFIRM_PALLET",self))
                pass
        else:
            #print("This pallet doesn't have any ticket yet!!!")
            self.showNotification("Ud. debe imprimir al menos un ticket para poder cerrar esta paleta.")


    def returnToProducts(self):
        self.objmgr.changeView(1)
        pass

    def updateWeight(self,weight):
        weight = "{:4.2f}".format(float(weight))
        ##print(weight)
        self.lcdNumber.setProperty("value", str(weight))
        pass

    def updateNeto(self,neto):
        neto = "{:4.2f}".format(float(neto))
        self.labelNeto.setText(str(neto))
        pass

    def getInfoOp(self,op):
        result = []
        # get all bob. as part of an production order from db
        return result

    def fillFields(self,dataDic):
        #self.lineOp.setCurrentText(dataDic["op"])
        self.linePesoMax.setText(dataDic["maxWeightBob"])
        self.linePesoMin.setText(dataDic["minWeightBob"])
        self.lineBxP.setText(dataDic["bxp"])
        self.lineTara.setText(dataDic["tara"])
        self.linePaletaAct.setText(dataDic["actualPallet"])
        self.comboCodigo.setCurrentText(dataDic["productCode"])
        self.comboBoxProd.setCurrentText(dataDic["product"])
        self.comboBoxClient.setCurrentText(dataDic["client"])
        self.lineCantidad.setText(dataDic["amtPallet"])

    def fillPesoMin(self,peso_min,peso_max):
        self.linePesoMin.setText(str(peso_min))
        self.linePesoMax.setText(str(peso_max))

    # Make sure to call this method only where you are trying to print tickets
    def readFieldsBobina(self):
        op = ""
        product = ""
        client = ""
        neto = ""
        bruto = ""
        tara = ""
        codigo = ""
        ticket = "1"
        nPaleta = ""
        bobina = "0"
        hora = getCurrentTime()
        date = getDate()
        turno = str(getTurn())
        #fullDate = getFullDate()
        user = self.objmgr.getUser()["nombre"] + " " + self.objmgr.getUser()["apellido"] #self.objmgr.getUser()["usuario"]
        ficha = self.objmgr.getUser()["ficha"]
        bobinaMatriz = "" #self.labelBobMatriz.text() #str(self.objmgr.getBobMatriz())
        if self.checkbm.isChecked:
            bobinaMatriz = self.labelBobMatriz.text()
        #
        fechaEmision = date
                                                    #(12,1.0,1.0,23,23,"25/06/2022",1256845,3020)
        last_ticket_rows = self.objmgr.dbMGR.ultimoticket("proceso_bobina")
        hablador = ""
        totalOp = ""
        ticket = "1"

        if True:
            if last_ticket_rows:
                ticket = str(int(last_ticket_rows[0][0])+1)

            op = self.lineOp.currentText()
            #product = self.comboBoxProd.currentText()
            #client = self.comboBoxClient.currentText()
            #codigo = self.comboCodigo.currentText()
            self.tara_inter()
            tara = "{:4.2f}".format(float(self.tara_intermediaria))#Modificado el 30/10/2023
            self.objmgr.settarainter(self.tara_intermediaria)
            self.objmgr.updateWeight(self.objmgr.getWeight())

            neto = "{:4.2f}".format(float(self.objmgr.getNeto()))
            bruto = "{:4.2f}".format(float(self.objmgr.getBruto()))
            
            #print("neto=>",neto," bruto=>",bruto," tara=>",tara)
            bxPaleta = self.lineBxP.text()
            actualPallet = self.linePaletaAct.text()

            #print("Storing ticket result,",successStore," with data ",data)
            # first check if op exist on db
            opRow = self.objmgr.getAnOp(str(op))
            #print("check op row result, ",opRow," lenght=>",len(opRow)>0)
            # if not exist store a new oprow on db

            if not len(opRow)>0:
                product = self.comboBoxProd.currentText()
                client = self.comboBoxClient.currentText()
                codigo = self.comboCodigo.currentText()

                tara = "{:4.2f}".format(float(self.objmgr.getTara()))

                actPallet = self.linePaletaAct.text() #opRow[4]
                data = (ticket,bruto,neto,actPallet,bobinaMatriz,fechaEmision,op,ficha,hora,"1",self.supervisor_aprobador)
                #print(data)
                successStore = self.objmgr.storeTicket(data)

                nPaleta = self.lineCantidad.text() #opRow[3] #considering an op start with 1 and every close increment
                dataOp = (op,tara,nPaleta,bxPaleta,1,bobinaMatriz,hablador,totalOp,codigo)
                successStoreOp = self.objmgr.storeOp(dataOp)
                #print("Success storing op at DB, data:",dataOp," result:",successStoreOp)
                ###########
                bobina = str(len(self.objmgr.countBobinasPalletNew(op,actPallet))) # this is the number coil over the pallet
                #print("1bobina=",bobina,"\ntickets=",newTickets,"\nop=",op," pallet=",actPallet)
                ###########
            else:

                #opRow = self.objmgr.getAnOp(op)
                tara = "{:4.2f}".format(float(opRow[1]))
                #print(f"Tara en else: {tara}.")
                #tara = "{:4.2f}".format(float(self.objmgr.getTara()))
                #print(f"OP ROW: {opRow}")
                #resultProducts,arrProducts = self.objmgr.getProductsOnDB()
                #resultClient,arrClient = self.objmgr.getClientsOnDB()

                #productRow = getProductRowByOp(opRow,arrProducts,op)

                productRow = self.objmgr.getProductRowByOPDB(opRow)
                #print(f"ProductRow: {productRow}")
                product = productRow[1] #opRow[] #self.comboBoxProd.currentText()
                client_id = productRow[3]
                #clientRow = getClientfromId(arrClient,client_id) #self.comboBoxClient.currentText() # 
                clientRow = self.objmgr.getClientfromIDDB(client_id)
                #print(f"clienteRow: {clientRow}")
                client = clientRow[2] # client name
                codigo = productRow[0] #self.comboCodigo.currentText() # This is the product code.
                #print("product",product,"codigo",codigo,"cliente",client)
                actPallet = opRow[4]
                actPallet = self.linePaletaAct.text()
                data = (ticket,bruto,neto,actPallet,bobinaMatriz,fechaEmision,op,ficha,hora,"0",self.supervisor_aprobador)

                successStore = self.objmgr.storeTicket(data)
                ###########
                bobina = len(self.objmgr.countBobinasPalletNew(op,actPallet))
                #bobinas_eliminados =  countBobinasPallet(deletedTickets,op,actPallet)
                bobinas_eliminados =  len(self.objmgr.countBobinasPalletNew_Deleted(op,actPallet))

                bobina = bobina + bobinas_eliminados
                if bobina == 0:
                    # The first of the pallet
                    self.objmgr.updateBobinaOnDB(ticket,"1")
                if bobina > 0:
                    # The n>0 of the pallet
                    self.objmgr.updateBobinaOnDB(ticket,bobina)

                #print("for this op=> ",bobina," deleted=> ",bobinas_eliminados)
                #print("2bobina=",bobina,"\ntickets=",newTickets,"\nop=",op," pallet=",actPallet)
                ###########

            ##UPDATE HERE ALL FIELDS IN SCRElockFields(cptEEN
            self.comboBoxProd.setCurrentText(product)
            self.comboBoxClient.setCurrentText(client)
            self.comboCodigo.setCurrentText(codigo)
            self.lineTara.setText(tara)
            #### THIS WILL OVERRRIDE ANY ERROR OF PRODUCT,CODE, OR CLIENT INDEXS.

        self.labelNeto.setText(neto)

        if bobinaMatriz == "0" :
            bobinaMatriz = ""
            
        result = {
            "code": codigo,
            "producto" : product,
            "client" : client,
            "operador" : user,

            "reimpresion" : "",
            "bobMatriz" : bobinaMatriz,
            "bobina" : str(bobina),

            "turno" : str(turno),
            "op" : op,

            "neto" : "{:4.2f}".format(float(neto)),
            "bruto" : "{:4.2f}".format(float(bruto)),
            "tara" : "{:4.2f}".format(float(tara)),

            "date" : date,
            "ticketCode" : ticket,
        }
        #print("TICKET TO PRINT =>",result)
        resultTable = {
            "ticket": ticket,
            "op": op,
            "productCode": codigo,
            "description": product.upper(),
            "bruteWeight": bruto
        }
        #print("TICKET TO TABLE =>",resultTable)
        # this is only the header
        self.rowCount,self.items,self.tablaPesaje = appendTable(self.rowCount,5,self.items,self.tablaPesaje,resultTable)

        self.checkOp()
        return result 

    def readFieldsPallet(self):
        # Read only relevant records using indexed queries
        op = self.lineOp.currentText()
        actualPallet = self.linePaletaAct.text()
        try:
            actualPallet = str( int(self.linePaletaAct.text()) - 1  )
        except:
            pass
        successCoils, coilsForPallet = self.objmgr.dbMGR.getBobinasPallet_(op, actualPallet)
        successClients,dataClient = self.objmgr.getClientsOnDB()
        fullDate = getFullDate()
        dataOp = self.objmgr.getAnOp(op)
        dataPallet = [] #getTicketsForPallet(coilsForPallet)
        clientCode = ""
        productCode = ""
        product = ""
        product = self.comboBoxProd.currentText()
        client = self.comboBoxClient.currentText()
        if len(dataOp)>0 and successClients and successCoils:
            productCode = dataOp[8]
            #coilsForPallet = getTheSameCoils(coils,op)
            #print("\nsuccess getting clients: ",dataClient," code will go for ",client,"\n")
            clientCode = getCodeFromClient(dataClient,client) 
            #resultIncPallet = self.objmgr.incPalletOnDB(op,actualPallet)
            #print("result updating pallet counter, ",resultIncPallet)
        bobinas = 0 #str(dataOp[3])# Verificado 03/06/2022 # Verify, this is the number of coils per pallet of the order, not the counter.
        
        pesoBruto, pesoNeto = getTotalsForPallet(coilsForPallet)
        bobinas,dataPallet = getTicketsForPallet(coilsForPallet) 

        #paletas = str(dataOp[2]) # Verificar este es el numero de paletas totales, no es la paleta actual.
        userName = self.objmgr.getUser()["nombre"] + " " + self.objmgr.getUser()["apellido"] #self.objmgr.getUser()["usuario"]
        tara = self.lineTara.text()
        # Ticket width = 10 height = 5
        # Check if mgrCode change some times
        # 03/06/2022 corregido el numero de bobinas, numero de palletas.
        supervisor = self.objmgr.getSupervisor()
        result = {
            "date" : fullDate,
            "clientCode" : clientCode,
            "client" : client,
            "productCode" : productCode,
            "product" : product,
            "tara": tara,
            "bobinas" : str(bobinas),
            "pesoBruto" : str(pesoBruto),
            "pesoNeto" : str(pesoNeto),

            "mgrCode" : "MGR-GPR-F19(Ed.01)",
            "op" : op,
            "paletas": actualPallet,
            
            "header" : [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]],

            "data"  : dataPallet,
            "usr" : userName,
            "supervisor": supervisor
        }

        return result

    def readFieldsOp(self):
        op = self.lineOp.currentText()

        netoFloat = self.objmgr.getNeto()
        neto = "{:4.2f}".format(netoFloat)
        bruto = str(self.objmgr.getBruto())
        tara = str(self.objmgr.getTara())

        date = getDate()
        turno = str(getTurn())
        fullDate = getFullDate()
        user = self.objmgr.getUser()["user"]

        infoOp = self.getInfoOp("op")
        dataOp = infoOp["data"]
        

        product = infoOp ["product"] #self.comboBoxProd.currentText()
        productId = infoOp["productCode"]
        client = infoOp["client"] #self.comboBoxClient.currentText()
        clientId = infoOp["clientCode"] 
        accum = infoOp["accum"] # calcular si no esta en db
        amount = infoOp["amount"] # calcular si no esta en db
        total = infoOp["total"] # calcular si no esta en db
        units = infoOp["units"] # calcular si no esta en db
        
        # ticket width = 10 height = 5
        result = {
            "op" : op, 

            "clientId" : clientId,
            "clientName" : client,

            "productName" : product,
            "productId" : productId,

            "accum" : accum,
            "amount" : amount,
            "user" : user,

            "total" : total,
            "units" : units,
        }
        return result

    def fillSelectors(self,arrCodigo, arrProduc, arrClient):
        self.comboCodigo.setEditable(True)
        self.comboBoxProd.setEditable(True)
        self.comboCodigo.addItems(arrCodigo)
        self.comboBoxProd.addItems(arrProduc)
        self.comboBoxClient.addItems(arrClient)


    def lockFields(self):
        #self.lineTara.setEnabled(False)
        self.lineTicket.setEnabled(False)
        self.lineKg.setEnabled(False)
        self.linePesoMax.setEnabled(False)
        #self.lineBxP.setEnabled(False)
        self.comboCodigo.setEnabled(False)
        self.comboBoxProd.setEnabled(False)
        #self.comboBoxClient.setEnabled(False)
        #self.lineCantidad.setEnabled(False)
        self.comboBoxProd.setEnabled(False)
        self.comboBoxClient.setEnabled(False)

    def unlockFields(self):
        self.lineTara.setEnabled(True)
        self.lineTicket.setEnabled(True)
        self.lineKg.setEnabled(True)
        self.linePesoMax.setEnabled(True)
        #self.lineBxP.setEnabled(True)
        self.comboCodigo.setEnabled(True)
        self.comboBoxProd.setEnabled(True)
        #self.lineCantidad.setEnabled(True)
        self.comboBoxProd.setEnabled(True)
        #self.comboBoxClient.setEnabled(True)

    def tare(self):
        opRow = self.objmgr.getAnOp(self.lineOp.currentText())
        if len(opRow):
            # Crear proceso de validacion de la tara aqui
            self.objmgr.updateTara()
            taraFloat = self.objmgr.getTara()
            tara = "{:4.2f}".format(taraFloat)
            self.labelTara.setText(tara)
            self.lineTara.setText(tara)
            # Despues de capturar el peso bloqueamos la tara
            self.labelTara.setEnabled(True)
            self.labelNeto.setEnabled(False)
            # Luego bloqueamos el boton tara de esa bobina
        else:
            # 
            self.objmgr.updateTara()
            taraFloat = self.objmgr.getTara()
            tara = "{:4.2f}".format(taraFloat)
            self.labelTara.setText(tara)
            self.lineTara.setText(tara)
            # 
            self.labelTara.setEnabled(True)
            self.labelNeto.setEnabled(False)
            # 

    
    def incRowCount(self):
        self.rowCount = self.rowCount + 1
        self.tablaPesaje.setRowCount(self.rowCount) 

    def palletHasTicket(self):
        op = self.lineOp.currentText()
        cuPallet = self.linePaletaAct.text()
        return len(self.objmgr.countBobinasPalletNew(op,cuPallet)) > 0
    
    """def eventFilter(self, obj, event):
        #print("ENTER PRESIONADO")
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Return:
                self.initWeight()
                return True
        return QtWidgets.QMainWindow.eventFilter(self, obj, event)"""
    

    def keyPressEvent(self,event):
        #print(f"Tipo de evento2: {event.type()}")
        #print(f"Tecla presionada2: {event.key()}")
        #print(f"Texto de la tecla2: {event.text()}")
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            #print("Enter presionado")
            if self.index==0:
                list_vacio = ["empty","empty"]
                self.loginWidget.login()
                #self.login(list_vacio)
        if event.key() == QtCore.Qt.Key_Space:
            #print("Espacio presionado")
            pass
        super().keyPressEvent(event)

    def updateScreenValues(self):
        op = self.lineOp.currentText()
        opRow = self.objmgr.getAnOp(op)
        if len(opRow)>0:
            #print("opRow for update screen=> ",opRow," looking for=> ",op)
            actualPallet = opRow[4] 
            tara_db = opRow[1] 
            self.linePaletaAct.setText(str(actualPallet))
            self.lineTara.setText("{:4.2f}".format(float(tara_db)))
            #result, arrTickets = self.objmgr.getCoilsOnDB()
            result, arrTickets = self.objmgr.getCoilsOPonDB(op)
            coilsForOp = 0
            #coilsForOp = getTheSameCoils(arrTickets,op)
            coilsForOp = self.objmgr.getTheSameCoils(op)
            #print("op=>",op,"\n")
            #print("opRow=>",opRow,"\n")
            #print("actualPallet=>",opRow[4],"\n")
            #print("arrTickets=>",arrTickets,"\n")
            #print("\ncoils for op",coilsForOp,"\n")
            coilsForPallet = 0
            #coilsForPallet = getTheSameCoilsPallet(arrTickets,op,actualPallet)
            coilsForPallet = self.objmgr.getTheSameCoilsPallet(op,actualPallet)
            #print("\ncoils for pallet",coilsForPallet,"\n")
            #print(f"Coils for Pallet: {coilsForPallet}")
            #print(f"Coils for OP: {coilsForOp}")
            pesoBrutoPallet, acumPallet = getTotalsForPallet(coilsForPallet)
            pesoBrutoOp, acumOp = getTotalsForOp(coilsForOp)
            currentCountPallet = 0
            currentCountBobina = 0

            if len(opRow)>0 and result:
                #print("oprow for scree values=> ",opRow)
                totalPallet = int(opRow[2])
                totalBobina = int(opRow[3]) if opRow[3] not in (None, "") else 0 
                #currentCountPallet = countPallets(arrTickets) # check if there is necesari to show the value for tickets or op
                currentCountPallet = int(opRow[4])
                #currentCountBobina = countBobinas(arrTickets,op,currentCountPallet)
                currentCountBobina = len(self.objmgr.countBobinasPalletNew(op,currentCountPallet))
                lastTicketOp = getLastTicketOp(op,arrTickets)
                if lastTicketOp != -1:
                    #print("last Ticket op =>",lastTicketOp)
                    self.labelTicket.setText(str(lastTicketOp))
                    self.labelNBobina.setText(str(currentCountBobina)+"/"+str(totalBobina))
                    self.labelNPaleta.setText(str(currentCountPallet)+"/"+str(totalPallet))              
                    self.labelAcumPaleta.setText("{:4.2f}".format(float(acumPallet)))               
                    self.labelAcumOp.setText("{:4.2f}".format(float(acumOp)))

class PesajeUi(QMainWindow, UiPesoWindow):
    # Heredamos de QMainWindow y de la interfaz

    def __init__(self, objmgr):

        # Llamamos al constructor de la superclase
        super().__init__()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        # Ejecutamos el método setupUi heredado del diseño,
        # gracias al cual se generará la interfaz gráfica
        self.setupUi(self, objmgr)

