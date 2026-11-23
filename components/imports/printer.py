
import win32print
import win32ui
import win32api

from PySide6 import QtCore
from PySide6.QtWidgets import QLabel

from PySide6.QtCore import (QRect, Qt)

import pdfkit

from PIL import Image, ImageWin
from components.functions import scalePdf

from components.clasess import Alert
from components.constants.alerts import *