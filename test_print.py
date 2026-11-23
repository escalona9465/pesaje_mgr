import subprocess
import win32print
sumatra_path = r"C:\Program Files\SumatraPDF\SumatraPDF.exe"
impresora = win32print.GetDefaultPrinter()
comando = f'{sumatra_path} -print-to "{impresora}" tempPdf.pdf -print-settings "fit,landscape"'
print(comando)
subprocess.call(comando)