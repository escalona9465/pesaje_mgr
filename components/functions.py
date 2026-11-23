############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.imports.functions import *
from PySide6 import QtWidgets
from datetime import date
import time
import calendar
from datetime import date
from components.dbHandler import DBHandler

# Only for dates with the format 2022-04-18
#def convertDateSpace(date,separator,newSeparator):
#    arrDate = date.split(separator)
#    return date[0] + newSeparator + date[2] + newSeparator + date[4]

######################################################
######### PIEZAS FUNCTIONS ###########################
######################################################
def is_caja_in_piezas(tickets_piezas,caja):
    result = False
    for row_pieza in tickets_piezas:
        ticket_caja = row_pieza[3] # n_caja
        if str(ticket_caja).replace(" ","") == str(caja).replace(" ",""):
            result = True
    return result

def getTicketsForCaja(piezas_op_caja):
    total_bultos = len(piezas_op_caja)
    total_piezas = 0
    dataCaja = []
    # [N&deg;. ,9. Paquetes,10. Piezas/Bulto,11. Piezas]
    if len(piezas_op_caja)<=40:
        for i in range(len(piezas_op_caja)):
            nro0 = str( piezas_op_caja[i][2] ) # Numero de bulto
            paquetes0 =  str(piezas_op_caja[i][10]) # paquetes
            piezas0 = str(piezas_op_caja[i][9])
            pieza_paquete_0 = ""
            try:
                total_piezas = total_piezas + int(piezas0)
                pieza_paquete_0 = '~' + str( int( int(str(piezas0).replace(" ",""))/int(str(paquetes0).replace(" ","")) ) )
            except:
                pass
            if piezas0 == "0" or piezas0 == " " or piezas0 == None:
                piezas0 = ""
            # [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]]
            line = [nro0,paquetes0,pieza_paquete_0,piezas0,"-","-","-","-"]
            dataCaja.append(line)
        for i in range(len(piezas_op_caja),40):
            line = ["-","-","-","-","-","-","-","-"]
            dataCaja.append(line)
    elif len(piezas_op_caja)>40:
        for i in range(40):
            nro0 = str( piezas_op_caja[i][9] ) # str(i+1) # Este es el numero de bobina de la paleta, asumiendo un correcto orden en la base de datos.
            paquetes0 = str(piezas_op_caja[i][10]) # paquetes
            piezas0 = str(piezas_op_caja[i][9])
            pieza_paquete_0 = ""
            try:
                pieza_paquete_0 = '~' + str( int( int(str(total_piezas).replace(" ",""))/int(str(paquetes0).replace(" ","")) ) )
            except:
                pass
            if piezas0 == "0"  or piezas0 == " " or piezas0 == None:
                piezas0 = ""
            nro1 = ""
            paquetes1 = ""
            pieza_paquete_1 = ""
            piezas1 = ""
            # if data exist append to other columnn not max of 80 tickets for op and table!!!
            if (i+40) < len(piezas_op_caja):
                nro1 = str( piezas_op_caja[i+40][9] ) # str(i+41)
                paquetes1 = str(piezas_op_caja[i+40][10]) # paquetes
            try:
                pieza_paquete_1 = '~' + str( int( int(str(piezas1).replace(" ",""))/int(str(paquetes1).replace(" ","")) ) )
            except:
                pass
                piezas1 = str(piezas_op_caja[i+40][9])
                try:
                    if piezas1 == "0"  or piezas1 == " " or piezas1 == None:
                        piezas1 = ""
                except:
                    pass
            # [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]]
            line = [nro0,paquetes0,pieza_paquete_0,piezas0,nro1,paquetes1,pieza_paquete_1,piezas1]
            try:
                total_piezas = total_piezas + int(piezas0)
            except:
                pass
            dataCaja.append(line)
    elif len(piezas_op_caja) == 0:
        for i in range(40):
            dataCaja.append([str(int(i + 1)),"-","-","-",str(int(i + 40 + 1)),"-","-","-"])

    return total_bultos,total_piezas,dataCaja

######################################################
######### END ########################################
######################################################

def getCurrentTime():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S %p", t)
    return str(current_time)

ALPHABETH = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def orderByAlphabeth2(__array__,__substr__):
    resultArray = []
    indexes = []
    for k in range(len(ALPHABETH)):
        for l in range(len(__array__)):
            try:
                if ALPHABETH[k] == list( __array__[l].replace(__substr__,"") )[0] and indexes.count(l)==0:
                    resultArray.append(__array__[l])
                    indexes.append(l)
            except:
                pass
        if len(indexes) == len(__array__):
            break
    return resultArray

def orderByAlphabeth(__array__,__substr__):
    #print(f"Array inicial: {__array__}")
    __array__.sort()
    #print(f"Array luego de sort: {__array__}")
    resultArray = __array__
    #print(f"Lista resultante: {resultArray}")
    return resultArray
    
def turnToDescription(turn):
    result = ""
    try:
        intTurn = str(turn)
    except:
        pass    
    print("turno=>",turn)
    if intTurn == "1" or intTurn == "PRIMER TURNO":
        result = "PRIMER TURNO"
    elif intTurn == "2" or intTurn == "SEGUNDO TURNOO" :
        result = "SEGUNDO TURNO"
    elif intTurn == "3" or intTurn == "TERCER TURNO" :
        result = "TERCER TURNO"
    elif intTurn == "" or intTurn == "EMPTY FIELD":
        result = "EMPTY FIELD"  
    return result

def lookForTicketOnPallet(op,pallet,tickets):
    result = False
    for k in range(len(tickets)):
        #print("comparing=>",str( tickets[k][3])," with ",str(pallet)," result=>",str( tickets[k][3]) == str(pallet))
        if str(tickets[k][6]) == str(op):
            if str( tickets[k][3]) == str(pallet):
                result = True
                #print("has countered a ticket ",tickets[k][0]," with pallet ",tickets[k][3]," ",pallet)
    return result

def getLastTicketOp(op,arrTickets):
    lastTicket = -1
    for k in range(len(arrTickets)):
        if str(arrTickets[k][6]) == str(op):
            if int(arrTickets[k][0]) > lastTicket:
                lastTicket =  int(arrTickets[k][0])
    return lastTicket


#def dateToDays(dd,mm,aa):
    #print("convertin day for =>"," dd:",dd," mm:",mm," aa:",aa)
    # 11:32:50 AM
    #current_year = int(date.today().year)
    #current_year = int(date.today().year)
    #month_range = calendar.monthrange(int(aa), int(mm))
    #month_days = int( month_range[1] )
    #print("month_range:",month_range," month_days:",month_days)
    #time_in_days = int(dd) + int(mm)*month_days + int(aa)*365
    #return time_in_days

#def dateToDays(dd,mm,aa):
    #print("convertin day for =>"," dd:",dd," mm:",mm," aa:",aa)
    # 11:32:50 AM
    #time_in_days = int(dd) + int(mm)*31 + int(aa)*365
    #return time_in_days

def is_bisiesto(year):
    return ( (year % 4) == 0 ) 

