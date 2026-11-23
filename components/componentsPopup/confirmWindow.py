from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)
from PySide6 import QtCore
from PySide6 import QtWidgets

def confirmWindow(obj):
    obj.loop = QtCore.QEventLoop()

    obj.setWindowTitle("Confirmacion")
    obj.accepted = False

    obj.message = QLabel("")
    obj.message.setAlignment(Qt.AlignCenter)

    obj.message.setObjectName(obj.name + "_message")

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
    
    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    
    obj.mainLayout.addWidget(obj.message)
    obj.mainLayout.addLayout(obj.bottomLayout)


    