############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.styles.bobinas import BOBINAS_STYLES
from components.constants.pesajeBobina import *
from components.styles.colors import *

def loadStyles(obj,type):
    if type == INIT_PESAJE:
        """
        obj.botonOP.setStyleSheet(
            QPushButton#botonOP{
                background-color:"""+yellow_normal+""";
            }
            )
        """
        try:
            obj.botonCaptura.setStyleSheet("""
                QPushButton#botonCaptura{
                    background-color:"""+red_normal+""";
                }
            """)
        except:
            pass
        try:
            obj.botonCerrar.setStyleSheet("""
                QPushButton#botonCerrar{
                    background-color:"""+yellow_normal+""";
                }
            """)
        except:
            pass
        try:
            obj.botonTara.setStyleSheet("""
                QPushButton#botonTara{
                    background-color:"""+yellow_normal+""";
                }
            """)
        except:
            pass
        try:
            obj.botonIniciar.setStyleSheet("""
                QPushButton#botonIniciar{
                    background-color:"""+green_normal+""";
                }
            """)
        except:
            pass
    elif type == CAPTURE_WEIGHT:
        """
        obj.botonOP.setStyleSheet(
            QPushButton#botonOP{
                background-color:"""+yellow_normal+""";
            }
            )
        """
        try:
            obj.botonCaptura.setStyleSheet("""
                QPushButton#botonCaptura{
                    background-color:"""+red_normal+""";
                }
            """)
        except:
            pass
        try:
            obj.botonCerrar.setStyleSheet("""
                QPushButton#botonCerrar{
                    background-color:"""+yellow_normal+""";
                }
            """)
        except:
            pass
        try:
            obj.botonTara.setStyleSheet("""
                QPushButton#botonTara{
                    background-color:"""+yellow_normal+""";
                }
            """)
        except:
            pass
        try:
            obj.botonIniciar.setStyleSheet("""
                QPushButton#botonIniciar{
                    background-color:"""+green_normal+""";
                }
            """)
        except:
            pass
    elif type == NORMAL:
        """
        obj.botonOP.setStyleSheet(
            QPushButton#botonOP{
                background-color:"""+blue_light+""";
            }
            )
        """
        try:
            obj.botonCerrar.setStyleSheet("""
                QPushButton#botonCerrar{
                    background-color:"""+blue_light+""";
                }
            """)
        except:
            pass
        try:
            obj.botonTara.setStyleSheet("""
                QPushButton#botonTara{
                    background-color:"""+blue_light+""";
                }
            """)
        except:
            pass
        try:
            obj.botonCaptura.setStyleSheet("""
                QPushButton#botonCaptura{
                    background-color:"""+blue_light+""";
                }
            """)
        except:
            pass
        try:
            obj.botonIniciar.setStyleSheet("""
                QPushButton#botonIniciar{
                    background-color:"""+blue_light+""";
                }
            """)
        except:
            pass