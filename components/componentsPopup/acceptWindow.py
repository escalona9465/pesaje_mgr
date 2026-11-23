from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

def acceptWindow(obj):
    obj.setWindowTitle("Confirmacion")
    obj.message = QLabel("")
    obj.message.setAlignment(Qt.AlignCenter)

    obj.okBtn = QPushButton("Aceptar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    
    obj.okBtn.clicked.connect(obj.accept)

    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)
    obj.bottomLayout.addWidget(obj.okBtn)
    
    obj.mainLayout.addWidget(obj.message)
    obj.mainLayout.addWidget(obj.bottomLayout)