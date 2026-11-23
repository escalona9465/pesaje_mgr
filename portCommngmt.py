import subprocess
import sys
from time import sleep
from socket import gethostname
from getpass import getuser

def obtener_info(action):
    #Obtener el nombre del equipo
    workstation = gethostname()
    print(f"Nombre del equipo: {workstation}.")

    #Obtener el nombre de usuario
    username = getuser()
    print(f"Nombre de usuario loggeado: {username}.")

    # Definir las credenciales de administrador
    user = f'{workstation}\\{username}'
    password = 'YuJo..14'

    portname = 'ACPI\\PNP0501\\2'



    # Disable the device
    disable_port = f"pnputil -disable-device {portname}"

    #Activar el puerto
    enable_port = f"pnputil -enable-device {portname}"
    if action == "disable":
        return disable_port
    if action == "enable":
        return enable_port

# Enable the device
#subprocess.run(['pnputil', '/enable-device', portname] )

def disablePort():
    actionPort = obtener_info("disable")
    # Construir el comando runas con las credenciales y la aplicación a ejecutar
    command = ['runas', '/user:' + 'Administrador', '/savecred:' + 'C0r1m0n4.0', actionPort]
    # Crear un proceso subprocess con el comando runas
    proc = subprocess.Popen(command, stdin=subprocess.PIPE)
    sleep(5)
def enablePort():
    actionPort = obtener_info("enable")
    # Construir el comando runas con las credenciales y la aplicación a ejecutar
    command2 = ['runas', '/user:' + 'Administrador', '/savecred:' + 'C0r1m0n4.0', actionPort]
    # Crear un proceso subprocess con el comando runas
    proc = subprocess.Popen(command2, stdin=subprocess.PIPE)
    sleep(10)

"""disablePort()
sleep(10)
enablePort()"""