def get_days_by_month(year,month):
    year = int(str(year).replace(" ",""))
    month = int(str(month).replace(" ",""))
    if month == 1:
        return 31
    elif month == 2:
        if is_bisiesto(year):
            return 29
        else:
            return 28
    elif month == 3:
        return 31
    elif month == 4:
        return 30
    elif month == 5:
        return 31
    elif month == 6:
        return 30
    elif month == 7:
        return 31
    elif month == 8:
        return 31
    elif month == 9:
        return 30
    elif month == 10:
        return 31
    elif month == 11:
        return 30
    elif month == 12:
        return 31

def get_day_of_year(year):
    year = int(str(year).replace(" ",""))
    if is_bisiesto(year):
        return 366
    else:
        return 365
        
def get_days_till_month(year,month):
    year = int(str(year).replace(" ",""))
    month = int(str(month).replace(" ",""))
    acum_days = 0
    for k in range(1,month):
        acum_days = acum_days + get_days_by_month(year,k)
    return acum_days

def dateToDays(dd,mm,aa):
    #print("convertin day for =>"," dd:",dd," mm:",mm," aa:",aa)
    # 11:32:50 AM
    time_in_days = int(dd) + get_days_till_month(aa,mm) + int(aa)*get_day_of_year(aa)
    return time_in_days

def timeToSeconds(hh,mm,ss):
    #print("convertin day for =>"," dd:",dd," mm:",mm," aa:",aa)
    # 11:32:50 AM
    time_in_seconds = int(hh)*3600 + int(mm)*60 + int(ss)
    return time_in_seconds

def getCoilsInRange(initDate,toDate,initHora,endHora,arrProcess):
    inRangeProcess = []

    initHora = initHora.replace("AM","")
    initHora = initHora.replace("PM","")
    arrInitHour = str(initHora).split(":")
    hh_init = arrInitHour[0]
    min_init = arrInitHour[1]
    ss_init = "0" #arrInitHour[2].split(" ")[0]
    initSeconds = timeToSeconds(hh_init,min_init,ss_init)
    #print("hh_init=>",hh_init)
    #print("min_init=>",min_init)
    #print("ss_init=>",ss_init)
    #print("init_seconds=>",initSeconds)

    endHora = endHora.replace("AM","")
    endHora = endHora.replace("PM","")
    arrEndHour = str(endHora).split(":")
    hh_end = arrEndHour[0]
    min_end = arrEndHour[1]
    ss_end = "0" #arrEndHour[2].split(" ")[0]
    endSeconds = timeToSeconds(hh_end,min_end,ss_end)
    #print("initHora:",initHora," endHora:",endHora)
    #print("hh_end=>",hh_end)
    #print("min_end=>",min_end)
    #print("ss_end=>",ss_end)
    #print("end_seconds=>",endSeconds)

    #print(hh_init,min_init,ss_init ,hh_end,min_end,ss_end)
    arrInitDate = str(initDate).split("-")
    dd_init = arrInitDate[2]
    mm_init = arrInitDate[1]
    aa_init = arrInitDate[0]
    arrEndDate = str(toDate).split("-")
    dd_end = arrEndDate[2]
    mm_end = arrEndDate[1]
    aa_end = arrEndDate[0]
    initDays = dateToDays(dd_init,mm_init,aa_init)
    endDays = dateToDays(dd_end,mm_end,aa_end)
    for k in range(len(arrProcess)):
        currentHour = arrProcess[k][8]
        arrCurrentDate = str(arrProcess[k][5]).split("-")
        #print(arrCurrentDate)
        dd = arrCurrentDate[2]
        mm = arrCurrentDate[1]
        aa = arrCurrentDate[0]
        currentDays = dateToDays(dd,mm,aa)

        arrCurrentHour = str(currentHour).split(":")
        hh_current = arrCurrentHour[0]
        min_current = arrCurrentHour[1]
        ss_current = arrCurrentHour[2].split(" ")[0]
        currentSeconds = timeToSeconds(hh_current,min_current,ss_current)
        #print("hh_current=>",hh_current)
        #print("min_current=>",min_current)
        #print("ss_current=>",ss_current)
        #print("current_seconds=>",currentSeconds," init_seconds=>",initSeconds," end_seconds=>",endSeconds)

        

        #print("looking for =>",arrProcess[k])
        #print("\nlooking for current_days => ",currentDays," initDays =>",initDays," endDays:",endDays)
        #print("looking for in hour=> ",currentHour," current_seconds=>",currentSeconds," initSeconds =>",initSeconds," endSeconds:",endSeconds)
        checkDays = currentDays <= endDays and currentDays >= initDays
        #print("hh_init:(",hh_init,") hh_end:(",hh_end,") endHora:(",endHora,")")
        if (str(hh_init).replace(" ","") == "18" or str(hh_init).replace(" ","") == "22") and endHora.replace(" ","") == "6:00":
            checkHour = currentSeconds >= endSeconds or currentSeconds <= initSeconds
            #print("you are trying to look for in new range...",checkHour)
        else:
            checkHour = currentSeconds <= endSeconds and currentSeconds >= initSeconds
        if checkDays and checkHour:
            #print("new coil found in range, result: ",arrProcess[k],"\n")
            inRangeProcess.append(arrProcess[k]) # store tickets on result.
    return inRangeProcess

def getCoilsInDate(initDate,toDate,arrProcess):
    inRangeProcess = []

    #print(hh_init,min_init,ss_init ,hh_end,min_end,ss_end)
    arrInitDate = str(initDate).split("-")
    dd_init = arrInitDate[2]
    mm_init = arrInitDate[1]
    aa_init = arrInitDate[0]
    arrEndDate = str(toDate).split("-")
    dd_end = arrEndDate[2]
    mm_end = arrEndDate[1]
    aa_end = arrEndDate[0]
    initDays = dateToDays(dd_init,mm_init,aa_init)
    endDays = dateToDays(dd_end,mm_end,aa_end)
    for k in range(len(arrProcess)):
        currentHour = arrProcess[k][8]
        arrCurrentDate = str(arrProcess[k][5]).split("-")
        #print(arrCurrentDate)
        dd = arrCurrentDate[2]
        mm = arrCurrentDate[1]
        aa = arrCurrentDate[0]
        currentDays = dateToDays(dd,mm,aa)

        #print("looking for =>",arrProcess[k])
        #print("\nlooking for current_days => ",currentDays," initDays =>",initDays," endDays:",endDays)
        #print("looking for in hour=> ",currentHour," current_seconds=>",currentSeconds," initSeconds =>",initSeconds," endSeconds:",endSeconds)
        checkDays = currentDays <= endDays and currentDays >= initDays
        #print("hh_init:(",hh_init,") hh_end:(",hh_end,") endHora:(",endHora,")")
        if checkDays:
            #print("new coil found in range, result: ",arrProcess[k],"\n")
            inRangeProcess.append(arrProcess[k]) # store tickets on result.
    return inRangeProcess

def getCoilsByOperator(arrCoils,ficha):
    result = []
    #print("looking for:",arrCoils," ficha:",ficha)
    for k in range(len(arrCoils)):
        if str(arrCoils[k][7]) == str(ficha):
            result.append(arrCoils[k])
    return result

