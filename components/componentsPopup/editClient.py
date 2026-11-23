from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

def editClient(obj):
    obj.setWindowTitle("Editar producto")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(0)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.clientNameLbl = QLabel("Nombre de cliente")
    obj.clientNameLbl.setObjectName("_lbl")

    #obj.clientName.setObjectName("op_combo")
    
    obj.clientName = QComboBox()
    obj.clientName.setObjectName("_combo")
    obj.clientName.addItems(["item 1","atem 2","etem 3","ftem 4","gtem 5"])
    obj.clientName.setEditable(False)
    obj.clientName.mouseDoubleClickEvent = obj.clientName.setEditable(True)

    obj.codeLbl = QLabel("Codigo de cliente")
    obj.codeLbl.setObjectName("_lbl")

    obj.code = QLineEdit()

    obj.descriptionLbl = QLabel("Descripcion")
    obj.descriptionLbl.setObjectName("_lbl")

    obj.description = QLineEdit()

    obj.generateBtn = QPushButton("Guardar")
    obj.generateBtn.setCursor(QCursor(Qt.PointingHandCursor))

    obj.cancelBtn = QPushButton("Cancelar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.formLayout = QFormLayout()
    
    obj.formLayout.addRow(obj.clientNameLbl,obj.clientName)
    obj.formLayout.addRow(obj.codeLbl,obj.code)
    obj.formLayout.addRow(obj.descriptionLbl,obj.description)

    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.formLayout)

    obj.bottomLayout.setSpacing(20)
    obj.bottomLayout.addWidget(obj.generateBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    obj.mainLayout.addLayout(obj.bottomLayout)  