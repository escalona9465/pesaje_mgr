cadena_original = "MONDELEZ / 30.8 KG"
# Divide la cadena solo en el primer espacio
partes = (cadena_original.split('/', 1))
# El primer elemento de la lista es "MONDELEZ"
resultado = (partes[0])[:-1]
print(resultado,len(resultado))
