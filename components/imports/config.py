import serial
from PySide6 import QtCore
from PySide6.QtCore import QRect
from components.clasess import Alert
from components.clasess import Action
from PySide6.QtGui import (QCursor,QIcon)
from components.constants.alerts import *
from components.constants.pesajeBobina import *
from components.constants.config import SUCCESS,FAILURE
from components.styles.config import CONFIG_STYLES
from PySide6.QtCore import (QCoreApplication,QMetaObject,QRect,QSize,Qt)

from components.functions import (getAvalaiblePrinters, getallPorts, findComIndex)

from PySide6.QtWidgets import (QCheckBox, QComboBox,QFrame,QLabel,QLineEdit, QMainWindow, 
QMenuBar, QPushButton,QStatusBar,QWidget,QFormLayout)

from components.constants.alerts import (ALERT_INVALID_GENERAL)