############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################
from components.styles.colors import *
from components.clasess import Responsive
responsive = Responsive()
#responsive.setCurrentPixelsX()
#responsive.setCurrentPixelsY()

CONFIG_STYLES = """
        *{
            background:#f1f1f1;
        }

        QFrame#frameDatos{
            background:#cdcdcd;
            border:"""+responsive.scaleFontStr(8)+""" solid """+blue_light+""";
        }
        QLabel#labelTitulo{
            background:transparent;
            color:#04336b;
            font:bold """+responsive.scaleFontStr(20)+""" MS Sans Serif;
        }
        QLineEdit{
            background:white;
            border-radius:5px;
        }
        QComboBox{
            background:white;
            border:none;
            border-radius:5px;
            min-width:185px;
        }

        QLabel{
            background:transparent;
            color:#04336b;
            font: bold """+responsive.scaleFontStr(13)+""" Arial  Black;
        }

        QPushButton{
            font:bold """+responsive.scaleFontStr(12)+""" Arial;
            border:none;
            border-radius:5px;
        }

        QPushButton:hover{
            background:"""+blue_light+""";
        }

        QPushButton#btnRegresar{
            background:"""+blue_light+"""; 
        }

        QPushButton#botonCaptura{
            background:"""+blue_light+""";
        }

        QCheckBox{
            background:transparent;
            font: bold """+responsive.scaleFontStr(12)+""" Arial Black;
            color:#04336b;
        }

        QFrame#framePeso{
            border:1px solid #cdcdcd;
        }

        QLCDNumber{
            background:white;
            color:#04336b;
        }
        QLabel#labelTicket{
            background:white;
            border:1px solid black;
        }
        QLabel#labelTara{
            background:white;
        }

        QHeaderView{
            Background:transparent;
        }

        QHeaderView::section {
            Font-size:"""+responsive.scaleFontStr(14)+"""; 
            Font-family:Aria Black;
            Color: #FFFFFF; 
            Background:#04336b; 
            Text-align:center;  
            Min-height: 30px;
            max-height:30px; 
        }
        QTableWidget{
            Background: #FFFFFF;
            Font-size: """+responsive.scaleFontStr(12)+"""; 
            Font-family: Arial Black; 
            color:black;
        }

        QLineEdit#lineKg{
            color:#04336b;
            font:"""+responsive.scaleFontStr(48)+""" Arial;
            background:transparent;
        }
        QLineEdit#lineTicket{
            color:#04336b;
            font:"""+responsive.scaleFontStr(26)+""" Arial;
            background:transparent;
        }
        QLabel#lineNotify{
            background-color:#ff0000;
            border-radius:5px;
            font-weight:700;
            color:white;
            text-align:center;
        }  
        QLabel#titleForm{
            font-size:"""+responsive.scaleFontStr(30)+""";
        }  
        QWidget#formWidget{
            border-radius:5px;
        }   
"""