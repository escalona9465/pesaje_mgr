import sys
import time

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from components.componentsPopup.confirmConfig import confirmConfig

from components.constants.popUp import *
from components.styles.popUp import *
from components.clasess import Action
from components.functions import (isFloat,lookForClient,lookForProduct,deleteClient,deleteProductOnDB,appendTable)
from components.componentsPopup.addOp import * 
from components.componentsPopup.deleteOp  import *
from components.componentsPopup.editOp import *

from components.componentsPopup.deleteProduct import *
from components.componentsPopup.addProduct import *
from components.componentsPopup.editProduct import *

from components.componentsPopup.deleteClient import *
from components.componentsPopup.addClient import *
from components.componentsPopup.editClient import *

from components.componentsPopup.reportPieza import *
from components.componentsPopup.reportPallet import *
from components.componentsPopup.reportOp import *
from components.componentsPopup.inputOrder import *
from components.componentsPopup.inputMatriz import *
from components.componentsPopup.inputHablador import *
from components.componentsPopup.inputWindow import *
from components.componentsPopup.acceptWindow import *
from components.componentsPopup.waitWindow import *
from components.componentsPopup.confirmWindow import *
from components.componentsPopup.confirmWindow import *
from components.componentsPopup.reportTicket import *
from components.componentsPopup.addUsr import *

from components.constants.dataExample import dataExampleTurn,dataExampleGeneralOp,dataExampleDetailedOp

from components.icons import getPopUpIcon,getAicon

from components.constants.dataExample import dataExamplePallet,dataExampleBobina

from components.componentsPopup.actions import actionAccept
