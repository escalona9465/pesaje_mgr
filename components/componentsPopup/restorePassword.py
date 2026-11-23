from PySide6 import QtCore
from PySide6.QtGui import (QCursor)
from PySide6.QtCore import (Qt,QMargins)
from PySide6.QtWidgets import (QComboBox,QLabel,QLineEdit,QPushButton,QTableWidget,QHBoxLayout,QFormLayout)

from PySide6 import QtWidgets

from components.functions import appendTable,getClientsFromTable,getNamesFromClients


def restorePassword(obj):
    
    obj.rowCount = 1
    obj.columns = 4 # 4 columns on this table
    obj.items = []

    obj.timer = QtCore.QTimer()

    obj.setWindowTitle("Cambiar contraseña")
    obj.bottomLayout = QHBoxLayout()
    obj.bottomLayout.setContentsMargins(QMargins(0,0,0,0))
    obj.bottomLayout.setSpacing(10)
    obj.bottomLayout.setAlignment(Qt.AlignCenter)

    obj.title = QLabel("")
    obj.title.setObjectName("_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.titleSuper = QLabel("superusuario")

    obj.superUserLbl = QLabel("Usuario")
    obj.superUserLbl.setObjectName("_lbl")

    obj.superUser = QLineEdit()
    obj.superUser.setObjectName("_combo")

    obj.superPassLbl = QLabel("Contraseña")
    obj.superPassLbl.setObjectName("_lbl")

    obj.titleUser = QLabel("Usuario")

    obj.superPass = QLineEdit()
    obj.superPass.setEchoMode(QLineEdit.Password)
    obj.superPass.setObjectName("_combo")

    obj.userLbl = QLabel("Usuario")
    obj.userLbl.setObjectName("_lbl")

    obj.user = QLineEdit()
    obj.user.setObjectName("_combo")

    obj.passwordLbl = QLabel("Contraseña")
    obj.passwordLbl.setObjectName("_lbl")

    obj.password = QLineEdit()
    obj.password.setEchoMode(QLineEdit.Password)
    obj.password.setObjectName("_combo")

    obj.confirmPasswordLbl = QLabel("Confirmar contraseña")
    obj.confirmPasswordLbl.setObjectName("_lbl")

    obj.confirmPassword = QLineEdit()
    obj.confirmPassword.setEchoMode(QLineEdit.Password)
    obj.confirmPassword.setObjectName("_combo")

    obj.message = QLabel()
    obj.message.setObjectName("message_restore")
    obj.message.hide()

    obj.okBtn = QPushButton("Restablecer")
    obj.okBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.okBtn.clicked.connect(obj._restorePassword)

    obj.cancelBtn = QPushButton(" Cerrar ")
    obj.cancelBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.cancelBtn.clicked.connect(obj.close)

    obj.formLayout = QFormLayout()

    obj.formLayout.addRow(obj.titleSuper)          
    obj.formLayout.addRow(obj.superUserLbl,obj.superUser)
    obj.formLayout.addRow(obj.superPassLbl,obj.superPass)
    obj.formLayout.addRow(obj.titleUser)    
    obj.formLayout.addRow(obj.userLbl,obj.user)
    obj.formLayout.addRow(obj.passwordLbl,obj.password)
    obj.formLayout.addRow(obj.confirmPasswordLbl,obj.confirmPassword)
    obj.formLayout.addRow(obj.message) 

    obj.mainLayout.addWidget(obj.title)
    obj.mainLayout.addLayout(obj.formLayout)

    obj.bottomLayout.addWidget(obj.okBtn)
    obj.bottomLayout.addWidget(obj.cancelBtn)
    obj.mainLayout.addLayout(obj.bottomLayout)  

    mgrObj = obj.action.obj

    result,products = mgrObj.getProductsOnDB()

    success,clients = mgrObj.getClientsOnDB()

    