from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets,QtCore

def inputMatriz(obj):
    obj.loop = QtCore.QEventLoop()

    obj.setWindowTitle("Bobina matriz")
    obj.bobinaMatriz = 0
    obj.okBtn = QPushButton("Aceptar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn = QPushButton("Cancelar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.setObjectName(obj.name + "_okBtn")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.setObjectName(obj.name + "_cancelBtn")
    
    obj.okBtn.clicked.connect(obj.accept)
    obj.cancelBtn.clicked.connect(obj.close)

    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.centerLayout = QHBoxLayout()
    obj.centerLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.centerLayout.setSpacing(0)
    obj.centerLayout.setAlignment(Qt.AlignCenter)

    obj.input = QLineEdit()
    obj.input.setObjectName(obj.name + "_input")

    obj.message = QLabel("")
    obj.message.setAlignment(Qt.AlignCenter)
    obj.message.setObjectName(obj.name + "_message")

    obj.mainLayout.addWidget(obj.message)

    obj.centerLayout.addWidget(obj.input)

    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)

    obj.mainLayout.addLayout(obj.centerLayout)
    obj.mainLayout.addLayout(obj.bottomLayout)