def getOpRow(arrBobinas,op):
    opRow = []
    for k in range(len(arrBobinas)):
        #print("arrBobinas=>",arrBobinas,"op=>",op)
        if str(arrBobinas[k][0]) == str(op):
            opRow = arrBobinas[k]
    return opRow


def getOpRowItems(arrBobinas,op):
    opRow = []
    for k in range(len(arrBobinas)):
        #print("arrBobinas=>",arrBobinas,"op=>",op)
        if str(arrBobinas[k][0]) == str(op):
            opRow = arrBobinas[k]
    return opRow

# Busca en la base de datos las bobinas enntre las fechas y horas solicitadas, y su respectivo operador
def getDataTurnNew(mgrObject,fecha_inicio,hora_inicio,fecha_final,hora_final,ficha):
    dataTurn = []
    bobinasenRango = mgrObject.obtenerBobinas_reporte(fecha_inicio,hora_inicio,fecha_final,hora_final,ficha)
    totalUnd = len(bobinasenRango)
    totalKgOp = sum(ticket[2] for ticket in bobinasenRango)
    opsEnRango = list(set(ticket[6] for ticket in bobinasenRango))
    print(f"ops en rango: {opsEnRango}")
    line = []
    for op in opsEnRango:
        datosOp = mgrObject.getAnOp(op)
        #print(f"Datos op: {datosOp}")
        productoOp = mgrObject.getAProduct(datosOp[8])
        #print(f"producto op {productoOp}")
        nombre_producto = productoOp[1]
        #print(f"Nombre producto:{nombre_producto}")
        cliente_op = mgrObject.getClientfromIDDB(productoOp[3])
        #print(f"Cliente Op: {cliente_op}")
        nombre_cliente_op = cliente_op[2]
        #print(f"Nombre cliente op: {nombre_cliente_op}")
        #result,bobinasOp = mgrObject.getCoilsOPonDB(str(op))
        unidades = 0
        KgOp = 0.0
        for bobina in bobinasenRango:
            if bobina[6] == op:
                #print("bobina encontrada")
                unidades = unidades + 1
                KgOp = KgOp + bobina[2]
        #print(f"Bobinas op: {bobinasOp}")
        #unidades = len(bobinasOp)
        #print(f"Unidades: {unidades}")
        #print(f"Kg op: {KgOp}")
        #KgOp = sum(bobinas[2] for bobinas in bobinasOp)
        line = [op,nombre_cliente_op,nombre_producto,str(unidades),"{:4.2f}".format(float(KgOp))]
        dataTurn.append(line)
        print(line)
    return dataTurn,totalUnd,totalKgOp

# Realizar recorrido mediante op, no mediante ticket como se conciba ahora.
def getDataTurn(arrBobinas,arrProcess,arrClients,arrProducts,ficha):
    #print("getting data turn from => ","\n",arrBobinas,"\n",arrProcess,"\n",arrClients,"\n",arrProducts)
    dataTurn = []
    totalUnd = 0
    totalKgOp = 0.0
    if len(arrBobinas)>0 and len(arrProcess)>0 and len(arrClients)>0 and len(arrProducts)>0:
        for k in range(len(arrBobinas)):
            #print("Ticket=>",arrProcess[k])
            op = arrBobinas[k][0]     
            opRow = getOpRow(arrBobinas,op)
            #print("opRow from getDataTurn=>",opRow)
            productRow = getProductRowByOp(opRow,arrProducts,op)
            ##print("\nproduct row",productRow,"\n")
            productName = productRow[1]
            clientId = productRow[3]
            cliente = getClientfromId(arrClients,clientId)
            ##print("\nclient row",cliente,"\n")
            clientName = cliente[2]
            kgop,und = getTotalToTurn(ficha,op,arrProcess)
            #
            totalUnd = totalUnd + int(und)
            totalKgOp = totalKgOp + float(kgop)
            #
            line = [op,clientName,productName,str(und),"{:4.2f}".format(float(kgop))]
            #print("dataTurn line=>",line)
            if int(und) != 0 and float(kgop) != 0.0:
                dataTurn.append(line)
            else:
                pass
            #
    return dataTurn,totalUnd,totalKgOp

def getUsrByFicha(arrUsr,ficha):
    row = []
    for k in range(len(arrUsr)):
        if str(arrUsr[k][5]) == str(ficha):
            row = arrUsr[k]
    return row

def getUsrFromTable(arrUsr,usrValue):
    #print("looking for usr:",arrUsr," val",usrValue)
    usrRow = []
    for k in range(len(arrUsr)):
        if str(arrUsr[k][3]) == str(usrValue):
            usrRow = arrUsr[k]
    return usrRow

def getTotalToTurn(ficha,op,arrProcess):
    accum = 0.0
    counter = 0
    for i in range(len(arrProcess)):
        if (str(arrProcess[i][7]) == str(ficha) ) and (str(op) == str(arrProcess[i][6])):
            accum = accum + float(arrProcess[i][2]) # arrProcess[i][2] es el peso neto.
            counter = counter + 1
    return accum,counter

def getTotalByOperator(ficha,arrProcess):
    accum = 0.0
    counter = 0
    for i in range(len(arrProcess)):
        #print("ficha=>",ficha,"arrProcess[i][7]=>",arrProcess[i][7])
        if str(arrProcess[i][7]) == str(ficha):
            accum = accum + float(arrProcess[i][2]) # arrProcess[i][2] es el peso neto.
            counter = counter + 1
    return accum,counter

def getPosByOp(arrOp,op):
    #(131235, 2.0, 12, 1, 1, 1, 1, 10.5, '12')
    pos = -1
    try:
        pos = arrOp[4]
    except:
        pass
    return pos

def getProductByOp(arrOp,arrProducts,op):
    productCode = ""
    product = ""
    productCode = arrOp[8]
    for j in range(len(arrProducts)):
        # 
        if str(productCode) == str(arrProducts[j][0]):
            product = arrProducts[j][1]
    return product,productCode

# testing format: (13131, 2.0, 12, 1, 1, 1, 1, 10.5, '12') 
# [(12, '13', '', 'frfr'), (13, '12', '', 'frfr'), ('codigo 0', 'producto 0', '', 'frfr')] 
# 1
def getProductRowByOp(arrOp,arrProducts,op):
    ##print("testing format:",arrOp,arrProducts,op)
    productCode = ""
    product = ""
    productCode = arrOp[8]
    productRow = []
    for j in range(len(arrProducts)):
        if str(productCode) == str(arrProducts[j][0]):
            productRow = arrProducts[j]
    return productRow






def getProductRowByName(name,arrProducts):
    #print("\nlooking for=> name",name," arrProducts=>",arrProducts,"\n")
    productRow = []
    for j in range(len(arrProducts)):
        if str(name) == str(arrProducts[j][1]):
            productRow = arrProducts[j]
    return productRow

def getProductRowByCodigo(codigo,arrProducts):
    productRow = []
    for j in range(len(arrProducts)):
        if str(codigo) == str(arrProducts[j][0]):
            productRow = arrProducts[j]
    return productRow

