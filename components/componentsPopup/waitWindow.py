from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

from PySide6 import QtCore

def waitWindow(obj):
    obj.setWindowTitle("Por favor espere...")

    obj.message = QLabel("")
    obj.message.setAlignment(Qt.AlignCenter)

    obj.message.setObjectName(obj.name + "_message")
    obj.mainLayout.addWidget(obj.message)

    QtCore.QTimer.singleShot(1000, obj.close)