from PySide6.QtCore import (Qt,QMargins,QDate)

from PySide6.QtGui import (QCursor)

from PySide6.QtWidgets import (QWidget,QComboBox,QLabel,QLineEdit,QStackedLayout,QPushButton,QTableWidget,QHBoxLayout,QVBoxLayout,QFormLayout)

from components.functions import getNamesFromUsr
from PySide6 import QtWidgets
from datetime import date, datetime
from components.clasess import Preview

def reportOp(obj):
    obj.type = "TURN"
    obj.setWindowTitle("Reporte de produccion")
    obj.bottomLayout = QHBoxLayout()
    
    obj.turno = QComboBox()
    obj.turno.addItems([" 6:00AM-14:15PM "," 14:15PM-22:15PM "," 6:00AM-18:00PM "," 18:00PM-6:00AM "," 22:15PM-6:00AM "])
    obj.turno.addItem("TURNO-COMPLETO")

    obj.title = QLabel("")
    obj.title.setObjectName(obj.name + "_title")
    obj.title.setAlignment(Qt.AlignCenter)

    obj.fromOpLbl = QLabel("Desde")
    obj.fromOpLbl.setObjectName(obj.name + "_lbl")

    dateToday = QDate()
    dateToday.setDate(datetime.now().year,datetime.now().month,datetime.now().day)
    obj.fromOp = QtWidgets.QDateTimeEdit(calendarPopup=True) #QLineEdit()
    obj.fromOp.setDate(dateToday)
    obj.fromOp.setDisplayFormat("yyyy-MM-dd")
    obj.fromOp.setObjectName("_edit") 

    obj.fromTime = QtWidgets.QTimeEdit()
    obj.fromTime.setObjectName("_edit")
    obj.fromTime.setDisplayFormat("hh:mm:ss A")

    obj.toInputOpLbl = QLabel("Hasta")
    obj.toInputOpLbl.setObjectName(obj.name + "_lbl")

    obj.toInputOp = QtWidgets.QDateTimeEdit(calendarPopup=True)
    obj.toInputOp.setDate(dateToday)
    obj.toInputOp.setDisplayFormat("yyyy-MM-dd")
    obj.toInputOp.setObjectName("_edit")

    obj.toTime = QtWidgets.QTimeEdit()
    obj.toTime.setObjectName("_edit")
    obj.toTime.setDisplayFormat("hh:mm:ss A")

    obj.web = Preview(obj)
    #obj.web.setStyleSheet(STYLES_GENERAL)
    obj.web.setFileName("tempHtml.html")
    obj.web.getPreview().loadView()
    obj.web.getPreview().setSize(500,640)
    obj.web.setSize(550,640)
    obj.web.moveToCenter()

    names = []
    try:
        mgrObject = obj.action.obj
        op = mgrObject.getCurrentOp()
        obj.opDate = op
        result,tableUsr = mgrObject.getUsrOnDB()
        obj.users = tableUsr
        if mgrObject.currentUser["nivel"] == "SUPERVISOR" or mgrObject.currentUser["nivel"] == "ADMINISTRADOR":
            names = mgrObject.getUserbylevel("all")
        else:
            names = mgrObject.getUserbylevel("operador")
        #names = getNamesFromUsr(tableUsr)
        print("\nResult getting table from users db:", result,"\ntable:",tableUsr,"\nnames:",names)
    except:
        pass

    obj.from1 = QVBoxLayout()
    obj.from2 = QVBoxLayout()


    obj.operador = QComboBox()
    obj.operador.setObjectName("_combo_op")
    obj.operador.addItems(names)
    if mgrObject.currentUser["nivel"] == "SUPERVISOR" or mgrObject.currentUser["nivel"] == "ADMINISTRADOR":
        obj.operador.addItem("GENERAL")
    else:
        pass
    
    
    obj.generateBtn = QPushButton("Generar")
    obj.generateBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.generateBtn.clicked.connect(obj.generateAndPrintTurn)

    obj.previewBtn = QPushButton("Previa")
    obj.previewBtn.setCursor(QCursor(Qt.PointingHandCursor))
    obj.previewBtn.clicked.connect(obj.previewTurn)

    obj.lineForm1 = QHBoxLayout()
    obj.lineForm1.setAlignment(Qt.AlignCenter)

    obj.lineForm2 = QHBoxLayout()
    obj.lineForm2.setAlignment(Qt.AlignCenter)

    obj.lineForm3 = QHBoxLayout()
    obj.lineForm3.setAlignment(Qt.AlignCenter)

    obj.lineForm1.addWidget(obj.fromOpLbl)
    obj.from1.addWidget(obj.fromOp)
    #obj.from1.addWidget(obj.fromTime)
    obj.lineForm1.addLayout(obj.from1)
    #obj.lineForm1.addWidget(obj.fromOp)
    #obj.lineForm1.addWidget(obj.fromTime)

    obj.lineForm1.addWidget(obj.toInputOpLbl)
    obj.from2.addWidget(obj.toInputOp)
    #obj.from2.addWidget(obj.toTime)
    obj.lineForm1.addLayout(obj.from2)
    #obj.lineForm1.addWidget(obj.toInputOp)
    #obj.lineForm1.addWidget(obj.toTime)


    obj.stackedLayout = QStackedLayout()
    obj.firstWidget = QWidget()
    obj.firstLayout = QVBoxLayout()
    obj.firstLayout.setAlignment(Qt.AlignCenter)
    obj.firstWidget.setLayout(obj.firstLayout)

    obj.stackedLayout.addWidget(obj.firstWidget)
    obj.stackedLayout.addWidget(obj.web)

    obj.lineForm2.addWidget(obj.operador)
    obj.lineForm3.addWidget(obj.turno)
    
    obj.firstLayout.addWidget(obj.title)

    obj.firstLayout.addLayout(obj.lineForm1)
    obj.firstLayout.addLayout(obj.lineForm3)
    obj.firstLayout.addLayout(obj.lineForm2)

    obj.bottomLayout.addWidget(obj.generateBtn)
    obj.bottomLayout.addWidget(obj.previewBtn)
    obj.firstLayout.addLayout(obj.bottomLayout)

    obj.mainLayout.addLayout(obj.stackedLayout)