def getClientRowByCodigo(codigo,arrClients):
    clientRow = []
    for j in range(len(arrClients)):
        if str(codigo) == str(arrClients[j][0]):
            clientRow = arrClients[j]
    return clientRow

# [["505555","03/12/2020 09:36:00 AM","Eliezer Rodriguez","27.80","0.30","27.5"]]
#(22, 13.0, 2.6, '', 0, '2022-04-18', 4, 1)
def getDataDetailed(coils,tara,users):
    # check if need users or clients
    #print("Getting data detailed",coils," tara=>",tara," users",users)
    dataResult = []
    if len(coils) and len(users) and str(tara) != "":
        for i in range(len(coils)):
            op = str(coils[i][6])
            ticket = str(coils[i][0])
            fecha = str(coils[i][5])
            bruto = "{:4.2f}".format(float(coils[i][1])) 
            #opRow = getAnOp(ops,op)
            tara = "{:4.2f}".format(float(tara))  #opRow[1]
            neto = "{:4.2f}".format(float(coils[i][2])) 
            ficha = coils[i][7]
            operador = getUsrByFicha(users,ficha) # this get a row from usr with correct ficha.
            #print("Op row=>",operador)
            opName =str(operador[3]) + " " + str(operador[5])
            line = [ticket,fecha,opName,bruto,tara,neto]
            #print(line)
            dataResult.append(line)
    return dataResult

def getAnOp(ops,op):
    opRow = []
    #print("Getting an opRow from => ",ops," for op=>",op)
    for k in range(len(ops)):
        if str(op) == str(ops[k][0]):
            opRow = ops[k]
    return opRow

def getAmtByOp(arrProcess,op):
    amount = 0.0
    for k in range(len(arrProcess)):
        # arrProcess[k][6] represents the op
        if str(op) == str(arrProcess[k][6]):
            amount = amount + int(arrProcess[k][1])
    return amount

def getArrHablador(dataDic):
    op = dataDic["op"]
    posicion = dataDic["position"]
    cantidad = dataDic["amount"]
    producto = dataDic["product"]
    observacion = dataDic["observations"]
    return [op,cantidad,posicion,observacion,producto]

def getTotalsForOp(arrSameTickets):
    neto,bruto = 0.0,0.0
    for i in range(len(arrSameTickets)):
        # arrSameTickets[i][1] = peso_bruto on db, and arrSameTickets[i][2] = peso_neto on db
        try:
            bruto = bruto + float(arrSameTickets[i][1])
            neto = neto + float(arrSameTickets[i][2])
        except:
            pass
    #print("total bruto:",bruto," neto:",neto)
    return bruto,neto

def getTotalsForPallet(arrSameTicketsPallet):
    neto,bruto = 0.0,0.0
    for i in range(len(arrSameTicketsPallet)):
        # arrSameTickets[i][1] = peso_bruto on db, and arrSameTickets[i][2] = peso_neto on db
        try:
            bruto = bruto + float(arrSameTicketsPallet[i][1])
            neto = neto + float(arrSameTicketsPallet[i][2])
        except:
            pass
    #print("total bruto:",bruto," neto:",neto)
    return bruto,neto

def getCodeFromClient(arrClient,client):
    code = ""
    for i in range(len(arrClient)):
        if str(client) == str(arrClient[i][2]):
            code = arrClient[i][1]
    return code

def getTheSameCoils(arrTable,valueOp):
    result = []
    for i in range(len(arrTable)):
        #print("looking for the same op ",valueOp," on ",arrTable)
        if str(arrTable[i][6]) == str(valueOp): # op field
            result.append(arrTable[i])
    return result

def getTheSameCoilsPallet(arrTable,valueOp,valuePallet):
    result = []
    count = 0
    for i in range(len(arrTable)):
        count = count + 1
        #print("looking for the same op and pallet",valueOp," on ",arrTable," and pallet ",valuePallet)
        if str(arrTable[i][6]) == str(valueOp) and str(arrTable[i][3]) == str(valuePallet): # op field
            result.append(arrTable[i])
    print(f"Iteraciones en getthesamecoilspallet: {count}")      
    return result

def countPallets(coilsPallet):
    count = 0
    if len(coilsPallet)>0:
        #print("getting coils from: ",coilsPallet)
        count = int(coilsPallet[0][3])
        for i in range(1,len(coilsPallet)):
            try:
                #print("count pallet, ",coilsPallet[i])
                if count<int(coilsPallet[i][3]):
                    count = int(coilsPallet[i][3])
            except:
                pass
    return count

def countBobinas(coilsOp,op,countPallet):
    count = 0
    #print("count bobinas for coilsOp =>",coilsOp,"op",op,"countPallet",countPallet)
    if len(coilsOp)>0:
        #print(f"Longitud: {len(coilsOp)}")
        ##print("getting bobinas from: ",coilsOp)
        for i in range(len(coilsOp)):
            try:
                ##print("count coils, ",coilsOp[i])
                if str(op) == str(coilsOp[i][6]) and str(countPallet)==str(coilsOp[i][3]):
                    count = count +1 #int(coilsOp[i][0])
            except:
                pass
            # change if index start from 1, now starts with 0
    return count 

def countBobinasOp(coils,op):
    count = 0
    for k in range(len(coils)):
        if str(coils[k][6]) == str(op):
            count = count + 1
    return count

def getTicketsByOpPlusPallet(coilsOp,op,pallet):
    tickets = []
    for k in range(len(coilsOp)):
        if str(coilsOp[k][6]) == str(op) and str(coilsOp[k][3])== str(pallet):
            tickets.append(coilsOp[k])
    return tickets



def countToTickets(ticket,coilsOp,op,pallet):
    count = 0
    flag = 0
    for k in range(len(coilsOp)):
        if str(coilsOp[k][0])==str(ticket) and str(coilsOp[k][6]) == str(op) and str(coilsOp[k][3])== str(pallet) and flag == 0:
            count = k + 1
            flag == 1
            break
    return count

def countBobinasPallet(coils,op,pallet):
    count = 0
    for k in range(len(coils)):
        if str(coils[k][6]) == str(op) and str(coils[k][3])== str(pallet):
            count = count + 1
            #flag == 1
            #break
    return count

