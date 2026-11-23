from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

def inputWindow(obj):
    obj.setWindowTitle("")
    obj.input = QLineEdit()

    obj.message = QLabel("")
    obj.message.setAlignment(Qt.AlignCenter)

    obj.mainLayout.addWidget(obj.message)
    obj.mainLayout.addWidget(obj.input)