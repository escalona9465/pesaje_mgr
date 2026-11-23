############# DIgitalizacion Insdustrial #########################
############# Autor: Eliezer R  ##################################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.functions import absPathNormal
from components.functions import absPath
from components.qr import QR
from PySide6 import QtCore

# data = [[nro,peso,ticket,bob.Matriz,nro,peso,ticket,bob.Matriz]], two columns
def placeStrTable(data):
    result = "<table>" + "\n"
    for i in range(len(data)):
        line = ""
        for j in range(len(data[0])):
            #
            if j == 0 or j == 4:
                line = line + """<td class = "box width-1">""" + str(data[i][j]) + "</td>\n" 
            elif (j > 0 and j < 3) or (j > 4 and j < 7):
                line = line + """<td class = "box width-2">""" + str(data[i][j]) + "</td>\n"
            else:
                line = line + """<td class = "box width-3">""" + str(data[i][j]) + "</td>\n"
            #
        result = result + """<tr class = "box">""" + line + "</tr>\n"
    result = result + "\n" + "</table>" 
    return result

def getBodyPallet(dataDic,peso_paleta):
    
    date = dataDic["date"] #""
    clientCode = dataDic["clientCode"] #""
    clientName = dataDic["client"] #""
    productCode = dataDic["productCode"] #""
    productName = dataDic["product"] #""

    bobinas = dataDic["bobinas"] #"0"
    pesoBruto = dataDic["pesoBruto"] #"0,00"
    pesoTotal = "{:4.2f}".format(float(peso_paleta) + float(pesoBruto))
    pesoBruto = "{:4.2f}".format(float(pesoBruto))
    pesoNeto = dataDic["pesoNeto"] #"0,00"
    pesoNeto = "{:4.2f}".format(float(pesoNeto))

    mgrCode = dataDic["mgrCode"] #"MGR-GPR-F19(Ed.01)"
    op = dataDic["op"] #""
    paletas = dataDic["paletas"]
    
    header = [[" N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "," N&deg;. "," 9. Peso "," 10. Ticket "," 11. Bob. Matriz "]]

    data  = dataDic["data"] #[]

    username = dataDic["usr"]

    tara = dataDic["tara"]

    supervisor = dataDic["supervisor"]

    body_ticket_pallet = """
        <div class = "content">
            <table class = "top-box">
                <tr>
                    <td class = "box icon-space">
                        <table>
                            <tr><img src=" """+absPathNormal("sources/logo.png")+""" " class = "logo" /></tr>
                            <tr><h6 class = "rif_label">J-00025642-0</h6></tr>
                        </table>
                    </td>
                    <td class = ""><h2 class = "main-title"> LISTA DE EMPAQUE EN PESO </h2></td>
                </tr>           
            </table>
            <table>
                <tr class = "line-box">
                    <td class = "box width-1">1.</td>
                    <td class = "box width-4"> Fecha y hora de Elaboraci&oacute;n: </td>
                    <td class = "box  width-5">"""+date+"""</td>
                </tr>
                <tr class = "line-box">
                    <td class = "box width-1">2.</td>
                    <td class = "box width-4"> C&oacute;digo de Cliente: </td>
                    <td class = "box width-5">"""+clientCode+"""</td>
                </tr> 
                <tr class = "line-box">
                    <td class = "box width-1">3.</td>
                    <td class = "box width-4"> Nombre de Cliente: </td>
                    <td class = "box width-5">"""+clientName+"""</td>
                </tr> 
                <tr class = "line-box">
                    <td class = "box width-1">4.</td>
                    <td class = "box width-4"> C&oacute;digo del Producto: </td>
                    <td class = "box width-5">"""+productCode+"""</td>
                </tr> 
                <tr class = "line-box">
                    <td class = "box width-1">5.</td>
                    <td class = "box width-4"> Nombre de Producto: </td>
                    <td class = "box width-5">"""+productName+"""</td>
                </tr>
                <table>
                    <tr class = "line-box">
                        <td class = "box width-1">6.</td>
                        <td class = "box width-7"> Orden de producci&oacute;n: </td>
                        <td class = "box width-8">"""+op+"""</td>

                        <td class = "box width-1">7.</td>
                        <td class = "box width-9"> N&deg; Paletas: </td>
                        <td class = "box width-10">"""+paletas+"""</td>
                    </tr>            
                </table>
                <table>
                    <tr class = "line-box">
                        <td class = "box width-1">8.</td>
                        <td class = "box width-2"> Tara: </td>
                        <td class = "box width-2">"""+tara+"""</td>
                        <td class = "box width-3"> Kg </td>
                        <td class = "box width-6"></td>
                    </tr>             
                </table> 
                                    
            </table>
            """+placeStrTable(header)+"""
            """+placeStrTable(data)+"""
            <table>
                <tr class = "line-box">
                    <td class = "box width-1">12.</td>
                    <td class = "box width-21"> Bobinas: </td>
                    <td class = "box  width-20">"""+ bobinas +"""</td>

                    <td class = "box width-1">13.</td>
                    <td class = "box width-21"> Peso Bruto: </td>
                    <td class = "box width-24">"""+ pesoBruto +"""</td>
                    <td class = "box width-1"> kg </td>
                </tr>                    
            </table>
            <table>
                <tr class = "line-box">
                    <td class = "box width-1">14.</td>
                    <td class = "box width-21"> Peso Neto: </td>
                    <td class = "box width-24">"""+ pesoNeto +"""</td>
                    <td class = "box width-1"> kg </td>

                    <td class = "box width-1"> 15. </td>
                    <td class = "box width-21"> Peso Total de Paleta: </td>
                    <td class = "box width-24">"""+ pesoTotal +"""</td>
                    <td class = "box width-1"> Kg</td> 
                </tr>           
            </table>
            <table>
                <tr class = "line-box">
                    <td class = "box width-1">15.</td>
                    <td class = "box width-21"> Usuario: </td>
                    <td class = "box width-20">"""+username+"""</td>
                    <td class = "box width-1">17.</td>
                    <td class = "box width-21"> Supervisor: </td>
                    <td class = "box width-20">"""+supervisor+"""</td>               
                </tr>           
            </table>
            <table>
                <tr class = "line-box">
                    <td class = "box width-16 text-right"> """+ mgrCode +"""</td>          
                </tr>          
            </table>
        </div>
    """
    return body_ticket_pallet

