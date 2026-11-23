from components.imports.types import *
from PySide6.QtWidgets import QComboBox, QApplication

class UiProductWindow(object):
    def setupUi(self, Dialog, objmgr):
        self.objmgr = objmgr
        responsive = objmgr.getResponsive()
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1366, 768)
        Dialog.setStyleSheet(STYLES_TYPE_PRODUCT)
        self.frameSelect = QFrame(Dialog)
        self.frameSelect.setObjectName(u"frameSelect")
        self.frameSelect.setGeometry(responsive.qRectScaled(140, 150, 1071, 371))
        
        font = QFont()
        font.setBold(True)

        self.frameSelect.setFont(font)
        self.frameSelect.setFrameShape(QFrame.StyledPanel)
        self.frameSelect.setFrameShadow(QFrame.Raised)

        self.piezasButton = QPushButton(self.frameSelect)
        self.piezasButton.setObjectName(u"piezasButton")
        self.piezasButton.setGeometry(responsive.qRectScaled(560, 120, 341, 181))
        self.piezasButton.setCursor(QCursor(Qt.PointingHandCursor))

        font1 = QFont()
        font1.setPointSize(24)
        font1.setBold(True)

        self.piezasButton.setFont(font1)

        icon = QIcon()
        icon.addFile(u"components/recursos/resma.png", QSize(), QIcon.Normal, QIcon.Off)

        self.piezasButton.setIcon(icon)
        width,height = responsive.sizeScaled(100, 100)
        self.piezasButton.setIconSize(QSize(width,height)) # QSize(100, 100)

        self.label = QLabel(self.frameSelect)
        self.label.setObjectName(u"label")
        self.label.setGeometry(responsive.qRectScaled(390, 50, 321, 41))
        self.label.setFont(font1)

        self.bobinasButton = QPushButton(self.frameSelect)
        self.bobinasButton.setObjectName(u"bobinasButton")
        self.bobinasButton.setGeometry(responsive.qRectScaled(100, 120, 341, 181))
        self.bobinasButton.setCursor(QCursor(Qt.PointingHandCursor))

        font2 = QFont()
        font2.setPointSize(24)
        font2.setBold(True)
        font2.setStyleStrategy(QFont.PreferDefault)

        self.bobinasButton.setFont(font2)

        icon1 = QIcon()
        icon1.addFile(u"components/recursos/bobina.png", QSize(), QIcon.Normal, QIcon.Off)

        self.bobinasButton.setIcon(icon1)
        width,height = responsive.sizeScaled(100, 100)
        self.bobinasButton.setIconSize(QSize(width, height)) # QSize(100, 100)

        self.label_2 = QLabel(self.frameSelect)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(responsive.qRectScaled(10, 10, 131, 31))

        font3 = QFont()
        font3.setPointSize(10)
        font3.setBold(True)
        
        self.label_2.setFont(font3)

        self.bobinasButton.raise_()
        self.piezasButton.raise_()

        self.label.raise_()
        self.label_2.raise_()

        self.frameMgr = QFrame(Dialog)
        self.frameMgr.setObjectName(u"frameMgr")
        self.frameMgr.setGeometry(responsive.qRectScaled(1090, 50, 121, 91))
        self.frameMgr.setFrameShape(QFrame.StyledPanel)
        self.frameMgr.setFrameShadow(QFrame.Raised)

        self.labelUser = QLabel(Dialog)
        #self.labelUser.setText(Dialog)
        self.labelUser.setObjectName(u"labelUser")
        self.labelUser.setGeometry(responsive.qRectScaled(190, 120, 120, 13))
        self.labelUser.setFont(font3)

        self.labelTurno = QLabel(Dialog)
        self.labelTurno.setObjectName(u"labelTurno")
        self.labelTurno.setGeometry(responsive.qRectScaled(320, 118, 120, 20))
        self.labelTurno.setFont(font3)

        self.labelSupervisor = QLabel(Dialog)
        self.labelSupervisor.setText("SUPERVISOR")
        self.labelSupervisor.setObjectName(u"labelSupervisor")
        self.labelSupervisor.setGeometry(responsive.qRectScaled(450, 121, 120, 13))
        self.labelSupervisor.setFont(font3)

        self.comboSupervisor = QComboBox(Dialog)
        self.comboSupervisor.setObjectName(u"comboSupervisor")
        self.comboSupervisor.setGeometry(responsive.qRectScaled(550, 119, 120, 20))
        self.comboSupervisor.setFont(font3)
        self.comboSupervisor.currentIndexChanged.connect(self.updateSupervisor)
        #print("Aca")
        result,self.Supervisores = self.objmgr.dbMGR.getTable("usuarios","supervisor")
        #print(self.Supervisores)
        fixedSupervisores = [i[3]+" "+i[4] for i in self.Supervisores]
        #print(fixedSupervisores)
        #fixedSupervisores = ["Jose Vargas","Sairo Gonzalez","Jhonny Ramayo","Jesus Alvarez","Jose A. Perez"]
        self.comboSupervisor.addItems(fixedSupervisores)

        self.frameIconUser = QFrame(Dialog)
        self.frameIconUser.setObjectName(u"frameIconUser")
        self.frameIconUser.setGeometry(responsive.qRectScaled(140, 110, 41, 31))
        self.frameIconUser.setFrameShape(QFrame.StyledPanel)
        self.frameIconUser.setFrameShadow(QFrame.Raised)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def updateSupervisor(self):
        self.objmgr.setSupervisor( self.comboSupervisor.currentText() )
        pass

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.piezasButton.setText(QCoreApplication.translate("Dialog", u"PIEZAS", None))
        self.piezasButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.piezasButton.clicked.connect(self.goToPiezas)

        self.label.setText(QCoreApplication.translate("Dialog", u"Tipo de Producto", None))
        self.bobinasButton.setText(QCoreApplication.translate("Dialog", u"BOBINAS", None))
        self.bobinasButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.bobinasButton.clicked.connect(self.goToBobinas)

    #if QT_CONFIG(shortcut)
        self.bobinasButton.setShortcut("")
    #endif // QT_CONFIG(shortcut)
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Captura de datos", None))
    # retranslateUi

    def goToPiezas(self):
        self.objmgr.changeView(3)
        self.objmgr.updateWeight(0.0)

    def goToBobinas(self):
        self.objmgr.changeView(2)
        pass

    def setUser(self,user):
        #print(self.labelUser)
        
        self.labelUser.setText(user)
        QApplication.processEvents()
        #print(user)

    def clearUser(self):
        self.labelUser.clear()
        QApplication.processEvents()

    def setTurn(self,turn):
        self.labelTurno.setText(turn)


class ProductUi(QMainWindow, UiProductWindow):
    # Heredamos de QMainWindow y de la interfaz

    def __init__(self, objmgr):

        # Llamamos al constructor de la superclase
        super().__init__()

        # Ejecutamos el método setupUi heredado del diseño,
        # gracias al cual se generará la interfaz gráfica
        self.setupUi(self, objmgr)
