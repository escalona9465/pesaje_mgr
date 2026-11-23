from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout,
    QStackedLayout,QWidget,QVBoxLayout)

from PySide6 import QtWidgets
from components.clasess import Preview

def reportPieza(obj):
    obj.type = "PLEGADIZO"
    obj.setWindowTitle("Reporte de piezas")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setText("Reporte de producto plegadizo")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.nroOpLbl = QLabel(" N° OP")
    obj.nroOpLbl.setObjectName("_lbl")

    obj.nroOp = QLineEdit()
    obj.nroOp.setObjectName("_input_pallet")

    obj.nroCajaLbl = QLabel(" N° Caja")
    obj.nroCajaLbl.setObjectName("_lbl")

    obj.nroCaja = QLineEdit()
    obj.nroCaja.setObjectName("_input_pallet")

    obj.generateBtn = QPushButton("Generar")
    obj.generateBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.generateBtn.clicked.connect(obj.generateAndPrintPlegadizo)

    obj.previewBtn = QPushButton("Previa")
    obj.previewBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.previewBtn.clicked.connect(obj.previewPlegadizo)

    obj.lineForm0 = QHBoxLayout()   
    obj.lineForm1 = QHBoxLayout()

    obj.lineForm0.addWidget(obj.nroOpLbl)
    obj.lineForm0.addWidget(obj.nroOp)

    obj.lineForm1.addWidget(obj.nroCajaLbl)
    obj.lineForm1.addWidget(obj.nroCaja)

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

    obj.bottomLayout.addWidget(obj.generateBtn)
    obj.bottomLayout.addWidget(obj.previewBtn)
    obj.firstLayout.addLayout(obj.bottomLayout)

    obj.mainLayout.addLayout(obj.stackedLayout)