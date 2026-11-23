############# Digitalizacion Insdustrial #########################
############# Autor: Eliezer R. & Alejandro P. ###################
############# Proyecto: Pesaje MGR  ##############################
############# Objeto Printer  ####################################

from components.imports.printer import *
#from components.functions import PDFrotate
import win32print
import subprocess
import time

class Printer():
    def __init__(self):

        self.printHandler = win32ui.CreateDC ()
        self.name = win32print.GetDefaultPrinter()   
        self.enableScale = False # use enable scale to change the status of doc to be printed.

        self.HORZRES = 8 
        self.VERTRES = 10

        self.LOGPIXELSX = 88 
        self.LOGPIXELSY = 90

        self.PHYSICALWIDTH = 110 
        self.PHYSICALHEIGHT = 111 

        self.PHYSICALOFFSETX = 0 
        self.PHYSICALOFFSETY = 0 

        self.optionA4 = {
            'dpi': 203,
            'page-height': '297mm',
            'page-width': '210mm',
            'margin-top': '0.4in',
            'margin-right': '0.4in',
            'margin-bottom': '0.4in',
            'margin-left': '0.6in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }

        self.optionA4H = {
            'dpi': 203,
            'page-height': '210mm',
            'page-width': '297mm',
            'margin-top': '1.0in',
            'margin-right': '0.5in',
            'margin-bottom': '0.5in',
            'margin-left': '1.0in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }

        self.optionTicket_old = {
            'dpi': 203,
            'page-height': '155mm',
            'page-width': '301mm',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }

        self.optionTicket = {
            'dpi': 1200,
            'page-height': '155mm',
            'page-width': '301mm',
            'margin-top': '0in',
            'margin-right': '0in',
            'margin-bottom': '0in',
            'margin-left': '0in',
            'encoding': "UTF-8",
            'no-outline': None,
            'enable-local-file-access': None
        }

        self.options = self.optionTicket

    def setOptions(self,option):
        if option == "TICKET":
            self.options = self.optionTicket
            #print("setting printer options to TICKET.")
        elif option == "A4":
            #print("setting printer options to A4.")
            self.options = self.optionA4
        elif option == "A4H":
            self.options = self.optionA4H

    def getPrinters(self):
        printers = []
        for (a,b,name,d) in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
            printers.append(name)
        return printers

    def printFromImage(self,path):
        try:
            self.printHandler.CreatePrinterDC(self.name)
            printable_area = self.printHandler.GetDeviceCaps (self.HORZRES), self.printHandler.GetDeviceCaps (self.VERTRES)
            printer_size = self.printHandler.GetDeviceCaps (self.PHYSICALWIDTH), self.printHandler.GetDeviceCaps (self.PHYSICALHEIGHT)
            printer_margins = self.printHandler.GetDeviceCaps (self.PHYSICALOFFSETX), self.printHandler.GetDeviceCaps (self.PHYSICALOFFSETY)

            bmp = Image.open (path)
            if bmp.size[0] > bmp.size[1]:
                bmp = bmp.rotate (0)

            ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
            scale = min (ratios)

            self.printHandler.StartDoc(path)
            self.printHandler.StartPage()

            dib = ImageWin.Dib (bmp)
            scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
            x1 = int ((printer_size[0] - scaled_width) / 2)
            y1 = int ((printer_size[1] - scaled_height) / 2)
            x2 = x1 + scaled_width
            y2 = y1 + scaled_height
            dib.draw (self.printHandler.GetHandleOutput(), (x1, y1, x2, y2))

            self.printHandler.EndPage()
            self.printHandler.EndDoc()
            self.printHandler.DeleteDC()
            print("e")
        except Exception as e:
            print(e)
            pass

    def printFromPdf(self,pdfFileName):
        try:
            win32api.ShellExecute (0, "print", pdfFileName, None, ".", 0)
        except Exception as e:
            print(f"Error en printFromPdf {e}")
            pass

    def printFromHtml(self,strHtml,impresora=None):
        print("Init print...")
        result = False
        pdfFileName = "tempPdf.pdf"
        sumatra_path = r"C:\Program Files\SumatraPDF\SumatraPDF.exe"
        try:
            self.resultSetDFPrinter = win32print.SetDefaultPrinter(self.name)
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
            #inicio_pdfkit=time.time()
            self.resultPdfKit = pdfkit.from_string(strHtml,pdfFileName, options = self.options,configuration=config)
            #tiempo_pdfkit=time.time()-inicio_pdfkit
            #print(f"Tiempo pdfkit: {tiempo_pdfkit}")
            
            #inicio_win32api=time.time()
            #print(f"Nombre arhivo: {pdfFileName}")
            
            #impresora = win32print.GetDefaultPrinter()
            comando = f'{sumatra_path} -print-to "{impresora}" tempPdf.pdf -print-settings "fit,landscape"'
            #print(comando)
            subprocess.call(comando)
            #tiempo_win32api=time.time()-inicio_win32api
            #print(f"Tiempo win32api: {tiempo_win32api}")
            result = True
            print("print end...")
        except Exception as e:
            print("Error trying to print from tempPdf, trying to print from other file.")
            print(e)
            try:
                pdfFileName = "tempPdf2.pdf"
                self.resultSetDFPrinter = win32print.SetDefaultPrinter(self.name)
                self.resultPdfKit = pdfkit.from_string(strHtml,pdfFileName, options = self.options)
                comando = f'{sumatra_path} -print-to "{impresora}" tempPdf2.pdf -print-settings "fit,landscape"'
                #print(comando)
                subprocess.call(comando)
                result = True
                print("second print end...")
            except Exception as e:
                print("error printing: ",e)
                self.enableScale = False
        return result

    def printFromHtml_old(self,strHtml):
        print("Init print...")
        result = False
        pdfFileName = "tempPdf.pdf"
        try:
            self.resultSetDFPrinter = win32print.SetDefaultPrinter(self.name)
            config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
            inicio_pdfkit=time.time()
            self.resultPdfKit = pdfkit.from_string(strHtml,pdfFileName, options = self.options,configuration=config)
            tiempo_pdfkit=time.time()-inicio_pdfkit
            print(f"Tiempo pdfkit: {tiempo_pdfkit}")
            #PDFrotate(pdfFileName,pdfFileName+"_",90)
            inicio_win32api=time.time()
            #print(f"Nombre arhivo: {pdfFileName}")
            self.resultShell = win32api.ShellExecute (0, "print", pdfFileName, None, ".", 0)
            tiempo_win32api=time.time()-inicio_win32api
            print(f"Tiempo win32api: {tiempo_win32api}")
            result = True
            print("print end...")
        except Exception as e:
            print("Error trying to print from tempPdf, trying to print from other file.")
            print(e)
            try:
                pdfFileName = "tempPdf2.pdf"
                self.resultSetDFPrinter = win32print.SetDefaultPrinter(self.name)
                self.resultPdfKit = pdfkit.from_string(strHtml,pdfFileName, options = self.options)
                self.resultShell = win32api.ShellExecute (0, "print", pdfFileName, None, ".", 0)
                result = True
                print("second print end...")
            except Exception as e:
                print("error printing: ",e)
                self.enableScale = False
        return result

    def generateFromHtml(self,strHtml):
        result = False
        pdfFileName = "tempPdf.pdf"
        config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
        try:
            self.resultPdfKit = pdfkit.from_string(strHtml,pdfFileName, options = self.options, configuration=config)
            result = True
            print("gen end...")
        except Exception as e:
            print("Error trying to gen from tempPdf, trying to print from other file.")

    def printWithPreview(self,adobePath):
        try:
            pdf_file  = QtCore.QFileInfo("tempPdf.pdf").absoluteFilePath() #r'C:\Users\elrodriguez\Desktop\pesaje_mgr_PC_20_06_2022\tempPdf.pdf'
            acrobat = adobePath #r'C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe'
            #print(f"Acrobad: {acrobat}\nPDF: {pdf_file}")
            cmd = '"{}" /p "{}"'.format(acrobat, pdf_file)
            #cmd = 'runas /user:Administrador /savecred:C0r1m0n4.0 "{} /p {}"'.format(acrobat, pdf_file)
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #stdout, stderr = proc.communicate()
            #exit_code = proc.wait()
        except:
            pass

    def setName(self,name):
        self.name = name

    def enable(self):
        self.enableScale = True