css_ticket_pallet = """

    *{
        font-family: Arial, Helvetica, sans-serif;
    }

    .logo{
        max-width:70px;
        min-width:90px;
        min-height:70px;
        max-width:90px;
    }
    .weight_box{
        border:solid;
        border-width:1px;
        border-color:black;
        text-align:center;
        padding-left:20px;
        padding-right:20px;
    }
    .height-1{
        max-height:20px;
        height:20px;
    }

    .sub_title{
        max-height:10px;
        height:10px;
    }
    .value{
        font-weight:500;
        max-height:10px;
        height:10px;
        padding-left:20px;
        padding-right:20px;
    }

    .main-title{
        min-width:500px;
        max-width:500px;
        width:500px;

        padding-left:114.8px;
        padding-right:114.8px;
    }
    .rif_label{
        margin-top:0px;
        padding-top:0px;
        padding-bottom:0px;

        font-size:14px;
        font-weight:500;
        max-height:16px;
        height:16px;
    }
    .top-box{
        border:solid;
        border-width:1px;
        border-color:back;
        margin:0px;
        border-collapse: collapse;

        min-height:120px;
        max-height:120px;

        min-width:847px;
        max-width:848px;

        padding:0px;
        border-collapse: collapse;

        text-align:center;
    }
    .box{
        text-align:center;
        border:solid;
        border-width:1px;
        border-color:back;
        margin:0px;
        border-collapse: collapse;
    }
    .line-box{
        padding:0px;
        border-collapse: collapse;
    }
    table{
        border-collapse: collapse;
    }
    .width-1{
        max-width:40px;
        min-width:40px;
        width:40px;
    }
    .width-kg-last{
        max-width:39.5px;
        min-width:39.5px;
        width:39.5px;
    }
    .width-2{
        max-width:110px;
        min-width:110px;
        width:110px;
    }
    .width-3{
        max-width:150px;
        min-width:150px;
        width:150px;
    }
    .width-4{
        max-width:223px;
        min-width:223px;
        width:223px;
    }
    .width-5{
        max-width:572px;
        min-width:572px;
        width:572px;
    }
    .width-6{
        max-width:419px;
        min-width:419px;
        width:419px;
    }
    .width-7{
        max-width:223px;
        min-width:223px;
        width:223px;
    }
    .width-8{
        max-width:150px;
        min-width:150px;
        width:150px;
    }
    .width-9{
        max-width:186px;
        min-width:186px;
        width:186px;
    }
    .width-10{
        max-width:188px !important;
        min-width:188px !important;
        width:188px !important;
    }
    .width-11{
        max-width:110px;
        min-width:110px;
        width:100px;
    }
    .width-12{
        max-width:110px;
        min-width:110px;
        width:110px;
    }
    .width-13{
        max-width:115px;
        min-width:115px;
        width:115px;
    }
    .width-14{
        max-width:111px;
        min-width:111px;
        width:111px;
    }
    .width-15{
        max-width:111px;
        min-width:111px;
        width:111px;
    }
    .width-16{
        max-width:822px;
        min-width:822px;
        width:822px;
    }
    .width-mgrcode{
        max-width:823px;
        min-width:823px;
        width:823px;
    }
    .width-17{
        max-width:111px;
        min-width:111px;
        width:111px;
    }
    .width-18{
        max-width:111px;
        min-width:111px;
        width:111px;
    }
    .width-19{
        max-width:376px;
        min-width:376px;
        width:376px;
    }

    .width-20{
        max-width:187px;
        min-width:187px;
        width:187px;
    }
    .width-supervisor{
        max-width:186px;
        min-width:186px;
        width:186px;
    }
    .width-21{
        max-width:186px;
        min-width:186px;
        width:186px;
    }
    .width-22{
        max-width:111px;
        min-width:111px;
        width:111px;
    }
    .width-24{
        max-width:144px;
        min-width:144px;
        width:144px;
    }
    .width-23{
        max-width:111px;
        min-width:111px;
        width:111px;
    }

    .icon-space{
        margin-top:5px;
        margin-left:5px;
        padding-left:10px;
        padding-right:10px;
        padding-top:10px;
    }
    .text-right{
        text-align:right;
        padding-right:20px;
    }
"""

