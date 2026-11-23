from PySide6 import QtCore
from PySide6 import QtWidgets
from components.clasess import Alert
from components.constants.alerts import *
from PySide6.QtGui import (QCursor,QFont,QIcon)
from components.constants.pesajeBobina import *
from components.styles.piezas import PIEZAS_STYLES
from PySide6.QtCore import (QCoreApplication,QMetaObject,QRect,QSize, Qt)
from components.functions import (getTurn,getDate,getFullDate,appendTable,check3DigitsOp,isFloat,
changeToError,changeToNormal,changeToSuccess)

from PySide6.QtWidgets import (QAbstractScrollArea,QComboBox,QFrame, QLCDNumber, QLabel,QLineEdit,
    QMainWindow, QMenuBar, QPushButton,QSizePolicy, QStatusBar, QTableWidget, QWidget)

from components.constants.dataExample import (dataExampleTablePiezas, dataExampleFieldsBobinas,
    arrExampleCodigo, arrExampleProduc)

from components.constants.alerts import (ALERT_INVALID_GENERAL)
from components.functionsPieza import loadStyles