############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.functions import absPathNormal
from components.functions import absPath
from components.qr import QR
from PySide6 import QtCore

def getBodyHablador(dataDic):

    product = dataDic["product"]
    position = dataDic["position"]
    amount = dataDic["amount"]
    amount = "{:4.2f}".format(float(amount))
    observations = dataDic["observations"]
    
    body_report_hablador = """
        <div class = "content scaled">
            <table class = "top-box">
                <tr>
                    <td class = "box icon-space">
                        <table>
                            <tr>
                                <img src=" """+absPathNormal("sources/logo.png")+""" " class = "logo" />
                                <h6 class = "rif_label">J-00025642-0</h6>
                            </tr>
                        </table>
                    </td>
                    <td class = ""><h2 class = "main_title font-bold"> DESCRIPCION DEL PRODUCTO </h2></td>
                </tr>           
            </table>
            <hr class = "divider">
            <table class="padding-20">
                <tr>
                    <td class = "width-1 font-bold product"> """+product+""" </td>
                </tr>
            </table>
            <hr class = "divider">
            <table class="padding-20">
                <tr>
                    <td class = "position text-center font-bold f-0"> POSICION: </td>
                    <td class = "text-center pos_area font-bold f-1"> """+position+""" </td>
                    <td class = "text-center font-bold f-0"> CANT.: </td>
                    <td class = "text-center amt_area font-bold f-1"> """+amount+""" Kg</td>
                </tr>
            </table> 
            <hr class = "divider"> 
            <table class="padding-20">
                <tr>
                    <td class = "title_observation f-0"> OBSERVACIONES:<br>"""+observations+"""</td>
                </tr>
            </table> 
                 
        </div>
    """
    return body_report_hablador

css_hablador = """
    *{
        font-family: Arial, Helvetica, sans-serif;
    }
    .product{
        font-size:60px;  
    }
    .f-0{
        font-size:55px !important;  
    }
    .f-1{
        font-size:85px !important;  
    }
    .rif_label{
        font-size:22px;
        margin-top:-6px !important;
    }
    .observation,.product,position{
        margin-left:20px;
    }
    .content{
        margin-top:300px;
        border:solid;
        border-width:1px;
        padding:10px;
    }
    .logo{
        max-width:120px;
        min-width:140px;
        min-height:120px;
        max-width:140px;
    } 
    .main_title{
        font-size:50px;
        padding-left:100px;    
    }
    td{
        font-size:25px;
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
    .padding-20{
        padding:20px;
    }
    .title_observation{
        font-size:50px;
        font-weight:800;
    }
    .pos_area,.amt_area{
        padding-left:20px;
        padding-right:20px;
    }


"""

def fillHtmlTicketHablador(body_report_hablador,css_hablador):
    html_report_op =  """
    <html><head><style>
                """+ css_hablador +"""
        </style>
        </head>
        <body>
            """+ body_report_hablador +"""
        </body>
    </html>
    """
    return html_report_op

def getHtmlHabladorFilled(dataDic):
    qr = QR()
    html = """"""
    try:
        # Update qrcode with dataDic["op"]
        #op = dataDic["op"]
        #qr.generate(op, absPath("sources/qr.png"))
        body = getBodyHablador(dataDic)
        html = fillHtmlTicketHablador(body,css_hablador)

        # adapt view... content to be print.
        html = html.replace(
            """<html><head><style>""",
            """
    <html>
        <head>
        <style>

    body{
            transform: scale(0.2);
            transform-origin: 0% -47%;
            width:1200px;
            height:800px;
            padding:0px;
            margin:0px;
        }
        html{
            width:1200px;
            height:800px;
            padding:0px;
            margin:0px;        
        }            
            """)
        dir = QtCore.QFileInfo("tempHtml.html").absoluteFilePath()
        file = open(dir,"w", encoding='utf-8')
        file.write(html)
        file.close()


    except Exception as e:
        print(e)
        pass
    return html
