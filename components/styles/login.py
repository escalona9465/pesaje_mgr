from components.clasess import Responsive
responsive = Responsive()
#responsive.setCurrentPixelsX()
#responsive.setCurrentPixelsY()
STYLES_LOGIN ="""
    *{
        background-image: url(components/recursos/indexMgr3.png);
    }
    QFrame#frameLogin{
        background-image: url(components/recursos/Degradado.png);
        border-radius: 15;
    }
    QPushButton{
        background:#f8be09;
    }
    QLineEdit{
        color:black;
        background:white;
        border-radius:15px;
        font-size:"""+responsive.scaleFontStr(20)+""";
    }
    QPushButton{
        color:#04336b;
        font-weight:bold;
        font-size:"""+responsive.scaleFontStr(20)+""";
        border-radius:15px;
    }
        QPushButton:hover{
        background:#04336b;
        color:white;
    }
    QToolButton{
        background:transparent;
    }
    QLabel{
        background:transparent;
        color:white;
    }
    QLabel#labelExtra2{
        color:black;
    }
    QFrame#iconUser{
        background-image: url(components/recursos/usuario.png);
        background-repeat: no-repeat;
    }
    QFrame#iconUser_2{
        background-image: url(components/recursos/clave.png);
        background-repeat: no-repeat;
    }
    QCommandLinkButton{
        Background:transparent;
    }
    QCommandLinkButton:hover{
        Background:transparent;
        color:white;
    }
    #labelTitulo,#labelTitulo2{
        font-size:"""+responsive.scaleFontStr(72)+""";
        font-family:Agency FB;
    }
    #labelTitulo{
        padding-left:5px;
    }
"""