from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout,QVBoxLayout,QWidget,QStackedLayout)

from PySide6 import QtWidgets
from components.clasess import Preview
from components.functions import getPosByOp,getProductByOp,getAmtByOp

def inputHablador(obj):
    obj.type = "HABLADOR"
    obj.hablador = {}

    obj.setWindowTitle("Hablador")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("Hablador")
    obj.title.setObjectName(obj.name + "_title")
    obj.title.setAlignment(Qt.AlignCenter)
    
    obj.inputOpLbl = QLabel("OP")
    obj.inputOpLbl.setObjectName(obj.name + "_label")
    obj.inputOp = QLineEdit()
    obj.inputOp.setObjectName(obj.name + "_edit")

    obj.inputPosLbl = QLabel("Posicion")
    obj.inputPosLbl.setObjectName(obj.name + "_label")
    obj.inputPos = QLineEdit()
    obj.inputPos.setEnabled(True)
    obj.inputPos.setObjectName(obj.name + "_edit")

    obj.inputAmtLbl = QLabel("Cantidad")
    obj.inputAmtLbl.setObjectName(obj.name + "_label")
    obj.inputAmt = QLineEdit()
    obj.inputAmt.setObjectName(obj.name + "_edit")

    obj.inputObsLbl = QLabel("Observaciones")
    obj.inputObsLbl.setObjectName(obj.name + "_label")
    obj.inputObs = QLineEdit()
    obj.inputObs.setObjectName(obj.name + "_edit")
    obj.inputObs.setEnabled(True)

    obj.unitLbl = QLabel("Kg")
    obj.unitLbl.setObjectName(obj.name + "_label")

    obj.printBtn = QPushButton("Imprimir")
    obj.printBtn.setObjectName(obj.name + "_printBtn")
    obj.printBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.printBtn.clicked.connect(obj.generateAndPrintHabl)


    obj.previewBtn = QPushButton("Previa")
    obj.previewBtn.setObjectName(obj.name + "_printBtn")
    obj.previewBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.previewBtn.clicked.connect(obj.previewHabl)

    obj.cancelBtn = QPushButton("Cancelar")
    obj.cancelBtn.setObjectName(obj.name + "_cancelBtn")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.lineForm1 = QHBoxLayout()
    obj.lineForm1.setAlignment(Qt.AlignCenter)
    obj.lineForm2 = QHBoxLayout()
    obj.lineForm2.setAlignment(Qt.AlignCenter)
    obj.lineForm3 = QHBoxLayout()
    obj.lineForm3.setAlignment(Qt.AlignCenter)
    
    obj.lineForm1.addWidget(obj.inputOpLbl)
    obj.lineForm1.addWidget(obj.inputOp)

    obj.lineForm2.addWidget(obj.inputPosLbl)
    obj.lineForm2.addWidget(obj.inputPos)
    obj.lineForm2.addWidget(obj.inputAmtLbl)
    obj.lineForm2.addWidget(obj.inputAmt)
    obj.lineForm2.addWidget(obj.unitLbl)

    obj.lineForm3.addWidget(obj.inputObsLbl)
    obj.lineForm3.addWidget(obj.inputObs)

    #obj.bottomLayout.addWidget(obj.printBtn)
    #obj.bottomLayout.addWidget(obj.cancelBtn)

    #obj.mainLayout.addWidget(obj.title)
    #obj.mainLayout.addLayout(obj.lineForm1)
    #obj.mainLayout.addLayout(obj.lineForm2)
    #obj.mainLayout.addLayout(obj.lineForm3)
    #obj.mainLayout.addLayout(obj.bottomLayout)

    pesajeObject = obj.action.obj

    mgrObject = pesajeObject.objmgr
    
    if mgrObject.getModePrintHablador() == 1:

        op = pesajeObject.getCurrentOp()

        opRow = mgrObject.getAnOp(op)

        success1,process = mgrObject.getCoilsOnDB()
        success2,products = mgrObject.getProductsOnDB()

        #position = getPosByOp(opRow,op) # position is not the current pallet of 'talker'
        position = obj.inputPos.text() 
        product,productCode = getProductByOp(opRow,products,op)
        cantidad = getAmtByOp(process,op)

        obj.arrHablador = [op,position,product,cantidad]

        print(opRow)
        obj.inputOp.setText(op)
        obj.inputPos.setText(str(position))
        obj.inputAmt.setText(str(cantidad))

        #obj.inputOp.setEnabled(False)
        #obj.inputAmt.setEnabled(False)


    obj.web = Preview(obj)
    #obj.web.setStyleSheet(STYLES_GENERAL)
    obj.web.setFileName("tempHtml.html")
    obj.web.getPreview().loadView()
    obj.web.getPreview().setSize(320,260)
    obj.web.setSize(340,280)
    obj.web.moveToCenter()

    obj.stackedLayout = QStackedLayout()
    obj.firstWidget = QWidget()
    obj.firstLayout = QVBoxLayout()
    obj.firstWidget.setLayout(obj.firstLayout)

    obj.stackedLayout.addWidget(obj.firstWidget)
    obj.stackedLayout.addWidget(obj.web)

    obj.firstLayout.addWidget(obj.title)
    obj.firstLayout.addLayout(obj.lineForm1)
    obj.firstLayout.addLayout(obj.lineForm2)
    obj.firstLayout.addLayout(obj.lineForm3)
    obj.firstLayout.addLayout(obj.bottomLayout)

    obj.bottomLayout.addWidget(obj.printBtn)
    obj.bottomLayout.addWidget(obj.previewBtn)
    obj.firstLayout.addLayout(obj.bottomLayout)

    obj.mainLayout.addLayout(obj.stackedLayout)