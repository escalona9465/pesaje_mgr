from components.clasess import Responsive
responsive = Responsive()
#responsive.setCurrentPixelsX()
#responsive.setCurrentPixelsY()

STYLES_TYPE_PRODUCT = """
    *{
        background:#f1f1f1;
        color:#04336b;
    }

    QPushButton{
        background:#d2deed;
        color:#04336b;
        border:2px solid #04336b;
    }

    QPushButton:hover{
        background:#04336b;
        color:#d2deed;
        border:2px solid #d2deed;
    }

    QFrame#frameSelect{
        border:1px solid #04336b;
    }

    QFrame#frameMgr{
        image: url(:/components/recursos/MGR.png);
    }

    QLabel#labelTurno{
        color:#4CAF50;
    }

    QFrame#frameIconUser{
        image: url(:/components/recursos/iconUser.png);
    }
"""