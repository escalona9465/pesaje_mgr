
from components.functions import getModeMeasure,convertModeMeasure
from components.imports.config import *
from components.printer import Printer

class UiConfigWindow(object):
    def setupUi(self, pesoWindow, objmgr):
        self.objmgr = objmgr
        responsive = objmgr.getResponsive()
        if not pesoWindow.objectName():
            pesoWindow.setObjectName(u"pesoWindow")
        width,height = responsive.sizeScaled(1366, 780) 
        pesoWindow.resize(1366, 780) # 1366, 780
        icon = QIcon()
        icon.addFile(u"components/recursos/balanza.png", QSize(), QIcon.Normal, QIcon.Off)
        pesoWindow.setWindowIcon(icon)
        pesoWindow.setStyleSheet(CONFIG_STYLES)

        self.initConfig = self.objmgr.getConfigOnDB()
        self.init_modeB1 = self.initConfig[9]
        self.init_modeB2 = self.initConfig[10]
        print("init config result=>",self.initConfig)
        # Auxiliary attributes

        self.centralwidget = QWidget(pesoWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.frameForm = QFrame(self.centralwidget)
        self.frameForm.setObjectName(u"frameDatos")
        self.frameForm.setGeometry(responsive.qRectScaled(40, 25, 1290, 700)) # QRect(40, 25, 1290, 700)
        self.frameForm.setFrameShape(QFrame.StyledPanel)
        self.frameForm.setFrameShadow(QFrame.Raised)

        self.titleForm = QLabel(self.frameForm)
        self.titleForm.setObjectName(u"titleForm")
        self.titleForm.setText("Configuracion")
        self.titleForm.setGeometry(responsive.qRectScaled(500, 20, 260, 80)) # QRect(500, 20, 260, 80)

        self.titleGen = QLabel(self.frameForm)
        self.titleGen.setText("Generales")
        self.titleGen.setGeometry(responsive.qRectScaled(580, 120, 180, 30)) # QRect(580, 120, 180, 30)

        self.formWidgetGeneral = QWidget(self.frameForm)
        self.formWidgetGeneral.setObjectName("formWidget")
        self.formWidgetGeneral.setGeometry(responsive.qRectScaled(430,150,415,440)) # QRect(430,150,415,440)
        self.formGeneral = QFormLayout()
        self.formWidgetGeneral.setLayout(self.formGeneral)

        self.omitirOpDigits = QCheckBox()

        self.omitirMaxTara = QCheckBox()

        self.maxTara = QLineEdit()

        self.mode = QComboBox()
        self.mode.addItem("Manual")
        self.mode.addItem("Servidor")
        self.mode.addItem("Cobertura")

        self.modeAdobe = QCheckBox()
        self.pathAdobe = QLineEdit()
        
        self.backupPath = QLineEdit() 
        
        self.formGeneral.addRow(QLabel("Balanzas"))
        self.formGeneral.addRow("Omitir Op 131-134:",self.omitirOpDigits)
        self.formGeneral.addRow("Omitir error de Tara:",self.omitirMaxTara)
        self.formGeneral.addRow("Maxima tara [kg]:",self.maxTara)
        self.formGeneral.addRow("Fuente de datos:",self.mode)
        self.formGeneral.addRow("Usar adobe:",self.modeAdobe)
        self.formGeneral.addRow("Ruta de adobe:",self.pathAdobe)
        self.formGeneral.addRow("Ruta de respaldo:",self.backupPath)

        self.formGeneral.addRow(QLabel("Impresoras"))

        self.avalaiblePrinters = []

        p = Printer()
        self.avalaiblePrinters = p.getPrinters()

        self.comboPrinters = QComboBox()
        self.comboPrinters.addItems(self.avalaiblePrinters)
        self.formGeneral.addRow("Modelo:",self.comboPrinters)
        self.formGeneral.addRow(QLabel("Etiquetadora"))

        self.comboTickers = QComboBox()
        self.comboTickers.addItems(self.avalaiblePrinters)
        self.comboTickers.addItem("ZDesigner TLP 2844")
        self.formGeneral.addRow("Modelo:",self.comboTickers)

        #self.titleGen.setGeometry(QRect(220, 120, 180, 30))
        #self.formWidgetGeneral.setGeometry(QRect(100,150,300,440))
        self.titleServer = QLabel(self.frameForm)
        self.titleServer.setText("Servidor")
        self.titleServer.setGeometry(responsive.qRectScaled(200, 120, 180, 30)) # QRect(200, 120, 180, 30)

        self.avalaiblePorts = getallPorts()
        self.formWidgetServer = QWidget(self.frameForm)
        self.formWidgetServer.setObjectName("formWidget")
        self.formWidgetServer.setGeometry(responsive.qRectScaled(100,150,300,150)) # QRect(100,150,300,150)
        self.formServer = QFormLayout()
        self.formWidgetServer.setLayout(self.formServer)
        self.serverIp = QLineEdit()
        self.serverPort = QLineEdit()
        self.userServer = QLineEdit()
        self.passServer = QLineEdit()
        self.formServer.addRow(" Ip: ",self.serverIp)
        self.formServer.addRow(" Puerto: ",self.serverPort)
        self.formServer.addRow(" Usuario: ",self.userServer)
        self.formServer.addRow(" Contraseña: ",self.passServer)

        self.titleDB = QLabel(self.frameForm)
        self.titleDB.setText("Base de datos")
        self.titleDB.setGeometry(responsive.qRectScaled(220, 400, 180, 30)) # QRect(220, 400, 180, 30)

        self.formWidgetDB = QWidget(self.frameForm)
        self.formWidgetDB.setObjectName("formWidget")
        self.formWidgetDB.setGeometry(responsive.qRectScaled(100,430,300,150)) # QRect(100,430,300,150)
        self.formDB = QFormLayout()
        self.formWidgetDB.setLayout(self.formDB)
        self.ipDB = QLineEdit()
        self.portDB = QLineEdit()
        self.userDB = QLineEdit()
        self.passDB = QLineEdit()
        self.formDB.addRow(" Ip: ",self.ipDB)
        self.formDB.addRow(" Puerto: ",self.portDB)
        self.formDB.addRow(" Usuario: ",self.userDB)
        self.formDB.addRow(" Contraseña: ",self.passDB)

        self.titleBalanza1 = QLabel(self.frameForm)
        self.titleBalanza1.setText("Balanza 1")
        self.titleBalanza1.setGeometry(responsive.qRectScaled(980, 120, 180, 30)) # QRect(980, 120, 180, 30)

        self.formWidgetB1 = QWidget(self.frameForm)
        self.formWidgetB1.setObjectName("formWidget")
        self.formWidgetB1.setGeometry(responsive.qRectScaled(875,150,300,150)) # QRect(875,150,300,150)
        self.formB1 = QFormLayout()
        self.formWidgetB1.setLayout(self.formB1)
        self.portB1 = QComboBox()
        self.modeB1 = QComboBox()
        self.modeB1.addItems(["Continuo MT BBA231C","Continuo ohaus T21P","GNT Ohaus T21P","Directo"])
        currentModeB1 = convertModeMeasure(self.init_modeB1)
        self.modeB1.setCurrentText(currentModeB1)
        self.portB1.addItems(self.avalaiblePorts)
        #print(self.avalaiblePorts)
        for port in self.avalaiblePorts:
            if port.startswith(self.initConfig[7]):
                self.portB1.setCurrentText(self.initConfig[7])
                print(f"Fijando balanza 1 a: {self.initConfig[7]}")
        #self.portB1.se
        self.formB1.addRow(" Puerto 1: ",self.portB1)
        self.formB1.addRow(" Modo: ",self.modeB1)
        self.titleBalanza2 = QLabel(self.frameForm)
        self.titleBalanza2.setText("Balanza 2")
        self.titleBalanza2.setGeometry(responsive.qRectScaled(980, 400, 180, 30)) # QRect(980, 400, 180, 30)        

        self.formWidgetB2 = QWidget(self.frameForm)
        self.formWidgetB2.setObjectName("formWidget")
        self.formWidgetB2.setGeometry(responsive.qRectScaled(875,430,300,150)) # QRect(875,430,300,150)
        self.formB2 = QFormLayout()
        self.formWidgetB2.setLayout(self.formB2)
        self.portB2 = QComboBox()
        self.modeB2 = QComboBox()
        self.modeB2.addItems(["Continuo MT BBA231C","Continuo ohaus T21P","GNT Ohaus T21P","Directo"])
        currentModeB2 = convertModeMeasure(self.init_modeB2)
        self.modeB2.setCurrentText(currentModeB2)
        self.portB2.addItems(self.avalaiblePorts)
        for port in self.avalaiblePorts:
            if port.startswith(self.initConfig[8]):
                self.portB1.setCurrentText(self.initConfig[8])
                print(f"Fijando balanza 2 a: {self.initConfig[8]}")
        self.formB2.addRow(" Puerto 2: ",self.portB2)
        self.formB2.addRow(" Modo: ",self.modeB2)

        print("modeB1:",currentModeB1," modeB2:",currentModeB2)
        self.btnRegresar = QPushButton(self.frameForm)
        self.btnRegresar.setGeometry(responsive.qRectScaled(470, 610, 130, 40)) # QRect(470, 610, 130, 40)
        self.btnRegresar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnRegresar.setObjectName(u"btnRegresar")
        self.btnRegresar.clicked.connect(self.returnToTypeProduct)
        self.btnRegresar.setText("Regresar")

        self.btnGuardar = QPushButton(self.frameForm)
        self.btnGuardar.setGeometry(responsive.qRectScaled(670, 610, 130, 40)) # QRect(670, 610, 130, 40)
        self.btnGuardar.setCursor(QCursor(Qt.PointingHandCursor))
        self.btnGuardar.setObjectName(u"btnRegresar")
        self.btnGuardar.clicked.connect(self.saveFields)
        self.btnGuardar.setText("Guardar")

        pesoWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(pesoWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(responsive.qRectScaled(0, 0, 1366, 22)) # QRect(0, 0, 1366, 22)

        pesoWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(pesoWindow)
        self.statusbar.setObjectName(u"statusbar")

        pesoWindow.setStatusBar(self.statusbar)

        self.retranslateUi(pesoWindow)

        self.alert = Alert(self.frameForm,"")
        self.alert.setLocation(responsive.qRectScaled(200, 80, 840, 25)) # QRect(200, 80, 840, 25)

        QMetaObject.connectSlotsByName(pesoWindow)
    # setupUi

    def retranslateUi(self, pesoWindow):
        pesoWindow.setWindowTitle(QCoreApplication.translate(u"pesoWindow", u"MainWindow", None))

    def returnToTypeProduct(self):
        self.objmgr.changeView(1)
        pass

    def saveModePorts(self):
        modeB1 = self.modeB1.currentText()
        modeB2 = self.modeB2.currentText()
        #print("storing on mgrObject b1=>",modeB1," modeB2=>",modeB2)
        self.objmgr.updateModeMeasureB1(modeB1)
        self.objmgr.updateModeMeasureB2(modeB2)
        currentModeB1 = convertModeMeasure(self.init_modeB1)
        self.portB1.setCurrentText(currentModeB1)
        currentModeB2 = convertModeMeasure(self.init_modeB2)
        self.portB2.setCurrentText(currentModeB2)

    def saveComPort(self,balanza,namePort):
        comPort = findComIndex(namePort)
        ##print(comPort)
        if comPort!=-1:
            portComName = "COM"+str(comPort)
            if balanza == "BALANZA1":
                self.objmgr.comPort = portComName
                # save here the port selected on DB
                try:
                    self.objmgr.vport = serial.Serial(port = self.objmgr.comPort, baudrate = 9600, timeout = 0.5)
                    self.alert.setMode(SUCCESS)
                    self.alert.showNotification(message)
                    print("se han guardado el puerto seleccionado para la balanza 1")
                except Exception as e:
                    message = "No se ha podido establecer el puerto seleccionado para balanza 1"
                    #print(message)
                    self.alert.setMode(FAILURE)
                    self.alert.showNotification(message)

            elif balanza == "BALANZA2":
                self.objmgr.comPort = portComName
                # save here the port selected on DB
                try:
                    self.objmgr.vport2 = serial.Serial(port = self.objmgr.comPort, baudrate = 9600, timeout = 0.5)
                    self.alert.setMode(SUCCESS)
                    print("se han guardado el puerto seleccionado para la balanza 2")
                except Exception as e:
                    message = "No se ha podido establecer el puerto seleccionado para balanza 2"
                    #print(message)
                    self.alert.setMode(FAILURE)
                    self.alert.showNotification(message)
        else:
            message = "No se han encontrado puertos disponibles"
            #print(message)
            self.alert.showNotification(message)  
 

    def saveFields(self):
        self.objmgr.showConfirmConfigWindow(Action("SAVE_CONFIG",self))

    def updateDB():
        pass

class ConfigUi(QMainWindow, UiConfigWindow):
    # Heredamos de QMainWindow y de la interfaz

    def __init__(self, objmgr):

        # Llamamos al constructor de la superclase
        super().__init__()

        # Ejecutamos el método setupUi heredado del diseño,
        # gracias al cual se generará la interfaz gráfica
        self.setupUi(self, objmgr)