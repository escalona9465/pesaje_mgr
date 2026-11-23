
dataExampleAddOp = {
    "op":"12",
    "clientName":"Cliente 01",
    "productName":"Producto 01",
    "productCode":"code01",
    "maxWeight":"120.0",
    "cantPallets":"12",
    "bobxPallets":"4"
}

# cambiar numero del item al cargar desde DB
dataExampleAddClient = {
    "nro":"0",
    "clientName":"Cliente 01",
    "clientCode":"code01",
    "description":"este es un producto de calidad."
}

# cambiar numero del item al cargar desde DB
dataExampleAddProduct = {
    "nro":"0",
    "productName":"Producto 01",
    "productCode":"code01",
    "clientName":"Cliente 01"
}

dataExampleHablador = {
    "op":"25145698",
    "product":"Etiq. Kapo Manzana 250 mL",
    "position":"3",
    "amount":"412.98",
    "observations":"La paleta le falta una bobina por ordenes\ndel cliente."
}
#Código = FM0-NESXXXXX
#Producto = ENV. COCOSETTE
#Cliente = NESTLE TOCUYO

dataExampleBobina = {'code':'FM0-NESXXXXX','producto': 'ENV. COCOSETTE', 'client': 'NESTLE TOCUYO', 'operador': '1', 'reimpresion': '2022-04-11 09:59:19.048128', 'bobMatriz': '0', 'bobina': '0', 'turno': '1', 'op': '131132598', 'neto': '0.6000000000000001', 'bruto': '0.8', 'tara': '0.2', 'date': 
'2022-04-11', 'ticketCode': '9'}

dataPallet = []
for i in range(40):
    dataPallet.append([str(int(i + 1)),"   ","   ","   ",str(int(i + 40 + 1)),"   ","   ","   "])

dataExamplePallet = {
    "date" : "",
    "tara" : "",
    "clientCode" : "",
    "client" : "",
    "productCode" : "",
    "product" : "",

    "bobinas" : "0",
    "pesoBruto" : "0.0",
    "pesoNeto" : "0.0",

    "paletas" : "0",
    "usr" : "elirod27",
    "mgrCode" : "MGR-GPR-F19(Ed.01)",
    "op" : "",
    
    "header" : [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]],

    "data"  : dataPallet

}

dataExampleOp = {
    "op" : "13117002", 

    "clientId" : "FM0-PEP221004",
    "clientName" : "Eliezer R.",

    "productName" : "Doritos pincante 2022+",
    "productId" : "FM0-PEP221004",

    "accum" : "250.00",
    "amount" : "12",
    "user" : "ISNALDO TORREALBA",

    "total" : "250.00",
    "units" : "12",
}

dataExampleGeneralOp = {
    "op" : "13117002", 

    "clientId" : "FM0-PEP221004",
    "clientName" : "Eliezer R.",

    "productName" : "Doritos pincante 2022+",
    "productId" : "FM0-PEP221004",

    "nPaletas" : "6",
    "bxPaletas" : "26",

    "total" : "250.00",
    "units" : "12",
}

dataExampleDetailed = [["505555","03/12/2020 09:36:00 AM","Eliezer Rodriguez","27.80","0.30","27.5"],["505555","03/12/2020 09:36:00 AM","Eliezer Rodriguez","27.80","0.30","27.5"],["505555","03/12/2020 09:36:00 AM","Eliezer Rodriguez","27.80","0.30","27.5"]]

dataExampleDetailedOp = {
    "op" : "13117002", 
    "clientId" : "FM0-PEP221004",
    "clientName" : "Eliezer R.",
    "productName" : "Doritos pincante 2022+",
    "productId" : "FM0-PEP221004",
    "data":dataExampleDetailed
}

dataTurn = []
for i in range(8):
    dataTurn.append(["1 ","2   ","3   ","4   ","5   "])

dataExampleTurn = {
    "op": "1314563",
    "dateInit" : "05/02/2021 11:44:15 AM",
    "dateEnd" : "05/02/2021 11:44:15 AM",
    "dateToday" : "05/02/2021 11:44:15 AM",

    "numOp" : "644",
    "nameOp" : "Eliezer R.",

    "total" : "119",
    "weight" : "3350.70",

    "header" : [" LOTE "," CLIENTE "," PRODUCTO "," Piezas "," Kg/op "],

    "data"  : dataTurn,
 
}

dataExampleTablePiezas = {
    "ticket":"505518",
    "op":"13116542",
    "productCode":"FM0-BIG102103",
    "description":"Marq. Belmont BL (1mm) Bs".upper(),
    "Nbulto":"34",
    "Npiezas":"25"
}

dataExampleTableBobinas = {
    "ticket":"505518",
    "op":"13116542",
    "productCode":"FM0-BIG102103",
    "description":"Marq. Belmont BL (1mm) Bs".upper(),
    "bruteWeight":"34.70"
}

dataExampleFieldsBobinas = {
    "op":"13116542",
    "productCode":"FM0-BIG102103",
    "product":"Marq. Belmont BL (1mm) Bs".upper(),
    "client":"CIGARRERA BIGOTT",
    "maxWeightBob":"35",
    "maxWeightPallet":"6",
    "amtPallet":"24",
    "actualPallet":"2",
}

arrExampleCodigo = ["FM0-BIG102103","FM0-BIG102103","FM0-BIG102103","FM0-BIG102103","FM0-BIG102103","FM0-BIG102103"]

arrExampleProduc = ["MARQ. BELMONT BL (1MM) BS","MARQ. BELMONT BL (1MM) BS","MARQ. BELMONT BL (1MM) BS","MARQ. BELMONT BL (1MM) BS","MARQ. BELMONT BL (1MM) BS","MARQ. BELMONT BL (1MM) BS"]

arrExampleClient = ["CIGARRERA BIGOTT","CIGARRERA BIGOTT","CIGARRERA BIGOTT","CIGARRERA BIGOTT","CIGARRERA BIGOTT","CIGARRERA BIGOTT"]