from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

def inputOrder(obj):
    obj.setWindowTitle("Reportes de produccion")
    obj.message = QLabel("")
    obj.message.setObjectName(obj.name + "_message")
    obj.message.setAlignment(Qt.AlignCenter)
    
    obj.inputOpLbl = QLabel("OP")
    obj.inputOpLbl.setObjectName(obj.name + "_oplbl")
    obj.inputOpLbl.setAlignment(Qt.AlignCenter)

    obj.inputOp = QLineEdit()
    obj.inputOp.setObjectName(obj.name + "_op")

    obj.generalBtn = QPushButton("General")
    obj.generalBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.generalBtn.clicked.connect(obj.generalClicked)

    obj.detailedBtn = QPushButton("Detallado")
    obj.detailedBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.detailedBtn.clicked.connect(obj.detailedClicked)

    obj.lineForm1 = QHBoxLayout()
    obj.lineForm1.setAlignment(Qt.AlignCenter)
    obj.lineForm1.addWidget(obj.inputOpLbl)
    obj.lineForm1.addWidget(obj.inputOp)

    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)

    obj.bottomLayout.addWidget(obj.generalBtn)
    obj.bottomLayout.addWidget(obj.detailedBtn)

    obj.mainLayout.addWidget(obj.message) 
    obj.mainLayout.addLayout(obj.lineForm1)
    obj.mainLayout.addLayout(obj.bottomLayout)