def getTicketsForPallet(coils):
    dataPallet = []
    bobinas = len(coils)
    if len(coils)<=40:
        for i in range(len(coils)):
            nro0 = str( coils[i][9] )#str(i+1)
            peso0 =  "{:4.2f}".format(float(coils[i][2])) # peso neto
            ticket0 = coils[i][0]
            bobMatriz0 = str(coils[i][4])
            if bobMatriz0 == "0" or bobMatriz0 == " " or bobMatriz0 == None:
                bobMatriz0 = ""
            # [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]]
            line = [nro0,peso0,ticket0,bobMatriz0,"-","-","-","-"]
            dataPallet.append(line)
        for i in range(len(coils),40):
            line = ["-","-","-","-","-","-","-","-"]
            dataPallet.append(line)
    elif len(coils)>40:
        for i in range(40):
            nro0 = str( coils[i][9] ) #str(i+1) # Este es el numero de bobina de la paleta, asumiendo un correcto orden en la base de datos.
            peso0 = "{:4.2f}".format(float(coils[i][2])) # peso neto
            ticket0 = coils[i][0]
            bobMatriz0 = str(coils[i][4])
            if bobMatriz0 == "0"  or bobMatriz0 == " " or bobMatriz0 == None:
                bobMatriz0 = ""
            nro1 = ""
            peso1 = ""
            ticket1 = ""
            bobMatriz1 = ""
            # if data exist append to other columnn not max of 80 tickets for op and table!!!
            if (i+40) < len(coils):
                nro1 = str( coils[i+40][9] ) #str(i+41)
                peso1 = "{:4.2f}".format(float(coils[i+40][2])) # peso neto
                ticket1 = coils[i+40][0]
                bobMatriz1 = str(coils[i+40][4])
                try:
                    if bobMatriz1 == "0"  or bobMatriz1 == " " or bobMatriz1 == None:
                        bobMatriz1 = ""
                except:
                    pass
            # [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]]
            line = [nro0,peso0,ticket0,bobMatriz0,nro1,peso1,ticket1,bobMatriz1]
            dataPallet.append(line)
    elif len(coils) == 0:
        for i in range(40):
            dataPallet.append([str(int(i + 1)),"-","-","-",str(int(i + 40 + 1)),"-","-","-"])
    return bobinas,dataPallet

# get the op number from bobinas db
def lookForOp(dataArr):
    for i in range(len(dataArr)):
        pass

def lookValueOverMatrix(value,matrix):
    column = -1
    row = -1
    for k in range(len(matrix)):
        for j in range(len(matrix)):
            if value == matrix[k][j]:
                column = k 
                row = j
    return column, row

def lookValueOverArray(value,arr):
    index = -1
    for k in range(len(arr)):
        if value == arr[k]:
            index = k 
    return index

def containsValue(arr,value):
    result = False
    for i in range(len(arr)):
        try:
            if (str(arr[i][0]) == str(value)):
                result = True
                #print(arr[i][0]," is like ",value,"? ",result)
        except:
            pass
    return result

def getNamesFromClients(arrTable):
    result = []
    for i in range(len(arrTable)):
        client = str(arrTable[i][2])
        result.append(client)
    return result

def getCodesFromClients(arrTable):
    result = []
    for i in range(len(arrTable)):
        client = str(arrTable[i][1])
        result.append(client)
    return result

def get_match_index(sub_code,codes):
    index = -1
    for k in range(len(codes)):
        codes[k] = str(codes[k]).replace(" ","").upper()
        zero_lenght = len(list(str(sub_code)))
        result_srt = str( sub_code ).replace(codes[k],"")
        result_leght = len(list(result_srt))
        #print("k",k," codes[k]",codes[k],' zero_lenght',zero_lenght," result_srt",result_srt," result_leght",result_leght)
        if (result_leght < zero_lenght) and zero_lenght>=7: #or ((zero_lenght - 7) == result_leght) or (result_leght == 0 ) :
            index = k
            break
    return index 

def getNamesFromProducts(arrTable):
    result = []
    for i in range(len(arrTable)):
        products = str(arrTable[i][1])
        result.append(products)
    return result

def getCodesFromProducts(arrTable):
    result = []
    for i in range(len(arrTable)):
        codes = str(arrTable[i][0])
        result.append(codes)
    return result

def getOpFromTable(arrTable):
    result = []
    for i in range(len(arrTable)):
        op = str(arrTable[i][0])
        ##print(op)
        result.append(op)
    return result

# from table productos
def getClientsFromTable(arrTable):
    result = []
    for i in range(len(arrTable)):
        clientProduct = arrTable[i][3]
        #print(clientProduct)
        result.append(clientProduct)
    return result

def getProductFromCode(arrTable,value):
    result = []
    for i in range(len(arrTable)):
        if str(arrTable[i][0]) == str(value):
            #print("getting produc from code:",arrTable[i][0]," value:",value)
            result = arrTable[i]
    #print("product result:",result)
    return result


def getProductFromName(arrTable,value):
    result = []
    for i in range(len(arrTable)):
        #print("getting produc from code:",arrTable[i][0]," value:",value)
        if arrTable[i][1] == str(value): 
            result = arrTable[i]
    #print("product result:",result)
    return result

def getClientfromId(arrTable,id):
    result = []
    #print("arrTable:",arrTable)
    for i in range(len(arrTable)):
        #print("getting client from Id:",arrTable[i][0]," id:",id)
        if str(arrTable[i][0]) == str(id):
            result = arrTable[i]
    #print("client result:",result)
    return result

def getClientfromName(arrTable,id):
    result = []
    #print("arrTable:",arrTable)
    for i in range(len(arrTable)):
        #print("getting client from Id:",arrTable[i][0]," id:",id)
        if str(arrTable[i][2]) == str(id):
            result = arrTable[i]
    #print("client result:",result)
    return result

def getProductFromOp(arrOp):
    product = ""
    #print("arrTable:",arrOp)
    for i in range(len(arrOp)):
        #print("getting client from Id:",arrOp[i][0]," id:",id)
        if str(arrOp[i][0]) == str(id):
            result = arrOp[i]
    #print("product for hablador result:",product)
    return result   

def getTodayTickets(tableTickets):
    result = []
    for i in range(len(tableTickets)):
        # fecha_emision = tableTickets[i][5]
        ##print(tableTickets[i][5],str(date.today()))
        if str(tableTickets[i][5]) == str(date.today()):
            result.append(tableTickets[i])
    return result

def getLastTicket():
    """index = 0
    result = []
    if len(arrTicket) > 0:
        first = arrTicket[0][0] # ticket at pos 0
        for i in range(1,len(arrTicket)):
            try:
                if arrTicket[i][0] > first:
                    index = i #arrTicket[i][0] 
            except:
                pass
        #print("Result getting last ticket: ",result, " at ",index)
        result = arrTicket[index]"""
    result_TEMP=DBHandler.ultimoticket("proceso_bobina")
    result=result_TEMP[0][0]
    print(f"Ultimo ticket: {result}")
    return result

def getLastClient(arrClient):
    """index = 0
    result = []
    if len(arrClient) > 0:
        first = arrClient[0][0] # ticket at pos 0
        for i in range(1,len(arrClient)):
            try:
                if int(arrClient[i][0]) > int(first):
                    index = i #arrTicket[i][0] 
            except:
                pass
        #print("Result getting last client: ",result, " at ",index)
        result = arrClient[index]"""
    result = arrClient[-1]
    return result

def getNamesFromUsr(arrUsr):
    names = []
    for i in range(len(arrUsr)):
        names.append(arrUsr[i][3])
    return names

def checkInt(object):
    checkNumber = False
    try:
        number = int(object.text())
        if number != 0 :
            checkNumber = True
            changeToNormal(object)
        else:
            changeToError(object)
    except:
        checkNumber = False
        changeToError(object)
    return checkNumber

