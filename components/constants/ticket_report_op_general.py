############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.constants.bootstrap import BOOTSTRAP
from components.functions import absPathNormal
from components.functions import absPath
from components.qr import QR

def getBodyGeneral(dataDic):

    op = dataDic["op"] #"13117002" 

    clientId = dataDic["clientId"] # "FM0-PEP221004"
    clientName = dataDic["clientName"] # "Eliezer R."

    productName = dataDic["productName"] # "Doritos pincante 2022+"
    productId = dataDic["productId"] # "FM0-PEP221004"

    Npaletas = dataDic["nPaletas"] # "6"
    BxPaletas = dataDic["bxPaletas"] # "26"

    total = dataDic["total"] # "250.00"
    total = "{:4.2f}".format(float(total))
    units = dataDic["units"] # "12"

    body_report_general = """
        <div class = "content scaled">
            <table class = "top-box">
                <tr>
                    <td class = "box icon-space">
                        <table>
                            <tr><img src=" """+absPathNormal("sources/logo.png")+""" " class = "logo" /></tr>
                            <tr><h6 class = "rif_label">J-00025642-0</h6></tr>
                        </table>
                    </td>
                    <td class = ""><h2 class = "main_title font-bold"> REPORTE GENERAL OP </h2></td>
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

                    <td class = "col-auto font-bold"> COD. CLIENTE: </td>
                    <td class = "text-center">"""+ clientId +"""</td>
                </tr>
            </table>
            <table>
                <tr>
                    <td class = "col-auto font-bold"> PRODUCTO: </td>
                    <td class = "text-center">"""+ productName +"""</td>

                    <td class = "col-auto font-bold"> COD. PRODUCTO: </td>
                    <td class = "text-center">"""+ productId +"""</td>
                </tr>
            </table>
            <hr class = "divider">
            <table class = "main-table">
                <tr>
                    <td class = "col-auto text-center font-bold"> N Paletas </td>
                    <td class = "col-auto text-center">"""+ Npaletas +"""</td>
                    
                </tr>
            </table> 
            <hr class = "divider"> 
            <table class = "main-table">
                <tr>
                    <td class = "col-auto text-center font-bold"> Bobinas por Paletas </td>
                    <td class = "col-auto text-center">"""+ BxPaletas +"""</td>
                </tr>
            </table>   
            <hr class = "divider">     
            <table>
                <tr>
                    <td class = "text-center font-bold"> TOTAL: </td>
                    <td class = "text-center"> """+ total +""" </td>
                    <td class = "ml-1 text-center font-bold"> Kg </td>
                    <td class = "pl-units text-center font-bold"> TOTAL BOBINAS: </td>
                    <td class = "ml-1 text-center">"""+ units +"""</td>
                </tr>
            </table>      
        <div/>
    """
    return body_report_general

css_report_general = BOOTSTRAP + """
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
        padding-left:110px;
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
"""

def fillHtmlTicketOp(body_report_general,css_report_general):
    html_report_general =  """
    <!DOCTYPE html>
    <html>
        <head>
        <style>
                """+ css_report_general +"""
        </style>
        </head>
        <body>
            """+ body_report_general +"""
        </body>
    </html>
    """
    return html_report_general

def getHtmlGeneralFilled(dataDic):
    qr = QR()
    html = """"""
    try:
        # Update qrcode with dataDic["op"]
        op = dataDic["op"]
        qr.generate(op, absPath("sources/qr.png"))
        body = getBodyGeneral(dataDic)
        html = fillHtmlTicketOp(body,css_report_general)

        file = open("C:/Users/elrodriguez/Desktop/pesaje_mgr_PC_16_06_2022_L1/tempHtml.html","w", encoding='utf-8')
        file.write(html)
        file.close()


    except Exception as e:
        print(e)
        pass
    
    return html
