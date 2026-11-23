############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################
import qrcode,time

from components.functions import absPathNormal

class QR():
    def __init__(self) -> None:
        self.path = ""
        self.data = ""
        self.size = 8

    def generate(self,data,path):
        self.path = path
        handler = qrcode.make(data,box_size = self.size)
        handler.save(path)

    def generateLot(self,arrayInfo):
        for k in range(len(arrayInfo)):
            info = "[ "+ arrayInfo[k][0]+" | "+arrayInfo[k][1]+" | "+arrayInfo[k][2]+" | "+arrayInfo[k][3]+" | "+arrayInfo[k][4]+" | "+arrayInfo[k][5]+" | "+arrayInfo[k][6]+" | "+arrayInfo[k][7]+" | "+arrayInfo[k][8]+" | "+arrayInfo[k][9]+" | "+arrayInfo[k][10]+" | "+arrayInfo[k][11]+" | "+arrayInfo[k][12] + " ]"
            path = absPathNormal("sources/qrs/"+ arrayInfo[k][0] + ".png")
            self.generate(info,path)
        pass

