from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets,QtCore

from components.functions import appendTable,getClientsFromTable,getNamesFromClients,getCodesFromClients
from components.interfaces.pesajeBobina import ExtendedComboBox


def addProduct(obj):
    
    #obj.rowCount = 1
    #obj.columns = 4 # 4 columns on this table
    #obj.items = []
    #obj.products = []

    obj.timer = QtCore.QTimer()

    obj.message = QLabel()
    obj.message.setObjectName("message_product")
    obj.message.hide()

    obj.setWindowTitle("Añadir producto")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(10)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.productNameLbl = QLabel("Nombre de producto")
    obj.productNameLbl.setObjectName("_lbl")

    obj.productName = QLineEdit()
    obj.productName.setObjectName("_combo")

    obj.codeLbl = QLabel("Codigo de producto")
    obj.codeLbl.setObjectName("_lbl")

    obj.code = QLineEdit()
    obj.code.setObjectName("_combo")
    obj.code.textChanged.connect(obj.auto_fill_client)

    obj.pesoMaxLbl = QLabel("Peso maximo por bobina")
    obj.pesoMaxLbl.setObjectName("_lbl")

    obj.pesoMax = QLineEdit()
    obj.pesoMax.setObjectName("_combo")
    obj.pesoMax.setValidator(obj.action.obj.pesajeWidget.validador)

    obj.pesoMinLbl = QLabel("Peso minimo por bobina")
    obj.pesoMinLbl.setObjectName("_lbl")

    obj.pesoMin = QLineEdit()
    obj.pesoMin.setObjectName("_combo")
    obj.pesoMin.setValidator(obj.action.obj.pesajeWidget.validador)

    obj.productDescription = QLineEdit()
    obj.productDescription.setObjectName("_combo")

    obj.productDescriptionLbl = QLabel()
    obj.productDescriptionLbl.setObjectName("_lbl")

    obj.clientNameLbl = QLabel("Nombre de cliente")
    obj.clientNameLbl.setObjectName("_lbl")

    obj.clientName = ExtendedComboBox()
    obj.clientName.setObjectName("_combo")

    obj.okBtn = QPushButton("Guardar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj.saveProduct)

    """obj.modifyBtn = QPushButton("Modificar")
    obj.modifyBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.modifyBtn.clicked.connect(obj.new_modificar_producto)"""

    """obj.deleteBtn = QPushButton("Eliminar")
    obj.deleteBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.deleteBtn.clicked.connect(obj._deleteProduct)"""

    obj.cancelBtn = QPushButton(" Cerrar ")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.formLayout = QFormLayout()
          
    obj.formLayout.addRow(obj.productNameLbl,obj.productName)
    obj.formLayout.addRow(obj.codeLbl,obj.code)
    obj.formLayout.addRow(obj.pesoMaxLbl,obj.pesoMax)
    obj.formLayout.addRow(obj.pesoMinLbl,obj.pesoMin)
    obj.formLayout.addRow(obj.clientNameLbl,obj.clientName)
    obj.formLayout.addRow(obj.message)

    # table
    obj.table = QTableWidget()
    #obj.configureProductTable()
    
    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.formLayout)
    #obj.mainLayout.addWidget(obj.table)

    obj.bottomLayout.addWidget(obj.okBtn)
    #obj.bottomLayout.addWidget(obj.modifyBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    if obj.action.obj.currentUser["nivel"] == "ADMINISTRADOR" or obj.action.obj.currentUser["nivel"] == "SUPERVISOR":
        #obj.bottomLayout.addWidget(obj.deleteBtn)
        pass
    obj.mainLayout.addLayout(obj.bottomLayout)  

    mgrObj = obj.action.obj

    success,clients = mgrObj.getClientsOnDB()

    #obj.loadProducts()
    

    if success:
        obj.names = getNamesFromClients(clients)
        obj.codes = getCodesFromClients(clients)
        obj.names.sort()
        obj.clientName.addItems(obj.names)

    