from components.functions import absPathNormal
from components.functions import absPath
from components.qr import QR
from PySide6 import QtCore

# data = [[lote,cliente,producto,pieza,kg/op], two columns
def placeStrTable(data):
    result = """<table class = "">""" + "\n"
    for i in range(len(data)):
        line = ""
        if str(data[i][4])=="-1": 
            line = line +"""<th colspan="5">"""+str(data[i][0]) + " " +str(data[i][1])+ " "+str(data[i][2])+"""</th>\n"""
        elif str(data[i][4])=="-2": 
            line = line +"""<th colspan="5" align="right">"""+str(data[i][0]) + " " +str(data[i][1])+ " "+"""</th>\n"""
        else:
            for j in range(len(data[0])):
                if j == 0:
                    line = line + """<td class = "box width-1 text-center">""" + str(data[i][j]) + "</td>\n" 
                elif j == 1:
                    line = line + """<td class = "box width-2 text-center">""" + str(data[i][j]) + "</td>\n"
                elif j == 2:
                    line = line + """<td class = "box width-3 text-center">""" + str(data[i][j]) + "</td>\n"
                elif j == 3:
                    line = line + """<td class = "box width-4 text-center">""" + str(data[i][j]) + "</td>\n"
                elif j == 4:
                    line = line + """<td class = "box width-5 text-center">""" + str(data[i][j]) + "</td>\n"
        result = result + """<tr class = "box">""" + line + "</tr>\n"
    result = result + "\n" + "</table>" 
    #print(result)
    return result

def placeStrHeader(header):
    result = """<table class = "main-table">""" + "\n"
    line = ""
    for j in range(len(header)):
        #
        if j == 0:
            line = line + """<td class = "box width-1 font-bold">""" + str(header[j]) + "</td>\n" 
        elif j == 1:
            line = line + """<td class = "box width-2 font-bold">""" + str(header[j]) + "</td>\n"
        elif j == 2:
            line = line + """<td class = "box width-3 font-bold">""" + str(header[j]) + "</td>\n"
        elif j == 3:
            line = line + """<td class = "box width-4 font-bold">""" + str(header[j]) + "</td>\n"
        elif j == 4:
            line = line + """<td class = "box width-5 font-bold">""" + str(header[j]) + "</td>\n"
        #
    result = result + """<tr class = "box">""" + line + "</tr>\n"+ "\n" + "</table>" 
    return result

def getBodyTurn(dataDic):

    dateInit = dataDic["dateInit"] #"05/02/2021 11:44:15 AM"
    dateEnd = dataDic["dateEnd"] #"05/02/2021 11:44:15 AM"
    dateToday = dataDic["dateToday"] #"05/02/2021 11:44:15 AM"

    numOp = dataDic["numOp"] # "644"
    nameOp = dataDic["nameOp"] # "Eliezer R."

    total = dataDic["total"] # "119"
    weight = "{:4.2f}".format(float(dataDic["weight"])) # "3350.70"
    #
    header = [" LOTE "," CLIENTE "," PRODUCTO "," PIEZAS "," Kg/Op "]

    # Example values
    data  = dataDic["data"]
    #print("\nGetting body turn good; with:",data,"\n")

    body_report_turn = """
        <div class = "content">
            <table class = "">
                <tr>
                    <td class = "">
                        <table class = "width-icon-table">
                            <tr><img src=" """+absPathNormal("sources/logo.png")+""" " class = "logo" /></tr>
                            <tr><h6 class = "rif_label">J-00025642-0</h6></tr>
                        </table>
                    </td>
                    <td class = "">
                        <table>
                            <tr class = "">
                                <td>
                                    <table>
                                        <tr>
                                            <td> <strong> FECHA: </strong> </td>
                                            <td>"""+ dateToday +"""</td>                                    
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                            <tr class = "height-2">
                                <td class = "width-title"><h2 class = "main_title font-bold"> REPORTE DE PRODUCCI&Oacute;N POR TURNO </h2></td>
                            </tr>                       
                        </table>                
                    </td>
                </tr>           
            </table>
            <table>
                <tr>
                    <td class = "font-bold"> Fecha: </td>
                    <td>"""+ dateInit +"""</td>
                </tr>
                <tr>
                    <td>   </td>
                    <td>"""+ dateEnd +"""</td>
                    <td class = "pl-1 font-bold"> OPERADOR: </td>
                    <td>"""+ nameOp +""" ("""+ numOp +""") </td>
                </tr>
            </table>
            <hr class = "divider">
            """+placeStrHeader(header)+"""
            <hr class = "divider">
            """+placeStrTable(data)+"""
            <hr class = "divider">
            <table>
                <tr>
                    <td class = "pl-total font-bold"> Totales:</td>
                    <td>"""+ total +"""</td>
                    <td class = "pl-1">"""+ weight +"""</td>
                    <td class = "font-bold"> Kg </td>
                </tr>
            </table>
        <div/>
    """
    #print("Body was good, with: ",body_report_turn)
    return body_report_turn

