############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from PySide6.QtWidgets import (QStyle)
from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon

from components.functions import absPath


def getTicketIcon():
    icon = QIcon(absPath("sources/ticket.png"))
    return icon

def getCustomizeIcon():
    icon = QIcon(absPath("sources/customize.png"))
    return icon

def getActivateIcon(window):
    activateIcon = window.style().standardIcon(getattr(QStyle, "SP_DialogYesButton"))
    return activateIcon

def getUserIcon():
    icon = QIcon(absPath("sources/user.png"))
    return icon

def getCloseIcon():
    icon = QIcon(absPath("sources/close.png"))
    return icon

def getDeleteIcon():
    icon = QIcon(absPath("sources/delete.png"))
    return icon

def getEditIcon():
    icon = QIcon(absPath("sources/edit.png"))
    return icon

def getAddIcon():
    icon = QIcon(absPath("sources/add.png"))
    return icon

def getConfigIcon():
    icon = QIcon(absPath("sources/config.png"))
    return icon

def getHelpIcon():
    icon = QIcon(absPath("sources/help.png"))
    return icon

def getPalletIcon():
    icon = QIcon(absPath("sources/pallet.png"))
    return icon

def getOpIcon():
    icon = QIcon(absPath("sources/documents.png"))
    return icon

def getOperatorIcon():
    icon = QIcon(absPath("sources/worker.png"))
    return icon

def getTalkersIcon():
    icon = QIcon(absPath("sources/habladores.png"))
    return icon

def getPiecesIcon():
    icon = QIcon(absPath("sources/piezas.png"))
    return icon

def getProductionIcon():
    icon = QIcon(absPath("sources/production.png"))
    return icon

def getClientIcon():
    icon = QIcon(absPath("sources/team.png"))
    return icon

def getProductIcon():
    icon = QIcon(absPath("sources/product.png"))
    return icon

def getLogOutIcon():
    icon = QIcon(absPath("sources/log-out.png"))
    return icon

def getMGRIcon():
    icon = QIcon(absPath("sources/logo.png"))
    return icon

def getPopUpIcon():
    icon = QIcon(absPath("sources/software.png"))
    return icon    

def getAicon(name):
    icon = QIcon(absPath(f"sources/{name}.png"))
    return icon