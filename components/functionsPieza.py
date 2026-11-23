############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.styles.bobinas import BOBINAS_STYLES
from components.constants.pesajeBobina import *
from components.styles.colors import *


def loadStyles(obj,type):
    if type == INIT_PESAJE:
        obj.botonCaptura.setStyleSheet("""
            QPushButton#botonCaptura{
                background-color:"""+red_normal+""";
            }
        """)
        obj.botonOP.setStyleSheet("""
            QPushButton#botonOP{
                background-color:"""+yellow_normal+""";
            }
        """)
        obj.botonIniciar.setStyleSheet("""
            QPushButton#botonIniciar{
                background-color:"""+green_normal+""";
            }
        """)
    elif type == CAPTURE_WEIGHT:
        obj.botonCaptura.setStyleSheet("""
            QPushButton#botonCaptura{
                background-color:"""+red_normal+""";
            }
        """)
        obj.botonOP.setStyleSheet("""
            QPushButton#botonOP{
                background-color:"""+yellow_normal+""";
            }
        """)
        obj.botonIniciar.setStyleSheet("""
            QPushButton#botonIniciar{
                background-color:"""+green_normal+""";
            }
        """)
    elif type == NORMAL:
        obj.botonOP.setStyleSheet("""
            QPushButton#botonOP{
                background-color:"""+blue_light+""";
            }
        """)
        obj.botonCaptura.setStyleSheet("""
            QPushButton#botonCaptura{
                background-color:"""+blue_light+""";
            }
        """)
        obj.botonIniciar.setStyleSheet("""
            QPushButton#botonIniciar{
                background-color:"""+blue_light+""";
            }
        """)