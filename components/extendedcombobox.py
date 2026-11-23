from PySide6 import QtCore
from PySide6 import QtWidgets
from PySide6.QtWidgets import (QAbstractScrollArea,  QCheckBox, QComboBox,QFrame, QLCDNumber, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,QSizePolicy, QStatusBar, QTableWidget, 
    QTableWidgetItem,QWidget,QCompleter)
from PySide6.QtGui import (QCursor,QFont,QIcon)
from PySide6.QtCore import (QCoreApplication,QMetaObject,QRect,QSize, Qt,QSortFilterProxyModel,QStringListModel)


"""**********************************************************************************************************
*************************************************************************************************************
*************************** Agregado el 31/10/2023 para el filtrado *****************************************
*************************** dinamico del comboBox Cod. Productos ********************************************
*************************************************************************************************************
*************************************************************************************************************"""

class ExtendedComboBox(QComboBox):
        def __init__(self, parent=None):
            super(ExtendedComboBox, self).__init__(parent)
    
            self.setFocusPolicy(QtCore.Qt.StrongFocus)
            self.setEditable(True)
    
            # add a filter model to filter matching items
            self.pFilterModel = QSortFilterProxyModel(self)
            self.pFilterModel.setFilterCaseSensitivity(Qt.CaseInsensitive)
            self.pFilterModel.setSourceModel(self.model())
    
            # add a completer, which uses the filter model
            self.completer = QCompleter(self.pFilterModel, self)
            # always show all (filtered) completions
            self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
            self.setCompleter(self.completer)
    
            # connect signals
            self.lineEdit().textEdited[str].connect(self.pFilterModel.setFilterFixedString)
            self.completer.activated.connect(self.on_completer_activated)
    
    
        # on selection of an item from the completer, select the corresponding item from combobox
        def on_completer_activated(self, text):
            if text:
                index = self.findText(text)
                self.setCurrentIndex(index)
                self.activated.emit(self.itemText(index))
                
    
    
        # on model change, update the models of the filter and completer as well
        def setModel(self, model):
            super(ExtendedComboBox, self).setModel(model)
            self.pFilterModel.setSourceModel(model)
            self.completer.setModel(self.pFilterModel)
    
    
        # on model column change, update the model column of the filter and completer as well
        def setModelColumn(self, column):
            self.completer.setCompletionColumn(column)
            self.pFilterModel.setFilterKeyColumn(column)
            super(ExtendedComboBox, self).setModelColumn(column)

"""**********************************************************************************************************
*************************************************************************************************************"""
