from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets
    

def reportTicket(obj):
    obj.setWindowTitle("Reporte de ticket")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setText("Reporte de ticket")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.nroOpLbl = QLabel(" N° OP")
    obj.nroOpLbl.setObjectName("_lbl")

    obj.nroOp = QLineEdit()
    obj.nroOp.setObjectName("_input")

    obj.nroPalletLbl = QLabel(" N° Ticket")
    obj.nroPalletLbl.setObjectName("_lbl")

    obj.nroPallet = QLineEdit()
    obj.nroPallet.setObjectName("_input")

    obj.generateBtn = QPushButton("Generar")
    obj.generateBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.generateBtn.clicked.connect(obj.generate)
    
    obj.lineForm1 = QHBoxLayout()
    obj.lineForm0 = QHBoxLayout()

    obj.lineForm1.addWidget(obj.nroOpLbl)
    obj.lineForm1.addWidget(obj.nroOp)

    obj.lineForm1.addWidget(obj.nroPalletLbl)
    obj.lineForm1.addWidget(obj.nroPallet)

    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.lineForm1)

    obj.bottomLayout.addWidget(obj.generateBtn)
    obj.mainLayout.addLayout(obj.bottomLayout)