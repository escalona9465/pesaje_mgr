############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from ast import Try
from unittest import result
from components.imports.popUp import *
from components.functions import (getCoilsByOperator,getProductByOp,getDataDetailed,
    getTotalByOperator,getFullDate,getUsrFromTable,getDataTurn,getCoilsInRange,getFullDate,
    getTotalsForPallet,getTicketsForPallet,getTheSameCoils,getClientfromId,getLastClient,
    getClientfromName,seekTicketsByOp,seekTicketsByNumero,seekTicketsByFicha,seekTicketsByPaleta,
    changeToSuccess,changeToError,changeToNormal,getTheSameCoilsPallet,getRowFromItems,
    getTicketsByOpPlusPallet,countToTickets,getProductRowFromItems,getTicketsForCaja,
    countBobinasPallet,appendTableOp,getCoilsInDate,get_match_index,getDataTurnNew)

from components.componentsPopup.restorePassword import restorePassword

from components.componentsPopup.deleteTicket import *
from components.interfaces.mensajes import *
import hashlib
from components.interfaces.dialogos import *
from datetime import timedelta


class PopUp(QWidget):
    def __init__(self,objectName,type,action,op=None) -> None:

        super().__init__()
        
        self.width_ = 0
        self.height_ = 0

        self.action = action
        
        self.name = objectName
        
        self.setObjectName(objectName)
        
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.setWindowIcon(getPopUpIcon())
        
        if type == MODE_WAIT:
            waitWindow(self)
        elif type == MODE_CONFIRM:
            confirmWindow(self)
        elif type == MODE_ACCEPT:
            acceptWindow(self)
        elif type == MODE_INPUT:
            inputWindow(self)
        elif type == MODE_INPUT_MATRIZ:
            inputMatriz(self)
        elif type == MODE_INPUT_HABLADOR:
            inputHablador(self)
        elif type == MODE_INPUT_ORDER:
            inputOrder(self)
        elif type == MODE_REPORT_OP:
            reportOp(self)
        elif type == MODE_REPORT_PALLET:
            reportPallet(self)
        elif type == MODE_REPORT_PIEZA:
            reportPieza(self)
        elif type == MODE_ADD_CLIENT: 
            addClient(self)
        elif type == MODE_ADD_PRODUCT:
            addProduct(self)
        elif type == MODE_EDIT_PRODUCT:
            editProduct(self)
        elif type == MODE_EDIT_CLIENT: 
            editClient(self)
        elif type == MODE_DELETE_CLIENT:
            deleteClient(self)
        elif type == MODE_DELETE_PRODUCT:
            deleteProduct(self)
        elif type == MODE_EDIT_OP:
            editOp(self)
        elif type == MODE_DELETE_OP:
            deleteOp(self)
        elif type == MODE_ADD_OP:
            addOp(self,op)
        elif type == MODE_CONFIRM_CONFIG:
            confirmConfig(self)
        elif type == MODE_REPORT_TICKET:
            reportTicket(self)
        elif type == MODE_ADD_USR:
            addUsr(self)
        elif type == MODE_DELETE_TICKET:
            deleteTicket(self)
        elif type == MODE_RESTORE_PASSWORD:
            restorePassword(self)

        self.mainLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.mainLayout)    

    ####################################################
    # ELEMENTS FOR PLEGADIZO PREVIEW ###################
    ####################################################
    def printPlegadizoGenerated(self):
        self.action.obj.printPlegadizo()

    def generateAndPrintPlegadizo(self):
        self.generate()
        self.printPlegadizoGenerated()

    def previewPlegadizo(self):
        # First hide form fields
        # After tha create preview
        mgrObject = self.action.obj
        self.generate() 
        mgrObject.createPlegadizoPreview()
        # update object
        self.web.getPreview().loadView()
        mgrObject.reportPlegadizoWindow.setSize(570,660)
        self.stackedLayout.setCurrentIndex(1) # go to web preview
        self.moveToCenter()

    def nombresPaletas(self):
        mgrObject = self.action.obj
        consulta_lista_paletas = mgrObject.obtenerPaletasEmbalaje()
        lista_paletas = [pallet[0] for pallet in consulta_lista_paletas]
        consulta_pesos_paletas = mgrObject.obtenerPaletasPeso()
        pesos_paletas = [pallet[0] for pallet in consulta_pesos_paletas]
        lista_paletas_final = []
        for i in range(len(consulta_lista_paletas)):
            paleta = lista_paletas[i] + " / " + str(pesos_paletas[i]) + " KG"
            lista_paletas_final.append(paleta)
        #print(f"Lista paletas: {lista_paletas_final}")
        return lista_paletas_final

    def setPallet(self):
        mgrObject = self.action.obj
        self.paleta_seleccionada = (self.tipoPalletBox.currentText()).split(" / ")
        self.nombre_paleta_seleccionada = self.paleta_seleccionada[0]
        self.peso_paleta_seleccionada = (self.paleta_seleccionada[1]).split(" KG")
        self.pesoPaleta = self.peso_paleta_seleccionada[0]
        #print(f"Paleta seleccionada: {self.nombre_paleta_seleccionada} y Peso: {self.pesoPaleta}")
        mgrObject.paletaEmbalaje = float(self.pesoPaleta)

    def returnToFormPlegadizo(self):
        mgrObject = self.action.obj
        mgrObject.reportPlegadizoWindow.setSize(480,280)
        self.stackedLayout.setCurrentIndex(0) # go to web preview
        self.moveToCenter()
        
    ###########################################################################
    # ELEMENTS FOR PALLET PREVIEW #############################################
    ###########################################################################
    def previewPallet(self):
        if self.nroOp.text() != "" and self.nroOp.text() != " " and self.nroPallet.text() != "" and self.nroPallet.text() != " " and self.tipoPalletBox.currentText() != "" and self.tipoPalletBox.currentText() != " ":
            # First hide form fields
            # After tha create preview
            mgrObject = self.action.obj
            self.generate() 
            mgrObject.createPalletPreview()
            # update object
            self.web.getPreview().loadView()
            mgrObject.ReportPalletWindow.setSize(570,660)
            self.stackedLayout.setCurrentIndex(1) # go to web preview
            self.moveToCenter()

    def printPalletGenerated(self):
        self.action.obj.printPallet()
    
    def generateAndPrintPallet(self):
        self.generate()
        self.printPalletGenerated()

    def returnToFormPallet(self):
        mgrObject = self.action.obj
        mgrObject.ReportPalletWindow.setSize(480,280)
        self.stackedLayout.setCurrentIndex(0) # go to web preview
        self.moveToCenter()

    # ELEMENTS FOR TURN REPORT PREVIEW

    def previewTurn(self):
        # First hide form fields
        # After tha create preview
        mgrObject = self.action.obj
        self.generate() 
        mgrObject.createTurnPreview()
        # update object
        self.web.getPreview().loadView()
        mgrObject.reportOperatorWindow.setSize(570,660)
        self.stackedLayout.setCurrentIndex(1) # go to web preview
        self.moveToCenter()

    def printTurnGenerated(self):
        self.action.obj.printTurn()
    
    def generateAndPrintTurn(self):
        self.generate()
        self.printTurnGenerated()

    def returnToFormTurn(self):
        mgrObject = self.action.obj
        mgrObject.reportOperatorWindow.setSize(440,280)
        self.stackedLayout.setCurrentIndex(0) # go to web preview
        self.moveToCenter()

    # ELEMENTS FOR HABLADOR REPORT PREVIEW

    def previewHabl(self):
        # First hide form fields
        # After tha create preview
        mgrObject = self.action.obj.objmgr # reading from menu ui
        self.generateHablador() 
        mgrObject.createHablPreview()
        # update object
        self.web.getPreview().loadView()
        mgrObject.insertHablador.setSize(360,280)
        self.stackedLayout.setCurrentIndex(1) # go to web preview
        self.moveToCenter()

    def printHablGenerated(self):
        self.printHablador()
    
    def generateAndPrintHabl(self):
        self.generateHablador()
        self.printHablador()

    def returnToFormHabl(self):
        mgrObject = self.action.obj.objmgr # reading from menu ui
        mgrObject.insertHablador.setSize(500,320)
        self.stackedLayout.setCurrentIndex(0) # go to web preview
        self.moveToCenter()

    def setSize(self,width,height):
        self.width_ = width
        self.height_ = height
        self.resize(QSize(width,height))
        self.setMaximumHeight(height)
        self.setMinimumHeight(height)
        self.setMaximumWidth(width)
        self.setMinimumWidth(width)

    def setMessage(self,text):
        self.message.setText(text)

    def accept(self):
        actionAccept(self) 

    def generateHablador(self):

        check2 = self.inputPos.text().isnumeric()
        #posicion = self.inputPos.text()

        mgrObject = self.action.obj.objmgr  

        op = mgrObject.getCurrentOp()

        #opRow = mgrObject.getAnOp(op)
        #successCoils,process = mgrObject.getCoilsOnDB()
        #successProducts,products = mgrObject.getProductsOnDB()

        #position = getPosByOp(opRow,op)
        #product = getProductByOp(opRow,products,op)
        #cantidad = getAmtByOp(process,op)
        # [op,position,product,cantidad]
        product = ""
        if mgrObject.getModePrintHablador() == 1:
            op = str(self.arrHablador[0])
            position = str(self.arrHablador[1])
            product = str(self.arrHablador[2])
            cantidad = str(self.arrHablador[3])
        elif mgrObject.getModePrintHablador() == 2:
            op = self.inputOp.text()
            opRow = mgrObject.getAnOp(op)
            # if op exist
            if len(opRow)>0:
                success2,products = mgrObject.getProductsOnDB()
                product,productCode = getProductByOp(opRow,products,op)            
            position = self.inputPos.text()            
            cantidad = self.inputAmt.text()

        check4 = not self.inputObs.text().isnumeric()
        observaciones = self.inputObs.text()

        self.hablador = {
            "op":op,
            "product":product,
            "position":position,
            "amount":cantidad,
            "observations":observaciones
        }

        if check2 and check4:
            mgrObject.setHablador(self.hablador)
            mgrObject.createHablPreview()
            # HERE WAS ETHE OLD PRINT STATEMENTS

        elif not check2:
            pass
            ##print("el valor introducido en la posicion no es numerico")
        elif check4:
            pass
            ##print("el valor introducido en la observacion no puede ser numerico")

    def printHablador(self):
        if self.action.id == "INPUT_HABLADOR":
            self.action.obj.actionHablador(self.hablador)
        elif self.action.id == "GENERATE_HABLADOR":
            pesajeWidget = self.action.obj.objmgr.getPesajeWidget()
            pesajeWidget.actionReHablador(self.hablador)

    def custom(self):
        pass

    def generalClicked(self):

        op = self.inputOp.text()
        mgrObject = self.action.obj
        ops = mgrObject.getAnOp(op) # this is a row not matrix
        productCode = ops[8]
        tara = ops[1]
        product = mgrObject.getAnProduct(productCode)
        clientCode = product[3]
        ##print("success getting client code ",clientCode)
        client = mgrObject.getAnClient(clientCode)

        #resultCoils,coils = mgrObject.getCoilsOnDB()
        ##print("looking for op general:",op)

        ficha = mgrObject.getUser()["ficha"]
        #accum,counter = getTotalByOperator(ficha,coils)
        bobinas_op = mgrObject.obtenerPesoycantidadporOP(op)
        #print(bobinas_op)
        accum = bobinas_op[0]
        counter = bobinas_op[1]
        nPaletas = mgrObject.obtenerPaletaFinalOp(op)[3]
        #print(nPaletas)
        # productId or code
        dataGeneralOp = {
            "op" : str(op), 
            "clientId" : str(client[1]),
            "clientName" : str(client[2]),
            "productName" : str(product[1]),
            "productId" : str(product[0]),
            "nPaletas" : str(nPaletas),
            "bxPaletas" : str(ops[3]),
            "total" :"{:4.2f}".format(float(accum)),
            "units" : str(counter),
        }
        #print(dataGeneralOp)
        mgrObject.setData(dataGeneralOp)
        resultPrint = mgrObject.printGeneral()
        #print("result printing general=> ",resultPrint)
        self.close()


    def detailedClicked(self):
        op = self.inputOp.text()
        mgrObject = self.action.obj

        ops = mgrObject.getAnOp(op) # this is a row not matrix
        ##print("Looking for detailed clicked => ",ops," for op =>",op)
        productCode = ops[8]
        tara = ops[1]
        product = mgrObject.getAnProduct(productCode)
        ###print("get product result: ",product)
        clientCode = product[3]
        client = mgrObject.getAnClient(clientCode)
        ###print("get client result: ",client)

        resultCoils, sameCoils = mgrObject.dbMGR.getcoilsOP(op)
        resultUsr,users = mgrObject.getUsrOnDB() # check if report need users or client names
        #resultClient,clients = mgrObject.getClientsOnDB()
        dataDetailed = []
        if resultCoils and len(client)>0 and len(ops) and len(product):
            dataDetailed = getDataDetailed(sameCoils,tara,users)
        ##print("looking for op detailed:",op," result ",dataDetailed)

        dataDetailedOp = {
            "op" : str(op), 
            "clientId" : str(client[1]),
            "clientName" :str(client[2]),
            "productName" : str(product[1]),
            "productId" : str(product[0]),
            "data":dataDetailed
        }
        #print("dataDetailed=>",dataDetailedOp)
        ##print(dataDetailed)
        mgrObject.setData(dataDetailedOp)
        resultPrint = mgrObject.printDetailed()
        #print("printing detailed result=>",resultPrint)
        self.close()
        pass

    def setTitle(self,title):
        self.title.setText(title)
        pass


    def waitBalanza(self):
        if self.action.id == "WAIT_BALANZA":
            ##print("")
            pass

    def generate(self):
        if self.action.id == "REPORT_OPERATOR":
            
            fromDate = self.fromOp.text()
            initHora = self.fromTime.text()
            toDate = self.toInputOp.text()
            endHora = self.toTime.text()
            turno = self.turno.currentText()
            
            initHora = turno.split("-")[0]
            endHora = turno.split("-")[1]

            print("fromDate:",fromDate," fromTime:",initHora," toDate:",toDate," toTime:",endHora)
            operator = self.operador.currentText()
            print(f"Texto en seleccion: {self.turno.currentText()}")
            if str(operator).upper().replace(" ","") == "GENERAL":
                mgrObject = self.action.obj
                reportTurn = {
                    "dateInit" : fromDate +" "+ initHora,
                    "dateEnd" : toDate +" "+ endHora,
                    "dateToday" : str(getFullDate()),
                    "numOp" : "", # ficha, acum ficha from users row
                    "nameOp" : "", # fullName, acum names from users 
                    "total" : "", # str(totalUnd), acum here
                    "weight" : "",# str(totalKgOp)
                    "op" : "",
                    "header" : [" LOTE "," CLIENTE "," PRODUCTO "," Piezas "," Kg/op "],
                    "data"  : [], # dataTurn        
                }
                #
                numOp_ = ""
                nameOp_ = ""
                resultBobinas,arrBobinas = mgrObject.getOpsOnDB()
                print("1")
                resultClients,arrClients = mgrObject.getClientsOnDB()
                print("2")
                resultProducts,arrProducts = mgrObject.getProductsOnDB()
                print("3")
                dataTurn = []
                totalUnd = 0.0
                totalKgOp = 0.0
                baseProcess = mgrObject.dbMGR.Obtenter_Tabla_condicionada(
                    "proceso_bobina", "*", f"fecha_emision BETWEEN '{fromDate}' AND '{toDate}'"
                )
                for k in range(1,len(self.users)):
                    userRow = self.users[k] 
                    nameOp_ = nameOp_ + str(userRow[3]) +" "+ str(userRow[4]) + "\n"
                    numOp_ = numOp_ + str(userRow[5]) + "\n"
                    arrProcess = baseProcess
                    print(f"Texto en seleccion: {self.turno.currentText()}")
                    if self.turno.currentText() != "TURNO-COMPLETO":
                        arrProcess = getCoilsInRange(fromDate,toDate,initHora,endHora,arrProcess)
                    else:
                        arrProcess = getCoilsInDate(fromDate,toDate,arrProcess)
                    arrProcess = getCoilsByOperator(arrProcess,str(userRow[5]).replace(" ",""))
                    dt,tu,to = getDataTurn(arrBobinas,arrProcess,arrClients,arrProducts,str(userRow[5]))
                    
                    dataTurn.append([str(userRow[5]),str(userRow[3]),str(userRow[4]),"","-1"])

                    dataTurn = dataTurn + dt

                    dataTurn.append([" Unidades: "+str(tu),"        Total: "+"{:4.2f}".format(float(to))+" ","","","-2"])
                    #print("dt=>",dataTurn)
                    totalUnd = totalUnd + tu
                    totalKgOp = totalKgOp + to   
                    #print("\nfor:",self.users[k]," Data:",dataTurn," Total Und.:",tu," Total Kg:",totalKgOp,"\n")
                reportTurn['numOp'] = numOp_
                reportTurn['nameOp'] = nameOp_
                reportTurn['total'] = str(totalUnd)
                reportTurn['weight'] = str(totalKgOp)
                reportTurn['data'] = dataTurn
                self.action.obj.setData(reportTurn)
            else:
                stringName = operator.split()
                firstName,lastName = stringName[0],stringName[1]
                mgrObject = self.action.obj
                userRow = mgrObject.getUserbyName(firstName,lastName)[0]
                #print(userRow)
                #userRow = getUsrFromTable(self.users,operator)
                fullName = str(userRow[3]) +" "+ str(userRow[4])
                ficha = str(userRow[5])
                
                #resultBobinas,arrBobinas = mgrObject.getOpsOnDB()
                """resultProcess,arrProcess = mgrObject.getCoilsOnDB()

                if self.turno.currentText() != "TURNO-COMPLETO":
                    arrProcess = getCoilsInRange(fromDate,toDate,initHora,endHora,arrProcess)
                else:
                    arrProcess = getCoilsInDate(fromDate,toDate,arrProcess)
                arrProcess = getCoilsByOperator(arrProcess,ficha)
                resultClients,arrClients = mgrObject.getClientsOnDB()
                resultProducts,arrProducts = mgrObject.getProductsOnDB()"""
                fulldate = getFullDate()
                #arrBobinas = mgrObject.
                dataTurn = []
                dataTurn,totalUnd,totalKgOp = getDataTurnNew(mgrObject,fromDate,initHora,toDate,endHora,ficha)
                #dataTurn,totalUnd,totalKgOp = getDataTurn(arrBobinas,arrProcess,arrClients,arrProducts,ficha)
                reportTurn = {
                    "dateInit" : fromDate +" "+ initHora,
                    "dateEnd" : toDate +" "+ endHora,
                    "dateToday" : fulldate,

                    "numOp" : ficha,
                    "nameOp" : fullName,

                    "total" : str(totalUnd),
                    "weight" : str(totalKgOp),

                    "op" : "",
                    "header" : [" LOTE "," CLIENTE "," PRODUCTO "," Piezas "," Kg/op "],

                    "data"  : dataTurn,        
                }
                self.action.obj.setData(reportTurn)


        elif self.action.id =="REPORT_PALLET":
            
            
            mgrObject = self.action.obj

            op = self.nroOp.text()
            pallet = self.nroPallet.text()

            opRow = mgrObject.getAnOp(op)
            #successCoils, coils = mgrObject.getCoilsOnDB()
            #resultClients,arrClients = mgrObject.getClientsOnDB()
            #resultProducts,arrProducts = mgrObject.getProductsOnDB()

            productCode = str(opRow[8])
            bobinas = 0 #str(opRow[3])
            paletas = str(pallet) #str(opRow[2]) # cambio a paleta actual 03/6/22
            userName = mgrObject.getUser()["nombre"] + " " + mgrObject.getUser()["apellido"] #mgrObject.getUser()["usuario"]

            date = getFullDate()

            #coilsForPallet = getTheSameCoils(coils,op)
            #coilsForPallet = getTheSameCoilsPallet(coils,op,pallet)
            coilsForPallet = mgrObject.countBobinasPalletNew(op,pallet)
            pesoBruto = mgrObject.sumarPesosBobinasPaleta("peso_bruto",op,pallet)[0]
            pesoNeto = mgrObject.sumarPesosBobinasPaleta("peso_neto",op,pallet)[0]
            #pesoBruto, pesoNeto = getTotalsForPallet(coilsForPallet)
            bobinas,dataPallet = getTicketsForPallet(coilsForPallet)

            #product,productCode = getProductByOp(opRow,arrProducts,op)
        
            productRow = mgrObject.getAnProduct(productCode)
            clientId = productRow[3] # product[3] represents the client_id column
            clientRow = mgrObject.getClientfromIDDB(clientId)
            
            tara = str(opRow[1])

            supervisor = mgrObject.getSupervisor()
            print(f"Peso bruto: {pesoBruto}\nPeso Neto: {pesoNeto}")
            dataPallet = {
                "date" : date,
                "clientCode" : str(clientRow[1]),
                "client" : str(clientRow[2]),
                "tara":tara,
                "productCode" : productCode,
                "product" : productRow[1],
                "bobinas" : str(bobinas),
                "pesoBruto" : str(pesoBruto),
                "pesoNeto" : str(pesoNeto),
                "paletas" : paletas,
                "usr" : userName,
                "mgrCode" : "MGR-GPR-F19(Ed.01)",
                "op" : op,
                "header" : [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]],
                "data"  : dataPallet,
                "supervisor"  : supervisor
            }

            #print("dataPallet=>",dataPallet)
            self.action.obj.setData(dataPallet)
            #self.action.obj.printPallet()

        elif self.action.id =="REPORT_TICKET":
            op = self.nroOp.text()
            ticket = self.nroPallet.text()
            # look for data pallet on DB, change example data.
            self.action.obj.setData(dataExampleBobina)
            self.action.obj.printPallet()
            ##print("Report pallet => op:",op," ticket:",ticket)
            pass
        elif self.action.id == "REPORT_PLEGADIZO":

            mgrObject = self.action.obj

            op = self.nroOp.text()
            caja = self.nroCaja.text()

            opRow = mgrObject.getAPieza(op)
            
            piezas = mgrObject.get_piezas_by_op_and_caja(op,caja) # The same piezas for op and caja !!!

            p_code = str(opRow[6])
            userName = mgrObject.getUser()["nombre"] + " " + mgrObject.getUser()["apellido"] #mgrObject.getUser()["usuario"]

            date = getFullDate()

            bultos_total,piezas_total,dataCaja = getTicketsForCaja(piezas)

            productRow = mgrObject.getAProduct(p_code)
            product = productRow[1]
            c_id = productRow[3]
            clientRow = mgrObject.getAClient(c_id)
            
            supervisor = mgrObject.getSupervisor()
       
            dataCaja = {
                "date" : date,
                "clientCode" : str(clientRow[1]),
                "client" : str(clientRow[2]),
                "productCode" : p_code,
                "product" : product,
                "bultos_total" : bultos_total,
                "piezas_total" : piezas_total,
                "mgrCode" : "MGR-GPR-F19(Ed.01)",
                "op" : op,
                "caja" : caja,
                "header" : [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]],
                "data"  : dataCaja,
                "usr" : userName,
                "supervisor"  : supervisor
            }
            #print("dataCaja=>",dataCaja)
            self.action.obj.setData(dataCaja)

    def closeEvent(self, event):
        ##print("You have closed the sub-window!")
        return super().closeEvent(event)

    def saveOp(self):
        mgrObject = self.action.obj

        op = self.op.text()
        productName = self.productName.currentText()
        codigo = self.code.currentText()

        amtPallets = self.pallets.text()
        bxPallets = self.bxPallets.text()
        
        clientName = ""
        tara = str(self.currentTara)
        actualPallet = ""
        matriz = ""
        hablador = ""
        totalOp = ""

        dataOp = (op,tara,amtPallets,bxPallets,1,matriz,hablador,totalOp,codigo)
        #print("dataOp=>",dataOp)
        opRow = mgrObject.getAnOp(op)
        result = mgrObject.storeOp(dataOp)
        #print(f"{self.currentTara > 0.05} and {len(opRow) <= 0}")
        if len(opRow) <= 0:
            if result:
                print("Op added!",[op,clientName,productName,codigo,amtPallets,bxPallets])
                self.message.setText("Se ha guardado con exito la op.")
                self.message.show()
                changeToSuccess(self.message)
                self.timer.singleShot(6000,self.hideMessage)
                self.timer.singleShot(6001,self.changeToNormalMessage)
                self.configureOpTable()
                self.loadOps()
            else:
                self.message.setText("No se ha podido guardar la OP seleccionada.")
                self.message.show()
                changeToError(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage)
        else:
            self.message.setText("Esta OP ya se encuantra registrada.")
            self.message.show()
            changeToError(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)
        #self.close()

    def _deleteOp(self):

        mgrObject = self.action.obj

        #success,self.ops = mgrObject.getOpsOnDB()

        #indexes = self.selectOps()
        op_seleccionada = self.table.currentRow()
        op = self.table.item(op_seleccionada,0).text()
        #print(f"Op a eliminar: {op} Tipo: {type(op)}")
        result = mgrObject.deleteOpOnDB("op",op)
        result2 = mgrObject.deleteTicketsOnDB("op",op)
        self.table.clear()
        self.items = []
        self.rowCount = 0
        self.configureOpTable()
        self.loadOps()

        """if len(indexes)>0:
            for k in range(len(indexes)):
                mgrObject = self.action.obj
                opRow = self.ops[indexes[k]] #self.products[indexes[k]] #[1]
                op = opRow[0] #self.products[indexes[k]][0]
                # look for ticket index because op doesn't represente a valid id.
                #print("Op to be deleted =>",op)
                result = mgrObject.deleteOpOnDB("op",op)
                # and delete all tickets with the same op
                result2 = mgrObject.deleteTicketsOnDB("op",op)
                #print("Result deleting op=> ",result)
                self.table.clear()
                self.items = []
                self.rowCount = 0
                self.configureOpTable()
                self.loadOps()"""
                
        if result:
            self.message.setText("Op deleted on db.")
            self.message.show()
            changeToSuccess(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)
        else:
            self.message.setText("Can't delete op from db.")
            self.message.show()
            changeToError(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)
        return result

    def modifyClient(self):
        mgrObject = self.action.obj
        resultUpdate = self.updateClients()
        if resultUpdate:
            # This wil replace the local list of clients with new changes at pesaje widget.
            mgrObject.updateClientsFromDB()

    def modifyProduct(self):
        mgrObject = self.action.obj
        resultUpdate = self.updateProducts()
        if resultUpdate:
            # This wil replace the local list of clients with new changes at pesaje widget.
            mgrObject.updateProductsFromDB()

    def new_modificar_producto(self):
        mgrObject = self.action.obj
        fila_seleccionada = self.table.currentRow()
        codigo = self.table.item(fila_seleccionada,2).text()
        print(f"Producto a modificar: {codigo}")
        descripcion_producto = self.table.item(fila_seleccionada,1).text()
        peso_maximo = self.table.item(fila_seleccionada,4).text()
        peso_minimo = self.table.item(fila_seleccionada,5).text()
        lista_actualizar = [descripcion_producto,peso_maximo,peso_minimo]
        actualizacion_correcta = mgrObject.actualizarProductos(codigo,lista_actualizar)
        if actualizacion_correcta:
            mgrObject.updateProductsFromDB()
            print("Producto actualizado correctamente")
            mensajeok = Mensajes("producto_actualizado")
            mensajeok.setWindowModality(Qt.ApplicationModal)
            mensajeok.show()
            mensajeok.exec_()
        else:
            print("Error al actualizar el producto")

    def _modifyOp(self):
        mgrObject = self.action.obj
        resultUpdate = self.updateOps() # Update Op List
        if resultUpdate:
            # This wil replace the local list of clients with new changes at pesaje widget.
            mgrObject.updateOpsFromDB() #self.updateOpList()

    def saveClient(self):
        nameClient = self.clientName.text()
        clientCode = self.code.text()
        description = self.description.text()
        # do here database operations
        mgrObject = self.action.obj
        success,clients = self.action.obj.getClientsOnDB()
        lastClient = getLastClient(clients)
        lastIndex = 0

        if len(lastClient):
            lastIndex = int(lastClient[0])
            print(f"Guardando cliente con id: {lastIndex + 1}")
        result = mgrObject.saveClient([(lastIndex + 1),clientCode,nameClient,description])
        if result:
            self.configureProductTable()
            self.loadClients()

            self.message.setText("Se ha eliminado el cliente seleccionado.")
            self.message.show()
            changeToSuccess(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)  
        else:
            self.message.setText("No se ha podido eliminar el cliente seleccionado.")
            self.message.show()
            changeToSuccess(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)                 

    def auto_fill_client(self):
        current_product_code = self.code.text()
        index = get_match_index(current_product_code,self.codes)
        if index != -1:
            self.clientName.setCurrentIndex(index)

    def saveProduct(self):
        result = True
        productName = self.productName.text()
        productCode = self.code.text()
        pesoMax = self.pesoMax.text()
        pesoMin = self.pesoMin.text()
        clientName = self.clientName.currentText()
        description = self.productDescription.text()
        mgrObject = self.action.obj
        #success,products = mgrObject.getProductsOnDB()
        #result,clients = mgrObject.getClientsOnDB()
        #index = len(products) + 1

        if result:
            #clientRow = getClientfromName(clients,clientName)
            #clientCode = clientRow[0]
            clientCode = mgrObject.getAnClient_byname(clientName)[0]
            result = mgrObject.saveProduct([productCode,productName,pesoMax,clientCode,pesoMin])
            if result:
                #self.configureProductTable()
                #self.loadProducts()

                self.message.setText("Se ha guardado el producto en la base de datos.")
                self.message.show()
                changeToSuccess(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage) 

            else:
                self.message.setText("No se ha guardado el producto en la base de datos.")
                self.message.show()
                changeToError(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage) 

            # this will update the local client list.
            mgrObject.updateProductsFromDB()
        else:
            print("Error obteniendo clientes")

    def saveUsr(self):
        name = self.name.text()
        lastName = self.lastName.text()
        cedula = self.cedula.text()
        usr = self.usr.text()
        ficha = self.ficha.text()
        passWord = self.passWord.text()
        confirmPassWord = self.confirmPassWord.text()
        email = self.email.text()
        level = self.level.currentText()
        turn = self.turn.currentText()
        supervisor = ""
        data = [cedula,usr,name,lastName,ficha,passWord,email,level,turn,supervisor]
        if passWord == confirmPassWord:
            ##print("Password success",data)
            mgrObject = self.action.obj
            result = mgrObject.saveUsr(data)
            if result:
                self.message.setText("Se ha guardado el usuario en la base de datos.")
                self.message.show()
                changeToSuccess(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage) 
            else:
                self.message.setText("No se ha guardado el usuario en la base de datos.")
                self.message.show()
                changeToError(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage) 
        else:
            pass
            ##print("password unmatch!!!")


    def updateFieldsByProduct(self):
        op = self.op.text()
        #print("sub-window op,",op)
        opNotExist = len(self.objmgr.getAnOp(op)) <= 0
        # if op doesn't exist you can't fill fiels from manual data.
        # only fill when not are saving data.
        if opNotExist:
            nameProduct = self.productName.currentText()
            Product = self.objmgr.getProduct_By("producto",nameProduct)
            #print(Product)
            codeProduct = Product[0][0]
            self.code.setCurrentText(str(codeProduct))
            #success,products = self.objmgr.getProductsOnDB()
            ##print("updating...,",nameProduct,"\nsuccess=>",success,"\nproducts=>",products)
            """if success:
                productRow = getProductFromName(products,nameProduct)
                ##print("product row,\n","row=>",productRow)
                if len(productRow)>0:
                    toWriteCode = productRow[0] # it represents the name of product
                    # update fields here
                    self.code.setCurrentText(toWriteCode)
                    #print("changin to => ",toWriteCode,nameProduct)"""

        
    def printReportPieza(self):
        op = self.nroOp.text()
        mgrObject = self.action.obj

        opRow = mgrObject.getAnOp(op)

        pallet = opRow[2] #self.nroPallet.text() check if this is like that
                          # You are taking the total of pallets, please check if need to take actual pallet instead.                         

        successCoils, coilsForPallet = mgrObject.dbMGR.getcoilsOP(op)
        resultClients,arrClients = mgrObject.getClientsOnDB()
        resultProducts,arrProducts = mgrObject.getProductsOnDB()

        productCode = str(opRow[8])
        bobinas = str(opRow[3])
        paletas = str(opRow[2])
        userName = mgrObject.getUser()["usuario"]

        date = getFullDate()

        pesoBruto, pesoNeto = getTotalsForPallet(coilsForPallet)
        dataPallet = getTicketsForPallet(coilsForPallet)

        product,productCode = getProductByOp(opRow,arrProducts,op)
        productRow = mgrObject.getAnProduct(productCode)
        clientId = productRow[3] # product[3] represents the client_id column
        clientRow = getClientfromId(arrClients,clientId)
        
        dataPallet = {
            "date" : date,
            "clientCode" : str(clientRow[1]),
            "client" : str(clientRow[2]),
            "productCode" : productCode,
            "product" : product,
            "bobinas" : bobinas,
            "pesoBruto" : str(pesoBruto),
            "pesoNeto" : str(pesoNeto),
            "paletas" : paletas,
            "usr" : userName,
            "mgrCode" : "MGR-GPR-F19(Ed.01)",
            "op" : op,
            "header" : [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]],
            "data"  : dataPallet
        }
        mgrObject.setData(dataPallet)
        mgrObject.printPallet()
        self.close()
        


    def buscarTicket(self):
        mgrObject = self.action.obj
        if self.filtroCombo.currentText() == "Número":
            tickets = mgrObject.getTicketByNum(self.valorLine.text())
        elif self.filtroCombo.currentText() == "OP":
            tickets = mgrObject.getTicketByOP(self.valorLine.text())
        elif self.filtroCombo.currentText() == "Paleta":
            tickets = mgrObject.getTicketByPaleta(self.valorLine.text())
        elif self.filtroCombo.currentText() == "Ficha":
            tickets = mgrObject.getTicketByFicha(self.valorLine.text())
        #print(f"tickets generales: {tickets}")
        if len(tickets)>0:
            self.table.clear()
            self.items = []
            self.table.setHorizontalHeaderLabels(["Ticket","Bruto","Neto","Paleta","Bob. Matriz","Fecha","OP","Ficha"])
            self.table.setRowCount(0)
            for ticket in tickets:
                #print(ticket)
                item_nro = QTableWidgetItem(str(ticket[0]))
                item_nro.setTextAlignment(Qt.AlignCenter)
                item_bruto = QTableWidgetItem(str(ticket[1]))
                item_bruto.setTextAlignment(Qt.AlignCenter)
                item_neto = QTableWidgetItem(str(ticket[2]))
                item_neto.setTextAlignment(Qt.AlignCenter)
                item_paleta = QTableWidgetItem(str(ticket[3]))
                item_paleta.setTextAlignment(Qt.AlignCenter)
                item_bmatriz = QTableWidgetItem(str(ticket[4]))
                item_bmatriz.setTextAlignment(Qt.AlignCenter)
                item_fecha = QTableWidgetItem(str(ticket[5]))
                item_fecha.setTextAlignment(Qt.AlignCenter)
                item_op = QTableWidgetItem(str(ticket[6]))
                item_op.setTextAlignment(Qt.AlignCenter)
                item_ficha = QTableWidgetItem(str(ticket[7]))
                item_ficha.setTextAlignment(Qt.AlignCenter)
                nueva_fila = self.table.rowCount()
                self.table.insertRow(nueva_fila)
                self.table.setItem(nueva_fila,0,item_nro)
                self.table.setItem(nueva_fila,1,item_bruto)
                self.table.setItem(nueva_fila,2,item_neto)
                self.table.setItem(nueva_fila,3,item_paleta)
                self.table.setItem(nueva_fila,4,item_bmatriz)
                self.table.setItem(nueva_fila,5,item_fecha)
                self.table.setItem(nueva_fila,6,item_op)
                self.table.setItem(nueva_fila,7,item_ficha)
        else:
            mensajeError = Dialog_msj("ticket_no_encontrado")
            mensajeError.setWindowModality(Qt.ApplicationModal)
            mensajeError.exec_()
            


    def seekTicket(self):
        op = self.op.text()
        checkOp = self.checkOp.isChecked()

        numero = self.numero.text()
        checkNumero = self.checkNumero.isChecked()

        ficha = self.ficha.text()
        checkFicha = self.checkFicha.isChecked()

        paleta = self.paleta.text()
        checkPaleta = self.checkPaleta.isChecked()

        mgrObject = self.action.obj
        if checkOp:
            result,self.tickets = mgrObject.dbMGR.getTableByRow("proceso_bobina","op",op)
        elif checkNumero:
            result,self.tickets = mgrObject.dbMGR.getTableByRow("proceso_bobina","ticket",numero)
        elif checkFicha:
            result,self.tickets = mgrObject.dbMGR.getTableByRow("proceso_bobina","ficha",ficha)
        elif checkPaleta:
            result,self.tickets = mgrObject.dbMGR.getTableByRow("proceso_bobina","n_paleta",paleta)
        else:
            result,self.tickets = False, []

        self.table.clear()
        self.items = []
        self.table.setHorizontalHeaderLabels(["Ticket","Bruto","Neto","Paleta","Bob. Matriz","Fecha","OP","Ficha"])
        self.rowCount = 0
        if len(self.tickets) > 0 and (checkOp or checkNumero or checkFicha or checkPaleta):
            for k in range(len(self.tickets)):
                dataRow = {"ticket":self.tickets[k][0],"bruto":self.tickets[k][1],"neto":self.tickets[k][2],"paleta":self.tickets[k][3],"bobMatriz":self.tickets[k][4],"fecha":self.tickets[k][5],"op":self.tickets[k][6],"ficha":self.tickets[k][7]}
                #print(dataRow)
                self.rowCount,self.items,self.table = appendTable(self.rowCount,self.columns,self.items,self.table,dataRow)
            
    def printTicket(self,modo=None):
        #checkOp = self.checkOp.isChecked()
        #checkNumero = self.checkNumero.isChecked()
        #checkFicha = self.checkFicha.isChecked()
        #checkPaleta = self.checkPaleta.isChecked()  

        #indexes = self.selectTickets()
        ticket = self.table.currentRow()
        print("indexes=>",ticket)
        
        mgrObject = self.action.obj
       # ticket = self.table(fila_seleccionada,0).text()

        mgrObject = self.action.obj

        op = str(self.table.item(ticket,6).text())
        opRow = mgrObject.getAnOp(op)
        productCode = opRow[8]
        productRow = mgrObject.getAnProduct(productCode)
        clientId = productRow[3]
        clientRow = mgrObject.getAnClient(clientId)
        user = mgrObject.getUser()
        #result,coils = mgrObject.getCoilsOnDB()
        ticketCode = str(self.table.item(ticket,0).text())
        bruto = str(self.table.item(ticket,1).text())
        tara = "" 
        neto = str(self.table.item(ticket,2).text())
        date = str(self.table.item(ticket,5).text()) # takes the date of the old ticket
        turno = user["turno"]
        bobinaMatriz = str(self.table.item(ticket,4).text())
        product = productRow[1]
        client = clientRow[2]
        operador = user["nombre"] + user["apellido"]
        pallet = str(self.table.item(ticket,3).text())
        coilsOp = mgrObject.getCoilsByOpandPallet(op,pallet)#getTicketsByOpPlusPallet(coils,op,pallet)

        bobina = countToTickets(ticketCode,coilsOp,op,pallet) #str(indexes[k] + 1) #countBobinasPallet(coils,op,pallet) # this is the number coil over the pallet

        success_deleted,deletedTickets = mgrObject.dbMGR.getTable("proceso_bobina_eliminados")  
        
        bobinas_eliminados =  countBobinasPallet(deletedTickets,op,pallet)

        total_bobinas = bobina + bobinas_eliminados

        print("for this op=> ",bobina," deleted=> ",bobinas_eliminados,"oprow=>",opRow)

        
        #bobina = countBobinasOp(coils,op) # this is the number coil over op
        reimpresion = getFullDate()
        if len(opRow)>0:
            if opRow[1] != None and opRow != "":
                # Establish a new tara in the register !!!
                tara = str(opRow[1])
                neto = str( float(bruto) - float(opRow[1]))
                #print("new tara=>",tara," neto=>",neto)

        if bobinaMatriz == "0":
            bobinaMatriz = ""
        dataTicket = {
        "code":productCode,
        "producto" : product,
        "client" : client,
        "operador" : operador,

        "reimpresion" : reimpresion,
        "bobMatriz" : bobinaMatriz,
        "bobina" : str( total_bobinas ),

        "turno" : str(turno),
        "op" : op,

        "neto" : neto,
        "bruto" : bruto,
        "tara" : tara,

        "date" : date,
        "ticketCode" : ticketCode,
        }
        #print(dataTicket)
        mgrObject.setData(dataTicket)
        if modo == "reimpresion":
            mgrObject.rePrintBobina()
            print("reimprimiendo")
            # if one has been selected show preview else print selected tickets
        else:
            mgrObject.printBobina()

        self.table.clear()
        self.items = []
        self.table.setHorizontalHeaderLabels(["Ticket","Bruto","Neto","Paleta","Bob. Matriz","Fecha","OP","Ficha"])
        self.rowCount = 0   

        ##print("printing ticket",checkOp,checkNumero,checkFicha,checkPaleta)


    def selectTicket(self):
        index = -1
        if len(self.items)>0:
            for i in range(int(len(self.items)/self.columns)):
                if self.items[i*self.columns].isSelected():
                    index = index
                    #print("seleccionado item ", index,":",str(self.items[i*self.columns].isSelected()))
                    #print("row=> ", self.tickets[int(index)])
                    pass    
                pass
        return index

    def selectTickets(self):
        indexs = []
        if len(self.items)>0:
            for i in range(int(len(self.items)/self.columns)):
                if self.items[i*self.columns].isSelected():
                    indexs.append(i)
                    #print("seleccionado item ", i,":",str(self.items[i*self.columns].isSelected()))
                    #print("row=> ", self.tickets[int(i)])
                    pass    
                pass
        return indexs

    def selectOps(self):
        indexs = []
        if len(self.items)>0:
            for i in range(int(len(self.items)/self.columns)):
                if self.items[i*self.columns].isSelected():
                    indexs.append(i)
                    #print("seleccionado item ", i,":",str(self.items[i*self.columns].isSelected()))
                    #print("row=> ", self.ops[int(i)])
                    pass    
                pass
        return indexs

    def updateProducts(self):
        nameProduct = self.productName.text()
        productCode = self.code.text()
        pesoMax = self.pesoMax.text()
        clientName = self.clientName.currentText() # to get client id from client name.
        mgrObject = self.action.obj
        result,arrClients = mgrObject.getClientsOnDB()
        clientRow =  getClientfromName(arrClients,clientName)
        clientId = clientRow[0]
       
        result = False
        result,self.products = mgrObject.getProductsOnDB()

        indexes = self.selectProducts()
        #print("Indexes updating clients=>",indexes)
        if len(indexes)>0:
            for k in range(len(indexes)):
                mgrObject = self.action.obj
                #client = self.clients[indexes[k]] # this is the client row.

                resultRow,upProduct = getProductRowFromItems(indexes[k],self.items) # assume that you are taking 4 columns as fixed parameter.
                if resultRow:
                    #clientCode = self.clients[indexes[k]][1]
                    codigoProducto = self.products[indexes[k]][0] # product
                    clientId = self.products[indexes[k]][3]
                    # You can change the all others fields. Keeps the old client id.
                    #(codigo_producto,product,peso_max,client_id)
                    ##print("this is nro. 0=>",upProduct[0])
                    ##print("this is product 1=>",upProduct[1])
                    ##print("this is codigo 2=>",upProduct[2])
                    ##print("this is id_client 3=>",upProduct[3])
                    dataDb = (upProduct[0],upProduct[1],upProduct[2],clientId,codigoProducto)
                    #print(dataDb)
                    # look for ticket index because op doesn't represente a valid id.
                    #print("product to be updated =>",codigoProducto," with =>",dataDb)
                    result = mgrObject.updateProducts(dataDb)
                    #print("result updating=> ",result)
                    if result:
                        self.message.setText("Se ha realizado los cambios en los clientes seleccionados.")
                        self.message.show()
                        changeToSuccess(self.message)
                        self.timer.singleShot(1500,self.hideMessage)
                        self.timer.singleShot(1501,self.changeToNormalMessage)
                    else:
                        self.message.setText("No se ha podido establecer el cliente en la base de datos.")
                        self.message.show()
                        changeToError(self.message)
                        self.timer.singleShot(1500,self.hideMessage)
                        self.timer.singleShot(1501,self.changeToNormalMessage)                        
                    #self.table.clear()
                    #self.items = []
                    #self.table.setHorizontalHeaderLabels(["Nro.","Cliente","Cod. cliente","Descripcion"])
                    #self.rowCount = 0
                else:
                    self.message.setText("Por favor seleccione toda la fila del cliente.")
                    self.message.show()
                    changeToError(self.message)
                    self.timer.singleShot(1500,self.hideMessage)
                    self.timer.singleShot(1501,self.changeToNormalMessage)
        return result

    def updateClients(self):
        nameClient = self.clientName.text()
        clientCode = self.code.text()
        description = self.description.text()
        mgrObject = self.action.obj

        
        #clientCode = self.clients[indexes[k]][1]
        fila_seleccionada = self.table.currentRow()
        clientId = self.table.item(fila_seleccionada,0).text()
        codigo_cliente = self.table.item(fila_seleccionada,2).text()
        nombre_cliente = self.table.item(fila_seleccionada,1).text()
        descripcion = self.table.item(fila_seleccionada,3).text()
        # it only keeps the client id. and you can change the all others fields.
        dataDb = (clientId,codigo_cliente,nombre_cliente,descripcion,clientId)
        #print(dataDb)
        # look for ticket index because op doesn't represente a valid id.
        #print("client to be updated =>",clientCode," with =>",dataDb)
        result = mgrObject.updateClient(dataDb)
        #print("result updating=> ",result)
        if result:
            self.message.setText("Se ha realizado los cambios en los clientes seleccionados.")
            self.message.show()
            changeToSuccess(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)

            self.configureClientTable()
            self.loadClients()
        else:
            self.message.setText("No se ha podido establecer el cliente en la base de datos.")
            self.message.show()
            changeToError(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)                        
        return result

    def updateOps(self):
        op = self.op.text()
        tara = self.tara.text()
        #productname = self.productName.currentText()
        codigo = self.code.currentText()
        #pallets = self.pallets.text()
        #codigoXpallets = self.bxPallets.text()
       
        mgrObject = self.action.obj
        #result,self.ops = mgrObject.getOpsOnDB()
        #indexes = self.selectOps()
        #print("Indexes updating ops=>",indexes)

        fila_seleccionada = self.table.currentRow()
        #["Nro.","Tara","Cod. Producto","# Paletas","# Bob. X Paletas"]
        op = self.table.item(fila_seleccionada,0).text()
        cu_op = self.table.item(fila_seleccionada,0).text()
        tara = self.table.item(fila_seleccionada,1).text()
        paletas_total = self.table.item(fila_seleccionada,3).text()
        bobinas_paleta = self.table.item(fila_seleccionada,4).text()
        paleta_actual = "1"
        matriz = "0"
        hablador = " "
        total_op = " "
        codigo = self.table.item(fila_seleccionada,2).text()
        # (13118314,0.6,4,20,1,"","","","FM0-MUN221042",13118314)
        dataDb = (op,tara,paletas_total,bobinas_paleta,paleta_actual,matriz,hablador,total_op,codigo,cu_op)
        #print(dataDb)
        # look for ticket index because op doesn't represente a valid id.
        #print("op to be updated =>",cu_op," with =>",dataDb)
        result = mgrObject.updateOp(dataDb)
        #print("result updating =>",result)
        if result:
            self.message.setText("Se han realizado los cambios en las ops seleccionadas.")
            self.message.show()
            changeToSuccess(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)
        else:
            self.message.setText("No se han podido modificar las ops seleccionadas.")
            self.message.show()
            changeToError(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)                        
        return result

    def selectClients(self):
        indexs = []
        #print("items selecting tickets=>",self.items)
        if len(self.items)>0:
            for i in range(int(len(self.items)/self.columns)):
                if self.items[i*self.columns].isSelected():
                    indexs.append(i)
                    #print("seleccionado item ", i,":",str(self.items[i*self.columns].isSelected()))
                    #print("row=> ", self.clients[i])
                    pass    
                pass
        return indexs

    def selectProducts(self):
        indexs = []
        #print("items selecting tickets=>",self.items)
        if len(self.items)>0:
            for i in range(int(len(self.items)/self.columns)):
                if self.items[i*self.columns].isSelected():
                    indexs.append(i)
                    #print("seleccionado item ", i,":",str(self.items[i*self.columns].isSelected()))
                    #print("row=> ", self.products[i])
                    pass    
                pass
        return indexs

    def selectProducts(self):
        indexs = []
        if len(self.items)>0:
            for i in range(int(len(self.items)/self.columns)):
                if self.items[i*self.columns].isSelected():
                    indexs.append(i)
                    #print("seleccionado item ", i,":",str(self.items[i*self.columns].isSelected()))
                    #print("row=> ", self.products[i])
                    pass    
                pass
        return indexs

    def deleteTicket(self):
        """checkOp = self.checkOp.isChecked()
        checkNumero = self.checkNumero.isChecked()
        checkFicha = self.checkFicha.isChecked()
        checkPaleta = self.checkPaleta.isChecked()"""    
        result = False
        #index = self.selectTicket()
        print("deleting tickets!!!")

        mgrObject = self.action.obj
        fila_seleccionada = self.table.currentRow()
        ticket = self.table.item(fila_seleccionada,0).text()
        # look for ticket index because op doesn't represente a valid id.
        #print("ticket to be deleted for =>",ticket)
        ticketRow = mgrObject.getTicketByNum(ticket)[0]
        result = mgrObject.deleteTicketOnDB("ticket",ticket)
        #print("ticketRow=>",ticketRow)
        resultStore = mgrObject.storeDeletedTicket(ticketRow)
        #print("result deleting=> ",result)
        self.table.clear()
        self.items = []
        self.table.setHorizontalHeaderLabels(["Ticket","Bruto","Neto","Paleta","Bob. Matriz","Fecha","OP","Ficha"])
        self.rowCount = 0
        return result

    def _deleteClient(self):
        nameClient = self.clientName.text()
        clientCode = self.code.text()
        description = self.description.text()
        mgrObject = self.action.obj
        result = False
        result,self.clients = mgrObject.getClientsOnDB()

        indexes = self.selectClients()
        #print("Indexes deleting tickets=>",indexes)

        if len(indexes)>0:
            for k in range(len(indexes)):
                mgrObject = self.action.obj
                clientCode = self.clients[indexes[k]][1]
                # look for ticket index because op doesn't represente a valid id.
                #print("client to be deleted for =>",clientCode)
                result = mgrObject.deleteClientOnDB("codigo",clientCode)
                #print("result deleting client=> ",result)
            if result:
                self.message.setText("Se han eliminado los tickets seleccionados.")
                self.message.show()
                changeToSuccess(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage)

                self.configureClientTable()
                self.loadClients()
            else:
                self.message.setText("No se han eliminado los tickets seleccionados.")
                self.message.show()
                changeToError(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage)
        return result

    def hideMessage(self):
        self.message.hide()
        #self.close()
    
    def showMessage(self):
        self.message.show()

    def changeToErrorMessage(self):
        changeToError(self.message)

    def changeToSuccessMessage(self):
        changeToSuccess(self.message)

    def changeToNormalMessage(self):
        changeToNormal(self.message)

    def _restorePassword(self):
        superUser = self.superUser.text()
        superPassword = self.superPass.text()
        user = self.user.text()
        password = self.password.text()
        confirm = self.confirmPassword.text()
        mgrObject = self.action.obj
        if mgrObject.login_SU((superUser,superPassword)):
            if password == confirm:
                user_encrypted = hashlib.sha256(user.encode()).hexdigest()
                password_encrypted = hashlib.sha256(password.encode()).hexdigest()
                result = mgrObject.updatePwOnDB(user_encrypted,password_encrypted)
                print(f"Result: {result}")
                if result:
                    self.message.setText("La contraseña se ha restablecido satisfactoriamente.")
                    self.message.show()
                    changeToSuccess(self.message)
                    self.timer.singleShot(1500,self.hideMessage)
                    self.timer.singleShot(1503,self.changeToNormalMessage)
                    #print("Restore password result =>",result," superUser:",superUser," superPass:",superPassword," user:",user," password:",password," confirm:",confirm)
                    
                    superUser = self.superUser.setText("")
                    superPassword = self.superPass.setText("")
                    user = self.user.setText("")
                    password = self.password.setText("")
                    confirm = self.confirmPassword.setText("")

                else:
                    self.message.setText("No se ha podido establecer la contraseña en la base de datos.")
                    self.message.show()
                    changeToError(self.message)
                    self.timer.singleShot(1500,self.hideMessage)
                    self.timer.singleShot(1503,self.changeToNormalMessage) 
                    superPassword = self.superPass.setText("")      
                    password = self.password.setText("")
                    confirm = self.confirmPassword.setText("")             
            else:
                #print("La contraseña de usuario no coincide.")
                self.message.setText("La contraseña de usuario no coincide.")
                self.message.show()
                changeToError(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1503,self.changeToNormalMessage)    
                password = self.password.setText("")
                confirm = self.confirmPassword.setText("")                
        else:
            #print("La contraseña de superusuario no coincide.")
            self.message.setText("La contraseña de superusuario no coincide.")
            self.message.show()
            changeToError(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)    
            superPassword = self.superPass.setText("")

    def loadClients(self):
        mgrObject = self.action.obj

        success,clients = mgrObject.getClientsOnDB()

        for k in clients:
            """dataClient = {
                "nro":str(clients[k][0]),
                "clientName":str(clients[k][2]),
                "clientCode":str(clients[k][1]),
                "description":str(clients[k][3])
            }"""
            item_nro = QTableWidgetItem(str(k[0]))
            item_nro.setTextAlignment(Qt.AlignCenter)
            item_name = QTableWidgetItem(str(k[2]))
            item_name.setTextAlignment(Qt.AlignCenter)
            item_code = QTableWidgetItem(str(k[1]))
            item_code.setTextAlignment(Qt.AlignCenter)
            item_description = QTableWidgetItem(str(k[3]))
            item_description.setTextAlignment(Qt.AlignCenter)
            nueva_fila = self.table.rowCount()
            self.table.insertRow(nueva_fila)
            self.table.setItem(nueva_fila,0,item_nro)
            self.table.setItem(nueva_fila,1,item_name)
            self.table.setItem(nueva_fila,2,item_code)
            self.table.setItem(nueva_fila,3,item_description)
            #self.rowCount,self.items,self.table = appendTable(self.rowCount,self.columns,self.items,self.table,dataClient) 
        for row in range(self.table.rowCount()):
            item = self.table.item(row,0)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            """item = self.table.item(row,2)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  
            item = self.table.item(row,3)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  """        

    def loadOps(self):
        mgrObject = self.action.obj

        success,self.ops = mgrObject.getOpsOnDB()
        arrOp = []
        for k in self.ops:
            # ["Nro.","Tara","Cod. Producto","# Paletas","# Bob. X Paletas"]
            """dataOp = {
                "nro":str(self.ops[k][0]),
                "tara":str(self.ops[k][1]),
                "codigo":str(self.ops[k][8]),
                "paletas":str(self.ops[k][2]),
                "bobxpallets":str(self.ops[k][3])
            }
            ##print("k:",k," ",dataOp)
            self.rowCount,self.items,self.table,lineOp = appendTableOp(self.rowCount,self.columns,self.items,self.table,dataOp)          
            arrOp.append(lineOp)"""
            item_nro = QTableWidgetItem(str(k[0]))
            item_nro.setTextAlignment(Qt.AlignCenter)
            item_tara = QTableWidgetItem(str(k[1]))
            item_tara.setTextAlignment(Qt.AlignCenter)
            item_code = QTableWidgetItem(str(k[8]))
            item_code.setTextAlignment(Qt.AlignCenter)
            item_paletas = QTableWidgetItem(str(k[2]))
            item_paletas.setTextAlignment(Qt.AlignCenter)
            item_bobpxpaletas =  QTableWidgetItem(str(k[3]))
            item_bobpxpaletas.setTextAlignment(Qt.AlignCenter)
            nueva_fila = self.table.rowCount()
            self.table.insertRow(nueva_fila)
            self.table.setItem(nueva_fila,0,item_nro)
            self.table.setItem(nueva_fila,1,item_tara)
            self.table.setItem(nueva_fila,2,item_code)
            self.table.setItem(nueva_fila,3,item_paletas)
            self.table.setItem(nueva_fila,4,item_bobpxpaletas)
       #self.arrOp = arrOp

    def loadProducts(self):

        mgrObj = self.action.obj
        result,self.products = mgrObj.getProductsOnDB_BYORDER()
        valor,clientes = mgrObj.getTableClients()
        #print(clientes)
        clientes_dic = {cliente[0]: cliente[2] for cliente in clientes}
        #print(clientes_dic)
        self.table.setRowCount(0)
        for i in self.products:
            """dataAddProduct = {
                "ID":self.products[i][3],
                "productName":self.products[i][1],
                "productCode":self.products[i][0],
                "clientName":clientes_dic[self.products[i][3]],
                "Pesomaximo":self.products[i][2],
                "Pesominimo":self.products[i][4]
            }"""
            item_ID = QTableWidgetItem(str(i[3]))
            item_ID.setTextAlignment(Qt.AlignCenter)
            item_name = QTableWidgetItem(str(i[1]))
            item_name.setTextAlignment(Qt.AlignCenter)
            item_code = QTableWidgetItem(str(i[0]))
            item_code.setTextAlignment(Qt.AlignCenter)
            item_client = QTableWidgetItem(str(clientes_dic[i[3]]))
            item_client.setTextAlignment(Qt.AlignCenter)
            item_peso_max =  QTableWidgetItem(str(i[2]))
            item_peso_max.setTextAlignment(Qt.AlignCenter)
            item_peso_min = QTableWidgetItem(str(i[4]))
            item_peso_min.setTextAlignment(Qt.AlignCenter)
            nueva_fila = self.table.rowCount()
            self.table.insertRow(nueva_fila)
            self.table.setItem(nueva_fila,0,item_ID)
            self.table.setItem(nueva_fila,1,item_name)
            self.table.setItem(nueva_fila,2,item_code)
            self.table.setItem(nueva_fila,3,item_client)
            self.table.setItem(nueva_fila,4,item_peso_max)
            self.table.setItem(nueva_fila,5,item_peso_min)
            #self.rowCount,self.items,self.table = appendTable(self.rowCount,self.columns,self.items,self.table,dataAddProduct)
        for row in range(self.table.rowCount()):
            item = self.table.item(row,0)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            item = self.table.item(row,2)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  
            item = self.table.item(row,3)
            if item:
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  
            

    def _deleteProduct(self):

        """productName = self.productName.text()
        productCode = self.code.text()
        pesoMax = self.pesoMax.text()
        clientName = self.clientName.currentText()
        description = self.productDescription.text()"""

        mgrObject = self.action.obj

        """success,self.products = mgrObject.getProductsOnDB()

        result,clients = mgrObject.getClientsOnDB()

        index = len(self.products) + 1

        indexes = self.selectProducts()

        if len(indexes)>0:
            for k in range(len(indexes)):
                mgrObject = self.action.obj
                productRow = self.products[indexes[k]] #[1]
                productCode = self.products[indexes[k]][0]"""
        fila_seleccionada = self.table.currentRow()
        productCode = self.table.item(fila_seleccionada,2).text()
        print(f"ProductCode: {productCode}")
        # look for ticket index because op doesn't represente a valid id.
        print("product to be deleted for =>",productCode)
        result = mgrObject.deleteProductOnDB("codigo_producto",productCode)
        #print("result deleting product=> ",result)
        if result:
            self.configureProductTable()
            self.loadProducts()
                
            if result:
                self.message.setText("Se han eliminado los productos seleccionados.")
                self.message.show()
                changeToSuccess(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage)
            else:
                self.message.setText("No se han eliminado los productos seleccionados.")
                self.message.show()
                changeToError(self.message)
                self.timer.singleShot(1500,self.hideMessage)
                self.timer.singleShot(1501,self.changeToNormalMessage)
        return result

    def moveToCenter(self):
        r = Responsive()
        left,right = r.getPosToCenter(self.width_,self.height_)
        point = QPoint(left,right)
        #point.setX(left)
        #point.setY(right)
        self.move(point)

    def configureProductTable(self):
        self.rowCount = 1
        self.columns = 6 # 4 columns on this table
        self.items = []
        self.products = []

        self.table.clear()
        self.table.setColumnCount(6) # 3 columns
        self.table.setRowCount(1) # 1 row
        self.table.clearContents() 
        self.table.setHorizontalHeaderLabels(["ID","Producto","Cod. Producto","Cliente","Peso Max","Peso Min"])

        self.table.setColumnWidth(0,20)
        self.table.setColumnWidth(1,180)
        self.table.setColumnWidth(2,100)
        self.table.setColumnWidth(3,180)
        self.table.setColumnWidth(4,80)
        #self.table.setColumnWidth(4,180)
        self.table.setSortingEnabled(True)

        headerTable = self.table.horizontalHeader()   
        headerTable.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)

    def configureClientTable(self):
        self.rowCount = 1
        self.columns = 4
        self.items = []
        self.clients = []

        self.table.clear()
        self.table.setColumnCount(4) # 5 columns
        self.table.setRowCount(1) # 1 row
        self.table.clearContents() 
        self.table.setHorizontalHeaderLabels(["Nro.","Cliente","Cod. cliente","Descripcion"])

        self.table.setColumnWidth(0,100)
        self.table.setColumnWidth(1,110)
        self.table.setColumnWidth(2,160)

        headerTable = self.table.horizontalHeader()   
        headerTable.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def configureOpTable(self):
        self.rowCount = 1
        self.columns = 5 # 5 columns on this table
        self.items = []
        self.ops = []

        self.table.setColumnCount(5) # 5 columns
        self.table.setRowCount(1) # 1 row
        self.table.clearContents() 
        self.table.setHorizontalHeaderLabels(["Nro.","Tara","Cod. Producto","# Paletas","# Bob. X Paletas"])

        self.table.setColumnWidth(0,100)
        self.table.setColumnWidth(1,80)
        self.table.setColumnWidth(2,200)
        self.table.setColumnWidth(3,100)
        self.table.setColumnWidth(4,100)

        headerTable = self.table.horizontalHeader()   
        headerTable.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        #headerTable.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

    def tareFromLine(self):
        tara = 0.0
        try:
            tara = float(self.tara.text())
            self.currentTara = tara
        except:
            self.message.setText("Por favor introduzca un valor numerico.")
            self.message.show()
            changeToError(self.message)
            self.timer.singleShot(1500,self.hideMessage)
            self.timer.singleShot(1501,self.changeToNormalMessage)

    def onOpCellChanged(self, row, column):
        item = self.table.item(row, column)
        valueItem = item.text()
        ##print("r:",row," c:",column," v:",valueItem)
        #if int(column) != 2: # You can change the product code
        try:
            self.arrOp[row][column] = valueItem
        except:
            pass
        ##print(self.arrOp)
        