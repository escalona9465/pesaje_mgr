############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.clasess import Responsive
responsive = Responsive()
#responsive.setCurrentPixelsX()
#responsive.setCurrentPixelsY()

blueTextMessage = "rgb(4,51,107)"
blueTextBorder = "rgb(23,12,243)"
grayTextLabel = "rgb(56,56,56)"
softBlueBg = "rgb(210,220,237)"
middleBlueBg = "rgb(129,163,205)"
blueBorderEdit = "rgb(92,225,230)"
neutralGrayBg = "rgb(254,254,254)"

STYLES_GENERAL = """
    QPushButton{
        margin-top:10px;
        margin-bottom:10px;
        max-width:90px;
        min-height:30px;
        font-size:"""+responsive.scaleFontStr(16)+""";
        background-color:white;
        color:black;
        border:solid;
        border-color:"""+blueBorderEdit+""";
        border-width:1px;
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px;  
        padding-left:10px;  
        padding-right:10px; 
    }
    QPushButton:hover{
        border-width:1.5px;        
        border-top-right-radius: 2.5px;
        border-top-left-radius: 2.5px;
        border-bottom-right-radius: 2.5px;
        border-bottom-left-radius: 2.5px;   
    }    
    QLabel{
        font-size:"""+responsive.scaleFontStr(25)+""";
        color:"""+blueTextMessage+""";   
    }
    QLabel#verificador{
        font-size:"""+responsive.scaleFontStr(25)+""";
        color:"""+blueTextMessage+""";   
    }
    QLineEdit,QComboBox{
        border:solid;        
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        max-width:350px;
        min-height:30px;        
    }

"""

STYLES_MODE_WAIT = """
    QLabel{
        font-weight:500;
        color:"""+blueTextMessage+""";   
    }
    #mode_wait_printing_message{
        font-size:"""+responsive.scaleFontStr(38)+""";
    }
    #mode_wait_change_message{
        font-size:"""+responsive.scaleFontStr(38)+""";    
    }
    #mode_wait_order_message{
        font-size:"""+responsive.scaleFontStr(32)+""";    
    }
"""

STYLES_MODE_CONFIRM = """

    #mode_confirm_pallete_okBtn{
        margin-right:5px;
    }
    #mode_confirm_pallete_cancelBtn{
        margin-left:5px;
    }

    #mode_confirm_hablador_okBtn{
        margin-right:5px;
    }
    #mode_confirm_hablador_cancelBtn{
        margin-left:5px;
    }
    #mode_confirm_message{
        font-size:"""+responsive.scaleFontStr(30)+""";        
    }
    #mode_confirm_pallete_message{
        font-size:"""+responsive.scaleFontStr(32)+""";        
    }
    #mode_confirm_hablador_message{
        font-size:"""+responsive.scaleFontStr(32)+""";        
    }
"""

STYLES_MODE_ACCEPT = """

"""

STYLES_MODE_INPUT = """

"""

STYLES_MODE_INPUT_HABLADOR = """
    #mode_input_hablador{
  
    }
    #mode_input_hablador_cancelBtn{
        margin-left:10px;
    }
    #mode_input_hablador_printBtn{
        margin-right:10px;
    }
    #mode_input_hablador_title{
        font-weight:500;
        font-size:"""+responsive.scaleFontStr(32)+""";
        margin-bottom:25px;        
    }
    #mode_input_hablador_label{
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+""";        
    }
    #mode_input_hablador_edit{
        border:solid;
        border-color:"""+grayTextLabel+""";        
        border-width:0.5px;        
        border-top-right-radius: 2.5px;
        border-top-left-radius: 2.5px;
        border-bottom-right-radius: 2.5px;
        border-bottom-left-radius: 2.5px; 
        max-width:350px;
        min-height:30px;   
        font-size:"""+responsive.scaleFontStr(18)+""";      
    }
"""
STYLES_MODE_INPUT_MATRIZ = """
    #mode_input_matriz_input{ 
        margin-top:20px; 
        margin-bottom:20px;       
        max-width:60px;
        min-height:50px;
        font-size:"""+responsive.scaleFontStr(25)+""";
    }
    #mode_input_matriz_message{          
        font-size:"""+responsive.scaleFontStr(38)+""";
    }
    #mode_input_matriz_okBtn{          
        margin-right:10px;
    }
    #mode_input_matriz_cancelBtn{          
        margin-left:10px;
    }
"""

STYLES_MODE_INPUT_ORDER = """
    #mode_input_order_message{
        font-size:"""+responsive.scaleFontStr(18)+""";
        margin-bottom:15px;
        color:"""+grayTextLabel+""";
        font-weight:700;
    }
    #mode_input_order_oplbl{
        color:"""+grayTextLabel+""";
        margin-left:30px;
    }
    #mode_input_order_op{
        border-color:"""+grayTextLabel+""";
        margin-right:30px;
    }

