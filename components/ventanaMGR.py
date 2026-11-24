############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################
from components.dbHandler import DBHandler,DBCypher
from components.imports.mgrWindow import *
from components.constants.database import *
from components.functions import turnToDescription,getModeMeasure
from components.clasess import Responsive
from components.constants.ticket_report_pieza import getHtmlPlegadizoFilled
import serial,time,hashlib
from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout
from portCommngmt import disablePort,enablePort
from components.interfaces.dialogos import *
from datetime import datetime,timedelta
from PySide6 import QtCore

class PesajeMGR(QMainWindow):
    def __init__(self):
        self.app = QApplication()
        self.responsive = Responsive()
        #responsive.setCurrentPixelsX(1680)
        #responsive.setCurrentPixelsY(1050)

        super().__init__()  
        #self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False) # Modify the closeEvent of the Window to cut the provider method
        self.setWindowTitle("Sistema de pesaje MGR C.A.")
        self.setWindowIcon(getMGRIcon())
        self.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.dbPiezaMGR = DBHandler("piezas")
        self.dbMGR = DBHandler("pesaje")
        self.dbCypher = DBCypher("pesaje")
        self.dbCypher.setPath("pesaje")
        result,test = self.dbMGR.getTable_2("bobinas","op")
        #print(test)
        config = self.getConfigOnDB()
        #('127.0.0.1', '80', 'elrodriguez', 'lo123ve', 'Microsoft Print to PDF', 'Microsoft Print to PDF', 'Manual', 'COM6', 'COM6', 'default')
        self.supervisor = ""
        
        self.comPort = config[7]
        self.comPort2 = config[8]
        self.port1Open = False
        self.port2Open = False
        # Create an unique vport from mgrObject
        try:
            #disablePort()
            #enablePort()
            self.vport = serial.Serial(port = self.comPort, baudrate = 9600, timeout = 0.5)
            time.sleep(3)
            print("success open port from mgrObject ",self.comPort)
            self.port1Open = True
        except Exception as e:
            print("can't open port from mgrObject ",self.comPort)
            try:
                print("Trying second open port ",self.comPort)
                disablePort(self.comPort)
                enablePort(self.comPort)
                self.vport = serial.Serial(port = self.comPort, baudrate = 9600, timeout = 0.5)
                time.sleep(3)
                print("success open port from mgrObject ",self.comPort)
                self.port1Open = True
            except Exception as e:
                print("can't open port from mgrObject ",self.comPort)
        # Create an unique vport2 from mgrObject
        try:
            self.vport2 = serial.Serial(port = self.comPort2, baudrate = 9600, timeout = 0.5)
            time.sleep(3)
            print("success open port from mgrObject ",self.comPort2)
            self.port2Open = True
        except Exception as e:
            print("can't open port from mgrObject ",self.comPort2)
        #
        self.serverIp = config[0]
        self.serverPort = config[1]
        self.serverUsr = config[2]
        self.serverPass = config[3]
        self.serverUrl = "http://" + self.serverIp + ":" + self.serverPort

        self.paletaEmbalaje = 0.0

        self.printerName = config[4] # Impresora
        self.printerName2 = config[5]   # Etiquetadora

        self.modeProgram =  config[6]

        self.isCapt = True
        self.indexBalanza = 1
        self.indexBalanza2 = 1
        self.weight = 1.0
        self.weight_carucha = 70.0
        self.tara = 0.0
        self.neto = 0.0
        self.bruto = 0.0
        self.bobMatriz = "0"
        self.hablador = {
            "op":"",
            "product":"",
            "position":"",
            "amount":"",
            "observations":""
        }

        self.modeMeasureB1 = int(config[9])
        self.modeMeasureB2 = int(config[10])

        self.isActiveB1 = False
        self.isActiveB2 = False

        self.modeAdobe = config[11]
        self.pathAdobe = config[12]

        self.index = 0
        self.newOpFlag = False
        
        self.currentData = {}
        # fill user credentials from db calling reading method
        self.currentUser = {"id":"","cedula":"","usuario":"ELRODRIGUEZ","nombre":"","apellido":"","ficha":"3020","password":"","email":"","nivel":"","turno":"0","supervisor":""} # User credentials here
        # fill client credentials from db calling reading method
        self.currentClient = {"client":"client","code":"code"}
        # fill product credentials from db calling reading method
        self.currentProduct = {"product":"product","code":"code"}

        self.loginWidget = LoginUi(self)
        self.pesajeWidget = PesajeUi(self)
        self.piezasWidget = PiezaUi(self)
        self.productWidget = ProductUi(self)
        self.configWidget = ConfigUi(self)

        self.viewsLayout = QStackedLayout()

        self.viewsLayout.addWidget(self.loginWidget) # index = 0
        self.viewsLayout.addWidget(self.productWidget) # index = 1
        self.viewsLayout.addWidget(self.pesajeWidget) # index = 2
        self.viewsLayout.addWidget(self.piezasWidget) # index = 3
        self.viewsLayout.addWidget(self.configWidget) # index = 4
        
        self.changeView(0)

        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.viewsLayout)
        
        self.threadpool = QtCore.QThreadPool()
        self.provider = Provider(self)
        
        self.printer = Printer()

        self.modePrintHablador = 1 # 1 for printing using and registered Op, 2 for printing using a blank form

        self.init()
        self.setCentralWidget(self.mainWidget)

        """if (not self.isDBEncrypted()):
            self.dbCypher.encryptDB()"""

        self.isManualMode = False

    def set_productUI(self):
        self.productWidget = ProductUi(self)


    def keyPressEvent(self,event):
        #print(f"Tipo de evento: {event.type()}")
        #print(f"Tecla presionada: {event.key()}")
        #print(f"Texto de la tecla: {event.text()}")
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            #print("Enter presionado")
            if self.index==0:
                list_vacio = ["empty","empty"]
                self.loginWidget.login()
                #self.login(list_vacio)
        if event.key() == QtCore.Qt.Key_Space:
            #print("Espacio presionado")
            if self.viewsLayout.currentIndex() == 2:
                self.pesajeWidget.initWeight()
        super().keyPressEvent(event)

    def setStatusB1(self,isValue):
        self.isActiveB1 = isValue

    def setStatusB2(self,isValue):
        self.isActiveB2 = isValue

    def reconectar_balanza(self,balanza):
        if balanza == "BALANZA 1":
            disablePort()
            enablePort()
            try:
                self.vport = serial.Serial(port = self.comPort, baudrate = 9600, timeout = 0.5)
                time.sleep(3)
                mensajeOk =  Dialog_msj("balanza_conectada")
                mensajeOk.setWindowModality(Qt.ApplicationModal)
                mensajeOk.exec_()
            except Exception as e:
                mensajeError =  Dialog_msj("balanza_no_conectada")
                mensajeError.setWindowModality(Qt.ApplicationModal)
                mensajeError.exec_()
                print(e)

    def stopBalanza1(self):
        portBalanza1 = self.provider.getBalanza1()
        try:
            portBalanza1.write('STOP\n'.encode('utf-8'))
            portBalanza1.flushOutput()
            self.setStatusB1(False)
        except:
            pass

    def stopBalanza2(self):
        portBalanza2 = self.provider.getBalanza2()
        try:
            portBalanza2.write('STOP\n'.encode('utf-8'))
            portBalanza2.flushOutput()
            self.setStatusB2(False)
        except:
            pass

    def startBalanza1(self):
        portBalanza1 = self.provider.getBalanza1()
        try:
            portBalanza1.write('START\n'.encode('utf-8'))
            portBalanza1.flushInput()
            self.setStatusB1(True)
        except:
            pass

    def startBalanza2(self):
        portBalanza2 = self.provider.getBalanza2()
        try:
            portBalanza2.write('START\n'.encode('utf-8'))
            self.setStatusB2(True)
            portBalanza2.flushInput()
        except:
            pass

    def isActiveBalanza2(self):
        return self.isActiveB2

    def setSupervisor(self,supervisor):
        self.supervisor = supervisor

    def getSupervisor(self):
        return self.supervisor
    
    def getResponsive(self):
        return self.responsive

    def setModePrintHablador(self,mode):
        self.modePrintHablador = mode

    def getModePrintHablador(self):
        return self.modePrintHablador

    def showReportProductionWindow(self):
        pass

    def updateModeMeasureB1(self,modeB1):
        #["Continuo ohaus T21P","GNT Ohaus T21P","Continuo MT BBA231C"]
        self.modeMeasureB1 = getModeMeasure(modeB1)


    def updateModeMeasureB2(self,modeB2):
        self.modeMeasureB2 = getModeMeasure(modeB2)


    def getPesajeWidget(self):
        return self.pesajeWidget

    def loadMenu(self):
        self.menuBar().clear()
        self.menuB = self.menuBar()
        self.menuB.setStyleSheet("""
            *{
                font-size:12px;
                font-family: Arial, Helvetica, sans-serif;
                font-weight:400;
            }
            QMenuWidget{
                min-height:30px;
                height:30px;
                max-height:30px;
            }
        """)

        self.menuArchivo = self.menuB.addMenu("Usuario")
        # Change user variable to selt th text of user name saved on db
        # PySide6.QtWidgets.QMenu.addAction(NoneType, str, method, str)
        self.menuArchivo.addAction(getUserIcon(),self.currentUser["nombre"] + " " + self.currentUser["apellido"],self.sessionClose,"Contrl + C")
        self.menuArchivo.addAction(getLogOutIcon(),"Cerrar Cesion",self.sessionClose,"Contrl + C")

        self.subMenuGestion = self.menuArchivo.addMenu("Gestion")
        self.subMenuGestion.setIcon(getCustomizeIcon())

        self.subMenuGestion.addAction(getAddIcon()," Agregar / Eliminar / Editar",self.addUsr,"Contrl + C")
        self.subMenuGestion.setDisabled(True)
        if self.currentUser["nivel"] == "ADMINISTRADOR" or self.currentUser["nivel"] == "SUPERVISOR":
            self.subMenuGestion.setEnabled(True)
        #self.subMenuGestion.addAction(getEditIcon(),"Editar",self.editUsr,"Contrl + C")        
        #self.subMenuGestion.addAction(getDeleteIcon(),"Eliminar",self.deleteUsr,"Contrl + C")

        self.menuArchivo.addAction(getCloseIcon(),"Salir",self.close,"Contrl + C")

        self.menuReports = self.menuB.addMenu("Reportes")
        self.menuReports.addAction(getOpIcon(),"Op",self.reportOp,"Contrl + C")
        #self.menuReports.addAction(getOpIcon(),"Produccion",self.reportProduction,"Contrl + C")
        self.menuReports.addAction(getOperatorIcon(),"Operador",self.reportOperator,"Contrl + C")
        self.menuReports.addAction(getPalletIcon(),"Bobinas",self.reportTicket,"Contrl + C")
        self.menuReports.addAction(getPalletIcon(),"Paletas",self.reportPallet,"Contrl + C")
        self.menuReports.addAction(getTalkersIcon(),"Habladores",self.generateHablador,"Contrl + C")
        self.menuReports.addAction(getPiecesIcon(),"Piezas",self.reportPiezas,"Contrl + C")

        self.menuConfig = self.menuB.addMenu("Registros")

        #menuProduction = self.menuConfig.addMenu("Produccion")
        #menuProduction.setIcon(getProductionIcon())
        #menuProduction.addAction(getAddIcon(),"Agregar OP",self.addOp,"Contrl + C")
        #menuProduction.addAction(getEditIcon(),"Editar OP",self.editOp,"Contrl + C")
        #menuProduction.addAction(getDeleteIcon(),"Eliminar OP",self.deleteOp,"Contrl + C")

        menuClient = self.menuConfig.addMenu("Cliente")
        menuClient.setIcon(getClientIcon())
        menuClient.addAction(getAddIcon()," Agregar / Eliminar / Editar",self.addClient,"Contrl + C")
        menuClient.setDisabled(True)
        if self.currentUser["nivel"] == "ADMINISTRADOR" or self.currentUser["nivel"] == "SUPERVISOR":
            menuClient.setEnabled(True)
        #menuClient.addAction(getEditIcon(),"Editar Cliente",self.editClient,"Contrl + C")
        #menuClient.addAction(getDeleteIcon(),"Eliminar Cliente",self.deleteClient,"Contrl + C")

        menuPaletas = self.menuConfig.addMenu("Paletas")
        self.icono_paleta = QIcon("components\\sources\\pallet.png")
        menuPaletas.setIcon(self.icono_paleta)
        menuPaletas.addAction(self.icono_paleta, "Agrear / Eliminar / Editar", self.paletas)
        menuPaletas.setDisabled(True)
        if self.currentUser["nivel"] == "ADMINISTRADOR" or self.currentUser["nivel"] == "SUPERVISOR":
            menuPaletas.setEnabled(True)

        menuPlatform = self.menuConfig.addMenu("Producto")
        menuPlatform.setIcon(getProductIcon())
        menuPlatform.addAction(getAddIcon()," Agregar",self.addProduct,"Contrl + C")
        menuPlatform.addAction(getAddIcon()," Eliminar / Editar",self.editProductNew,"Contrl + C")
        menuPlatform.setDisabled(True)
        if self.currentUser["nivel"] == "ADMINISTRADOR" or self.currentUser["nivel"] == "SUPERVISOR":
            menuPlatform.setEnabled(True)
        #menuPlatform.addAction(getEditIcon(),"Editar Producto",self.editProduct,"Contrl + C")
        #menuPlatform.addAction(getDeleteIcon(),"Eliminar Producto",self.deleteProduct,"Contrl + C")

        menuTicket = self.menuConfig.addMenu("Ticket")
        menuTicket.setIcon(getTicketIcon())
        menuTicket.addAction(getAddIcon()," Agregar / Eliminar / Editar",self.deleteTicket,"Contrl + C")
        #menuTicket.addAction(getEditIcon(),"Editar ticket",self.editTicket,"Contrl + C")

        menuOP = self.menuConfig.addMenu("OP")
        menuOP.setIcon(getTicketIcon())
        menuOP.addAction(getAddIcon()," Agregar",self.addOP,"Contrl + C")
        menuOP.addAction(getAddIcon()," Editar / Eliminar",self.addOp,"Contrl + X")
        menuOP.setDisabled(True)
        if self.currentUser["nivel"] == "ADMINISTRADOR" or self.currentUser["nivel"] == "SUPERVISOR":
            menuOP.setEnabled(True)
        #menuTicket.addAction(getEditIcon(),"Editar ticket",self.editTicket,"Contrl + C")

        menuConfig = self.menuB.addMenu("Configuracion")
        menuConfig.addAction(getConfigIcon(),"Programa",self.changeToConfig,"Contrl + C")

        self.menuHelp = self.menuB.addMenu("Informacion")
        self.menuHelp.addAction(getHelpIcon(),"Ayuda",self.showHelp,"Contrl + C")

        self.etiquetadora = self.nombre_etiquetadora()

    def restorePassword(self):
        self.showRestorePasswordWindow(Action("RESTORE_PASSWORD",self))

    def deleteTicket(self):
        self.showDeleteTicketWindow(Action("DELETE_TICKET",self))

    def editTicket(self):
        self.showEditTicketWindow(Action("EDIT_TICKET",self))

    def showHelp(self):
        helpFilePath = f'"{absPath("manual_mgr.pdf")}"'
        helpFilePath = helpFilePath.replace("\components","")
        adobe = r'C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
        #print(helpFilePath)
        cmd = cmd = '"{}" /p {}'.format(adobe, helpFilePath)
        print(cmd)
        subprocess.Popen(cmd,shell=True)

    def enableOp(self):
        self.newOpFlag = True

    def setEnableOp(self,value):
        self.newOpFlag = value

    def disableOp(self):
        self.newOpFlag = False

    def isEnableOp(self):
        return self.newOpFlag
         
    def getMaxWeightBobina(self):
        return 20.0

    # Maximo peso por caja
    def getMaxWeightPieza(self):
        return 20.0

    def paletas(self):
        paletasWindow = newPopUp(self,"paletas")
        paletasWindow.setWindowModality(Qt.ApplicationModal)
        paletasWindow.exec_()

    def consultarPaletaEmbalaje(self,nombre):
        table = []
        result,table = self.dbMGR.getTableByRow("paletas","nombre",nombre)
        return table
    
    def obtenerPesoPaletaPorID(self,id):
        table = []
        result,table = self.dbMGR.getTableByRow("paletas","id",id)
        return table

    def actualizarPaletaEmbalaje(self,id,valores):
        result = self.dbMGR.actualizar_fila("paletas",id,valores)
        return result
    
    def guardarPaletaEmbalaje(self,valores):
        result = False
        try:
            self.dbMGR.insertarFila("paletas",valores)
            result = True
        except Exception as e:
            print(e)
        return result

    def obtenerUltimaPaletaEmbalaje(self):
        return self.dbMGR.obtenerUltimaFila("paletas","id")
    
    def obtenerPaletasEmbalaje(self):
        result,tabla = self.dbMGR.getTable_new("paletas","nombre")
        return tabla
    def obtenerPaletasPeso(self):
        result,tabla = self.dbMGR.getTable_new("paletas","peso")
        return tabla

    def changeToConfig(self):
        self.changeView(4)

    def getFramePeso(self):
        return self.pesajeWidget.getFramePeso()

    def getFramePieza(self):
        return self.piezasWidget.getFramePieza()

    def reportOperator(self):
        self.showReportOperatorWindow(Action("REPORT_OPERATOR",self))

    def reportOp(self):
        self.showInsertOrderWindow(Action("REPORT_OP",self))

    def reportPallet(self):
        self.showReportPalletWindow(Action("REPORT_PALLET",self))

    def reportTicket(self):
        self.showReportTicketWindow(Action("REPORT_TICKET",self))

    def reportPiezas(self):
        self.showReportPlegadizoWindow(Action("REPORT_PLEGADIZO",self))

    def generateHablador(self):
        self.setModePrintHablador(2)
        self.showInsertHabladorWindow(Action("GENERATE_HABLADOR",self.pesajeWidget))
    ################################
    # PIEZAS #######################
    ################################
    def reportPlegadizo(self):
        self.showPrintPlegadizoWindow(Action("REPORT_PLEGADIZO",self))

    def printPlegadizo(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if True or len(self.currentData) == 16: # 16 adding supervisor
            if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("A4")
                self.printer.setName(self.printerName) # La paleta se imprime por impresora
                result = self.printer.printFromHtml(getHtmlPlegadizoFilled(self.currentData))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("A4")
                self.printer.generateFromHtml(getHtmlPlegadizoFilled(self.currentData))
                result = self.printer.printWithPreview(self.pathAdobe)
        else:
            pass
            #print("the current data lenght doesn't match")
        return result

    ################################
    # END ##########################
    ################################

    #def reportProduction(self):
    #    self.showReportProductionWindow(Action("REPORT_OP",self))

    # Override closeEvent o QMainWindow to close the while cycle
    def closeEvent(self, event: PySide6.QtGui.QCloseEvent) -> None:
        #self.provider.kill()
        self.stopProvider()
        """if (not self.isDBEncrypted()):
            self.dbCypher.encryptDB()"""
        try:
            self.vport.close()
        except:
            pass
        try:
            self.vport2.close()
        except:
            pass
        print("Closing program!!!")
        return super().closeEvent(event)

    def showWindow(self):
        self.showFullScreen()
        #self.showMaximized()
        self.setCentralWidget(self.mainWidget)
        sys.exit(self.app.exec_())

    def getFramePeso(self):
        pass
    
    def run(self):
        self.provider.init()
        self.threadpool.start(self.provider) 
        self.pesajeWidget.botonIniciar.setDisabled(False) 
        pass

    def isManual(self):
        return self.isManualMode

    def stopManual(self):
        self.isManualMode = False

    def setManual(self):
        self.isManualMode = True

    def stopProvider(self):
        self.provider.kill()    
        self.provider = Provider(self)       

    def setIndexBalanza2(self,index):
        self.indexBalanza2 = index
        pass

    def getIndexBalanza2(self):
        return self.indexBalanza2

    def setIndexBalanza(self,index):
        self.indexBalanza = index
        pass

    def getIndexBalanza(self):
        return self.indexBalanza

    def setStyles(self,styles):
        self.app.setStyleSheet(styles)
        pass           

    def capturar(self,event):
        pass

    def reiniciar(self):
        pass   

    def setCapturing(self,isCapturing):
        self.isCapt = isCapturing
        pass

    def isCapturing(self):
        return self.isCapt

    def updateTara(self):
        self.tara = self.weight
        self.updateWeight(self.tara)

    def setTara(self,tara):
        self.tara = tara

    def settarainter(self,tara):
        self.tara = tara


    def getHablador(self):
        return self.hablador

    def setHablador(self,hablador):
        #self.hablador = {"op":"25145698","product":"Etiq. Kapo Manzana 250 mL","position":"3","amount":"412,98","observations":"La paleta le falta una bobina por ordenes\ndel cliente."}
        self.hablador = hablador

    def getBobMatriz(self):
        return self.bobMatriz

    def setBobMatriz(self,bobMatriz):
        self.bobMatriz = bobMatriz

    def getTara(self):
        return self.tara

    def getNeto(self):
        return self.neto

    def getBruto(self):
        return self.bruto

    def setIp(self,ip):
        self.serverIp = ip
        pass

    def setPort(self,port):
        self.serverPort = port
        pass  

    def setCom(self,com):
        self.comPort = com
        pass 

    def setUrl(self,url):
        self.serverUrl = url
        pass     

    def initSession(self):
        pass

    def sessionStart(self):
        pass

    def sessionClose(self):
        self.loginWidget.clearUser()
        self.productWidget.clearUser()
        self.changeView(0)
        self.productWidget.labelUser.setText(self.currentUser["nombre"] + " " + self.currentUser["apellido"])
        """if (not self.isDBEncrypted()):
            self.dbCypher.encryptDB()"""

    def addUsr(self):
        self.showAddUsrWindow(Action("ADD_USR",self))

    def deleteUsr(self):
        pass

    def editUsr(self):
        pass

    # Orden de produccion
    def addOp(self,op=None):
        self.showAddOpWindow(Action("ADD_OP",self),op)

    def editOp(self):
        self.showEditOpWindow(Action("EDIT_OP",self))

    def deleteOp(self):
        self.showDeleteOpWindow(Action("DELETE_OP",self))

    # Nuevas OP
    def addOP(self):
        self.AgregarOp = Dialog_msj("registro_op_BLK",self)
        self.AgregarOp.setWindowModality(Qt.ApplicationModal)
        self.AgregarOp.exec_()

    # Clientes
    def addClient(self):
        self.showAddClientWindow(Action("ADD_CLIENT",self))

    def editClient(self):
        self.showEditClientWindow(Action("EDIT_CLIENT",self))

    def deleteClient(self):
        self.showDeleteClientWindow(Action("DELETE_CLIENT",self))

    # Productos
    def addProduct(self):
        self.showAddProductWindow(Action("ADD_PRODUCT",self))
        pass

    def deleteProduct(self):
        self.showDeleteProductWindow(Action("DELETE_PRODUCT",self))
        pass
    
    def editProduct(self):
        self.showEditProductWindow(Action("EDIT_PRODUCT",self))
        pass

    def editProductNew(self):
        self.editarproducto = Dialog_msj("editar_producto",self)
        self.editarproducto.setWindowModality(Qt.ApplicationModal)
        self.editarproducto.exec_()

    def init(self):
        # Make all variables null, 0, or empty here.
        self.tara = 0.0
        self.weight = 0.0
        self.neto = 0.0
        self.currentData = []
        pass

    def getClient(self):
        pass

    def getProduct(self):
        pass

    def getUser(self):
        return self.currentUser

    def setData(self,data):
        self.currentData = data

    ##################################################
    # PIEZAS #########################################
    ##################################################
    def createPlegadizoPreview(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if True or len(self.currentData) == 16: # 13 check first
            self.printer.setOptions("A4")
            self.printer.setName(self.printerName) # La paleta se imprime por impresora
            html = getHtmlPlegadizoFilled(self.currentData) # this will rewrite temHtml.html file
            result = (html != "")
            print("Preview for plegadizo generated ",result)
        else:
            print("The current data lenght for plegadizo doesn't match to generate preview")
        return result

    # CREATE METHODS FOR PREVIEW POPUPS
    def createPalletPreview(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 16: # 16 adding supervisor
            self.printer.setOptions("A4")
            self.printer.setName(self.printerName) # La paleta se imprime por impresora
            html = getHtmlPalletFilled(self.currentData,self.paletaEmbalaje) # this will rewrite temHtml.html file
            result = (html != "")
            print("Preview for pallet generated ",result)
        else:
            print("The current data lenght for pallet doesn't match to generate preview")
        return result

    def createTurnPreview(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 10: # 16 adding supervisor
            self.printer.setOptions("A4")
            self.printer.setName(self.printerName) # La paleta se imprime por impresora
            html = getHtmlTurnFilled(self.currentData) # this will rewrite temHtml.html file
            result = (html != "")
            print("Preview for turn generated ",result)
        else:
            print("The current data lenght for turn doesn't match to generate preview")
        return result
    #
    def editarPaletas(self,id,valores):
        result = self.dbMGR.actualizar_fila("paletas",id,valores)
        return result


    def createHablPreview(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 5 or len(self.hablador) == 5:
            self.printer.setOptions("A4H")
            self.printer.setName(self.printerName) # El hablador se imprime mediante impresora
            html = getHtmlHabladorFilled(self.hablador)
            result = (html != "")
            print("Preview for hablador generated ",result)
        else:
            print("the current data lenght doesn't match to generate preview")
        return result

    def printPallet(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 16: # 16 adding supervisor
            #print(f"CurrentData en printPallet: {self.currentData}.")
            if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("A4")
                self.printer.setName(self.printerName) # La paleta se imprime por impresora
                result = self.printer.printFromHtml(getHtmlPalletFilled(self.currentData,self.paletaEmbalaje))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("A4")
                self.printer.generateFromHtml(getHtmlPalletFilled(self.currentData,self.paletaEmbalaje))
                result = self.printer.printWithPreview(self.pathAdobe)
        else:
            pass
            #print("the current data lenght doesn't match")
        return result

    def printBobina(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 14:
            #print(f"Datos para impresion: {self.currentData}")
            self.printer.setOptions("TICKET") # ticekt option for good print size.
            self.printer.setName(self.printerName2) # El ticket se imprime por etiquetadora
            result = self.printer.printFromHtml(getHtmlBobinaFilled(self.currentData),self.etiquetadora)
        else:
            #print("the current data lenght doesn't match")
            pass
        return result

    def nombre_etiquetadora(self):
        result,impresora_ = self.dbMGR.obtenerImpresora("etiquetadora")
        #print(impresora_)
        impresora = impresora_[0][0]
        #print(impresora)
        if result:
            return impresora
        else:
            return None

    def rePrintBobina(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 14:
            """if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("TICKET")
                self.printer.setName(self.printerName) # El reporte de Op se imprime mediante impresora
                result = self.printer.printFromHtml(getHtmlBobinaFilled(self.currentData))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("TICKET")
                self.printer.generateFromHtml(getHtmlBobinaFilled(self.currentData))
                result = self.printer.printWithPreview(self.pathAdobe)"""
            self.printer.printFromHtml(getHtmlBobinaFilled(self.currentData),self.etiquetadora)
        else:
            print("the current data lenght doesn't match")
            pass
        return result

    def printPieza(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 13:
            self.printer.setOptions("TICKET")
            self.printer.setName(self.printerName) # 
            result = self.printer.printFromHtml(getHtmlPiezaFilled(self.currentData))
        else:
            print("the current data lenght doesn't match")
            pass
        return result

    def printOp(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 10:
            if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("A4")
                self.printer.setName(self.printerName) # El reporte de Op se imprime mediante impresora
                result = self.printer.printFromHtml(getHtmlOpFilled(dataExampleOp))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("A4")
                self.printer.generateFromHtml(getHtmlOpFilled(dataExampleOp))
                result = self.printer.printWithPreview(self.pathAdobe)
        else:
            #print("the current data lenght doesn't match")
            pass
        return result

    def printGeneral(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 9:
            if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("A4")
                self.printer.setName(self.printerName) # El reporte de Op se imprime mediante impresora
                result = self.printer.printFromHtml(getHtmlGeneralFilled(self.currentData))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("A4")
                self.printer.generateFromHtml(getHtmlGeneralFilled(self.currentData))
                result = self.printer.printWithPreview(self.pathAdobe)
        else:
            #print("the current data lenght doesn't match")
            pass
        return result

    def printDetailed(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 6:
            if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("A4")
                self.printer.setName(self.printerName) # El reporte de Op se imprime mediante impresora
                result = self.printer.printFromHtml(getHtmlDetailedFilled(self.currentData))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("A4")
                self.printer.generateFromHtml(getHtmlDetailedFilled(self.currentData))
                result = self.printer.printWithPreview(self.pathAdobe)
        else:
            #print("the current data lenght doesn't match")
            pass
        return result

    def printTurn(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 10:
            if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("A4")
                self.printer.setName(self.printerName) # El reporte de Op se imprime mediante impresora
                result = self.printer.printFromHtml(getHtmlTurnFilled(self.currentData))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("A4")
                self.printer.generateFromHtml(getHtmlTurnFilled(self.currentData))
                result = self.printer.printWithPreview(self.pathAdobe)
        else:
            #print("the current data lenght doesn't match")
            pass
        return result

    def printHablador(self):
        result = False
        # Collect data from self and check steps to proceed here.
        if len(self.currentData) == 5 or len(self.hablador) == 5:
            if self.modeAdobe == False or self.modeAdobe == 0 :
                self.printer.setOptions("A4H")
                self.printer.setName(self.printerName) # El reporte de Op se imprime mediante impresora
                result = self.printer.printFromHtml(getHtmlHabladorFilled(self.hablador))
            if self.modeAdobe == True or self.modeAdobe == 1 :
                self.printer.setOptions("A4H")
                self.printer.generateFromHtml(getHtmlHabladorFilled(self.hablador))
                result = self.printer.printWithPreview(self.pathAdobe)
        else:
            pass
            #print("the current data lenght doesn't match")
        return result

    def getViewIndex(self):
        return self.index

    def changeView(self,index):
        self.viewsLayout.setCurrentIndex(index)
        self.index = index
        #self.tara = 0.0 # on other screen tara change

    def showRestorePasswordWindow(self,action):
        self.restorePasswordWindow = PopUp(MODE_RESTORE_PASSWORD.lower(),MODE_RESTORE_PASSWORD,action)
        self.restorePasswordWindow.setTitle("""Cambiar contraseña""")
        self.restorePasswordWindow.setSize(540,380)
        self.restorePasswordWindow.setStyleSheet(STYLES_REGISTER)
        self.restorePasswordWindow.show()

    def showDeleteClientWindow(self,action):
        self.deleteClientWindow = PopUp(MODE_DELETE_CLIENT.lower(),MODE_DELETE_CLIENT,action)
        self.deleteClientWindow.setTitle("""Eliminar Cliente""")
        self.deleteClientWindow.setSize(480,220)
        self.deleteClientWindow.setStyleSheet(STYLES_REGISTER)
        self.deleteClientWindow.show()

    def showDeleteProductWindow(self,action):
        self.deleteProductWindow = PopUp(MODE_DELETE_PRODUCT.lower(),MODE_DELETE_PRODUCT,action)
        self.deleteProductWindow.setTitle("""Eliminar Producto""")
        self.deleteProductWindow.setSize(480,220)
        self.deleteProductWindow.setStyleSheet(STYLES_REGISTER)
        self.deleteProductWindow.show()


    def showDeleteTicketWindow(self,action):
        self.deleteTicketWindow = PopUp(MODE_DELETE_PRODUCT.lower(),MODE_DELETE_TICKET,action)
        self.deleteTicketWindow.setTitle("""Eliminar Ticket""")
        self.deleteTicketWindow.setSize(640,420)
        self.deleteTicketWindow.setStyleSheet(STYLES_REGISTER)
        self.deleteTicketWindow.show()


    def showPrintingWindow(self,action):
        #print(f"Accion: {action}.")
        # Ventana de espera de impresion de ticket
        self.printingWindow = PopUp(MODE_WAIT.lower()+"_printing",MODE_WAIT,action)
        self.printingWindow.setMessage("""Imprimiendo ticket\nfavor esperar""".upper())
        self.printingWindow.setSize(480,220)
        self.printingWindow.setStyleSheet(STYLES_MODE_WAIT)
        self.printingWindow.show()

    def showErrorLogin(self):
        # Ventana de espera de impresion de ticket
        self.ErrorLogin = QDialog(self)
        self.ErrorLogin.setMessage("""Usuario o contraseña\nincorrecto""".upper())
        self.ErrorLogin.setSize(480,220)
        self.ErrorLogin.setStyleSheet(STYLES_MODE_WAIT)
        self.ErrorLogin.show()

    def closePrintingWindow(self):
        try:
            self.printingWindow = None
        except:
            pass

    def showInsertMatrizWindow(self,action):
        # Ventana para insertar Matriz
        self.insertMatrizWindow = PopUp(MODE_INPUT_MATRIZ.lower(),MODE_INPUT_MATRIZ,action)
        self.insertMatrizWindow.setMessage("""Inserte Bobina\nmatriz""".upper())
        self.insertMatrizWindow.setSize(480,260)
        self.insertMatrizWindow.setStyleSheet(STYLES_POPUP)
        self.insertMatrizWindow.show()
        self.insertMatrizWindow.loop.exec()

    def closeInsertMatrizWindow(self):
        try:
            self.insertMatrizWindow.close()
        except:
            pass

    def showInsertHabladorWindow(self,action):
        # Ventana para insertar Hablador
        self.insertHablador = PopUp(MODE_INPUT_HABLADOR.lower() ,MODE_INPUT_HABLADOR,action)
        self.insertHablador.setTitle("Hablador")
        self.insertHablador.setSize(500,320)
        self.insertHablador.setStyleSheet(STYLES_POPUP)
        self.insertHablador.show()

    def closeInsertHabladorWindow(self):
        try:
            self.insertHablador.close()
        except:
            pass

    def showReportProductionWindow(self,action):
        # Ventana para insertar Hablador
        self.reportProduction = PopUp(MODE_INPUT_HABLADOR.lower() ,MODE_INPUT_HABLADOR,action)
        self.reportProduction.setTitle("Reporte de produccion")
        self.reportProduction.setSize(500,320)
        self.reportProduction.setStyleSheet(STYLES_POPUP)
        self.reportProduction.show()

    def showEditProductWindow(self,action):
        # Ventana para editar el producto
        self.editProductWindow = PopUp(MODE_EDIT_PRODUCT.lower(),MODE_EDIT_PRODUCT,action)
        self.editProductWindow.setTitle("Editar producto")
        self.editProductWindow.setSize(480,280)
        self.editProductWindow.setStyleSheet(STYLES_REGISTER)
        self.editProductWindow.show()

    def closeEditProductWindow(self):
        try:
            self.editProductWindow.close()
        except:
            pass

    def showEditClientWindow(self,action):
        # Ventana para editar el cliente
        self.editClientWindow = PopUp(MODE_EDIT_CLIENT.lower(),MODE_EDIT_CLIENT,action)
        self.editClientWindow.setTitle("Editar cliente")
        self.editClientWindow.setSize(440,240)
        self.editClientWindow.setStyleSheet(STYLES_REGISTER)
        self.editClientWindow.show()

    def closeEditClientWindow(self):
        try:
            self.editClientWindow.close()
        except:
            pass

    def showAddOpWindow(self,action,op=None):
        self.addOpWindow = PopUp(MODE_ADD_OP.lower(),MODE_ADD_OP,action,op)
        self.addOpWindow.setTitle("Agregar OP")
        self.addOpWindow.setSize(720,520)
        self.addOpWindow.setStyleSheet(STYLES_REGISTER)
        self.addOpWindow.show()

    def showAddUsrWindow(self,action):
        self.addUsrWindow = PopUp(MODE_ADD_USR.lower(),MODE_ADD_USR,action)
        self.addUsrWindow.setTitle("Registro de usuario")
        self.addUsrWindow.setSize(720,520)
        self.addUsrWindow.setStyleSheet(STYLES_REGISTER)
        self.addUsrWindow.show()

    def showEditOpWindow(self,action):
        self.editOpWindow = PopUp(MODE_EDIT_OP.lower(),MODE_EDIT_OP,action)
        self.editOpWindow.setTitle("Editar OP")
        self.editOpWindow.setSize(720,520)
        self.editOpWindow.setStyleSheet(STYLES_REGISTER)
        self.editOpWindow.show()

    def showDeleteOpWindow(self,action):
        self.deleteOpWindow = PopUp(MODE_DELETE_OP.lower(),MODE_DELETE_OP,action)
        self.deleteOpWindow.setTitle("Eliminar OP")
        self.deleteOpWindow.setSize(480,280)
        self.deleteOpWindow.setStyleSheet(STYLES_REGISTER)
        self.deleteOpWindow.show()

    def showAddClientWindow(self,action):
        # Ventana para agregar cliente
        self.addClientWindow = PopUp(MODE_ADD_CLIENT.lower(),MODE_ADD_CLIENT,action)
        self.addClientWindow.setTitle("Agregar Cliente")
        self.addClientWindow.setSize(720,520)
        self.addClientWindow.setStyleSheet(STYLES_REGISTER)
        self.addClientWindow.show()

    def showAddProductWindow(self,action):
        # Ventana para agregar cliente
        self.addProductWindow = PopUp(MODE_ADD_PRODUCT.lower(),MODE_ADD_PRODUCT,action)
        self.addProductWindow.setTitle("Agregar Producto")
        self.addProductWindow.setSize(720,520)
        self.addProductWindow.setStyleSheet(STYLES_REGISTER)
        self.addProductWindow.show()

    def closeAddClientWindow(self):
        try:
            self.addClientWindow.close()
        except:
            pass

    def showReportOperatorWindow(self,action):
        # Ventana para imprimir reporte de Operador
        self.reportOperatorWindow = PopUp(MODE_REPORT_OP.lower(),MODE_REPORT_OP,action)
        self.reportOperatorWindow.setTitle("Reporte de Operador")
        self.reportOperatorWindow.setSize(440,280)
        self.reportOperatorWindow.setStyleSheet(STYLES_POPUP)
        self.reportOperatorWindow.show()

    def closeReportOperatorWindow(self):
        try:
            self.addClientWindow.close()
        except:
            pass

    def showReportPlegadizoWindow(self,action):
        # Ventana para imprimir reporte por pieza
        self.reportPlegadizoWindow = PopUp(MODE_REPORT_PIEZA.lower(),MODE_REPORT_PIEZA,action)
        self.reportPlegadizoWindow.setTitle("Reporte de producto plegadizo")
        self.reportPlegadizoWindow.setSize(440,280)
        self.reportPlegadizoWindow.setStyleSheet(STYLES_MODE_REPORT_PIEZA)
        self.reportPlegadizoWindow.show()

    def closeReportPlegadizoWindow(self):
        try:
            self.reportPiezaWindow.close()
        except:
            pass

    def showReportPalletWindow(self,action):
        # Ventana para imprimir reporte por paleta
        self.ReportPalletWindow = PopUp(MODE_REPORT_PALLET.lower(),MODE_REPORT_PALLET,action)
        #self.ReportPalletWindow.setTitle("Reporte por paleta")
        self.ReportPalletWindow.setSize(480,280)
        self.ReportPalletWindow.setStyleSheet(STYLES_REGISTER)
        self.ReportPalletWindow.show()

    def closeReportPalletWindow(self):
        try:
            self.ReportPalletWindow.close()
        except:
            pass

    def showReportTicketWindow(self,action):
        # Ventana para imprimir reporte por paleta
        self.ReportTicketWindow = PopUp(MODE_REPORT_TICKET.lower(),MODE_REPORT_TICKET,action)
        #self.ReportTicketWindow.setTitle("Reporte por paleta")
        self.ReportTicketWindow.setSize(480,230)
        self.ReportTicketWindow.setStyleSheet(STYLES_REGISTER)
        self.ReportTicketWindow.show()

    def closeReportTicketWindow(self):
        try:
            self.ReportTicketWindow.close()
        except:
            pass


    def showInsertOrderWindow(self,action):
        # Ventana para insertar la orden de produccion
        self.insertOrderWindow = PopUp(MODE_INPUT_ORDER.lower(),MODE_INPUT_ORDER,action)
        self.insertOrderWindow.setMessage("""Por favor introduzca la orden\nde produccion.""")
        self.insertOrderWindow.setSize(440,240)
        self.insertOrderWindow.setStyleSheet(STYLES_POPUP)
        self.insertOrderWindow.show()

    def closeInsertOrderWindow(self):
        try:
            self.insertOrderWindow.close()
        except:
            pass

    def showWaitOpContWindow(self):
        # Orden de produccion existente
        self.waitOpContWindow = PopUp(MODE_WAIT.lower()+"_order",MODE_WAIT)
        self.waitOpContWindow.setMessage("""Esta op ya existe.\n\nContinuando\ntransaccion...""".upper())
        self.waitOpContWindow.setSize(480,280)
        self.waitOpContWindow.setStyleSheet(STYLES_MODE_WAIT)
        self.waitOpContWindow.show()

    def closeWaitOpContWindow(self):
        try:
            self.waitOpContWindow.close()
        except:
            pass

    def showWaitBalanzaWindow(self,action):
        # Ventana de espera de cambio a balanza 2
        self.waitBalanzaWindow = PopUp(MODE_WAIT.lower()+"_change",MODE_WAIT,action)
        self.waitBalanzaWindow.setMessage("""Cambiando a balanza.\n2...""".upper())
        self.waitBalanzaWindow.setSize(480,220)
        self.waitBalanzaWindow.setStyleSheet(STYLES_MODE_WAIT)
        self.waitBalanzaWindow.show()

    def closeWaitBalanzaWindow(self):
        try:
            self.waitBalanzaWindow.close()
        except:
            pass

    def showClosePalleteWindow(self,action):
        # Ventana de confirmacion de cierre de paleta
        self.closePalleteWindow = PopUp(MODE_CONFIRM.lower()+"_pallete",MODE_CONFIRM,action)
        self.closePalleteWindow.setMessage("""¿Seguro que desea\ncerrar la paleta e\nincrementar el valor?""".upper())
        self.closePalleteWindow.setSize(480,280)
        self.closePalleteWindow.setStyleSheet(STYLES_POPUP)
        self.closePalleteWindow.show()
        self.closePalleteWindow.loop.exec()

    ####################################
    # BOX WINDOWS ######################
    ####################################

    def showCloseBoxWindow(self,action):
        # Ventana de confirmacion de cierre de paleta
        self.closeBoxWindow = PopUp(MODE_CONFIRM.lower()+"_pallete",MODE_CONFIRM,action)
        self.closeBoxWindow.setMessage("""¿Seguro que desea\nterminar esta caja\nincrementar el valor?""".upper())
        self.closeBoxWindow.setSize(480,280)
        self.closeBoxWindow.setStyleSheet(STYLES_POPUP)
        self.closeBoxWindow.show()
        self.closeBoxWindow.loop.exec()

    def killCloseBoxWindow(self):
        try:
            self.closeBoxWindow.close()
        except:
            pass
        pass
    
    def showPrintPlegadizoWindow(self,action):
        # Ventana de confirmacion de cierre de paleta
        self.printPlegadizoWindow = PopUp(MODE_CONFIRM.lower()+"_pallete",MODE_CONFIRM,action)
        self.printPlegadizoWindow.setMessage("""¿Desea imprimir la\nlista de producto\nplegadizo?""".upper())
        self.printPlegadizoWindow.setSize(480,280)
        self.printPlegadizoWindow.setStyleSheet(STYLES_POPUP)
        self.printPlegadizoWindow.show()
        self.printPlegadizoWindow.loop.exec()

    def showConfirmNewPiezaWindow(self,action):
        # Ventana de confirmacion para crear nueva op
        self.confirmNewPiezaWindow = PopUp(MODE_CONFIRM.lower()+"_new_op",MODE_CONFIRM,action)
        self.confirmNewPiezaWindow.setMessage("""Esta op no se encuentra registrada\n\n¿Seguro que desea crear una\nnueva orden de produccion?""".upper())
        self.confirmNewPiezaWindow.setSize(480,280)
        self.confirmNewPiezaWindow.setStyleSheet(STYLES_POPUP)
        self.confirmNewPiezaWindow.show()
        self.confirmNewPiezaWindow.loop.exec()

    ####################################
    ####################################
    ####################################

    def closeClosePalleteWindow(self):
        try:
            self.closePalleteWindow = None
        except:
            pass

    def showCreateHabladorWindow(self,action):
        # Ventana de confirmacion de hablador
        self.createHabladorWindow = PopUp(MODE_CONFIRM.lower()+"_hablador",MODE_CONFIRM,action)
        self.createHabladorWindow.setMessage("""¿desea crear un\nhablador?""".upper())
        self.createHabladorWindow.setSize(480,280)
        self.createHabladorWindow.setStyleSheet(STYLES_POPUP)
        self.createHabladorWindow.show()

    def closeCreateHabladorWindow(self):
        try:
            self.createHabladorWindow.close()
        except:
            pass

    def showConfirmNewOpWindow(self,action):
        # Ventana de confirmacion para crear nueva op
        self.confirmNewOpWindow = PopUp(MODE_CONFIRM.lower()+"_new_op",MODE_CONFIRM,action)
        self.confirmNewOpWindow.setMessage("""Esta op no se encuentra registrada\n\n¿Seguro que desea crear una\nnueva orden de produccion?""".upper())
        self.confirmNewOpWindow.setSize(480,280)
        self.confirmNewOpWindow.setStyleSheet(STYLES_POPUP)
        self.confirmNewOpWindow.show()

        self.confirmNewOpWindow.loop.exec()


    def setResponsePopUp(self,value):
        self.responsePopUp = value

    def closeConfirmNewOpWindow(self):
        try:
            self.confirmNewOpWindow.close()
        except:
            pass

    def showWaitPrintWindow(self,action):
        # Ventana de impresion de empaque
        self.waitPrintWindow = PopUp(MODE_CONFIRM.lower(),MODE_CONFIRM,action)
        self.waitPrintWindow.setMessage("""¿Desea imprimir la\nlista de empaque?""".upper())
        self.waitPrintWindow.setSize(480,280)
        self.waitPrintWindow.setStyleSheet(STYLES_POPUP)
        self.waitPrintWindow.show()

    def showExeedPalletWindow(self,action,limitPallet):
        # Ventana de impresion de empaque
        self.waitExeedPalletWindow = PopUp(MODE_CONFIRM.lower(),MODE_CONFIRM,action)
        self.waitExeedPalletWindow.setMessage("¿Desea cerrar la paleta\nexcediendo el limite de\n".upper()+str(limitPallet)+" paletas registradas?".upper())
        self.waitExeedPalletWindow.setSize(580,320)
        self.waitExeedPalletWindow.setStyleSheet(STYLES_POPUP)
        self.waitExeedPalletWindow.show()

    def showExeedBobinaWindow(self,action,limitBobinas):
        # Ventana de impresion de empaque
        self.waitExeedBobWindow = PopUp(MODE_CONFIRM.lower(),MODE_CONFIRM,action)
        self.waitExeedBobWindow.setMessage("¿Desea imprimir el ticket\nexcediendo el limite de\n".upper()+str(limitBobinas)+" bobinas registradas?".upper())
        self.waitExeedBobWindow.setSize(580,320)
        self.waitExeedBobWindow.setStyleSheet(STYLES_POPUP)
        self.waitExeedBobWindow.show()

    def closeWaitPrintWindow(self):
        try:
            self.waitPrintWindow.close()
        except:
            pass

    def showConfirmConfigWindow(self,action):
        # Ventana de impresion de empaque
        self.confirmConfigWindow = PopUp(MODE_CONFIRM_CONFIG.lower(),MODE_CONFIRM_CONFIG,action)
        self.confirmConfigWindow.setMessage("""¿Seguro que quiere cambiar\nla configuracion actual?""".upper())
        self.confirmConfigWindow.setSize(480,280)
        self.confirmConfigWindow.setStyleSheet(STYLES_POPUP)
        self.confirmConfigWindow.show()

    def closeConfirmConfigWindow(self):
        try:
            self.confirmConfigWindow.close()
        except:
            pass

    """
    def showRegisterOpWindow(self,action):
        # Ventana de confirmacion de cierre de paleta
        self.registerOpWindow = PopUp(MODE_CONFIRM.lower()+"_pallete",MODE_CONFIRM,action)
        self.registerOpWindow.setMessage('''¿Seguro que desea\nregistrar esta orden de\nproduccion?'''.upper())
        self.registerOpWindow.setSize(480,280)
        self.registerOpWindow.setStyleSheet(STYLES_POPUP)
        self.registerOpWindow.show()
    
    def closeRegisterOpWindow(self):
        try:
            self.registerOpWindow = None
        except:
            pass
    """


    def updateWeight(self,weight):
        if str(weight) != "":
            self.weight = float(str(weight))
            self.neto = self.weight - self.tara
            self.bruto = self.weight
            self.pesajeWidget.updateWeight(weight)
            self.pesajeWidget.updateNeto(self.neto)
            self.piezasWidget.updateWeight(weight)
            #self.piezasWidget.updateNeto(self.neto)

    def getWeight(self):
        return self.weight
        #takes the current weight of the indicator

    def login(self,credentials):
        """if self.isDBEncrypted():
            self.dbCypher.decryptDB()"""
        userTyped = credentials[0]
        passTyped = credentials[1]
        user_typed_encrypted = hashlib.sha256(userTyped.encode()).hexdigest()
        password_typed_encrypted = hashlib.sha256(passTyped.encode()).hexdigest()
        success,dbUsers = self.dbMGR.getTable("usuarios")
        #print("result:",success,"Typed=> User",userTyped," PassWord:",passTyped)
        #print(f"usuario encriptado: {user_typed_encrypted}\n Contraseña encriptada: {password_typed_encrypted}")
        result = False
        if success:
            for k in range(len(dbUsers)):
                dbId = dbUsers[k][0]
                dbCedula = dbUsers[k][1]
                dbUsername = dbUsers[k][2]
                dbName = dbUsers[k][3]
                dbApellido = dbUsers[k][4]
                dbFicha = dbUsers[k][5]
                dbPassWord = dbUsers[k][6]
                dbEmail = dbUsers[k][7]
                dbNivel = dbUsers[k][8]
                dbTurno = dbUsers[k][9]
                dbSupervisor = dbUsers[k][10]
                #print("db=> User",dbUsername," PassWord:",dbPassWord)
                if dbUsername == user_typed_encrypted and dbPassWord == password_typed_encrypted:
                    result = True
                    self.currentUser = {"id":dbId,"cedula":dbCedula,"usuario":dbUsername,"nombre":dbName,"apellido":dbApellido,"ficha":dbFicha,"password":dbPassWord,"email":dbEmail,"nivel":dbNivel,"turno":dbTurno,"supervisor":dbSupervisor}
                    self.productWidget.setUser(self.currentUser["nombre"] + " " + self.currentUser["apellido"])
                    turn = self.currentUser["turno"] 
                    description = turnToDescription(turn)
                    self.productWidget.setTurn(description)
                    #print("logged in => ",self.currentUser)
        else:
            """if ( not self.isDBEncrypted() ):
                self.dbCypher.encryptDB()
                # reset database here
                #print("error tratando de leer la base de datos")
                pass"""
        return result
    
    def login_supervisor(self,credentials):
        """if self.isDBEncrypted():
            self.dbCypher.decryptDB()"""
        userTyped = credentials[0]
        passTyped = credentials[1]
        user_typed_encrypted = hashlib.sha256(userTyped.encode()).hexdigest()
        password_typed_encrypted = hashlib.sha256(passTyped.encode()).hexdigest()
        success,dbUsers = self.dbMGR.getTable("usuarios")
        #print("result:",success,"Typed=> User",userTyped," PassWord:",passTyped)
        #print(f"usuario encriptado: {user_typed_encrypted}\n Contraseña encriptada: {password_typed_encrypted}")
        result = False
        supervisor_aprobador = "N/A"
        if success:
            for k in range(len(dbUsers)):
                dbId = dbUsers[k][0]
                dbCedula = dbUsers[k][1]
                dbUsername = dbUsers[k][2]
                dbName = dbUsers[k][3]
                dbApellido = dbUsers[k][4]
                dbFicha = dbUsers[k][5]
                dbPassWord = dbUsers[k][6]
                dbEmail = dbUsers[k][7]
                dbNivel = dbUsers[k][8]
                dbTurno = dbUsers[k][9]
                dbSupervisor = dbUsers[k][10]
                #print("db=> User",dbUsername," PassWord:",dbPassWord)
                
                if dbUsername == user_typed_encrypted and dbPassWord == password_typed_encrypted and (dbNivel == "ADMINISTRADOR" or dbNivel == "SUPERVISOR"):
                    supervisor_aprobador = dbName + " " + dbApellido
                    result = True
        return result,supervisor_aprobador

    def login_SU(self,credentials):
        """if self.isDBEncrypted():
            self.dbCypher.decryptDB()"""
        userTyped = credentials[0]
        passTyped = credentials[1]
        user_typed_encrypted = hashlib.sha256(userTyped.encode()).hexdigest()
        password_typed_encrypted = hashlib.sha256(passTyped.encode()).hexdigest()
        success,dbUsers = self.dbMGR.getTable("usuarios")
        #print("result:",success,"Typed=> User",userTyped," PassWord:",passTyped)
        #print(f"usuario encriptado: {user_typed_encrypted}\n Contraseña encriptada: {password_typed_encrypted}")
        result = False
        if success:
            for k in range(len(dbUsers)):
                dbId = dbUsers[k][0]
                dbCedula = dbUsers[k][1]
                dbUsername = dbUsers[k][2]
                dbName = dbUsers[k][3]
                dbApellido = dbUsers[k][4]
                dbFicha = dbUsers[k][5]
                dbPassWord = dbUsers[k][6]
                dbEmail = dbUsers[k][7]
                dbNivel = dbUsers[k][8]
                dbTurno = dbUsers[k][9]
                dbSupervisor = dbUsers[k][10]
                #print("db=> User",dbUsername," PassWord:",dbPassWord)
                if dbUsername == user_typed_encrypted and dbPassWord == password_typed_encrypted and dbNivel == "ADMINISTRADOR":
                    result = True
                    self.currentUser = {"id":dbId,"cedula":dbCedula,"usuario":dbUsername,"nombre":dbName,"apellido":dbApellido,"ficha":dbFicha,"password":dbPassWord,"email":dbEmail,"nivel":dbNivel,"turno":dbTurno,"supervisor":dbSupervisor}
                    self.productWidget.setUser(self.currentUser["nombre"] + " " + self.currentUser["apellido"])
                    turn = self.currentUser["turno"] 
                    description = turnToDescription(turn)
                    self.productWidget.setTurn(description)
                    #print("logged in => ",self.currentUser)
        else:
            """if ( not self.isDBEncrypted() ):
                self.dbCypher.encryptDB()
                # reset database here
                #print("error tratando de leer la base de datos")
                pass"""
        return result

    # data = (0,25110897,"elirod","Eliezer","Rodriguez",3020,"lo123ve","examplegmailcom",10,1)
    def storeOp(self,data):
        ##print(data)
        result = self.dbMGR.insertRow("bobinas",BOBINAS,data)
        if result:
            pass
            print("op data stored on db")  
        else:
            pass
            print("can't store the data on database")   
        return result

    def storeConfig(self,data):
        result = False
        # ("127.0.0.2","8080","admin","admin","Microsoft Print To Pdf","Microsoft Print To Pdf","Manual","COM1","COM2","default")
        result = self.dbMGR.updateRow("config_proceso",CONFIG_UPDATE,data,"key")
        if result:
            print("configuration stored on db")  
            pass
        else:
            pass
            print("can't store the data on database")
        return result

    def storeTicket(self,data):
        result = False
        result = self.dbMGR.insertRow("proceso_bobina",PROCESO_BOBINA,list(data))
        if result:
            print("ticket saved on DB")  
            pass
        else:
            pass
            print("can't save the ticket on database")
        return result

    def storeDeletedTicket(self,data):
        result = False
        result = self.dbMGR.insertRow("proceso_bobina_eliminados",PROCESO_BOBINA_DELETED,list(data))
        return result

    def isDBEncrypted(self):
        result = True
        result,config = self.dbMGR.getTable("config_proceso")
        print("is encrypted? ",result)
        return (not result)

    #('127.0.0.1', '80', 'elrodriguez', 'lo123ve', 'Microsoft Print to PDF', 'Microsoft Print to PDF', 'Manual', 'COM6 - USB-SERIAL CH340 (COM6)', 'COM6 - USB-SERIAL CH340 (COM6)', 'default')
    def getConfigOnDB(self):
        config = []
        result,config = self.dbMGR.getTable("config_proceso")
        config = list(config[0])
        if result:
            portName = config[7]
            portName2 = config[8]
            
            portIndex= findComIndex(portName)
            portIndex2 = findComIndex(portName2)

            portName = "COM0"
            portName2 = "COM1"

            
            if portIndex !=-1:
                portName = "COM" + str(portIndex)
                config[7] = portName
                #print("1 ","1:",portName,portIndex,"2:",portName2,portIndex2)
            if portIndex2 !=-1:
                portName2 = "COM" + str(portIndex2)
                config[8] = portName2
                #print("2 ","1:",portName,portIndex,"2:",portName2,portIndex2)

        else:
            config = []
            #print("can't store the data on database")
        #print("success getting config: ",config)
        return config

    def getTicketsOnDB(self):
        tickets = []
        result,config = self.dbMGR.getTable("proceso_bobina")
        tickets = list(tickets[0])
        if result:
            pass
            #print("success getting config: ",tickets)
        else:
            tickets = []
            #print("can't store the data on database")
        return config

    def getTicket_byOp_unique(self):
        return self.dbMGR.obtenerTabla_unique("proceso_bobina","op")
    
    def getTicket_byPaleta_unique(self):
        return self.dbMGR.obtenerTabla_unique("proceso_bobina","n_paleta")
    
    def getTicket_byFicha_unique(self):
        return self.dbMGR.obtenerTabla_unique("proceso_bobina","ficha")

    def setTicketOnDB(self,ticket,paleta):
        self.dbMGR.updateValue("proceso_bobina",(ticket,paleta),("ticket","n_paleta"))

    def setBobinaOnDB(self,ticket,bobina):
        self.dbMGR.updateValue("proceso_bobina",(ticket,bobina),("ticket","bobina"))

    def updateTaraOnDB(self,op,tara): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("updating=> op:",op," tara:",tara)
        self.dbMGR.updateValue("bobinas",("tara",tara),("op",op)) # value,key(or path)

    def updatePesoMinBobina(self,codigo,peso_min):
        self.dbMGR.updateValue("productos",("peso_min",peso_min),("codigo_producto",codigo))

    def updatePesoMaxBobina(self,codigo,peso_max):
        self.dbMGR.updateValue("productos",("peso_max",peso_max),("codigo_producto",codigo))

    def getTableBobinas(self):
        return self.dbMGR.getTable("bobinas",)
    
    def getTableBobinas_OP(self):
        return self.dbMGR.getTable_2("bobinas","op")
    
    def getproductos_by(self,columna,filtro):
        return self.dbMGR.getProduct_by(columna,filtro)
    
    def getProduct_By(self,filtro,valor):
        result,tabla = self.dbMGR.getTableByRow("productos",filtro,valor)
        return tabla

    def getTableClients(self):
        return self.dbMGR.getTable("clientes")

    def getTableProducts(self):
        return self.dbMGR.getTable("productos")
    
    def getProductFromCode(self,code):
        table = []
        table = self.dbMGR.getProductFromCodeDB(code)
        table = table[0]
        return table

    def getAProduct(self,p_code):
        row = []
        result,row = self.dbMGR.getTableByRow("productos","codigo_producto",p_code)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                row = row[0]
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return row

    def obtenerPesoycantidadporOP(self,op):
        return self.dbMGR.sumarpesoycantidadbobinas(op)
    
    def obtenerPaletaFinalOp(self,op):
        return self.dbMGR.getLastPalletOp(op)

    def getAProductByName(self,p_name):
        row = []
        result,row = self.dbMGR.getTableByRow("productos","producto",p_name)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                row = row[0]
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return row

    def getAClient(self,c_id):
        row = []
        result,row = self.dbMGR.getTableByRow("clientes","id",c_id)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                row = row[0]
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return row

    def getAnOp(self,op):
        table = []
        result,table = self.dbMGR.getTableByRow("bobinas","op",op)
        #print(f"Tabala con Tara: {table}")
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                table = table[0]
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        #print(f"Tabla en getAnop: {table}")
        return table
    
    def getProductRowByOPDB(self,opRow):
        table = []
        table = self.dbMGR.productByRow(opRow)
        table = table[0]
        return table
    
    def getClientfromIDDB(self,clientid):
        table = []
        table = self.dbMGR.clientID(clientid)
        table = table[0]
        return table

    def getAnTicket(self,ticket):
        table = []
        result,table = self.dbMGR.getTableByRow("proceso_bobina","ticket",ticket)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                table = table[0]
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return table
    
    def getTicketByOP(self,op):
        table = []
        result,table = self.dbMGR.getTableByRow("proceso_bobina","op",op)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                table = table
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return table
    
    def getTicketByPaleta(self,paleta):
        table = []
        result,table = self.dbMGR.getTableByRow("proceso_bobina","n_paleta",paleta)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                table = table
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return table
    
    def actualizarTaraOP(self,op,tara):
        result = self.dbMGR.actualizarColumna("bobinas","tara",tara,"op",op)
        return result

    def getTicketByNum(self,num):
        table = []
        result,table = self.dbMGR.getTableByRow("proceso_bobina","ticket",num)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                table = table
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return table
    
    def getTicketByFicha(self,ficha):
        table = []
        result,table = self.dbMGR.getTableByRow("proceso_bobina","ficha",ficha)
        #print("\n","Success getting row for op = ",op," with row ",table,"\n")
        if result:
            try:
                table = table
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return table

    def getAnClient_byname(self,name):
        #print("Obteniendo cliente desde Nombre")
        table = []
        result,table = self.dbMGR.getTableByRow("clientes","cliente",name)
        #print("\n","Success getting row for op = ",codeId," with row ",table,"\n")
        if result:
            table = table[0]
        else:
            pass
            #print("can't get all from database for code=",codeId)
        return table


    def getAnClient(self,codeId):
        table = []
        result,table = self.dbMGR.getTableByRow("clientes","id",codeId)
        #print("\n","Success getting row for op = ",codeId," with row ",table,"\n")
        if result:
            table = table[0]
        else:
            pass
            #print("can't get all from database for code=",codeId)
        return table

    def getAnProduct(self,code):
        table = []
        result,table = self.dbMGR.getTableByRow("productos","codigo_producto",code)
        #print("\n","Success getting row for code = ",code," with row ",table,"\n")
        if result:
            table = table[0]
        else:
            pass
            #print("can't get all from database for code=",code)
        return table

    def saveProduct(self,data):
        result = False
        result = self.dbMGR.insertRow("productos",PRODUCTOS,list(data))
        if result:
            #print("ticket saved on DB") 
            pass 
        else:
            pass
            #print("can't save the ticket on database")
        return result 

    def saveProduct_2(self,data):
        result = False
        result = self.dbMGR.insertRow("productos",PRODUCTOS,list(data))
        if result:
            #print("ticket saved on DB")  
            pass
        else:
            pass
            #print("can't save the ticket on database")
        return result
        
    def getOpsOnDB(self):
        bobinas = []
        result,bobinas = self.dbMGR.getTable("bobinas")
        if result:
            #print("success getting bobinas: ",bobinas)
            pass
        else:
            bobinas = []
            #print("can't store the data on database")
        return result,bobinas


    def getProductsOnDB(self):
        products = []
        result,products = self.dbMGR.getTable("productos")
        if result:
            pass
        else:
            products = []
        return result,products
    
    def getProductsOnDB_BYORDER(self):
        products = []
        result,products = self.dbMGR.getTable_andOrder("productos","codigo_producto")
        if result:
            pass
        else:
            products = []
        return result,products
    
    def countBobinasPalletNew(self,op,nPallet):
        result,products = self.dbMGR.getBobinasPallet_(op,nPallet)
        if result:
            pass
        else:
            products=[]
        return products
    
    def sumarPesosBobinasPaleta(self,columna,op,paleta):
        result,resultado = self.dbMGR.sumarColumnaPesoBobinas(columna,"op",str(op),"n_paleta",str(paleta))
        if result:
            pass
        else:
            resultado = 0
        return resultado

    def countBobinasPalletNew_Deleted(self,op,nPallet):
        result,products = self.dbMGR.getBobinasPalletDeleted_(op,nPallet)
        if result:
            pass
        else:
            products=[]
        return products

    def saveClient(self,data):
        result = False
        result = self.dbMGR.insertRow("clientes",CLIENTES,list(data))
        if result:
            #print("ticket saved on DB")  
            pass
        else:
            #print("can't save the ticket on database")
            pass
        return result 


    def getClientsOnDB(self):
        clients = []
        result,clients= self.dbMGR.getTable("clientes")
        if result:
            pass
        else:
            clients = []
        return result,clients

    def saveUsr(self,data):
        result = False
        #self.currentUser = {"id":dbId,"cedula":dbCedula,"usuario":dbUsername,"nombre":dbName,"apellido":dbApellido,"ficha":dbFicha,"password":dbPassWord,"email":dbEmail,"nivel":dbNivel,"turno":dbTurno,"supervisor":dbSupervisor}
        # data = [cedula,usr,name,lastName,ficha,passWord,email,level,turn,supervisor]
        if str(self.currentUser['nivel']).upper().replace(" ","") == 'ADMINISTRADOR':
            data[1] = hashlib.sha256(str(data[1]).encode()).hexdigest()
            data[5] = hashlib.sha256(str(data[5]).encode()).hexdigest()
            result = False
            result,usrs = self.dbMGR.getTable("usuarios")
            index = 0
            #print("result: ",result,usrs)
            if result and len(usrs)>0:
                index = len(usrs)
                data.insert(0,index)
                #print("data usr:",data)
            result = self.dbMGR.insertRow("usuarios",USUARIOS,list(data))
            if result:
                #print("user saved on DB")  
                pass
            else:
                #print("can't save the user on database")
                pass
        else:
            print("you have no access to save new users on db")
            self.sessionClose()
        return result 


    def getUsrOnDB(self):
        usuarios = []
        result, usuarios= self.dbMGR.getTable("usuarios")
        if result:
            #print("success getting usuarios: ",usuarios)
            pass
        else:
            usuarios = []
            #print("can't store the data on database")
        return result,usuarios

    # coils means tickets on DB.
    def getCoilsOPonDB(self,op):
        coils = []
        result, coils= self.dbMGR.getcoilsOP(op)
        if result:
            pass
            #print("success getting coils: ",coils)
        else:
            coils = []
            #print("can't store the data on database")
        return result,coils
    
    def getUserbylevel(self,nivel):
        result, users = self.dbMGR.getTable("usuarios",nivel)
        names = [i[3]+" "+i[4] for i in users]
        #print(names)
        return names
    
    def getUserbyName(self,name,lastname):
        result, users = self.dbMGR.gettablebytwo("usuarios","nombre","apellido",name,lastname)
        #names = [i[3]+" "+i[4] for i in users]
        #print(names)
        return users

    def getCoilsByOpandPallet(self,op,pallet):
        return self.dbMGR.getTableBy2Rows("proceso_bobina","op",op,"n_paleta",pallet)

    def getCoilsOnDB(self):
        coils = []
        result, coils= self.dbMGR.getTable("proceso_bobina")
        if result:
            pass
            #print("success getting coils: ",coils)
        else:
            coils = []
            #print("can't store the data on database")
        return result,coils
    
    def getTheSameCoils(self,op):
        table = []
        table = self.dbMGR.samecoils(op)
        #table = table[0]
        return table
    
    def getTheSameCoilsPallet(self,op,actualPallet):
        table = []
        table = self.dbMGR.samecoilsPallet(op,actualPallet)
        #table = table[0]
        #print(f"Tabla en samecoilspallet ventanaMGR: {table}")
        return table

    def saveHablador(self,data):
        success = self.dbMGR.insertRow("habladores",HABLADORES,list(data))
        if success:
            #print("data habladores:",data) 
            pass
        else:
            #print("can't save the hablador on database")
            pass
        return success
    
    def getCurrentOp(self):
        return self.pesajeWidget.getCurrentOp()
    
    def obtenerBobinas_reporte(self,fecha_inicio_,hora_inicio,fecha_final_,hora_final,ficha):
        hora_inicio = hora_inicio.replace(" ","")
        hora_final = hora_final.replace(" ","")
        if len(hora_inicio)<7:
            hora_inicio = "0" + hora_inicio
        if len(hora_final)<7:
            hora_final = "0" + hora_final
        #print(f"Hora inicio: {hora_inicio}")
        #print(f"Hora final: {hora_final}")
        # Definir las fechas de inicio y fin como objetos date
        fecha_inicio = datetime.strptime(fecha_inicio_, '%Y-%m-%d').date()
        fecha_fin = datetime.strptime(fecha_final_, '%Y-%m-%d').date()

        # Restar y sumar días para obtener los nuevos límites del rango
        fecha_inicio_modificado = fecha_inicio + timedelta(days=1)  # Resta 1 día
        fecha_fin_modificado = fecha_fin + timedelta(days=-1)  # Suma 1 día

        # Formatear las fechas modificadas como cadenas en el formato YYYY-MM-DD
        fecha_inicio_modificado_str = fecha_inicio_modificado.strftime('%Y-%m-%d')
        fecha_fin_modificado_str = fecha_fin_modificado.strftime('%Y-%m-%d')

        # Formatear las horas como cadenas en el formato HH:MM:SS AM
        hora_inicio_modificada = hora_inicio[:2] + ":" + hora_inicio[3:5] + ":00 " + hora_inicio[5:]
        hora_final_modificada = hora_final[:2] + ":" + hora_final[3:5] + ":00 " + hora_final[5:]
        tabla = []
        if ((hora_inicio_modificada == "18:00:00 PM" and hora_final_modificada == "06:00:00 AM") or (hora_inicio_modificada == "22:15:00 PM" and hora_final_modificada == "06:00:00 AM")):
            horario_nocturno = True
        else:
            horario_nocturno = False
        #print(f"Horario nocturno: {horario_nocturno}")
        if ficha == "GENERAL":
            where = f"(( fecha_emision='{fecha_inicio}' and hora>='{hora_inicio}') or (fecha_emision='{fecha_fin}' and hora<='{hora_final}'))"
        else:
            #print((fecha_fin - fecha_inicio).days)
            if (fecha_fin - fecha_inicio).days > 1 and horario_nocturno == False:
                #print("Más de un día de diferencia y horario nocturno")
                where = f"""(
                    (
                    -- Rango de fechas general, con un rango de horas general aplicado
                ((fecha_emision BETWEEN '{fecha_inicio_}' AND '{fecha_fin}') AND (hora >= '{hora_inicio_modificada}' and hora<='{hora_final_modificada}'))

                    AND 
                    -- ficha de operador
                    (ficha='{ficha}')
                )
                )"""
            elif (fecha_fin - fecha_inicio).days > 1 and horario_nocturno == True:
                where = f"""(
                -- Rango de horas para la primera fecha (aplicado solo a esta fecha)
                ((fecha_emision = '{fecha_inicio}' AND hora >= '{hora_inicio_modificada}')
                OR
                -- Rango de horas para la última fecha (aplicado solo a esta fecha)
                (fecha_emision = '{fecha_fin}' AND hora <= '{hora_final_modificada}')
                OR
                -- Rango de fechas general, con un rango de horas general aplicado
                ((fecha_emision BETWEEN '{fecha_inicio_modificado_str}' AND '{fecha_fin_modificado_str}') AND ((hora>='{hora_inicio_modificada}') or (hora<'{hora_final_modificada}'))))
                AND
                -- ficha de operador
                (ficha='{ficha}')
                )"""
                #print(where)
            else:
                if horario_nocturno == True:
                    #print("Mismo día o 1 día de diferencia horario nocturno")
                    where = f"""(
                    -- Rango de horas para la primera fecha (aplicado solo a esta fecha)
                    ((fecha_emision = '{fecha_inicio}' AND hora >= '{hora_inicio_modificada}')
                    OR
                    -- Rango de horas para la última fecha (aplicado solo a esta fecha)
                    (fecha_emision = '{fecha_fin}' AND hora <= '{hora_final_modificada}')) 
                    AND 
                    -- ficha de operador
                    (ficha='{ficha}')
                    )"""
                    #print(where)
                elif horario_nocturno == False:
                    #print("Mismo dia o 1 dia de diferencia horario normal")
                    where = f"""(
                    (
                    -- Rango de fechas general, con un rango de horas general aplicado
                    ((fecha_emision BETWEEN '{fecha_inicio_}' AND '{fecha_fin}') AND (hora >= '{hora_inicio_modificada}' and hora<='{hora_final_modificada}'))

                    AND 
                    -- ficha de operador
                    (ficha='{ficha}')
                )
                )"""
                    #print(where)
            #print(where)
        tabla = self.dbMGR.Obtenter_Tabla_condicionada("proceso_bobina"," * ",where)
        #print(f"Tabla reporte: {tabla}")
        return tabla
    

    # This will update the local product list from DB.
    def updateProductsFromDB(self):
        self.pesajeWidget.updateProductsFromDB()

    # This will update the local client list from DB.
    def updateClientsFromDB(self):
        self.pesajeWidget.updateClientsFromDB()

    # This will update the local client list from DB.
    def updateOpsFromDB(self):
        self.pesajeWidget.updateOpList()

    def updatePalletValue(self):
        pass

    def updateBobinaOnDB(self,ticket,bobina):
        return self.dbMGR.updateValue("proceso_bobina",("bobina",bobina),("ticket",ticket))

    def updateMatrizOnDB(self,ticket,matriz):
        return self.dbMGR.updateValue("proceso_bobina",("bobina",matriz),("ticket",ticket))

    def updateBxPOnDB(self,op,bobPallet):
        return self.dbMGR.updateValue("bobinas",("bobinas_paleta",bobPallet),("op",op))

    def updateAmtPalletsOnDB(self,op,amtPallet):
        return self.dbMGR.updateValue("bobinas",("paletas_total",amtPallet),("op",op))

    def updateActualPalletOnDB(self,op,nPallet):
        return self.dbMGR.updateValue("bobinas",("paleta_actual",nPallet),("op",op))

    def updateBobMatrizOnDB(self,ticket,bobMatriz):
        return self.dbMGR.updateValue("proceso_bobina",("bobina_matriz",bobMatriz),("ticket",ticket))

    def updatePwOnDB(self,usuario,password):
        return self.dbMGR.updateValue("usuarios",("password",password),("usuario",usuario))

    def updateClient(self,upgradedClient):
        return self.dbMGR.updateRow("clientes",CLIENTES_UPDATE,upgradedClient,"id")

    def updateProducts(self,upgradedProduct):
        return self.dbMGR.updateRow("productos",PRODUCT_UPDATE,upgradedProduct,"codigo_producto")
    
    def actualizarProductos(self,codigo,data):
        #print("LLamando a actualizar Productos")
        return self.dbMGR.actualizar_fila("productos",codigo,data)

    def updateOp(self,upgradedOp):
        return self.dbMGR.updateRow("bobinas",BOBINAS_UPDATE,upgradedOp,"op")
    #############################################################################################
    # Piezas ####################################################################################
    #############################################################################################
    def getAPieza(self,op):
        table = []
        result,table = self.dbPiezaMGR.getTableByRow("piezas","op",op)
        #print("\n","Success getting piezas row for op = ",op," with row ",table,"\n")
        if result:
            try:
                table = table[0]
            except:
                pass
        else:
            pass
            #print("can't get all from database for op=",op)
        return table

    def getAllPiezasByOp(self,op):
        success,rows = self.dbPiezaMGR.getTableByRow('proceso_pieza','op',op)
        return rows

    def getAllPiezas(self):
        piezas = []
        result,piezas = self.dbPiezaMGR.getTable("piezas")
        if result:
            pass
        else:
            piezas = []
        return piezas

    def get_piezas_by_op_and_caja(self,op,caja_actual):
        results = self.dbPiezaMGR.getTableBy2Rows('proceso_pieza','op',op,'n_caja',caja_actual)
        return results

    def getAnTicketPieza(self,ticket):
        table = []
        result,table = self.dbPiezaMGR.getTableByRow("proceso_pieza","ticket",ticket)
        #print("\n","Success getting ticekt pieza with => ",table,"\n")
        if result:
            try:
                table = table[0]
            except:
                pass
        else:
            print("can't get all from database for op=",ticket)
        return table

    def getPiezaTicketsOnDB(self):
        tickets = []
        result,tickets = self.dbPiezaMGR.getTable("proceso_pieza")
        #tickets = list(tickets[0])
        if result:
            #print("Success getting ticekts with: ",tickets)
            pass
        else:
            print("can't get tickets on db")
            pass
        return result,tickets

    def storePiezaTicket(self,data):
        result = False
        result = self.dbPiezaMGR.insertRow("proceso_pieza",PROCESO_PIEZA,list(data))
        if result:
            print("Pieza ticket saved on DB")  
        else:
            print("Can't save the pieza ticket on database")
        return result

    def storePiezaOp(self,data):
        result = self.dbPiezaMGR.insertRow("piezas",PIEZAS,data)
        if result:
            print("Pieza op data stored on db")  
        else:
            print("can't store pieza the data on database")   
        return result

    def updateBultoOnDB(self,op,bulto_act): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("updating=> op:",op," Bulto actual:",bulto_act)
        self.dbPiezaMGR.updateValue("piezas",("bulto_actual",bulto_act),("op",op)) # value,key(or path)

    def updatePaquetesOnDB(self,op,paquetes): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("Updating=> op:",op," Paquetes:",paquetes)
        self.dbPiezaMGR.updateValue("piezas",("paquetes",paquetes),("op",op)) # value,key(or path)

    def updatePiezaXBultoOnDB(self,op,pieza_x_bulto): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("updating=> op:",op," BXP actual:",pieza_x_bulto)
        self.dbPiezaMGR.updateValue("piezas",("pieza_bulto",pieza_x_bulto),("op",op)) # value,key(or path)

    def updateBultoTotalOnDB(self,op,bulto_total): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("updating=> op:",op," Bulto actual:",bulto_total)
        self.dbPiezaMGR.updateValue("piezas",("bultos_total",bulto_total),("op",op)) # value,key(or path)

    def updatePalletPiezaOnDB(self,op,paleta_actual): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("updating=> op:",op," Paleta actual:",paleta_actual)
        self.dbPiezaMGR.updateValue("piezas",("paleta_actual",paleta_actual),("op",op)) # value,key(or path)

    def updateCajaPiezaOnDB(self,op,caja_actual): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("updating=> op:",op," Caja actual:",caja_actual)
        self.dbPiezaMGR.updateValue("piezas",("caja_total",caja_actual),("op",op)) # value,key(or path)

    def updateCajaOnDB(self,op,caja_actual): # UPDATE bobinas SET 4.55 = ? WHERE tara=?;
        #print("updating=> op:",op," Caja actual:",caja_actual)
        self.dbPiezaMGR.updateValue("piezas",("caja_actual",caja_actual),("op",op)) # value,key(or path)

    def incBoxOnDB(self,op):
        result = False
        opRow = self.getAPieza(op)
        if len(opRow)>0:
            old_cajas= int(opRow[4])
            actual_cajas = old_cajas + 1
            result = self.updateCajaOnDB(op,actual_cajas)
        return result

    ########################################################################################################
    # END ##################################################################################################
    ########################################################################################################

    def incPalletOnDB(self,op,nPallet):
        result = False
        opRow = self.getAnOp(op)
        if len(opRow)>0:
            oldPallets = int(opRow[4])
            actualPallet = oldPallets + 1
            result = self.updateActualPalletOnDB(op,actualPallet)
        return result

    def deleteTicketOnDB(self,key,value):
        result = False
        result= self.dbMGR.deleteRow("proceso_bobina",key,value)
        if result:
            print("success deleting ticket where key:",key," value:",value)
        else:
            result = False
            #print("can't store the data on database")
        return result

    def deleteTicketsOnDB(self,key,value):
        result = False
        result= self.dbMGR.deleteRow("proceso_bobina",key,value)
        if result:
            print("success deleting ticket where key:",key," value:",value)
        else:
            result = False
            #print("can't store the data on database")
        return result

    def deleteClientOnDB(self,key,value):
        result = False
        result = self.dbMGR.deleteRow("clientes",key,value)
        if result:
            print("success deleting client where key:",key," value:",value)
        else:
            result = False
            #print("can't store the data on database")
        return result

    def deleteProductOnDB(self,key,value):
        result = False
        result = self.dbMGR.deleteRow("productos",key,value)
        if result:
            print("success deleting product where key:",key," value:",value)
        else:
            result = False
            #print("can't store the data on database")
        return result

    def deleteOpOnDB(self,key,value):
        result = False
        result = self.dbMGR.deleteRow("bobinas",key,value)
        if result:
            print("success deleting op where key:",key," value:",value)
        else:
            result = False
            #print("can't store the data on database")
        return result

    def updateComPort(self):
        self.provider.connectToBal1()
        self.provider.connectToBal2()



 