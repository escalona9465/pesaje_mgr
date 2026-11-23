from PySide6.QtCore import Qt

from PySide6.QtWidgets import QTableWidgetItem

from pathlib import Path
import ctypes, sys, serial
from datetime import datetime
import subprocess
import serial.tools.list_ports
import PyPDF2