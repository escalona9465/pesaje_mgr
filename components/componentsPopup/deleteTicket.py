from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QCheckBox,QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

from components.constants.dataExample import dataExampleAddOp

from components.functions import appendTable

from components.extendedcombobox import ExtendedComboBox

def deleteTicket(obj):
    obj.rowCount = 1
    obj.columns = 8
    obj.items = []
    obj.tickets = []


    obj.setWindowTitle("Eliminar ticket")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(10)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.filtroLbl = QLabel("Buscar por ")
    obj.filtroLbl.setObjectName("_lbl")

    obj.filtroCombo = ExtendedComboBox()
    obj.filtroCombo.addItems(["Número","OP","Paleta","Ficha"])
    obj.filtroCombo.setCurrentIndex(-1)

    obj.valorLbl = QLabel("Filtro")
    obj.valorLbl.setObjectName("_lbl")

    obj.valorLine = QLineEdit()
    obj.valorLine.setObjectName("_edit")
    #obj.valorCombo.currentTextChanged.connect(obj.buscarTickets)

    """obj.oplbl = QLabel("OP:")
    obj.oplbl.setObjectName("_lbl")

    obj.op = QLineEdit()
    obj.op.setObjectName("_edit")

    obj.checkOp = QCheckBox()

    obj.numerolbl = QLabel("Numero de ticket:")
    obj.numerolbl.setObjectName("_lbl")

    obj.numero = QLineEdit()
    obj.numero.setObjectName("_edit")

    obj.checkNumero = QCheckBox()

    obj.paletalbl = QLabel("Paleta:")
    obj.paletalbl.setObjectName("_lbl")

    obj.paleta = QLineEdit()
    obj.paleta.setObjectName("_edit")

    obj.checkPaleta = QCheckBox()

    obj.fichalbl = QLabel("Ficha:")
    obj.fichalbl.setObjectName("_lbl")

    obj.ficha = QLineEdit()
    obj.ficha.setObjectName("_edit")"""

    #obj.checkFicha = QCheckBox()

    """obj.seekBtn = QPushButton("Buscar")
    obj.seekBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.seekBtn.clicked.connect(obj.seekTicket)"""

    obj.botonBuscar = QPushButton("Buscar")
    obj.botonBuscar.setCursor(QCursor(Qt.PointingHandCursor))
    obj.botonBuscar.clicked.connect(obj.buscarTicket)

    obj.okBtn = QPushButton("Eliminar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj.deleteTicket)

    obj.printBtn = QPushButton("Imprimir")
    obj.printBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.printBtn.clicked.connect(lambda:obj.printTicket("reimpresion"))

    obj.cancelBtn = QPushButton("Cerrar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.busquedalayout = QHBoxLayout()
    obj.busquedalayout.addWidget(obj.filtroLbl)
    obj.busquedalayout.addWidget(obj.filtroCombo)
    obj.busquedalayout.addWidget(obj.valorLbl)
    obj.busquedalayout.addWidget(obj.valorLine)
    obj.busquedalayout.addWidget(obj.botonBuscar)

    """obj.formLayout = QFormLayout()

    obj.line1 = QHBoxLayout()
    obj.line1.addWidget(obj.oplbl)
    obj.line1.addWidget(obj.op)
    obj.line1.addWidget(obj.checkOp)

    obj.line1.addWidget(obj.paletalbl)
    obj.line1.addWidget(obj.paleta)
    obj.line1.addWidget(obj.checkPaleta)

    obj.line2 = QHBoxLayout()

    obj.line2.addWidget(obj.numerolbl)
    obj.line2.addWidget(obj.numero)
    obj.line2.addWidget(obj.checkNumero)

    obj.line2.addWidget(obj.fichalbl)
    obj.line2.addWidget(obj.ficha)
    obj.line2.addWidget(obj.checkFicha)

    obj.formLayout.addRow(obj.line1)
    obj.formLayout.addRow(obj.line2)
    obj.formLayout.addRow(obj.seekBtn)"""

    # table
    obj.table = QTableWidget()
    obj.table.setColumnCount(8) # 7 columns
    obj.table.setRowCount(1) # 1 row
    obj.table.clearContents() 
    obj.table.setHorizontalHeaderLabels(["Ticket","Bruto","Neto","Paleta","Bob. Matriz","Fecha","OP","Ficha"])
    
    #dataExample = {"ticket":"23456","bruto":"79.0","neto":"23.0","paleta":"3","bobMatriz":"4","fecha":"19-05-2022","op":"13145678","ficha":"3020"}
    #obj.rowCount,obj.items,obj.table = appendTable(obj.rowCount,obj.columns,obj.items,obj.table,dataExample)
    
    obj.table.setColumnWidth(0,100)
    obj.table.setColumnWidth(1,110)
    obj.table.setColumnWidth(2,160)
    obj.table.setColumnWidth(5,110)
    obj.table.setColumnWidth(6,160)

    headerTable = obj.table.horizontalHeader()   
    headerTable.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    obj.table.setColumnWidth(4,100)
    
    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.busquedalayout)
    obj.mainLayout.addWidget(obj.table)

    obj.bottomLayout.addWidget(obj.printBtn)
    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    obj.mainLayout.addLayout(obj.bottomLayout)  