from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets,QtCore

from components.functions import appendTable
from components.constants.dataExample import dataExampleAddClient

def addClient(obj):
    obj.rowCount = 1
    obj.columns = 4
    obj.items = []
    obj.clients = []

    obj.timer = QtCore.QTimer()

    obj.setWindowTitle("Añadir/Modificar/Eliminar cliente")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(10)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.clientNameLbl = QLabel("Nombre de cliente")
    obj.clientNameLbl.setObjectName("_lbl")

    obj.clientName = QLineEdit()
    obj.clientName.setObjectName("_combo")

    obj.codeLbl = QLabel("Codigo de cliente")
    obj.codeLbl.setObjectName("_lbl")

    obj.code = QLineEdit()
    obj.code.setObjectName("_combo")

    obj.descriptionLbl = QLabel("Descripcion")
    obj.descriptionLbl.setObjectName("_lbl")

    obj.description = QLineEdit()
    obj.description.setObjectName("_combo")

    obj.message = QLabel()
    obj.message.setObjectName("message_client")
    obj.message.hide()

    obj.okBtn = QPushButton("Guardar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj.saveClient)

    obj.modifyBtn = QPushButton("Modificar")
    obj.modifyBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.modifyBtn.clicked.connect(obj.modifyClient)

    obj.deleteBtn = QPushButton("Eliminar")
    obj.deleteBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.deleteBtn.clicked.connect(obj._deleteClient)

    obj.cancelBtn = QPushButton("Cerrar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.formLayout = QFormLayout()
          
    obj.formLayout.addRow(obj.clientNameLbl,obj.clientName)
    obj.formLayout.addRow(obj.codeLbl,obj.code)
    obj.formLayout.addRow(obj.descriptionLbl,obj.description)
    obj.formLayout.addRow(obj.message) 

    # table
    obj.table = QTableWidget()
    obj.configureClientTable()
    obj.loadClients()
    #obj.rowCount,obj.items,obj.table = appendTable(obj.rowCount,obj.columns,obj.items,obj.table,dataExampleAddClient)
    
    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.formLayout)
    obj.mainLayout.addWidget(obj.table)

    obj.bottomLayout.addWidget(obj.okBtn) 
    obj.bottomLayout.addWidget(obj.modifyBtn) 
    obj.bottomLayout.addWidget(obj.cancelBtn)
    #obj.bottomLayout.addWidget(obj.deleteBtn)

    obj.mainLayout.addLayout(obj.bottomLayout)  