from PySide6 import QtCore
from PySide6 import QtWidgets
from components.clasess import Alert
from components.constants.pesajeBobina import *
from PySide6.QtGui import (QCursor,QFont,QIcon)
from PySide6.QtCore import (QCoreApplication,QMetaObject,QRect,QSize, Qt,QSortFilterProxyModel,QStringListModel)


"""from PyQt5.QtWidgets import QComboBox, QApplication, QCompleter"""
"""from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.Qt import QStringListModel"""
#from PySide6 import QtCore

from PySide6.QtWidgets import (QAbstractScrollArea,  QCheckBox, QComboBox,QFrame, QLCDNumber, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,QSizePolicy, QStatusBar, QTableWidget, 
    QTableWidgetItem,QWidget,QCompleter)

from components.constants.alerts import (ALERT_FIELDS_INIT_PRINT, ALERT_NOT_TARE, 
ALERT_OP_ZERO, ALERT_MAX_WEIGHT_EXEED, ALERT_WEIGHT_ZERO_BY_INIT, ALERT_INVALID_GENERAL)

from components.constants.dataExample import (dataExampleTableBobinas, dataExampleFieldsBobinas,
    arrExampleCodigo, arrExampleProduc)

from components.functions import (getTurn,getDate,getFullDate,appendTable,isFloat,check3DigitsOp,
    changeToError,changeToNormal,changeToSuccess,changeToDisable)

from components.clasess import Action
from components.constants.dataExample import dataExamplePallet

from components.styles.bobinas import BOBINAS_STYLES
from components.functionsBobina import loadStyles