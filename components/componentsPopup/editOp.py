from PySide6.QtCore import (Qt,QMargins)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets


def editOp(obj):
    obj.setWindowTitle("Editar orden de produccion")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(5)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.opLbl = QLabel("Nro. Op")
    obj.opLbl.setObjectName("_lbl")

    obj.op = QLineEdit()
    obj.op.setObjectName("_edit")

    obj.clientNameLbl = QLabel("Nombre de cliente")
    obj.clientNameLbl.setObjectName("_lbl")

    obj.clientName = QComboBox()
    obj.clientName.setObjectName("_combo")

    obj.productNameLbl = QLabel("Nombre de producto")
    obj.productNameLbl.setObjectName("_lbl")

    obj.productName = QComboBox()
    obj.productName.setObjectName("_combo")

    obj.codeLbl = QLabel("Codigo de producto")
    obj.codeLbl.setObjectName("_lbl")

    obj.code = QComboBox()
    obj.code.setObjectName("_combo")

    obj.maxWeightLbl = QLabel("Peso Max Bobina")
    obj.maxWeightLbl.setObjectName("_lbl")

    obj.weightMax = QLineEdit()
    obj.weightMax.setPlaceholderText("Kg")
    obj.weightMax.setObjectName(obj.name + "_edit")

    obj.palletsLbl = QLabel("Cantidad de paletas")
    obj.palletsLbl.setObjectName("_lbl")

    obj.pallets = QLineEdit()
    obj.pallets.setObjectName("_edit")

    obj.bxPalletsLbl = QLabel("Bobinas por paletas")
    obj.bxPalletsLbl.setObjectName("_lbl")

    obj.bxPallets = QLineEdit()
    obj.bxPallets.setObjectName("_edit")

    obj.okBtn = QPushButton("Eliminar")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj.accept)

    obj.cancelBtn = QPushButton("Cancelar")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.lineForm2 = QHBoxLayout()
    obj.lineForm3 = QHBoxLayout()
    obj.lineForm4 = QHBoxLayout()
    obj.lineForm5 = QHBoxLayout()
    obj.lineForm6 = QHBoxLayout()
    obj.lineForm7 = QHBoxLayout()
    obj.lineForm8 = QHBoxLayout()
    obj.lineForm9 = QHBoxLayout()

    obj.lineForm2.addWidget(obj.opLbl)
    obj.lineForm2.addWidget(obj.op)

    obj.lineForm3.addWidget(obj.clientNameLbl)
    obj.lineForm3.addWidget(obj.clientName)

    obj.lineForm4.addWidget(obj.productNameLbl)
    obj.lineForm4.addWidget(obj.productName)

    obj.lineForm5.addWidget(obj.codeLbl)
    obj.lineForm5.addWidget(obj.code)


    obj.lineForm6.addWidget(obj.maxWeightLbl)
    obj.lineForm6.addWidget(obj.weightMax)

    obj.lineForm7.addWidget(obj.palletsLbl)
    obj.lineForm7.addWidget(obj.pallets)

    obj.lineForm9.addWidget(obj.bxPalletsLbl)
    obj.lineForm9.addWidget(obj.bxPallets)

    obj.mainLayout.addWidget(obj.title)

    obj.mainLayout.addLayout(obj.lineForm2)
    obj.mainLayout.addLayout(obj.lineForm3)
    obj.mainLayout.addLayout(obj.lineForm4)
    obj.mainLayout.addLayout(obj.lineForm5)
    obj.mainLayout.addLayout(obj.lineForm6)
    obj.mainLayout.addLayout(obj.lineForm7)
    obj.mainLayout.addLayout(obj.lineForm9)
    obj.mainLayout.addLayout(obj.lineForm8)


    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    obj.mainLayout.addLayout(obj.bottomLayout) 