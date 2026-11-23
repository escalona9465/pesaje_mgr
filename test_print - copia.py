import subprocess
import win32print

# Ruta a Ghostscript
gspath = r"C:\Program Files\gs\gs10.04.0\bin\gswin64c.exe"
gsp_path = r"C:\Program Files\gs\gsprint.exe"

printer_name = win32print.GetDefaultPrinter()

# Ruta al archivo PDF de entrada
pdf_path = r"D:\Users\jescalona\OneDrive - Corimon\Proyectos\Pesaje MGR\Software\pesaje_mgr_PC_27_02_2025\tempPdf.pdf"

# Ruta al archivo PDF escalado (temporal)
scaled_pdf_path = r"D:\Users\jescalona\OneDrive - Corimon\Proyectos\Pesaje MGR\Software\scaled_tempPdf.pdf"

# Comando para escalar el PDF al tamaño A4
scale_command = [
    gspath,
    '-dBATCH',
    '-dNOPAUSE',
    '-sDEVICE=pdfwrite',
    '-dCompatibilityLevel=1.7',
    '-dPDFSETTINGS=/default',
    '-dPDFFitPage',
    '-dFIXEDMEDIA',
    '-dDEVICEWIDTHPOINTS=141.75',
    '-dDEVICEHEIGHTPOINTS=283.5',
    '-r600',
    '-dMaxBitmap=500000000',  # Aumenta el límite de memoria para bitmaps
    '-dBlockMerge=true',      # Mejora el manejo de bloques grandes
    '-dBufferSpace=100000000',# Aumenta el espacio de buffer
    f'-sOutputFile={scaled_pdf_path}',
    pdf_path
]

# Ejecutar el comando para escalar el PDF
try:
    subprocess.run(scale_command, check=True)
    print("El PDF se ha escalado correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Error al escalar el PDF: {e}")
    exit()

# Comando para imprimir el PDF escalado usando GSPrint
gsp_path = r"C:\Program Files\gs\gsprint.exe"  # Ruta a gsprint.exe
#printer_name = "Nombre de tu impresora"  # Nombre de la impresora

"""print_command = [
    gsp_path,
    '-ghostscript', gspath,
    '-printer', printer_name,
    scaled_pdf_path
]"""

print_command = [
    gsp_path,
    '-ghostscript', gspath,
    '-printer', printer_name,
    '-dPDFSETTINGS=/prepress',
    scaled_pdf_path
]

# Ejecutar el comando para imprimir
try:
    subprocess.run(print_command, check=True)
    print("El PDF se ha enviado a la impresora correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Error al imprimir el PDF: {e}")