def changeToError(obj):
    objName = obj.objectName()
    obj.setStyleSheet("""
        QComboBox#"""+objName+"""{
            background-color:#ff7f7f;
        }
        QLineEdit#"""+objName+"""{
            background-color:#ff7f7f;
        }
        QLCDNumber#"""+objName+"""{
            background-color:#ff7f7f;
            background:#ff7f7f;
        }
        QLabel#"""+objName+"""{
            background-color:#ff7f7f;
            background:#ff7f7f;
        }
    """)

def changeToDisable(obj):
    objName = obj.objectName()
    obj.setStyleSheet("""
        QComboBox#"""+objName+"""{
            background-color:#ff7f7f;
        }
        QLineEdit#"""+objName+"""{
            background-color:#e6e6e6;
        }
        QLCDNumber#"""+objName+"""{
            background-color:#ff7f7f;
            background:#ff7f7f;
        }
        QLabel#"""+objName+"""{
            background-color:#ff7f7f;
            background:#ff7f7f;
        }
    """)

def changeToNormal(obj):
    objName = obj.objectName()
    obj.setStyleSheet("""
        QComboBox#"""+objName+"""{
            background-color:white;
        }
        QLineEdit#"""+objName+"""{
            background-color:white;
        }
        QLCDNumber#"""+objName+"""{
            background-color:white;
            background:white;
        }
        QLabel#"""+objName+"""{
            background-color:white;
            background:white;
        }
    """)

def changeToSuccess(obj):
    objName = obj.objectName()
    obj.setStyleSheet("""
        QComboBox#"""+objName+"""{
            background-color:#66b266;
        }
        QLineEdit#"""+objName+"""{
            background-color:#66b266;
        }
        QLCDNumber#"""+objName+"""{
            background-color:#66b266;
            background:#66b266;
        }
        QLabel#"""+objName+"""{
            background-color:#66b266;
            background:#66b266;
        }
    """)

def isIp(ip):
    result = False
    if ip != "":
        result = True
    return result

# [op,product,client,tara,pesoMaxBobina,amtPallets,coilsXPallets,currentPallet]
def getDataFromFields(fields):
    op = int(fields[0])
    producto = fields[1]
    tara = fields[3]
    paletas_total = fields[5]
    bobinas_paleta = fields[6]
    paleta_actual = fields[7]
    matriz = False
    hablador = False
    total_op = 123.0
    data = (op,tara,paletas_total,bobinas_paleta,paleta_actual,matriz,hablador,total_op,producto)
    #data = (1231,2.0,12,1,1,True,True,10.5,12)
    return data

def toIntArray(intNumber):
    result = []
    strNumber = str(intNumber)
    if strNumber.isnumeric():
        for digit in strNumber:
            result.append(int(digit))
    else:
        pass
        #print("check you are tryin to convert an integer")
    return result

# check the first e digits of op to verify it's start from 131 or 134
def check3DigitsOp(op):
    arrOp = toIntArray(op)
    check1 = False
    check2 = False
    if len(arrOp)>0:
        check1 = arrOp[0] == 1 and arrOp[1] == 3 and arrOp[2] == 1
        check2 = arrOp[0] == 1 and arrOp[1] == 3 and arrOp[2] == 4
    return (check1 or check2)

def scalePdf(pathFile,width,height):
    pdf = PyPDF2.PdfFileReader(pathFile)
    page0 = pdf.getPage(0)
    #deg = page0.get('/Rotate',90)
    page0.scaleTo(width,height) 
    #page0.mergeTranslatedPage(page0, -200, -100, expand = False)
    writer = PyPDF2.PdfFileWriter() 
    writer.addPage(page0)
    with open(pathFile, "wb+") as f:
        writer.write(f)


import PyPDF2
 
