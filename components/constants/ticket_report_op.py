############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.functions import absPathNormal
from components.functions import absPath
from components.qr import QR

def getBodyOp(dataDic):

    op = dataDic["op"] #"13117002" 

    clientId = dataDic["clientId"] # "FM0-PEP221004"
    clientName = dataDic["clientName"] # "Eliezer R."

    productName = dataDic["productName"] # "Doritos pincante 2022+"
    productId = dataDic["productId"] # "FM0-PEP221004"

    accum = dataDic["accum"] # "250.00"
    amount = dataDic["amount"] # "12"
    user = dataDic["user"] # "ISNALDO TORREALBA"

    total = dataDic["total"] # "250.00"
    units = dataDic["units"] # "12"

    body_report_op = """
        <div class = "content scaled">
            <table class = "top-box">
                <tr>
                    <td class = "box icon-space">
                        <table>
                            <tr><img src=" """+absPathNormal("sources/logo.png")+""" " class = "logo" /></tr>
                            <tr><h6 class = "rif_label">J-00025642-0</h6></tr>
                        </table>
                    </td>
                    <td class = ""><h2 class = "main_title font-bold"> REPORTE DE OP </h2></td>
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
                    <td class = "width-1 font-bold"> CLIENTE: </td>
                    <td class = "text-center">"""+ clientName +"""</td>

                    <td class = "width-cod font-bold pl-1"> COD. CLIENTE: </td>
                    <td class = "text-center">"""+ clientId +"""</td>
                </tr>
            </table>
            <table>
                <tr>
                    <td class = "width-1 font-bold"> PRODUCTO: </td>
                    <td class = "text-center">"""+ productName +"""</td>

                    <td class = "width-cod font-bold pl-1"> COD. PRODUCTO: </td>
                    <td class = "text-center">"""+ productId +"""</td>
                </tr>
            </table>
            <hr class = "divider">
            <table class = "main-table">
                <tr>
                    <td class = "accum-width text-center font-bold"> ACUMULADO </td>
                    <td class = "amt-width text-center font-bold"> CANTIDAD </td>
                    <td class = "user-width text-center font-bold"> USUARIO </td>
                </tr>
            </table> 
            <hr class = "divider"> 
            <table class = "main-table">
                <tr>
                    <td class = "accum-width text-center">"""+ accum +"""</td>
                    <td class = "amt-width text-center">"""+ amount +"""</td>
                    <td class = "user-width text-center">"""+ user +"""</td>
                </tr>
            </table>   
            <hr class = "divider">     
            <table>
                <tr>
                    <td class = "text-center font-bold"> Total: </td>
                    <td class = "text-center"> """+ total +""" </td>
                    <td class = "ml-1 text-center font-bold"> Kg </td>
                    <td class = "pl-units text-center font-bold"> Unidades </td>
                    <td class = "ml-1 text-center">"""+ units +"""</td>
                </tr>
            </table>      
        <div/>
    """
    return body_report_op

css_report_op = """
    *{
        font-family: Arial, Helvetica, sans-serif;
    }
    .logo{
        max-width:60px;
        min-width:80px;
        min-height:60px;
        max-width:80px;
    } 
    .main_title{
        padding-left:250px;      
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

def fillHtmlTicketOp(body_report_op,css_report_op):
    html_report_op =  """
    <!DOCTYPE html>
    <html>
        <head>
        <style>
                """+ css_report_op +"""
        </style>
        </head>
        <body>
            """+ body_report_op +"""
        </body>
    </html>
    """
    return html_report_op

def getHtmlOpFilled(dataDic):
    qr = QR()
    html = """"""
    try:
        # Update qrcode with dataDic["op"]
        op = dataDic["op"]
        qr.generate(op, absPath("sources/qr.png"))
        body = getBodyOp(dataDic)
        html = fillHtmlTicketOp(body,css_report_op)

        file = open("C:/Users/elrodriguez/Desktop/pesaje_mgr_PC_16_06_2022_L1/tempHtml.html","w", encoding='utf-8')
        file.write(html)
        file.close()


    except Exception as e:
        print(e)
        pass
    
    return html
