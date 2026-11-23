from components.clasess import Action
from components.functions import lookForClient,lookForProduct,isIp,comNameToPort,getModeMeasure

def actionAccept(obj):
    if obj.action.id == "CONFIRM_PALLET":
        print("pallet confirmed!!!")
        pesajeObject = obj.action.obj
        mgrObj = pesajeObject.objmgr
        op = pesajeObject.lineOp.currentText()
        actualPallet = pesajeObject.linePaletaAct.text()
        
        has_ticket = pesajeObject.palletHasTicket()

        resultIncPallet = False
        if has_ticket:
            # verify first the number of pallets registered
            opRow = mgrObj.getAnOp(op)
            numPallet = opRow[2] # This is the total of pallets for this op
            cuNumPallet = opRow[4]
            print("numPallet=>",numPallet," cuNumPallet=>",cuNumPallet)
            if numPallet <= cuNumPallet:
                print("You are trying to close this pallet out of range registered!!!")
                mgrObj.showExeedPalletWindow(Action("EXEED_PALLET",mgrObj),numPallet)
            else:
                resultIncPallet = mgrObj.incPalletOnDB(op,actualPallet)
                if resultIncPallet:
                    obj.action.obj.actionPallet()
                    pesajeObject.updateScreenValues()
                    print("success inc pallet for current op",resultIncPallet)
                else:
                    print("can't make increment over the pallet!!!",resultIncPallet) 
        else:
            print("you have to print at least one ticket to close this pallet my friend!")
    elif obj.action.id == "CONFIRM_PRINT":
        obj.action.obj.actionPrintPallet()
    elif obj.action.id == "INPUT_MATRIZ":
        
        pesajeObject = obj.action.obj
        mgrObj = pesajeObject.objmgr
        try:
            print("input matriz accepted!!!")
            mgrObj.bobinaMatriz = int(obj.input.text())
            print("bobina matriz guardada..., ",mgrObj.bobinaMatriz)


            # Cargo el diccionario actual de la bobina
            bobMatriz = mgrObj.bobinaMatriz
            fields = pesajeObject.readFieldsBobina()
            print("Result reading database \n",fields,"\n setting main coil with ",bobMatriz)
            if len(fields)>0:
                fields["bobMatriz"] = str(bobMatriz)
                mgrObj.setData(fields)
                # Envio la impresion del ticket
                mgrObj.printBobina()

                mgrObj.showPrintingWindow(pesajeObject.actionBobina)
                
                # cierro la ventana emergente de notificacion
                #self.objmgr.closePrintingWindow() #closing with timer
                # make all verifications here... 
                #  
            else:
                pass
                #print("some error printing coils....")  
        except Exception as e:
            print(e)
            pass
    elif obj.action.id == "EXEED_PALLET":
        mgrObj = obj.action.obj
        pesajeObject = mgrObj.getPesajeWidget()
        op = pesajeObject.lineOp.currentText()
        opRow = mgrObj.getAnOp(op)
        actualPallet = opRow[5]
        #
        resultIncPallet = mgrObj.incPalletOnDB(op,actualPallet)
        if resultIncPallet:
            pesajeObject.actionPallet()
            pesajeObject.updateScreenValues()
            print("success inc pallet for current op",resultIncPallet)
        else:
            print("can't make increment over the pallet!!!",resultIncPallet) 
    elif obj.action.id == "EXEED_BOBINA":
        pesajeObj = obj.action.obj
        pesajeObj.initPrint()

    elif obj.action.id == "CONFIRM_PALLET_HABLADOR":
        obj.action.obj.objmgr.showCreateHabladorWindow(Action("CREATE_HABLADOR",obj.action.obj))
    elif obj.action.id == "CREATE_HABLADOR":
        obj.action.obj.objmgr.showInsertHabladorWindow(Action("INPUT_HABLADOR",obj.action.obj))
    elif obj.action.id == "EDIT_CLIENT":
        nameClient = obj.clientName.text()
        print("client edited! ",lookForClient(nameClient))            
    elif obj.action.id == "DELETE_CLIENT":
        nameProduct = obj.productName.text()
        print("client deleted!",lookForProduct(nameProduct))
    elif obj.action.id == "SAVE_CONFIG":
        configObj = obj.action.obj
        mgrObj = obj.action.obj.objmgr 

        printerName = configObj.comboPrinters.currentText()
        mgrObj.printerName = printerName
        printerName2 = configObj.comboTickers.currentText()
        mgrObj.printerName2 = printerName2
        namePort = comNameToPort(configObj.portB1.currentText())
        namePort2 = comNameToPort(configObj.portB2.currentText())
        serverIp = configObj.serverIp.text()
        serverPort = configObj.serverPort.text()
        userServer = configObj.userServer.text()
        passServer =  configObj.passServer.text()
        mode = configObj.mode.currentText()  
        mode_adobe = configObj.modeAdobe.isChecked()
        path_adobe = configObj.pathAdobe.text()

        dbIp = configObj.ipDB.text()
        dbPort = configObj.portDB.text()
        userDB = configObj.userDB.text()
        passDB = configObj.passDB.text()

        if not isIp(serverIp):
            serverIp = "127.0.0.1"  

        if not isIp(dbIp):
            dbIp = "127.0.0.1"  

        modeB1 = str(getModeMeasure(configObj.modeB1.currentText()))
        modeB2 = str(getModeMeasure(configObj.modeB2.currentText()))
        #print("storing on DB b1=>",modeB1," modeB2=>",modeB2)
        #("127.0.0.2","8080","admin","admin","Microsoft Print To Pdf","Microsoft Print To Pdf","Manual","COM1","COM2","default")
        data = (serverIp,serverPort,userServer,passServer,printerName,printerName2,mode,namePort,namePort2,modeB1,modeB2,mode_adobe,path_adobe,"default")
        print("To be stored =>",data)
        if mgrObj.storeConfig(data):
            configObj.saveModePorts()
            configObj.saveComPort("BALANZA1",namePort)
            configObj.saveComPort("BALANZA2",namePort2)
            mgrObj.printerName = printerName
            mgrObj.updateComPort()
            mgrObj.printerName2 = printerName2
            mgrObj.modeAdobe = mode_adobe
            mgrObj.pathAdobe = path_adobe
            print("Se ha guardado la configuracion en la base de datos\n",data)
        else:
            print("No se pudo establecer la configuracion en la base de datos")
    elif obj.action.id == "NEW_OP":
        mgrObj = obj.action.obj.objmgr
        mgrObj.enableOp()
        mgrObj.setResponsePopUp(True)
        obj.loop.exit()
        print("you have accepted to create a new op!!!",mgrObj.isEnableOp())
    ##########################################################################
    # PIEZA ACTIONS ##########################################################
    ##########################################################################
    elif obj.action.id == 'CLOSE_BOX':
        mgrObject = obj.action.obj.objmgr
        piezaObject = obj.action.obj
        op = piezaObject.lineOp.currentText()
        mgrObject.incBoxOnDB(op) # increment caja on piezas
        # Action was comfirmed !!! and you have to ask for print plegadizo list
        mgrObject.killCloseBoxWindow()
        mgrObject.showPrintPlegadizoWindow(Action("PRINT_PLEGADIZO",piezaObject))
        obj.loop.exit()
    elif obj.action.id == 'NEW_PIEZA':
        mgrObj = obj.action.obj.objmgr
        mgrObj.enableOp()
        mgrObj.setResponsePopUp(True)
        print("you have accepted to create a new op in pieza!!!",mgrObj.isEnableOp())
        obj.loop.exit()
    elif obj.action.id == 'PRINT_PLEGADIZO':
        print('you accepted to print plegadizo report!!!!')
        mgrObject = obj.action.obj.objmgr
        mgrObject.printPlegadizo() # data have to be set before print the report, first make sure you have set it...
        obj.loop.exit()
    #########################################################################
    # END ###################################################################
    #########################################################################
    obj.close()
    pass