"""

STYLES_MODE_REPORT_OP = """
    #mode_report_op_title{
        font-size:"""+responsive.scaleFontStr(18)+""";
        margin-bottom:30px;
        color:"""+grayTextLabel+""";
        font-weight:700;       
    }

    #mode_report_op_lbl{
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+""";      
    }    

    #mode_report_op_combo{
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+"""; 
        background-color:"""+softBlueBg+""";    
        border-color:"""+blueBorderEdit+"""; 
    }

    #mode_report_op_edit{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+blueBorderEdit+""";
    }

"""

STYLES_REPORT_PALLET = """
    #mode_report_pallet_title{
        font-size:"""+responsive.scaleFontStr(18)+""";
        margin-bottom:30px;
        color:"""+grayTextLabel+""";
        font-weight:700;
    }
    #mode_report_pallet_nroOp{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+blueBorderEdit+"""; 
    }
    #mode_report_pallet_nroPallete{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+blueBorderEdit+"""; 
    }

    #mode_report_pallet_nroOpLbl{
        font-size:"""+responsive.scaleFontStr(18)+""";
        font-weight:700;
        color:"""+grayTextLabel+""";  
    }
    #mode_report_pallet_nroPalleteLbl{
        font-size:"""+responsive.scaleFontStr(18)+""";
        font-weight:700;
        color:"""+grayTextLabel+"""; 
    }

"""

STYLES_MODE_REPORT_PIEZA = """

    QPushButton{
        margin-top:10px;
        margin-bottom:10px;
        max-width:90px;
        min-height:30px;
        font-size:"""+responsive.scaleFontStr(16)+""";
        background-color:white;
        color:black;
        border:solid;
        border-color:"""+blueBorderEdit+""";
        border-width:1px;
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px;  
        padding-left:10px;  
        padding-right:10px; 
    }
    QPushButton:hover{
        border-width:1.5px;        
        border-top-right-radius: 2.5px;
        border-top-left-radius: 2.5px;
        border-bottom-right-radius: 2.5px;
        border-bottom-left-radius: 2.5px;   
    }    
    QLineEdit,QComboBox{
        border:solid;     
        border-color:"""+grayTextLabel+""";   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:30px;        
    }
    QLabel{
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+""";  
        font-weight:700;  
    }

    #mode_report_pieza_nroOpLbl{
        font-size:"""+responsive.scaleFontStr(18)+""";
        font-weight:700;
        color:"""+grayTextLabel+""";
    }

"""

STYLES_REGISTER_NEW = """

    #_title{
        font-size:"""+responsive.scaleFontStr(22)+""";
        margin-bottom:30px;
        color:"""+grayTextLabel+""";
        font-weight:700;
    }

    QLineEdit,QComboBox{
        border:solid;     
        border-color:"""+grayTextLabel+""";   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:30px;        
    }

    QLabel#_lbl{
        font-size:"""+responsive.scaleFontStr(20)+""";
        color:"""+grayTextLabel+""";  
        font-weight:700;      
    }


    QLabel#_input_pallet{
        max-width:50px;
        min-width:50px;
        width:50px;
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+""";        
    }

    #_addBtn{
        border-color:"""+grayTextLabel+""";
        min-width:160px;
    }

    QLineEdit#_input{
        font-size:"""+responsive.scaleFontStr(15)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:600;
    }

    ExtendedComboBox{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700;         
    }

    QSortFilterProxyModel{
            font-size:"""+responsive.scaleFontStr(18)+""";
            border-color:"""+grayTextLabel+""";
            font-weight:700;         
        }


    QCompleter{
            font-size:"""+responsive.scaleFontStr(18)+""";
            border-color:"""+grayTextLabel+""";
            font-weight:700;         
        }    


    QComboBox#_combo{
        font-size:"""+responsive.scaleFontStr(15)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:600;         
    }

    QComboBox#_combo2{
        font-size:"""+responsive.scaleFontStr(15)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:600;         
    }

    QCompleter{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700;         
    }


    

    QComboBox#_comboPallet{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700; 
        max-width:100px;        
    }

    QPushButton{
        margin-top:10px;
        margin-bottom:10px;
        max-width:90px;
        min-height:30px;
        font-size:"""+responsive.scaleFontStr(18)+""";
        background-color:white;
        color:black;
        border:solid;
        border-color:"""+blueBorderEdit+""";
        border-width:1px;
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px;  
        padding-left:10px;  
        padding-right:10px; 
    }
    QPushButton:hover{
        border-width:1.5px;        
        border-top-right-radius: 2.5px;
        border-top-left-radius: 2.5px;
        border-bottom-right-radius: 2.5px;
        border-bottom-left-radius: 2.5px;   
    }
    QLabel#message_restore{
        border:solid;     
        border-color:white;   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:22px; 
        font-size:"""+responsive.scaleFontStr(12)+""";
    }
    QLabel#message_client{
        border:solid;     
        border-color:white;   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:22px; 
        font-size:"""+responsive.scaleFontStr(12)+""";
    }
    QLabel#message_product{
        border:solid;     
        border-color:white;   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:22px; 
        font-size:"""+responsive.scaleFontStr(12)+""";
    }
"""

