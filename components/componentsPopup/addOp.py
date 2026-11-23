from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets,QtCore

from components.constants.dataExample import dataExampleAddOp

from components.functions import (appendTable,getProductFromCode,getProductFromName,
    getNamesFromClients,getNamesFromProducts,getCodesFromProducts)

from components.interfaces.pesajeBobina import ExtendedComboBox

def addOp(obj,op=None):
    obj.objmgr = obj.action.obj

    #obj.rowCount = 1
    #obj.columns = 5
    #obj.items = []
    #obj.ops = []
    obj.arrOp = []

    obj.timer = QtCore.QTimer()

    obj.message = QLabel()
    obj.message.setObjectName("message_product")
    obj.message.hide()

    obj.setWindowTitle("Añadir orden de produccion")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(10)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.opLbl = QLabel("Nro. Op")
    obj.opLbl.setObjectName("_lbl")

    obj.op = QLineEdit()
    obj.op.setObjectName("_edit")
    obj.op.setText(op)

    obj.productNameLbl = QLabel("Nombre de producto")
    obj.productNameLbl.setObjectName("_lbl")

    obj.productName = ExtendedComboBox()
    obj.productName.setObjectName("_combo")
    obj.productName.currentTextChanged.connect(obj.updateFieldsByProduct)
    obj.productName.currentIndexChanged.connect(obj.updateFieldsByProduct)

    obj.codeLbl = QLabel("Codigo de producto")
    obj.codeLbl.setObjectName("_lbl")

    obj.code = ExtendedComboBox()
    #obj.code.setEnabled(False)
    obj.code.setObjectName("_combo")
    #obj.code.setDisabled(True)

    obj.palletsLbl = QLabel("Cantidad de paletas")
    obj.palletsLbl.setObjectName("_lbl")

    obj.pallets = QLineEdit()
    obj.pallets.setObjectName("_edit")

    obj.pallets = QLineEdit()
    obj.pallets.setObjectName("_edit")

    obj.bxPalletsLbl = QLabel("Bobinas por paletas")
    obj.bxPalletsLbl.setObjectName("_lbl")

    obj.bxPallets = QLineEdit()
    obj.bxPallets.setObjectName("_edit")

    obj.tara = QLineEdit()
    obj.tara.setObjectName("_edit")
    obj.tara.setPlaceholderText("0.00")
    obj.tara.textChanged.connect(obj.tareFromLine)
    
    obj.currentTara = 0.00

    obj.taraLbl = QLabel("Tara")
    obj.taraLbl.setObjectName("_lbl")

    obj.okBtn = QPushButton("Guardar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj.saveOp)

    obj.modificarBtn = QPushButton("Modificar")
    obj.modificarBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.modificarBtn.clicked.connect(obj._modifyOp)

    obj.eliminarBtn = QPushButton("Eliminar")
    obj.eliminarBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.eliminarBtn.clicked.connect(obj._deleteOp)

    obj.cancelBtn = QPushButton("Cerrar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.formLayout = QFormLayout()

    obj.formLayout.addRow(obj.message)
    obj.formLayout.addRow(obj.opLbl,obj.op)    
    obj.formLayout.addRow(obj.taraLbl,obj.tara)         
    obj.formLayout.addRow(obj.productNameLbl,obj.productName)
    obj.formLayout.addRow(obj.codeLbl,obj.code)
    obj.formLayout.addRow(obj.palletsLbl,obj.pallets)
    obj.formLayout.addRow(obj.bxPalletsLbl,obj.bxPallets)
       
    # Table
    obj.table = QTableWidget()
    obj.table.cellChanged.connect(obj.onOpCellChanged)
    obj.configureOpTable()
    
    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.formLayout)
    obj.mainLayout.addWidget(obj.table)

    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.modificarBtn)
    obj.bottomLayout.addWidget(obj.eliminarBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    obj.mainLayout.addLayout(obj.bottomLayout)  

    #successProducts,products = obj.objmgr.getProductsOnDB()
    productos = obj.objmgr.getproductos_by("codigo_producto,producto","ALL")
    codigo_productos = [i[0] for i in productos]
    nombre_productos = [i[1] for i in productos]
    #print(nombre_productos)
    #print(codigo_productos)
    codigo_productos.sort()
    nombre_productos.sort()
    obj.productName.addItems(nombre_productos)
    obj.code.addItems(codigo_productos)
    
    obj.loadOps()

    """if successProducts:
        nameProducts = getNamesFromProducts(products)
        codes = getCodesFromProducts(products)
        nameProducts.sort()
        obj.productName.addItems(nameProducts)
        codes.sort()
        obj.code.addItems(codes)"""

    

