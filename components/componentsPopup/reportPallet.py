from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QVBoxLayout,QWidget,QStackedLayout,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets
from components.clasess import Preview
from components.styles.popUp import STYLES_GENERAL

def reportPallet(obj):
    obj.type = "PALLET"
    obj.setWindowTitle("Reporte por paleta")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setText("Reporte por paleta")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.nroOpLbl = QLabel(" N° OP")
    obj.nroOpLbl.setObjectName("_lbl")

    obj.nroOp = QLineEdit()
    obj.nroOp.setObjectName("_input_pallet")

    obj.nroPalletLbl = QLabel(" N° Paleta")
    obj.nroPalletLbl.setObjectName("_lbl")

    obj.nroPallet = QLineEdit()
    obj.nroPallet.setObjectName("_input_pallet")

    obj.tipoPalletLbl = QLabel("Tipo Paleta")
    obj.tipoPalletLbl.setObjectName("_lbl")
    obj.tipoPalletBox = QComboBox()
    obj.tipoPalletBox.setMinimumHeight(40)
    obj.tipoPalletBox.setMinimumWidth(120)
    paletas = obj.nombresPaletas()
    obj.tipoPalletBox.addItems(paletas)
    obj.tipoPalletBox.setCurrentIndex(-1)
    obj.tipoPalletBox.currentTextChanged.connect(obj.setPallet)

    obj.generateBtn = QPushButton("Generar")
    obj.generateBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.generateBtn.clicked.connect(obj.generateAndPrintPallet)

    obj.previewBtn = QPushButton("Previa")
    obj.previewBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.previewBtn.clicked.connect(obj.previewPallet)

    obj.lineForm0 = QHBoxLayout()   
    obj.lineForm1 = QHBoxLayout()
    obj.lineForm2 = QHBoxLayout()

    obj.lineForm0.addWidget(obj.nroOpLbl)
    obj.lineForm0.addWidget(obj.nroOp)

    obj.lineForm1.addWidget(obj.nroPalletLbl)
    obj.lineForm1.addWidget(obj.nroPallet)

    obj.lineForm2.addWidget(obj.tipoPalletLbl)
    obj.lineForm2.addWidget(obj.tipoPalletBox)

    obj.web = Preview(obj)
    #obj.web.setStyleSheet(STYLES_GENERAL)
    obj.web.setFileName("tempHtml.html")
    obj.web.getPreview().loadView()
    obj.web.getPreview().setSize(500,640)
    obj.web.setSize(550,640)
    obj.web.moveToCenter()

    obj.stackedLayout = QStackedLayout()
    obj.firstWidget = QWidget()
    obj.firstLayout = QVBoxLayout()
    obj.firstWidget.setLayout(obj.firstLayout)

    obj.stackedLayout.addWidget(obj.firstWidget)
    obj.stackedLayout.addWidget(obj.web)

    obj.firstLayout.addWidget(obj.title)
    obj.firstLayout.addLayout(obj.lineForm0)
    obj.firstLayout.addLayout(obj.lineForm1)
    obj.firstLayout.addLayout(obj.lineForm2)

    obj.bottomLayout.addWidget(obj.generateBtn)
    obj.bottomLayout.addWidget(obj.previewBtn)
    obj.firstLayout.addLayout(obj.bottomLayout)

    obj.mainLayout.addLayout(obj.stackedLayout)