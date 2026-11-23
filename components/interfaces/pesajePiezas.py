from components.imports.piezas import *
from PySide6.QtWidgets import QCheckBox
from components.functions import (getProductRowByCodigo,getClientRowByCodigo,getLastTicketOp,
getCurrentTime,getProductRowByName,getColumn,getColumnAsStr,is_caja_in_piezas)
from components.functionsBobina import loadStyles
from components.clasess import Action
import time

class UiPiezaWindow(object):
    def setupUi(self, pesoWindow, objmgr):
        self.objmgr = objmgr
        responsive = objmgr.getResponsive()
        if not pesoWindow.objectName():
            pesoWindow.setObjectName(u"pesoWindow")
        pesoWindow.resize(1366, 780)
        icon = QIcon()
        icon.addFile(u"components/recursos/balanza.png", QSize(), QIcon.Normal, QIcon.Off)
        pesoWindow.setWindowIcon(icon)
        pesoWindow.setStyleSheet(PIEZAS_STYLES)
        # Auxiliary attributes
        self.items = []

        self.centralwidget = QWidget(pesoWindow)
        self.centralwidget.setObjectName(u"centralwidget")

        self.frameDatos = QFrame(self.centralwidget)
        self.frameDatos.setObjectName(u"frameDatos")
        self.frameDatos.setGeometry(responsive.qRectScaled(40, 20, 400, 680))
        self.frameDatos.setFrameShape(QFrame.StyledPanel)
        self.frameDatos.setFrameShadow(QFrame.Raised)

        self.labelTitulo = QLabel(self.frameDatos)
        self.labelTitulo.setObjectName(u"labelTitulo")
        self.labelTitulo.setGeometry(responsive.qRectScaled(165, 10, 81, 31))

        font = QFont()
        font.setBold(True)
        font.setItalic(False)

        self.labelTitulo.setFont(font)
        
        self._checkOp = False 
        self._checkNBoxes = False 
        self._CxBoxes = False
        self._checkGeneral = False

        self.lineOp = QComboBox(self.frameDatos)
        self.lineOp.setObjectName(u"lineOp")
        self.lineOp.setGeometry(responsive.qRectScaled(110, 50, 111, 30))
        self.lineOp.setEditable(True)
        self.lineOp.currentTextChanged.connect(self.checkOp)
        

        self.lblOp = QLabel(self.frameDatos)
        self.lblOp.setText("Op")
        self.lblOp.setObjectName(u"lineOp")
        self.lblOp.setGeometry(responsive.qRectScaled(70, 50, 20, 30))
        self.lblOp.setAlignment(Qt.AlignCenter)

        self.lblCodigo = QLabel(self.frameDatos)
        self.lblCodigo.setText("Cod. Producto")
        self.lblCodigo.setObjectName(u"lblCodigo")
        self.lblCodigo.setGeometry(responsive.qRectScaled(30, 130, 100, 30))

        self.comboCodigo = QComboBox(self.frameDatos)
        self.comboCodigo.setObjectName(u"comboCodigo")
        self.comboCodigo.setGeometry(responsive.qRectScaled(140, 130, 240, 30))

        self.lblBoxProd  = QLabel(self.frameDatos)
        self.lblBoxProd.setText("Producto")
        self.lblBoxProd.setObjectName(u"lblBoxProd")
        self.lblBoxProd.setGeometry(responsive.qRectScaled(30, 90, 105, 30))

        self.comboBoxProd = QComboBox(self.frameDatos)
        self.comboBoxProd.setObjectName(u"comboBoxProd")
        self.comboBoxProd.setGeometry(responsive.qRectScaled(140, 90, 240, 30))
        self.comboBoxProd.currentTextChanged.connect(self.fill_code_by_product)

        self.lblBoxClient = QLabel(self.frameDatos)
        self.lblBoxClient.setText("Cliente")
        self.lblBoxClient.setObjectName(u"lblBoxClient")
        self.lblBoxClient.setGeometry(responsive.qRectScaled(30, 170, 100, 30))

        self.comboBoxClient = QComboBox(self.frameDatos)
        self.comboBoxClient.setObjectName(u"comboBoxClient")
        self.comboBoxClient.setGeometry(responsive.qRectScaled(140, 170, 240, 30))

        self.lblCxB = QLabel(self.frameDatos)
        self.lblCxB.setText("Cant. x Bultos")
        self.lblCxB.setObjectName(u"lblCxB")
        self.lblCxB.setGeometry(responsive.qRectScaled(20, 210, 111, 30))
        self.lblCxB.setAlignment(Qt.AlignCenter)

        self.linePxBulto = QLineEdit(self.frameDatos)
        self.linePxBulto.setObjectName(u"lineCxB")
        self.linePxBulto.setGeometry(responsive.qRectScaled(135, 210, 80, 30))
        self.linePxBulto.setAlignment(Qt.AlignCenter)
        self.linePxBulto.textChanged.connect(self.line_pxb_changed)#self.calculatePiezas)

        self.lblNB = QLabel(self.frameDatos)
        self.lblNB.setText("N° Bultos")
        self.lblNB.setObjectName(u"lblNB")
        self.lblNB.setGeometry(responsive.qRectScaled(205, 210, 111, 30))
        self.lblNB.setAlignment(Qt.AlignCenter)

        self.lineNBoxes = QLineEdit(self.frameDatos)
        self.lineNBoxes.setObjectName(u"lineNB")
        self.lineNBoxes.setGeometry(responsive.qRectScaled(300, 210, 80, 30))
        self.lineNBoxes.setAlignment(Qt.AlignCenter)
        self.lineNBoxes.textChanged.connect(self.bulto_total_changed)#self.calculatePiezas)

        self.lblPAQ = QLabel(self.frameDatos)
        self.lblPAQ.setText("N° Paquetes")
        self.lblPAQ.setObjectName(u"lblPAQ")
        self.lblPAQ.setGeometry(responsive.qRectScaled(65, 250, 200, 30))
        self.lblPAQ.setAlignment(Qt.AlignCenter)

        self.linePAQ = QLineEdit(self.frameDatos)
        self.linePAQ.setObjectName(u"linePAQ")
        self.linePAQ.setGeometry(responsive.qRectScaled(210, 250, 80, 30))
        self.linePAQ.setAlignment(Qt.AlignCenter)
        self.linePAQ.textChanged.connect(self.line_paq_changed)

        #######################################################
        # RAFAGA DE TICKETS POR CAJA DE IGUAL PARAMETROS ######
        #######################################################
        self.lbl_caja_actual = QLabel(self.frameDatos)
        self.lbl_caja_actual.setText("CAJA ACTUAL:")
        self.lbl_caja_actual.setObjectName(u"lbl_as_btn")
        self.lbl_caja_actual.setGeometry(responsive.qRectScaled(95, 320, 200, 30))
        self.lbl_caja_actual.setAlignment(Qt.AlignCenter)

        self.lbl_check_print_xcaja = QLabel(self.frameDatos)
        self.lbl_check_print_xcaja.setText('Impresion por caja'.upper())
        self.lbl_check_print_xcaja.setGeometry(responsive.qRectScaled(120, 280, 300, 30))

        self.check_print_xcaja = QCheckBox(self.frameDatos)
        self.check_print_xcaja.setObjectName(u"check_print_xcaja")
        self.check_print_xcaja.setGeometry(responsive.qRectScaled(100, 280, 30, 30)) # QRect(170, 400, 111, 30)
        #self.check_print_xcaja.setCursor(QCursor(Qt.PointingHandCursor))
        #self.check_print_xcaja.stateChanged.connect(self.check_print_xcajaChanged)
        #######################################################

        self.botonIniciar = QPushButton(self.frameDatos)
        self.botonIniciar.setObjectName(u"botonIniciar")
        self.botonIniciar.setGeometry(responsive.qRectScaled(130, 370, 130, 41))
        self.botonIniciar.setCursor(QCursor(Qt.PointingHandCursor))
        self.botonIniciar.clicked.connect(self.initWeight)

        self.botonCerrar = QPushButton(self.frameDatos)
        self.botonCerrar.setText("Cerrar caja")
        self.botonCerrar.setObjectName(u"botonCerrar")
        self.botonCerrar.setGeometry(responsive.qRectScaled(130, 430, 130, 41))
        self.botonCerrar.setCursor(QCursor(Qt.PointingHandCursor))
        self.botonCerrar.clicked.connect(self.closeBox)

        #self.botonPaleta = QPushButton(self.frameDatos)
        #self.botonPaleta.setText("Cerrar paleta")
        #self.botonPaleta.setObjectName(u"botonIniciar")
        #self.botonPaleta.setGeometry(responsive.qRectScaled(130, 440, 130, 41))
        #self.botonPaleta.setCursor(QCursor(Qt.PointingHandCursor))
        #self.botonPaleta.clicked.connect(self.closeBox)

        self.botonCaptura = QPushButton(self.frameDatos)
        self.botonCaptura.setObjectName(u"botonCaptura")
        self.botonCaptura.setGeometry(responsive.qRectScaled(130, 500, 130, 41))
        self.botonCaptura.setCursor(QCursor(Qt.PointingHandCursor))
        self.botonCaptura.clicked.connect(self.cptWeight)

        self.botonSalir = QPushButton(self.frameDatos)
        self.botonSalir.setObjectName(u"botonSalir")
        self.botonSalir.setGeometry(responsive.qRectScaled(140, 590, 111, 41))
        self.botonSalir.clicked.connect(self.returnToProducts) # If want to logged out return to login
        self.botonSalir.setCursor(QCursor(Qt.PointingHandCursor))

        self.framePeso = QFrame(self.centralwidget)
        self.framePeso.setObjectName(u"framePeso")
        self.framePeso.setGeometry(responsive.qRectScaled(450, 20, 880, 680)) #width = 921

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.framePeso.sizePolicy().hasHeightForWidth())

        self.framePeso.setSizePolicy(sizePolicy)
        self.framePeso.setCursor(QCursor(Qt.ArrowCursor))
        self.framePeso.setLayoutDirection(Qt.LeftToRight)
        self.framePeso.setFrameShape(QFrame.NoFrame)
        self.framePeso.setFrameShadow(QFrame.Plain)

        self.lcdNumber = QLCDNumber(self.framePeso)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(responsive.qRectScaled(60, 5, 361, 70))
        self.lcdNumber.setMaximumSize(QSize(16777215, 91))
        self.lcdNumber.setFrameShape(QFrame.StyledPanel)
        self.lcdNumber.setFrameShadow(QFrame.Raised)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(6)
        self.lcdNumber.setMode(QLCDNumber.Dec)
        self.lcdNumber.setSegmentStyle(QLCDNumber.Flat)
        self.lcdNumber.setProperty("value", 0.00)

        self.lcdInput = QLCDNumber(self.framePeso)
        self.lcdInput.setObjectName(u"lcdInput")
        self.lcdInput.setGeometry(responsive.qRectScaled(60, 85, 361, 70))
        self.lcdInput.setMaximumSize(QSize(16777215, 91))
        self.lcdInput.setFrameShape(QFrame.StyledPanel)
        self.lcdInput.setFrameShadow(QFrame.Raised)
        self.lcdInput.setSmallDecimalPoint(False)
        self.lcdInput.setDigitCount(6)
        self.lcdInput.setMode(QLCDNumber.Dec)
        self.lcdInput.setSegmentStyle(QLCDNumber.Flat)
        self.lcdInput.setProperty("value", 0.00)
        self.lcdInput.setStyleSheet("""
            #lcdInput{
                font-size:40px;
                color:#04336b;
            }
        """)

        self.tablaPiezas = QTableWidget(self.framePeso)
        if (self.tablaPiezas.columnCount() < 6):
            self.tablaPiezas.setColumnCount(6)
            self.rowCount = 1
            self.tablaPiezas.setRowCount(self.rowCount)
            self.tablaPiezas.clearContents() 

        self.tablaPiezas.setObjectName(u"tablaPesaje")
        self.tablaPiezas.setGeometry(responsive.qRectScaled(20, 240, 840, 400))

        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tablaPiezas.sizePolicy().hasHeightForWidth())

        self.tablaPiezas.setSizePolicy(sizePolicy1)
        self.tablaPiezas.setMaximumSize(QSize(881, 16777215))
        self.tablaPiezas.setAutoFillBackground(False)
        self.tablaPiezas.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tablaPiezas.setColumnCount(6)
        self.tablaPiezas.horizontalHeader().setCascadingSectionResizes(False)
        self.tablaPiezas.horizontalHeader().setDefaultSectionSize(210)
        self.tablaPiezas.verticalHeader().setDefaultSectionSize(40)

        headerTabla = self.tablaPiezas.horizontalHeader()       
        self.tablaPiezas.setColumnWidth(0,100)
        self.tablaPiezas.setColumnWidth(1,110)
        self.tablaPiezas.setColumnWidth(2,160)
        headerTabla.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        self.tablaPiezas.setColumnWidth(4,100)
        self.tablaPiezas.setColumnWidth(5,100)

        self.labelTicket = QLabel(self.framePeso)
        self.labelTicket.setObjectName(u"labelTicket")
        self.labelTicket.setGeometry(responsive.qRectScaled(730, 20, 121, 31))
        self.labelTicket.setFrameShape(QFrame.StyledPanel)

        self.comboBoxBal = QComboBox(self.framePeso)
        self.comboBoxBal.addItem("")
        self.comboBoxBal.addItem("")
        self.comboBoxBal.addItem("")
        self.comboBoxBal.setObjectName(u"comboBoxBal")
        self.comboBoxBal.setGeometry(responsive.qRectScaled(250, 165, 101, 22))
        self.comboBoxBal.currentTextChanged.connect(self.changeBal)

        self.linePiezas = QLineEdit(self.framePeso)
        self.linePiezas.setObjectName(u"lineKg")
        self.linePiezas.setGeometry(responsive.qRectScaled(420, 20, 180, 50))

        self.lineKg = QLineEdit(self.framePeso)
        self.lineKg.setObjectName(u"lineKg")
        self.lineKg.setGeometry(responsive.qRectScaled(420, 98, 180, 55))

        font2 = QFont()
        font2.setBold(False)
        font2.setItalic(False)

        self.linePiezas.setFont(font2)
        self.linePiezas.setReadOnly(True)

        self.lineKg.setFont(font2)
        self.lineKg.setReadOnly(True)
        self.lineKg.setEnabled(False)

        self.lineTicket = QLineEdit(self.framePeso)
        self.lineTicket.setObjectName(u"lineTicket")
        self.lineTicket.setGeometry(responsive.qRectScaled(610, 20, 113, 31))
        self.lineTicket.setReadOnly(True)
        
        self.label_16 = QLabel(self.framePeso)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(responsive.qRectScaled(60, 165, 161, 20))

        pesoWindow.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(pesoWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(responsive.qRectScaled(0, 0, 1366, 22))

        pesoWindow.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(pesoWindow)
        self.statusbar.setObjectName(u"statusbar")

        pesoWindow.setStatusBar(self.statusbar)

        self.retranslateUi(pesoWindow)

        self.timer = QtCore.QTimer()

        self.alert = Alert(self.framePeso,"")
        QMetaObject.connectSlotsByName(pesoWindow)

        self.objmgr.setIndexBalanza2(5)

        cu_number_of_tickets = len(self.objmgr.getPiezaTicketsOnDB())
        self.lineTicket.setText(str(cu_number_of_tickets))
        ##########################################
        # THOSE FIELDS WILL ALWAYS BE LOCKED AND #
        # ONLY BE CHANGED BY OP OR PRODUCT NAME. #
        ##########################################
        self.comboCodigo.setEnabled(False)
        self.comboBoxClient.setEnabled(False)
        ##########################################

        ###################################################################################################
        # Preload values ##################################################################################
        ###################################################################################################
        self.comboBoxClient.addItem('')
        self.comboBoxProd.addItem('')
        self.comboCodigo.addItem('')
        self.comboBoxClient.setCurrentText('')
        self.comboBoxProd.setCurrentText('')
        self.comboCodigo.setCurrentText('')
        self.reloadOps()
        self.reloadClients()
        self.reloadProducts()
        ###################################################################################################

    #############################################
    # QLineEdit Changed Methods #################
    #############################################

    def bulto_total_changed(self):
        bulto_total = self.lineNBoxes.text()
        op = self.lineOp.currentText() 
        op_row = self.objmgr.getAPieza(op)
        if len(op_row)>0:
            self.objmgr.updateBultoTotalOnDB(op,bulto_total)

    def line_pxb_changed(self):
        p_x_bulto = self.linePxBulto.text()
        op = self.lineOp.currentText() 
        op_row = self.objmgr.getAPieza(op)
        if len(op_row)>0:
            self.objmgr.updatePiezaXBultoOnDB(op,p_x_bulto)

    def line_paq_changed(self):
        act_paq = self.linePAQ.text()
        op = self.lineOp.currentText() 
        op_row = self.objmgr.getAPieza(op)
        if len(op_row)>0:
            self.objmgr.updatePaquetesOnDB(op,act_paq)

    #############################################
    # END #######################################
    #############################################

    def setCajaActual(self):
        
        pass

    def palletHasTicketPieza(self):
        pass

    def cajaHasBox(self):
        op = self.lineOp.currentText()
        #print('cajaHasBox=>',self.objmgr.getAllPiezasByOp(op))
        caja = self.objmgr.getAPieza(op)[4]
        tickets_piezas = self.objmgr.getAllPiezasByOp(op)
        exist_caja_in_piezas = is_caja_in_piezas(tickets_piezas,caja)
        #print("current caja in op:",caja)
        #print("tickets in op:",tickets_piezas)
        #print("exist:",exist_caja_in_piezas)
        return exist_caja_in_piezas

    def closeBox(self):
        if self.cajaHasBox():
            print('of course this pallet has at least one box!')
            self.objmgr.showCloseBoxWindow(Action('CLOSE_BOX',self))
        else:
            print("This pallet doesn't Have boxes!")

    def closePallet(self):
        if self.palletHasTicketPieza():
            print('of course this pallet has at least one box!')

    def cptWeight(self):
        if self.comboBoxBal.currentText() == 'ON':
            self.objmgr.setCapturing(not self.objmgr.isCapturing())
            if self.objmgr.isCapturing():
                loadStyles(self,NORMAL)
            else:
                loadStyles(self,INIT_PESAJE)

    def retranslateUi(self, pesoWindow):
        pesoWindow.setWindowTitle(QCoreApplication.translate("pesoWindow", u"MainWindow", None))
        self.labelTitulo.setText(QCoreApplication.translate("pesoWindow", u"Piezas", None))

        self.botonIniciar.setText(QCoreApplication.translate("pesoWindow", u"Iniciar Impresion", None))
        self.botonCaptura.setText(QCoreApplication.translate("pesoWindow", u"Capturar peso", None))

        self.botonSalir.setText(QCoreApplication.translate("pesoWindow", u"Salir", None))

        self.tablaPiezas.setHorizontalHeaderLabels(['N° Ticket','OP','Cod Producto', 'Descripcion Producto', 'N° Bulto','N° Piezas'])

        self.labelTicket.setText("")
        self.comboBoxBal.setItemText(0, QCoreApplication.translate("pesoWindow", u"OFF", None))
        self.comboBoxBal.setItemText(1, QCoreApplication.translate("pesoWindow", u"ON", None))
        #self.comboBoxBal.setItemText(2, QCoreApplication.translate("pesoWindow", u"MANUAL", None))

        self.linePiezas.setText(QCoreApplication.translate("pesoWindow", u"Piezas", None))
        self.lineKg.setText(QCoreApplication.translate("pesoWindow", u"Kg", None))

        self.lineTicket.setText(QCoreApplication.translate("pesoWindow", u"N\u00ba Ticket", None))
        self.label_16.setText(QCoreApplication.translate("pesoWindow", u"Activar Balanza", None))

    def reloadProducts(self):
        res = False
        cu_product = self.comboBoxProd.currentText()
        cu_product_code = self.comboCodigo.currentText()
        success,db_products = self.objmgr.getProductsOnDB()
        if len(db_products)>0:
            self.product_names = getColumn(db_products,1)
            self.product_code = getColumn(db_products,0)
            self.comboBoxProd.clear()
            self.comboCodigo.clear()
            self.comboBoxProd.addItems([''] + self.product_names)
            self.comboCodigo.addItems([''] + self.product_code)
            self.comboBoxProd.setCurrentText(cu_product)
            self.comboCodigo.setCurrentText(cu_product_code)
            res = True
        return res

    def reloadClients(self):
        res = False
        cu_client = self.comboBoxClient.currentText()
        success,db_clients = self.objmgr.getClientsOnDB()
        if len(db_clients)>0:
            self.client_names = getColumn(db_clients,2)
            self.comboBoxClient.clear()
            self.comboBoxClient.addItems([''] + self.client_names)
            self.comboBoxClient.setCurrentText(cu_client)
            res = True
        return res

    def reloadOps(self):
        cu_op = self.lineOp.currentText()
        db_Ops = self.objmgr.getAllPiezas()
        print('reloading Ops=>',db_Ops)
        res = False
        if len(db_Ops)>0:
            self.pieza_ops = getColumnAsStr(db_Ops,0)
            self.lineOp.clear()
            self.lineOp.addItems([''] + self.pieza_ops)
            self.lineOp.setCurrentText(cu_op)
            # Update fields by Op ####################
            self.fill_by_op(cu_op) ###################
            ##########################################
            res = True
        return res

    def fill_by_op(self,cu_op):
        # Update fields by Op
        try:
            op_row = self.objmgr.getAPieza(cu_op)
            if len(op_row)>0: # The op exist and you have to lock fields.
                self.lbl_caja_actual.setText("CAJA ACTUAL: "+str(op_row[4]))
                product_code = op_row[6]
                product_row = self.objmgr.getAProduct(product_code)
                product_code = product_row[0]
                product_name = product_row[1]
                self.comboBoxProd.setCurrentText(product_name)
                self.comboCodigo.setCurrentText(product_code)
                client_id = product_row[3]
                client_row = self.objmgr.getAClient(client_id)
                client_name = client_row[2]
                self.comboBoxClient.setCurrentText(client_name)
                self.linePxBulto.setText(str(op_row[2])) # pieza_bulto
                self.lineNBoxes.setText(str(op_row[1])) # bultos_total
                self.linePAQ.setText(str(op_row[7])) # paquetes
                self.lockFields()
            else:
                self.unlockFields()
        except Exception as e:
            print('exception in filling_op=>',e)

    def fill_code_by_product(self):
        # Update product code by product name ONLY IF NOT EXIST OP.
        try:
            cu_op = self.lineOp.currentText()
            op_row = self.objmgr.getAPieza(cu_op)
            cu_product = self.comboBoxProd.currentText()
            product_row = self.objmgr.getAProductByName(cu_product)
            print('product_row:',product_row)
            if len(op_row)<=0 and len(product_row)>0: # The op doesn't exist and the product exist.
                product_code = product_row[0]
                self.comboCodigo.setCurrentText(product_code)
                client_id = product_row[3]
                client_row = self.objmgr.getAClient(client_id)
                client_name = client_row[2]
                self.comboBoxClient.setCurrentText(client_name)
            else:
                print('This product exist or you need to change the product')
                pass
        except Exception as e:
            print('exception in filling_op=>',e)

    def blink(self,obj):
        self.timer.singleShot(500,obj.hide)
        self.timer.singleShot(1000,obj.show)
        self.timer.singleShot(1500,obj.hide)
        self.timer.singleShot(2000,obj.show)
        self.timer.singleShot(2500,obj.hide)
        self.timer.singleShot(3000,obj.show)
        self.timer.singleShot(3500,obj.hide)
        self.timer.singleShot(4000,obj.show)
        self.timer.singleShot(4500,obj.hide)
        self.timer.singleShot(5000,obj.show)
        self.timer.singleShot(5500,obj.hide)

    def getFramePieza(self):
        return self.framePeso
        
    def showNotification(self,alertText):
        self.lineNotify = QLabel(self.framePeso)
        responsive = self.objmgr.getResponsive()
        self.lineNotify.setGeometry(responsive.qRectScaled(20, 205, 840, 25))
        #self.lineNotify.setGeometry(QRect(20, 205, 840, 25))
        self.lineNotify.setAlignment(Qt.AlignCenter)
        self.lineNotify.setObjectName(u"lineNotify")
        self.lineNotify.show()
        self.lineNotify.setText(alertText)
        self.blink(self.lineNotify)

    def changeOp(self):
        self.comboCodigo.clear()
        self.comboBoxProd.clear()
        self.comboBoxClient.clear()

    def changeBal(self):
        if self.comboBoxBal.currentText() == "ON":
            self.objmgr.setIndexBalanza2(4)
            #print("balanza ON...",4)
        elif self.comboBoxBal.currentText() == "OFF":
            self.objmgr.setIndexBalanza2(5)
            self.objmgr.setTara(0.0)
            self.objmgr.updateWeight(0.0)
            if self.objmgr.isCapturing():
                self.objmgr.setCapturing(False)
            #print("balanza OFF...",5)
        else:
            pass
        pass

    def calculatePiezas(self):
        self.checkCxBoxes()
        self.checkNBoxes()
        self.checkOp()
        print("cxb:",self.checkCxBoxes()," checkNBoxes:",self.checkNBoxes()," checkOp:",self.checkOp())
        self.checkGeneral()
        print("calculating piezas...")
        if self._checkGeneral:
            #self.lockFields()
            #loadStyles(INIT_PESAJE)
            #self.objmgr.setCapturing(False)
            try:
                cxB = int(self.linePxBulto.text())
                nBultos = int(self.lineNBoxes.text())
                totalPiezas = cxB*nBultos
                print("\nTotal piezas:",totalPiezas," cxb:",cxB," nBultos:",nBultos,"\n")
                self.lcdNumber.setProperty("value", str(totalPiezas))
                op = self.lineOp.currentText()
                if len( self.objmgr.getAPieza(op) ) > 0:
                    self.objmgr.updateBultoTotalOnDB(op,nBultos)
                    self.objmgr.updatePiezaXBultoOnDB(op,cxB)
                    print("objects updated")
            except:
                if self.linePxBulto.text() !=  "" and self.lineNBoxes.text() !="":
                    # error in data input, maybe are not numeric int
                    self.showNotification(ALERT_INVALID_GENERAL)
                    #print("some error capturing fields, please provide right data!")
        else:
            pass

    def returnToProducts(self):
        self.objmgr.changeView(1)

    def getInfoOp(self,op):
        result = []
        # get all bob. as part of an production order from db
        return result

    def lockFields(self):
        #self.lineOp.setEnabled(False)
        self.lineTicket.setEnabled(False)
        self.lineKg.setEnabled(False)
        self.comboBoxProd.setEnabled(False)
        #self.comboCodigo.setEnabled(False)        
        #self.comboBoxClient.setEnabled(False)

    def unlockFields(self):
        #self.lineOp.setEnabled(True)
        self.lineTicket.setEnabled(True)
        self.lineKg.setEnabled(True)
        #self.comboCodigo.setEnabled(True)
        self.comboBoxProd.setEnabled(True)
        #self.comboBoxClient.setEnabled(True)
    
    def incRowCount(self):
        self.rowCount = self.rowCount + 1
        self.tablaPiezas.setRowCount(self.rowCount) 

    def updateWeight(self,weight):
        weight = "{:4.2f}".format(float(weight))
        ##print(weight)
        self.lcdInput.setProperty("value", str(weight))
        pass

    def actionPieza(self):
        pass

    def checkNBoxes(self):
        self._checkNBoxes = self.checkInt(self.lineNBoxes)
        return self._checkNBoxes

    def checkCxBoxes(self):
        self._CxBoxes = self.checkInt(self.linePxBulto)
        return self._CxBoxes

    def checkInt(self,object):
        checkNumber = False
        print("checking int:",object.text())
        try:
            number = int(object.text())
            if number >= 0 :
                checkNumber = True
                changeToNormal(object)
                print("with result:",checkNumber)
            else:
                self._checkOp = False
                changeToError(object)
        except Exception as e:
            checkNumber = False
            changeToError(object)
            print(e)
        return checkNumber

    def checkOp(self):
        
        try:
            op = int(self.lineOp.currentText())
            #print('cheking OP ',op,' digits:',check3DigitsOp(int(op)))
            if op != 0 and  check3DigitsOp(int(op)) and len(list(self.lineOp.currentText()))==8:
                self._checkOp = True
                #print('changin to normal')
                changeToNormal(self.lineOp)
                #print('filling by Op')
                self.fill_by_op(op)
                #print('End filling Op')
            else:
                self._checkOp = False
                changeToError(self.lineOp)
        except:
            self._checkOp = False
            changeToError(self.lineOp)
        return self._checkOp

    def checkGeneral(self):
        self.checkNBoxes()
        self.checkCxBoxes()
        self.checkOp()
        self._checkGeneral = self._checkNBoxes and self._CxBoxes and self._checkOp
        print('check general with=>',self._checkNBoxes,' ',self._CxBoxes,' ',self._checkOp)
        return self._checkGeneral 

    def initPrint(self):
        self.objmgr.stopProvider() # Fast execution when stoping the provider cycle.
        opRow = self.objmgr.getAPieza(self.lineOp.currentText())
        self.objmgr.setEnableOp(len(opRow)>0) # If exist op pass to process!!!
        if not self.objmgr.isEnableOp():
            self.objmgr.showConfirmNewPiezaWindow(Action("NEW_PIEZA",self))
        print("Result enabling to create op",self.objmgr.isEnableOp())
        if self.objmgr.isEnableOp():
            self.objmgr.disableOp() # Turn off enter to new op on DB    
            self._checkGeneral = self.checkGeneral()   
            print('init printing cheking general',self._checkGeneral)
            if self._checkGeneral: 
                # Cargo el diccionario actual de la bobina
                fields = self.readFieldsPieza() # this will store the op if not exist
                print('init printing reading fields',fields)
                self.objmgr.setData(fields)
                self.objmgr.printPieza()
                # Envio la impresion del ticket
                self.objmgr.showPrintingWindow(None)
                self.objmgr.setCapturing(True)
                self.reloadOps()
                if self.objmgr.isCapturing():
                    loadStyles(self,NORMAL)
            elif not self._checkGeneral:
                print("Some field doesn't match.")
            else:
                print("You have to make capturing before init print and data need to match.")
        else:
            pass
        # Run provider againt
        if self.comboBoxBal.currentText() == "ON":
            self.objmgr.run() 

    def initWeight(self):
        # print a lot of tickets here or print one ticket
        if self.check_print_xcaja.isChecked():
            num_tickets = 10
            self.print_gust(num_tickets)
        else:
            if self.lineOp.currentText != "" and self.lineOp.currentText != " " and self.lineOp.currentText != None:
                if self.objmgr.isCapturing():
                    loadStyles(self,INIT_PESAJE)
                self.initPrint()

    def print_first_ticket(self,row_pieza,op,user,turno,piezas,date,new_ticket,neto,ficha,hora,paquetes):
        # Caja exist on db
        product_code = row_pieza[6]
        caja = row_pieza[4] # caja_actual
        #resultTickets,arrTickets = self.objmgr.getPiezaTicketsOnDB()
        resultProducts,arrProducts = self.objmgr.getProductsOnDB()
        resultClient,arrClient = self.objmgr.getClientsOnDB()

        #print("\nLooking product row:",product_code,arrProducts)
        product_row = getProductRowByCodigo(product_code,arrProducts)
        client_code = product_row[3]

        #print("\nLooking client row:",client_code,arrClient)
        client_row = getClientRowByCodigo(client_code,arrClient)
        product_name = product_row[1]
        client_name = client_row[2]

        try:
            print("row_pieza:",row_pieza)
            bulto_actual = int( row_pieza[3]) # The op
            self.objmgr.updateBultoOnDB(op,bulto_actual + 1)
            new_bulto_actual = len(self.objmgr.get_piezas_by_op_and_caja(op,caja)) + 1 #bulto_actual of this caja
        except:
            print("can't update bulto on DB!!!")

        result = {
            "producto" : str(product_name),
            "client" : str(client_name),
            "operador" : str(user),
            "reimpresion" : "",
            "bulto" : str(new_bulto_actual),
            "turno" : turno,
            "op" : str(op),
            "piezas" : str(piezas),
            "date" : str(date),
            "ticketCode" : str(new_ticket),
            "code" : str(product_code),
            "bruto" : str(neto),
            "caja" : str(caja)
        }
        #
        n_caja = caja
        n_paleta = "1"
        paleta_total = "1" # Cambiar por el numero de paleta
        codigo = product_code
        # ("ticket","neto","n_bulto","n_caja","n_paleta","fecha_emision","op","ficha","hora")
        data = [new_ticket,neto,new_bulto_actual,n_caja,n_paleta,date,op,ficha,hora,piezas,paquetes]
        resultTicket = self.objmgr.storePiezaTicket(data)
        print("data:",data," ",resultTicket) 
        return result

    def print_after_first_ticket(self,op,arrTickets,user,turno,piezas,date,neto,caja,bulto_total,pieza_bulto,paquetes,ficha,hora):
        # Write database if not exist, and save first result.
        product_name = self.comboBoxProd.currentText()
        client_name = self.comboBoxClient.currentText()
        print("product_name:",product_name," client_name:",client_name)
        #resultTickets,arrTickets = self.objmgr.getPiezaTicketsOnDB()
        resultProducts,arrProducts = self.objmgr.getProductsOnDB()
        #resultClient,arrClient = self.objmgr.getClientsOnDB()
        
        product_row = getProductRowByName(product_name,arrProducts)
        product_code = product_row[0]

        try:
            new_ticket = 1
            last_ticket = int( getLastTicketOp(op,arrTickets) )
            if last_ticket != -1 :
                new_ticket = last_ticket + 1
        except:
            pass

        result = {
            "producto" : str(product_name),
            "client" : str(client_name),
            "operador" : str(user),
            "reimpresion" : "",
            "bulto" : "1",
            "turno" : str(turno),
            "op" : str(op),
            "piezas" : str(piezas),
            "date" : str(date),
            "ticketCode" : str(new_ticket),
            "code" : str(product_code),
            "bruto" : str(neto),
            "caja" : str(caja)
        }
        #
        n_caja = "1"
        n_paleta = "1"
        bulto_actual = "1"
        caja_actual = "1"
        paleta_total = "1" # Change this in case of future
        codigo = product_code
        # Store ticket
        # ["op","bultos_total","pieza_bulto","bulto_actual","caja_actual","paleta_total","codigo"]
        dataOp = [op,bulto_total,pieza_bulto,bulto_actual,caja_actual,paleta_total,codigo,paquetes]
        resultOp = self.objmgr.storePiezaOp(dataOp)
        print("result:",result," ",resultOp)
        #[0, '0.0', '1', '1', '1', '2022-08-22', '13116542', 648, '11:55:22 AM']
        # ("ticket","neto","n_bulto","n_caja","n_paleta","fecha_emision","op","ficha","hora")
        data = [new_ticket,neto,bulto_actual,n_caja,n_paleta,date,op,ficha,hora,piezas,paquetes]
        resultTicket = self.objmgr.storePiezaTicket(data)
        print("data:",data," ",resultTicket)
        return result

    def get_conmon_data(self):
        op = self.lineOp.currentText()
        amtBultos = 0
        amtXBultos = 0
        try:
            amtBultos = int(self.lineNBoxes.text())
            amtXBultos = int(self.linePxBulto.text())
            pieza_bulto = int( self.linePxBulto.text() )
        except:
            pass
        arrTickets = []
        try:
            new_ticket = 1
            resultTickets,arrTickets = self.objmgr.getPiezaTicketsOnDB()
            last_ticket = len(arrTickets)
            if last_ticket != 0 :
                new_ticket = last_ticket + 1
        except:
            pass
        #######################
        # Some Op Fields ######
        #######################
        piezas = pieza_bulto #amtBultos*amtXBultos
        paquetes = self.linePAQ.text()
        bulto_total = self.lineNBoxes.text()
        #######################
        # End #################
        #######################
        user = self.objmgr.getUser()["nombre"] + " " + self.objmgr.getUser()["apellido"] 
        ficha = self.objmgr.getUser()["ficha"]
        
        hora = getCurrentTime()
        date = getDate()
        turno = str(getTurn())
        caja = "1"
        #print("fixed=>"," op:",op," bultos:",amtBultos," BXP:",amtXBultos," piezas:",piezas," user:",user," ficha:",ficha," date:",date," turno",turno)
        row_pieza = self.objmgr.getAPieza(op)
        print("\n",row_pieza,"\n")
        # Write database is exist op
        neto = "0.0"
        conmon_data = {
            'op':op,
            'row_pieza':row_pieza,
            'user':user,
            'turno':turno,
            'piezas':piezas,
            'date':date,
            'new_ticket':new_ticket,
            'ficha':ficha,
            'hora':hora,
            'arrTickets':arrTickets,
            'caja':caja,
            'bulto_total':bulto_total,
            'pieza_bulto':pieza_bulto,
            'paquetes':paquetes
        }
        return conmon_data

    def readFieldsPieza(self):
        result = {}
        conmon_data = self.get_conmon_data()
        op = conmon_data['op']
        row_pieza = conmon_data['row_pieza']
        user = conmon_data['user']
        turno = conmon_data['turno']
        piezas = conmon_data['piezas']
        date = conmon_data['date']
        new_ticket = conmon_data['new_ticket']
        ficha = conmon_data['ficha']
        hora = conmon_data['hora']
        arrTickets = conmon_data['arrTickets']
        caja = conmon_data['caja']
        bulto_total = conmon_data['bulto_total']
        pieza_bulto = conmon_data['pieza_bulto']
        paquetes = conmon_data['paquetes']
        neto = "0.0"
        #
        if self.comboBoxBal.currentText() == 'ON':
            neto = "{:4.2f}".format(float(self.objmgr.getBruto()))
        if len(row_pieza)> 0 :
            result = self.print_first_ticket(row_pieza,op,user,turno,piezas,date,new_ticket,neto,ficha,hora,paquetes)
        else:
            result = self.print_after_first_ticket(op,arrTickets,user,turno,piezas,date,neto,caja,bulto_total,pieza_bulto,paquetes,ficha,hora)
        return result 
    
    def print_gust(self,num_bultos):
        for k in range(num_bultos):
            self.initPrint()
            time.sleep(1)


class PiezaUi(QMainWindow, UiPiezaWindow):
    # Heredamos de QMainWindow y de la interfaz

    def __init__(self, objmgr):

        # Llamamos al constructor de la superclase
        super().__init__()

        # Ejecutamos el método setupUi heredado del diseño,
        # gracias al cual se generará la interfaz gráfica
        self.setupUi(self, objmgr)