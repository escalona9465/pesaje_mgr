from components.ventanaMGR import PesajeMGR
from components.dbHandler import DBHandler

def getCoilsOnDB(dbMGR):
    coils = []
    result, coils= dbMGR.getTable("proceso_bobina")
    if result:
        pass
        #print("success getting coils: ",coils)
    else:
        coils = []
        #print("can't store the data on database")
    return result,coils

def getOpsOnDB(dbMGR):
    bobinas = []
    result,bobinas = dbMGR.getTable("bobinas")
    if result:
        #print("success getting bobinas: ",bobinas)
        pass
    else:
        bobinas = []
        #print("can't store the data on database")
    return result,bobinas

def updateBobinaOnDB(dbMGR,ticket,bobina):
    return dbMGR.updateValue("proceso_bobina",("bobina",bobina),("ticket",ticket))

dbMGR = DBHandler("components/database/pesaje.db")

result, opsTable = getOpsOnDB(dbMGR)
esult, arrTickets = getCoilsOnDB(dbMGR)

for k in range(len(opsTable)):
    op = opsTable[k][0] # op
    codigo = opsTable[k][8] # codigo_producto
    bobina = 1
    pallet = 1
    for p in range(len(arrTickets)):
        
        ticket = arrTickets[p][0]

        if str(op) == str(arrTickets[p][6]) and str(arrTickets[p][3]) != str(pallet):
            pallet = arrTickets[p][3]
            bobina = 1

        if str(op) == str(arrTickets[p][6]):
            updateBobinaOnDB(dbMGR,str(ticket),str(bobina))
            bobina = bobina + 1
            #print("op=>",op," pallet=>",pallet," ticket=>", arrTickets[p],"\n")


