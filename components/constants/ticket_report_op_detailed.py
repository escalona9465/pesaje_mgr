############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.constants.bootstrap import BOOTSTRAP
from components.functions import absPathNormal
from components.functions import absPath
from components.qr import QR

def placeStrTable(data):
    result = """<table class = "main-table">""" + "\n"
    for i in range(len(data)):
        line = ""
        for j in range(len(data[0])):
            #
            if j == 0:
                line = line + """<td class = "unbox accum-width">""" + str(data[i][j]) + "</td>\n" 
            elif j == 1:
                line = line + """<td class = "unbox amt-width">""" + str(data[i][j]) + "</td>\n"
            elif j == 2:
                line = line + """<td class = "unbox user-width">""" + str(data[i][j]) + "</td>\n"
            elif j > 2:
                line = line + """<td class = "unbox weight-width">""" + str(data[i][j]) + "</td>\n"
            #
        result = result + """<tr class = "unbox">""" + line + "</tr>\n"
    result = result + "\n" + "</table>" 
    return result

def getBodyDetailed(dataDic):

    op = dataDic["op"] #"13117002" 

    clientId = dataDic["clientId"] # "FM0-PEP221004"
    clientName = dataDic["clientName"] # "Eliezer R."

    productName = dataDic["productName"] # "Doritos pincante 2022+"
    productId = dataDic["productId"] # "FM0-PEP221004"

    data = dataDic["data"]

    body_report_detailed = """
        <div class = "content scaled">
            <table class = "top-box">
                <tr>
                    <td class = "box icon-space">
                        <table>
                            <tr><img src=" """+absPathNormal("sources/logo.png")+""" " class = "logo" /></tr>
                            <tr><h6 class = "rif_label">J-00025642-0</h6></tr>
                        </table>
                    </td>
                    <td class = ""><h2 class = "main_title font-bold"> REPORTE DETALLADO OP </h2></td>
                </tr>           
            </table>
            <table>
                <tr>
                    <td class = "text-center font-bold"> NUMERO DE OP: </td>
                    <td class = "text-center">"""+ op +"""</td>
                </tr>
            </table>
            <hr class = "divider">
            <table>
                <tr>
                    <td class = "col-auto font-bold"> CLIENTE: </td>
                    <td class = "text-center">"""+ clientName +"""</td>

                    <td class = "col-auto font-bold pl-1"> COD. CLIENTE: </td>
                    <td class = "text-center">"""+ clientId +"""</td>
                </tr>
            </table>
            <table>
                <tr>
                    <td class = "col-auto font-bold"> PRODUCTO: </td>
                    <td class = "text-center">"""+ productName +"""</td>

                    <td class = "col-auto font-bold pl-1"> COD. PRODUCTO: </td>
                    <td class = "text-center">"""+ productId +"""</td>
                </tr>
            </table>
            <hr class = "divider">
            <table class = "main-table">
                <tr>
                    <td class = "accum-width text-center font-bold"> N Ticket </td>
                    <td class = "amt-width text-center font-bold"> Fecha de Emision </td>
                    <td class = "user-width text-center font-bold"> Usuario </td>

                    <td class = "weight-width text-center font-bold"> Bruto (Kg) </td>
                    <td class = "weight-width text-center font-bold"> Tara (Kg) </td>
                    <td class = "weight-width text-center font-bold"> Neto (Kg) </td>
                </tr>
            </table> 
            <hr class = "divider"> 
            """+placeStrTable(data)+"""   
            <hr class = "divider">           
        <div/>
    """
    return body_report_detailed

css_report_detailed = BOOTSTRAP + """
    *{
        font-family: Arial, Helvetica, sans-serif;
    }
    .logo{
        max-width:70px;
        min-width:90px;
        min-height:70px;
        max-width:90px;
    }
    .main_title{
        padding-left:200px;      
    }
    .main-table{
        padding-left:40px;
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
    .divider{

    }
    .width-1{
        max-width:100px;
        min-width:100px;
        width:100px;
    }
    .accum-width{
        max-width:200px;
        min-width:200px;
        width:200px;
    }
    .amt-width{
        max-width:150px;
        min-width:150px;
        width:150px;
    }
    .user-width{
        max-width:200px;
        min-width:200px;
        width:200px;
    }
    .width-cod{
        max-width:150px;
        min-width:150px;
        width:150px;        
    }
    .weight-width{
        max-width:150px;
        min-width:150px;
        width:200px;        
    }
    .text-center{
        text-align:center;
    }

    .ml-1{
        margin-left:30px;
    }
    .pl-1{
        padding-left:200px;
    }
    .font-bold{
        font-weight:700;
    }
    .font-normal{
        font-weight:500;
    }
    .pl-units{
        padding-left:30px;
    }
    .unbox{
        text-align:center;
        border:none !important;
        border-collapse: collapse;        
    }
"""

def fillHtmlTicketOp(body_report_detailed,css_report_detailed):
    html_report_detailed =  """
    <!DOCTYPE html>
    <html>
        <head>
        <style>
                """+ css_report_detailed +"""
        </style>
        </head>
        <body>
            """+ body_report_detailed +"""
        </body>
    </html>
    """
    return html_report_detailed

def getHtmlDetailedFilled(dataDic):
    qr = QR()
    html = """"""
    try:
        # Update qrcode with dataDic["op"]
        op = dataDic["op"]
        qr.generate(op, absPath("sources/qr.png"))
        body = getBodyDetailed(dataDic)
        html = fillHtmlTicketOp(body,css_report_detailed)

        file = open("C:/Users/elrodriguez/Desktop/pesaje_mgr_PC_16_06_2022_L1/tempHtml.html","w", encoding='utf-8')
        file.write(html)
        file.close()


    except Exception as e:
        print(e)
        pass
    
    return html
