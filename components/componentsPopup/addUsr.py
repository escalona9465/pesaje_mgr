from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets,QtCore

from components.constants.dataExample import dataExampleAddOp

from components.functions import appendTable

def addUsr(obj):
    obj.rowCount = 1
    obj.columns = 7
    obj.items = []

    obj.timer = QtCore.QTimer()

    obj.message = QLabel()
    obj.message.setObjectName("message_product")
    obj.message.hide()

    obj.setWindowTitle("Añadir usuario")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(10)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.namelbl = QLabel("Nombre:")
    obj.namelbl.setObjectName("_lbl")

    obj.name= QLineEdit()
    obj.name.setObjectName("_edit")

    obj.lastNamelbl = QLabel("Apellido:")
    obj.lastNamelbl.setObjectName("_lbl")

    obj.lastName = QLineEdit()
    obj.lastName.setObjectName("_edit")

    obj.cedulalbl = QLabel("Cedula:")
    obj.cedulalbl.setObjectName("_lbl")

    obj.cedula = QLineEdit()
    obj.cedula.setObjectName("_edit")

    obj.usrlbl = QLabel("Usuario:")
    obj.usrlbl.setObjectName("_lbl")

    obj.usr = QLineEdit()
    obj.usr.setObjectName("_edit")

    obj.fichalbl = QLabel("Ficha:")
    obj.fichalbl.setObjectName("_lbl")

    obj.ficha = QLineEdit()
    obj.ficha.setObjectName("_edit")

    obj.passWordlbl = QLabel("Contraseña:")
    obj.passWordlbl.setObjectName("_lbl")

    obj.passWord = QLineEdit()
    obj.passWord.setEchoMode(QLineEdit.Password)
    obj.passWord.setObjectName("_edit")

    obj.confirmPassWordlbl = QLabel("Confirmar:")
    obj.confirmPassWordlbl.setObjectName("_lbl")

    obj.confirmPassWord = QLineEdit()
    obj.confirmPassWord.setEchoMode(QLineEdit.Password)
    obj.confirmPassWord.setObjectName("_edit")

    obj.emaillbl = QLabel("Correo:")
    obj.emaillbl.setObjectName("_lbl")

    obj.email = QLineEdit()
    obj.email.setObjectName("_edit")

    obj.levellbl = QLabel("Nivel:")
    obj.levellbl.setObjectName("_lbl")

    obj.level = QComboBox()
    obj.level.addItems(["ADMINISTRADOR","OPERADOR","SUPERVISOR"])
    obj.level.setObjectName("_combo")

    obj.turnlbl = QLabel("Turno:")
    obj.turnlbl.setObjectName("_lbl")

    obj.turn = QComboBox()
    obj.turn.addItems(["PRIMER TURNO","SEGUNDO TURNO","TERCER TURNO"])
    obj.turn.setObjectName("_combo")

    obj.okBtn = QPushButton("Guardar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj.saveUsr)

    obj.cancelBtn = QPushButton("Cancelar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.formLayout = QFormLayout()

    obj.line1 = QHBoxLayout()
    obj.line1.addWidget(obj.namelbl)
    obj.line1.addWidget(obj.name)
    obj.line1.addWidget(obj.lastNamelbl)
    obj.line1.addWidget(obj.lastName)

    #obj.formLayout.addRow(obj.namelbl,obj.name)            
    #obj.formLayout.addRow(obj.lastNamelbl,obj.lastName)
    obj.formLayout.addRow(obj.message)
    obj.formLayout.addRow(obj.line1)

    obj.line2 = QHBoxLayout()
    obj.line2.addWidget(obj.cedulalbl)
    obj.line2.addWidget(obj.cedula)
    obj.line2.addWidget(obj.usrlbl)
    obj.line2.addWidget(obj.usr)

    #obj.formLayout.addRow(obj.cedulalbl,obj.cedula)
    #obj.formLayout.addRow(obj.usrlbl,obj.usr)
    obj.formLayout.addRow(obj.line2)

    obj.line3 = QHBoxLayout()
    obj.line3.addWidget(obj.fichalbl)
    obj.line3.addWidget(obj.ficha)
    obj.line3.addWidget(obj.emaillbl)
    obj.line3.addWidget(obj.email)

    #obj.formLayout.addRow(obj.fichalbl,obj.ficha)
    #obj.formLayout.addRow(obj.emaillbl,obj.email)
    obj.formLayout.addRow(obj.line3)

    obj.line4 = QHBoxLayout()
    obj.line4.addWidget(obj.levellbl)
    obj.line4.addWidget(obj.level)
    obj.line4.addWidget(obj.turnlbl)
    obj.line4.addWidget(obj.turn)

    #obj.formLayout.addRow(obj.levellbl,obj.level)
    #obj.formLayout.addRow(obj.turnlbl,obj.turn)
    obj.formLayout.addRow(obj.line4)

    obj.line5 = QHBoxLayout()
    obj.line5.addWidget(obj.passWordlbl)
    obj.line5.addWidget(obj.passWord)
    obj.line5.addWidget(obj.confirmPassWordlbl)
    obj.line5.addWidget(obj.confirmPassWord)

    #obj.formLayout.addRow(obj.passWordlbl,obj.passWord)
    #obj.formLayout.addRow(obj.confirmPassWordlbl,obj.confirmPassWord)
    obj.formLayout.addRow(obj.line5)

    # table
    obj.table = QTableWidget()
    obj.table.setColumnCount(7) # 7 columns
    obj.table.setRowCount(1) # 1 row
    obj.table.clearContents() 
    obj.table.setHorizontalHeaderLabels(["Id","Cedula","Usuario","Nombre","Apellido","Ficha","email","nivel","turno"])
    
    #obj.rowCount,obj.items,obj.table = appendTable(obj.rowCount,obj.columns,obj.items,obj.table,dataExampleAddUsr)
    
    obj.table.setColumnWidth(0,100)
    obj.table.setColumnWidth(1,110)
    obj.table.setColumnWidth(2,160)
    obj.table.setColumnWidth(5,110)
    obj.table.setColumnWidth(6,160)

    headerTable = obj.table.horizontalHeader()   
    headerTable.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    obj.table.setColumnWidth(4,100)
    
    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.formLayout)
    obj.mainLayout.addWidget(obj.table)

    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    obj.mainLayout.addLayout(obj.bottomLayout)  