def PDFrotate(origFileName, newFileName, rotation):
 
    pdfFileObj = open(origFileName, 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    pdfWriter = PyPDF2.PdfFileWriter()
    pageObj = pdfReader.getPage(0)
    pageObj.rotateClockwise(rotation)
    pdfWriter.addPage(pageObj)
    newFile = open(newFileName, 'wb')
    pdfWriter.write(newFile)
    pdfFileObj.close()
    newFile.close()

def strFilter(strObj, arrFilters):
    for i in range(len(arrFilters)):
        strObj = strObj.replace(arrFilters[i],"")
    return strObj

FILTERS = [
"-",
"False",
"True",
"CompletedProcess(args=['powershell', 'Command', 'GetPrinter | FormatTable']",
"Local",
"Type",
"ComputerName",
"PortName",
"DriverName",
"Shared",
"Published",
"DeviceType",
",",
"'",
"stderr=b",
"returncode=",
"stdout=",
"NameDevice",
"Connection",
"PORTPROMPT:",
"SHRFAX:",
"Device",
"Name",
".",
":"
]

def getAllPrintersStr():
    command = "Get-Printer | Format-Table"
    result = subprocess.run(["powershell","-Command",command],capture_output = True)
    return result

def getAvalaiblePrinters():
    strResult = str(getAllPrintersStr())
    strFiltered = strFilter(strResult,FILTERS)
    listFiltered = strFiltered.split("\\r\\")
    result = []
    for i in range(len(listFiltered)):
        try :
            arrLine = listFiltered[i].split("           ")
            if len(arrLine)>=3:
                count = 0
                value = ""
                line = []
                for k in range(len(arrLine)):
                    if len(list(arrLine[k])) >4 and arrLine[k] != "" and arrLine[k] != "n":
                        count = count + 1
                        value = arrLine[k]
                        if count == 1:
                            line.append(value)
                if count>=3:
                    if list(line[0])[0] == "n":
                        lineResult = line[0][1:] #line[0][:0] + "" + line[0][1:]
                    result.append(lineResult)
        except:
            pass
    return result


def getallPorts():
    names = []
    for port in list(serial.tools.list_ports.comports()):
        names.append(str(port))       
    return names

def findComIndex(portName):
    index = -1
    for j in range(20):   
        if str(portName).find("(COM"+str(j)+")") !=-1 or str(portName).find("COM"+str(j)) !=-1:
            index = j 
    return index  

def appendTable(counter,columns,items,table,dataLineDic):
    #keys = dataLineDic.keys()
    values = list(dataLineDic.values())
    lastRowIndex = int((len(items))/columns)
    for i in range(len(dataLineDic)):
        item = QTableWidgetItem()
        value = str(values[i])
        #print("value at =>",value,"\n")
        item.setText(value) # values and keys need to have in order {ticket,op,cod,product,brute Weight}.
        item.setTextAlignment(Qt.AlignCenter) 
        items.append(item)
        #table.setItem(0,i,item) # inser item from first row.
        table.setItem(lastRowIndex,i,item)  
        table.scrollToItem(item,QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
        counter = counter + 1
        table.setRowCount(counter) 
        #print(str(item)+"\n")
    table.selectRow(lastRowIndex)
    return counter,items,table

def appendTableOp(counter,columns,items,table,dataLineDic):
    #keys = dataLineDic.keys()
    values = list(dataLineDic.values())
    lastRowIndex = int((len(items))/columns)
    lineOp = []
    for i in range(len(dataLineDic)):
        item = QTableWidgetItem()
        value = str(values[i])
        #print("value at =>",value,"\n")
        item.setText(value) # values and keys need to have in order {ticket,op,cod,product,brute Weight}.
        item.setTextAlignment(Qt.AlignCenter) 
        items.append(item)
        lineOp.append(value)
        #table.setItem(0,i,item) # inser item from first row.
        table.setItem(lastRowIndex,i,item)  
        table.scrollToItem(item,QtWidgets.QAbstractItemView.ScrollHint.EnsureVisible)
        counter = counter + 1
        table.setRowCount(counter) 
        #print(str(item)+"\n")
    table.selectRow(lastRowIndex)

    return counter,items,table,lineOp

def getRowsFromItems(items,columns):
    array = []
    for k in range(int(len(items)/columns)):
        row = []
        for q in range(columns):
            row.append(items[int(k*(q+1))].text())
        array.append(row)
    return array

def isNumber(supNumber):
    arrNumber = list(supNumber)
    pass

def lookForClient(client):
    result = {"client":"dataName"}
    #
    # Buscar aqui el cliente en la DB        
    #         
    #print("client received from DB",result)
    return result

def lookForProduct(product):
    result = {"product":"dataProduct"}
    #
    # Buscar aqui el producto en la DB
    #
    #print("product received from DB",result)
    return result

def deleteClient(client):
    pass

def deleteProductOnDB(product):
    pass

def isFloat(strNumber):
    result = False
    try:
        number = float(strNumber)
        if type(number) == type(0.0):
            result = True
    except:
        result = False
    return result

def getTurn():
    time = str(datetime.now())
    hours = int(time.split(" ")[1].split(":")[0]) #int(str(datetime.now().hour()))
    minutes = int(time.split(" ")[1].split(":")[1])
    seconds =float(time.split(" ")[1].split(":")[2])
    result = 0
    if hours < 12:
        result = 1
    elif hours > 12:
        result = 2
    pass
    return result

def getDate():
    date = str(datetime.now()).split(" ")[0]
    return date

def getFullDate():
    date = str(datetime.now()).split(".")[0]
    print(f"Date: {date}")
    return date 

def absPath(file):
    return str(Path(__file__).parent.absolute() / file)

def absPathNormal(file):
    dir = r"" + absPath(file)
    dir = dir.replace("\\","/")
    return dir

def runAsAdm(runMethod):

    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        runMethod
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
        runMethod

def wordFilter(word):
    data = ""
    try:
        digits = list(word)
        if len(digits)>=15 and digits[5] == " " and digits[4]==" ":
            data = digits[6] +"."+ digits[7] + digits[8]
        if len(digits)>=15 and digits[5] != " " and digits[4]==" ":
            data = digits[5] + digits[6] +"."+ digits[7] + digits[8]
        if len(digits)>=15 and digits[5] != " " and digits[4]!=" ":
            data = digits[4] + digits[5] + digits[6] +"."+ digits[7] + digits[8]
    except Exception as e:
        print("at 953=> ",e)
    return data

"""
# VERIFY IF IT IS NOT BEING USED!!!
def wordFilter3(word):
    arrWord = list(word)
    data = "0.0"
    digits = (0,0,0,0,0)
    try:
        digits[0] = int(arrWord[5])
    except:
        pass
    try:
        digits[0] = int(arrWord[6])
    except:
        pass
    try:
        digits[0] = int(arrWord[7])
    except:
        pass
    try:
        digits[0] = int(arrWord[8])
    except:
        pass
    try:
        digits[0] = int(arrWord[9])
    except:
        pass
    data = str(arrWord[5]) + str(arrWord[6]) + str(arrWord[7]) +"."+ str(arrWord[8]) + str(arrWord[9])
    return data
"""

def getSample(port):
    #port = port #serial.Serial(port = comPort baudrate = 9600, timeout=0.5)
    start = "<"
    word = ""
    char = ""
    read = False
    try:
        char = port.read() 
        read = (char == start.encode('utf-8'))
    except Exception as e:
        print("at 996=> ",e)    
    if read:
        try:
            word = word + str(char.decode('utf-8'))
        except Exception as e:
            word = word + " "
            print("at 1002=> ",e)
        for i in range(1,15):
            try:
                char = port.read()
                word = word + str(char.decode('utf-8'))
            except Exception as e:
                word = word + " "
                print("at 1009=> ",e)
    sample = wordFilter(word)
    #if sample == "" or sample == " ":
    #    sample = "0.00"
    return sample


def getSample2(port):
    #port = port #serial.Serial(port = comPort baudrate = 9600, timeout=0.5)
    try:
        weight = port.readline().decode("utf-8")
        #print(weight)
        pos = weight.find("N")
        if pos > 0 :
            weight = weight[7:12].replace(" ","")
            #print(weight) #          146kg N
            #result = float(weight)
    except Exception as e:
        pass
        #print("at 1128=> ",e)
    return weight
    
def comNameToPort(portName):    
    portIndex = findComIndex(portName)
    portName = "COM0"
    if portIndex !=-1:
        portName = "COM" + str(portIndex)
        #print("finComIndex returned: ",portName," ",portIndex)
    return portName

def seekTicketsByOp(tickets,op):
    result = []
    for k in range(len(tickets)):
        if str(tickets[k][6]) == str(op):
            result.append(tickets[k])
    return result

def seekTicketsByNumero(tickets,numero):
    result = []
    for k in range(len(tickets)):
        if str(tickets[k][0]) == str(numero):
            result.append(tickets[k])
    return result

def seekTicketsByFicha(tickets,ficha):
    result = []
    for k in range(len(tickets)):
        if str(tickets[k][7]) == str(ficha):
            result.append(tickets[k])
    return result 

def seekTicketsByPaleta(tickets,paleta):
    result = []
    for k in range(len(tickets)):
        if str(tickets[k][3]) == str(paleta):
            result.append(tickets[k])
    return result

def getWeight3(word64):
    arrWeight = []
    strWeight = ""
    arrWord = list(word64)
    try:
        for k in range(len(arrWord)):
            if arrWord[k] == "G":
                pos = k
                break
            pass
        pass
    except Exception as e:
        print("at 1090=> ",e)
    try:
        arrWeight = arrWord[pos-8:pos-4] #  arrWord[pos-8:pos-4]
        if len(arrWeight)== 4:
            strWeight = ""
            for k in range(len(arrWeight)):
                strWeight = strWeight + str(arrWeight[k])
        else:
            pass
            #strWeight = "0.00"
    except Exception as e:
        print("at 1101=> ",e)
        #strWeight = "0.00"
    return float(strWeight)

def getSample3(port):
    port = port #serial.Serial(port = comPort baudrate = 9600, timeout=0.5)
    #start = " "
    word = ""
    if True:
        for i in range(1,64):
            try:
                char = port.read()
                #print(char)
                word = word + str(char.decode('utf-8'))
            except Exception as e:
                print("at 1116=> ",e)
                #word = word + " "
    return getWeight3(word)

def getSample4(port):
    #port = port #serial.Serial(port = comPort baudrate = 9600, timeout=0.5)
    result = 0.0
    try:
        weight = port.readline().decode("utf-8")
        if weight != " " and weight != "":
            result = float(weight)
    except Exception as e:
        print("at 1128=> ",e)
        #print("in sample,",e)
    return result

def getModeMeasure(modeStr):
    mode = -1
    #print("selected mode=>",modeStr)
    if modeStr == "Continuo MT BBA231C": #["Continuo ohaus T21P","GNT Ohaus T21P","Continuo MT BBA231C"]
        mode = 1
    elif modeStr == "Continuo ohaus T21P":
        mode = 2
    elif modeStr == "GNT Ohaus T21P":
        mode = 3
    elif modeStr == "Directo":
        mode = 4
    return mode

def convertModeMeasure(modeInt):
    mode = ""
    #print("selected mode=>",modeStr)
    if str(modeInt) == "1": #["Continuo ohaus T21P","GNT Ohaus T21P","Continuo MT BBA231C"]
        mode = "Continuo MT BBA231C"
    elif str(modeInt) == "2":
        mode = "Continuo ohaus T21P"
    elif str(modeInt) == "3":
        mode = "GNT Ohaus T21P"
    elif str(modeInt) == "4":
        mode = "GNT Ohaus T21P"
    return mode

def convertFormat(initFormat):
    #initFormat = 12:00:00 A. M.
    #12:00:00 AM
    #print("converting to =>",initFormat," ",len(initFormat.split(" ")))
    endFormat = str(initFormat.split(" ")[0]) +" "+  str(initFormat.split(" ")[1]).replace(".","") + str(initFormat.split(" ")[2]).replace(".","")
    return endFormat

def itemsToArray(items):
    result = []
    for k in range(int(len(items)/4)):
        for j in range(4):
            result[k][j] = items[k*4 + j]

def getRowFromItems(index,items):
    result = False
    #for k in range(len(items)):
    #    print("item at=>",k," item is=>",items[k].text(),"\n")
    id = items[index*4 + 0].text()
    id_is = items[index*4 + 0].isSelected()

    codigo = items[index*4 + 1].text()
    codigo_is = items[index*4 + 1].isSelected()

    cliente = items[index*4 + 2].text()
    cliente_is = items[index*4 + 2].isSelected()

    descripcion = items[index*4 + 3].text()
    descripcion_is = items[index*4 + 3].isSelected()

    # If Row is Selected
    result = id_is and codigo_is and cliente_is and descripcion_is
    # (21, 'COCA-COLA FRESA S.A.', 'FM0-ALP', 'ETIQ. CHINOTTO 355ML. LIBRE CALORIAS')
    row = (id,cliente,codigo,descripcion)
    #print("looking for index=>",index," Row from items =>",row)
    return result,row

def getProductRowFromItems(index,items):
    result = False
    #for k in range(len(items)):
    #    print("item at=>",k," item is=>",items[k].text(),"\n")

    codigo_producto = items[index*4 + 2].text()
    codigo_producto_is = items[index*4 + 2].isSelected()

    product = items[index*4 + 1].text()
    product_is = items[index*4 + 1].isSelected()

    peso_max = "50.0" #items[index*4 + 0].text()
    peso_max_is =  items[index*4 + 0].isSelected()

    client_id = items[index*4 + 3].text()
    client_id_is = items[index*4 + 3].isSelected()

    # If Row is Selected
    result = codigo_producto_is and product_is and peso_max_is and client_id_is
    # (21, 'COCA-COLA FRESA S.A.', 'FM0-ALP', 'ETIQ. CHINOTTO 355ML. LIBRE CALORIAS')
    row = (codigo_producto,product,peso_max,client_id)
    #print("looking for index=>",index," Row from items =>",row)
    return result,row

# ["Nro.","Tara","Cod. Producto","# Paletas","# Bob. X Paletas"]
def getOpRowFromItems(index,items):
    result = False

    #print("len(items)=>",len(items))
    op = items[index*4 + 0].text()
    op_is = items[index*4 + 0].isSelected()

    tara = items[index*4 + 1].text()
    tara_is = items[index*4 + 1].isSelected()

    codigo = items[index*4 + 2].text()
    codigo_is =  items[index*4 + 2].isSelected()

    paletas = items[index*4 + 3].text()
    paletas_is = items[index*4 + 3].isSelected()

    bxpaletas = items[index*4 + 4].text()
    bxpaletas_is = items[index*4 + 4].isSelected()

    # If Row is Selected
    result = op_is and tara_is and codigo_is and paletas_is and bxpaletas_is
    # (21, 'COCA-COLA FRESA S.A.', 'FM0-ALP', 'ETIQ. CHINOTTO 355ML. LIBRE CALORIAS')
    row = (op,tara,codigo,paletas,bxpaletas)
    #print("results is for index ",index,":",op_is,tara_is,codigo_is,paletas_is,bxpaletas_is)
    #print("looking for index=>",index," Row from items =>",row)
    return result,row

def getOpRowsFromItems(items):
    result = False
    rows = []
    for k in range(int( len(items)/5 )):
        op = items[k*4 + 0].text()
        op_is = items[k*4 + 0].isSelected()

        tara = items[k*4 + 1].text()
        tara_is = items[k*4 + 1].isSelected()

        codigo = items[k*4 + 2].text()
        codigo_is =  items[k*4 + 2].isSelected()

        paletas = items[k*4 + 3].text()
        paletas_is = items[k*4 + 3].isSelected()

        bxpaletas = items[k*4 + 4].text()
        bxpaletas_is = items[k*4 + 4].isSelected()

        row = [op,tara,codigo,paletas,bxpaletas]
        rows.append(row)

    # If Row is Selected
    #result = op_is and tara_is and codigo_is and paletas_is and bxpaletas_is
    # (21, 'COCA-COLA FRESA S.A.', 'FM0-ALP', 'ETIQ. CHINOTTO 355ML. LIBRE CALORIAS')
    #row = (op,tara,codigo,paletas,bxpaletas)
    #print("results is for index ",index,":",op_is,tara_is,codigo_is,paletas_is,bxpaletas_is)
    #print("looking for index=>",index," Row from items =>",row)
    return rows

# only works for a 4 columns row.
def isAnyRowSelected(items): 
    result = False
    for k in range(int(len(items)/4)):
        id_is = items[k*4 + 0].isSelected()
        codigo_is = items[k*4 + 1].isSelected()
        cliente_is = items[k*4 + 2].isSelected()
        descripcion_is = items[k*4 + 3].isSelected()
        _result = id_is and codigo_is and cliente_is and descripcion_is
        if _result:
            result = True
            break
    return result

def onOrder(str_chain):
    arr_str = list(str_chain)
    trash = "@#$%^&*()!<>"

def getColumn(matrix,index):
    column = []
    for row in matrix:
        column.append(row[index])
    return column

def getColumnAsStr(matrix,index):
    column = []
    for row in matrix:
        column.append(str(row[index]))
    return column
