
HEADER_BOBINAS = ["op","tara","paletas_total","bobinas_paleta","paleta_actual","matriz","hablador","total_op","codigo"]

BOBINAS= """ ("op","tara","paletas_total","bobinas_paleta","paleta_actual","matriz","hablador","total_op","codigo")  values(?,?,?,?,?,?,?,?,?)"""

BOBINAS_UPDATE = """ op =?,tara = ?,paletas_total = ?,bobinas_paleta = ?,paleta_actual=?,matriz=?,hablador=?,total_op=?,codigo=?"""

HEADER_CLIENTES = ["id","codigo","cliente"]

CLIENTES = """ ("id","codigo","cliente","descripcion")  values(?,?,?,?)"""

CLIENTES_UPDATE = """ id = ?,codigo = ?,cliente = ?,descripcion = ?"""

HEADER_PROCESO_BOBINA = ["ticket","peso_bruto","peso_neto","n_paleta","bobina_matriz","fecha","hora"]

PROCESO_BOBINA = """ ("ticket","peso_bruto","peso_neto","n_paleta","bobina_matriz","fecha_emision","op","ficha","hora","bobina","aprobado_por")  values(?,?,?,?,?,?,?,?,?,?,?)"""

PROCESO_BOBINA_DELETED = """ ("ticket","peso_bruto","peso_neto","n_paleta","bobina_matriz","fecha_emision","op","ficha","hora","bobina","aprobado_por")  values(?,?,?,?,?,?,?,?,?,?,?) """

PROCESO_BOBINA_UPDATE = """ ticket = ?, peso_bruto = ?, peso_neto = ?, n_paleta = ?, bobina_matriz = ?, fecha_emision = ?, op = ?, ficha = ?, hora = ?, bobina = ? """

HEADER_PRODUCTOS = ["codigo_producto","producto","peso_max","cliente_id"]

PRODUCT_UPDATE = """ codigo_producto = ?,producto = ?,peso_max = ?,cliente_id = ?"""

PRODUCTOS = """ ("codigo_producto","producto","peso_max","cliente_id","peso_min")  values(?,?,?,?,?)"""

HEADER_USUARIOS = ["id","cedula","usuario","nombre","apellido","ficha","password","email","nivel","turno","supervisor"]

USUARIOS = """ ("id","cedula","usuario","nombre","apellido","ficha","password","email","nivel","turno","supervisor")  values(?,?,?,?,?,?,?,?,?,?,?)"""

USUARIOS_ID = """ ("cedula","usuario","nombre","apellido","ficha","password","email","nivel","turno","supervisor")  values(?,?,?,?,?,?,?,?,?)"""

CONFIG = """ ("server_ip","server_port","server_usr","server_pw","printer1_name","printer2_name","data_source_type","com_port1","com_port2","mode_b1","mode_b2","mode_adobe","path_adobe","key")  values(?,?,?,?,?,?,?,?,?,?,?,?)"""

CONFIG_UPDATE = """ server_ip = ?,server_port = ?,server_usr = ?,server_pw = ?,printer1_name = ?,printer2_name = ?,data_source_type = ?,com_port1 = ?,com_port2 = ?,mode_b1 = ?,mode_b2 = ?,mode_adobe = ?,path_adobe = ?"""

HABLADORES = """ ("op","cantidad","posicion","observacion","producto")  values(?,?,?,?,?)"""

HEADER_HABLADORES = ["op","cantidad","posicion","observacion","producto"]

# PIEZAS

PIEZAS = """ ("op","bultos_total","pieza_bulto","bulto_actual","caja_actual","paleta_total","codigo","paquetes")  values(?,?,?,?,?,?,?,?)"""

PROCESO_PIEZA = """ ("ticket","neto","n_bulto","n_caja","n_paleta","fecha_emision","op","ficha","hora","piezas","paquetes")  values(?,?,?,?,?,?,?,?,?,?,?)"""

