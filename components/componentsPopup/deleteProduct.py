from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

def deleteProduct(obj):
    obj.setWindowTitle("Eliminar producto")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(5)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.productNameLbl = QLabel("Nombre de producto")
    obj.productNameLbl.setObjectName("_lbl")

    obj.productName = QComboBox()
    obj.productName.setEditable(True)
    obj.productName.setObjectName(obj.name + "_combo")

    obj.spacer = QLabel("")

    obj.okBtn = QPushButton("Eliminar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj.accept)

    obj.cancelBtn = QPushButton("Cancelar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.lineForm1 = QHBoxLayout()
    obj.lineForm2 = QHBoxLayout()
    
    obj.lineForm1.addWidget(obj.productNameLbl)
    obj.lineForm1.addWidget(obj.productName)

    obj.lineForm2.addWidget(obj.spacer)

    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.lineForm1)
    obj.mainLayout.addLayout(obj.lineForm2)

    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    obj.mainLayout.addLayout(obj.bottomLayout) 