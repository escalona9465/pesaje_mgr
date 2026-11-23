
# Bibliotecas graficas
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QStackedLayout,QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon,QCursor,QAction
from PySide6 import QtCore
from PySide6.QtCore import *
# Bibliotecas auxiliares
import sys
import time
import PySide6
from datetime import date
# Módulos auxiliares
from components.printer import Printer
from components.functions import absPath,findComIndex
from components.clasess import Action
# Componentes
from components.popup import PopUp
from components.provider import Provider
from components.icons import *
# Contantes 
from components.constants.popUp import *
# Styles
from components.styles.popUp import *

from components.interfaces.login import LoginUi
from components.interfaces.pesajeBobina import PesajeUi
from components.interfaces.pesajePiezas import PiezaUi
from components.interfaces.tipoProducto import ProductUi
from components.interfaces.config import ConfigUi

from components.constants.ticket_peso_bobina_test import getHtmlBobinaFilled
from components.constants.ticket_peso_pieza import getHtmlPiezaFilled
from components.constants.ticket_peso_pallet import getHtmlPalletFilled
from components.constants.ticket_report_op import getHtmlOpFilled
from components.constants.ticket_report_op_detailed import getHtmlDetailedFilled
from components.constants.ticket_report_op_general import getHtmlGeneralFilled
from components.constants.ticket_report_turn import getHtmlTurnFilled

from components.constants.dataExample import *

from components.constants.ticket_hablador import getHtmlHabladorFilled
from components.constants.dataExample import dataExampleHablador

import subprocess