css_report_turn = """
    *{
        font-family: Arial, Helvetica, sans-serif;
    }
    .width-icon-table{
        min-width:90px;
        max-width:90px;
    }
    .logo{
        max-width:100px;
        min-width:100px;
        width:100px;
        min-height:100px;
        max-height:100px;
        height:100px;
        margin:5px;
    }
    .main-table{
        padding-left:20px;
    }
    .main_title{
        min-width:700px;
        max-width:700px;
        width:700px;  
        padding-left:80px;      
    }
    .rif_label{
        margin-top:0px;
        padding-top:0px;
        padding-bottom:0px;
        margin-left:5px;

        font-size:14px;
        font-weight:500;
        max-height:16px;
        height:16px;        
    }
    .pl-1{
        padding-left:30px;
    }
    .pl-total{
        padding-left:390px;        
    }
    .width-1{
        max-width:120px;
        min-width:120px;
        width:120px;        
    }
    .width-2{
        max-width:400px;
        min-width:400px;
        width:400px;        
    }
    .width-3{
        max-width:260px;
        min-width:260px;
        width:260px;        
    } 
    .width-4{
        max-width:80px;
        min-width:80px;
        width:80px;        
    }  
    .width-5{
        max-width:60px;
        min-width:60px;
        width:60px;        
    } 
    .width-title{
        max-width:700px;
        min-width:700px;
        width:700px;        
    }
    .height-1{
        max-height:10px;
        min-height:10px;
        height:10px;        
    }
    .height-2{
        max-height:20px;
        min-height:20px;
        height:20px;        
    }
    .font-bold{
        font-weight:700;
    }
    .font-normal{
        font-weight:500;
    }
    .box{
        text-align:center;
    }
    .text-center{
        text-align:center;
    }
    .divider{
        margin-left:0px;
        padding-left:0px;
        max-width:1000px;
        width:1000px;
    }
"""

def fillHtmlTicketTurn(body_report_turn, css_return_turn):
    html_report_turn =  """
    <!DOCTYPE html>
    <html><head><style>
                """+ css_report_turn +"""
        </style>
        </head>
        <body>
            """+ body_report_turn +"""
        </body>
    </html>
    """
    return html_report_turn

def getHtmlTurnFilled(dataDic):
    qr = QR()
    html = """"""
    try:
        # Update qrcode with dataDic["op"]
        op = dataDic["op"]
        qr.generate(op, absPath("sources/qr.png"))
        body = getBodyTurn(dataDic)
        html = fillHtmlTicketTurn(body,css_report_turn)

        # adapt view... content to be print.
        html_preview = html.replace(
            """<html><head><style>""",
            """
    <html>
        <head>
        <style>

        body{
            transform: scale(0.46);
            transform-origin: 1.1% 0%;
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
        file.write(html_preview)
        file.close()

    except Exception as e:
        print(e)
    
    return html