def fillHtmlTicketPallet(body_ticket_pallet,css_ticket_pallet):
    html_ticket_pallete =  """
    <!DOCTYPE html>
    <html><head><style>
                """+ css_ticket_pallet +"""
        </style>
        </head>
        <body>
            """+ body_ticket_pallet +"""
        </body>
    </html>
    """
    return html_ticket_pallete

def getHtmlPalletFilled(dataDic,peso_paleta):
    qr = QR()
    html = """"""
    try:
        # Update qrcode with dataDic["op"]
        op = dataDic["op"]
        qr.generate(op, absPath("sources/qr.png"))
        body = getBodyPallet(dataDic,peso_paleta)
        html = fillHtmlTicketPallet(body,css_ticket_pallet)
        #print("Body pallet:",body)
        #print("html pallet:",html)


        # adapt view... content to be print.
        preview_html = html.replace(
            """<html><head><style>""",
            """
    <html>
        <head>
        <style>

    body{
            transform: scale(0.46);
            transform-origin: 2.2% 0%;
            width:3500px;
            height:8000px;
            padding:0px;
            margin:0px;
        }
        html{
            width:3500px;
            height:8000px;
            padding:0px;
            margin:0px;        
        }               
            """)
        dir = QtCore.QFileInfo("tempHtml.html").absoluteFilePath()
        file = open(dir,"w", encoding='utf-8')
        file.write(preview_html)
        file.close()

    except Exception as e:
        print("Generating the pallet print",e)
        pass
    
    return html