STYLES_REGISTER = """

    #_title{
        font-size:"""+responsive.scaleFontStr(18)+""";
        margin-bottom:30px;
        color:"""+grayTextLabel+""";
        font-weight:700;
    }

    QLineEdit,QComboBox{
        border:solid;     
        border-color:"""+grayTextLabel+""";   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:30px;        
    }

    QLabel#_lbl{
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+""";        
    }


    QLabel#_input_pallet{
        max-width:50px;
        min-width:50px;
        width:50px;
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+""";        
    }

    #_addBtn{
        border-color:"""+grayTextLabel+""";
        min-width:160px;
    }

    QLineEdit#_input{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700;
    }

    ExtendedComboBox{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700;         
    }

    QSortFilterProxyModel{
            font-size:"""+responsive.scaleFontStr(18)+""";
            border-color:"""+grayTextLabel+""";
            font-weight:700;         
        }


    QCompleter{
            font-size:"""+responsive.scaleFontStr(18)+""";
            border-color:"""+grayTextLabel+""";
            font-weight:700;         
        }    


    QComboBox#_combo{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700;         
    }

    QCompleter{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700;         
    }


    

    QComboBox#_comboPallet{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700; 
        max-width:100px;        
    }

    QPushButton{
        margin-top:10px;
        margin-bottom:10px;
        max-width:90px;
        min-height:30px;
        font-size:"""+responsive.scaleFontStr(18)+""";
        background-color:white;
        color:black;
        border:solid;
        border-color:"""+blueBorderEdit+""";
        border-width:1px;
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px;  
        padding-left:10px;  
        padding-right:10px; 
    }
    QPushButton:hover{
        border-width:1.5px;        
        border-top-right-radius: 2.5px;
        border-top-left-radius: 2.5px;
        border-bottom-right-radius: 2.5px;
        border-bottom-left-radius: 2.5px;   
    }
    QLabel#message_restore{
        border:solid;     
        border-color:white;   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:22px; 
        font-size:"""+responsive.scaleFontStr(12)+""";
    }
    QLabel#message_client{
        border:solid;     
        border-color:white;   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:22px; 
        font-size:"""+responsive.scaleFontStr(12)+""";
    }
    QLabel#message_product{
        border:solid;     
        border-color:white;   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:22px; 
        font-size:"""+responsive.scaleFontStr(12)+""";
    }
"""

STYLES_DATES = """
    QDateTimeEdit#_edit{
        font-size:"""+responsive.scaleFontStr(18)+""";
        border-color:"""+grayTextLabel+""";
        font-weight:700; 
        max-width:150px;         
    }
    QComboBox#_combo_op{
        max-width:150px;     
    }
"""

STYLES_POPUP = ""
STYLES_POPUP = STYLES_POPUP + STYLES_GENERAL + STYLES_MODE_ACCEPT + STYLES_MODE_CONFIRM + STYLES_MODE_INPUT + STYLES_MODE_INPUT_HABLADOR 
STYLES_POPUP = STYLES_POPUP + STYLES_MODE_INPUT_MATRIZ + STYLES_MODE_INPUT_ORDER + STYLES_MODE_WAIT + STYLES_REPORT_PALLET + STYLES_MODE_REPORT_PIEZA
STYLES_POPUP = STYLES_POPUP + STYLES_MODE_WAIT + STYLES_DATES

STYLES_DIALOGOS = """
    QPushButton{
        margin-top:10px;
        margin-bottom:10px;
        max-width:130px;
        min-height:30px;
        font-size:"""+responsive.scaleFontStr(18)+""";
        background-color:white;
        color:black;
        border:solid;
        border-color:"""+blueBorderEdit+""";
        border-width:1px;
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px;  
        padding-left:10px;  
        padding-right:10px; 

    }
    QPushButton:hover{
        border-width:1.5px;        
        border-top-right-radius: 2.5px;
        border-top-left-radius: 2.5px;
        border-bottom-right-radius: 2.5px;
        border-bottom-left-radius: 2.5px;   
    }
    QLineEdit{
        border:solid;     
        border-color:"""+grayTextLabel+""";   
        border-width:0.5px;        
        border-top-right-radius: 1.5px;
        border-top-left-radius: 1.5px;
        border-bottom-right-radius: 1.5px;
        border-bottom-left-radius: 1.5px; 
        min-height:30px;        
    }

    QLabel{
        font-size:"""+responsive.scaleFontStr(18)+""";
        color:"""+grayTextLabel+""";        
    }

    QLabel#etiqueta{
        font-weight:bold;        
    }"""