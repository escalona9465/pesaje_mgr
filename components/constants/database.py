
HEADER_BOBINAS = ["op","tara","paletas_total","bobinas_paleta","paleta_actual","matriz","hablador","total_op","codigo"]

BOBINAS= """ (`op`,`tara`,`paletas_total`,`bobinas_paleta`,`paleta_actual`,`matriz`,`hablador`,`total_op`,`codigo`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

BOBINAS_UPDATE = """ op=%s,tara=%s,paletas_total=%s,bobinas_paleta=%s,paleta_actual=%s,matriz=%s,hablador=%s,total_op=%s,codigo=%s"""

HEADER_CLIENTES = ["id","codigo","cliente"]

CLIENTES = """ (`id`,`codigo`,`cliente`,`descripcion`) values(%s,%s,%s,%s)"""

CLIENTES_UPDATE = """ id=%s,codigo=%s,cliente=%s,descripcion=%s"""

HEADER_PROCESO_BOBINA = ["ticket","peso_bruto","peso_neto","n_paleta","bobina_matriz","fecha","hora"]

PROCESO_BOBINA = """ (`ticket`,`peso_bruto`,`peso_neto`,`n_paleta`,`bobina_matriz`,`fecha_emision`,`op`,`ficha`,`hora`,`bobina`,`aprobado_por`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

PROCESO_BOBINA_DELETED = """ (`ticket`,`peso_bruto`,`peso_neto`,`n_paleta`,`bobina_matriz`,`fecha_emision`,`op`,`ficha`,`hora`,`bobina`,`aprobado_por`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

PROCESO_BOBINA_UPDATE = """ ticket=%s, peso_bruto=%s, peso_neto=%s, n_paleta=%s, bobina_matriz=%s, fecha_emision=%s, op=%s, ficha=%s, hora=%s, bobina=%s """

HEADER_PRODUCTOS = ["codigo_producto","producto","peso_max","cliente_id"]

PRODUCT_UPDATE = """ codigo_producto=%s,producto=%s,peso_max=%s,cliente_id=%s"""

PRODUCTOS = """ (`codigo_producto`,`producto`,`peso_max`,`cliente_id`,`peso_min`) values(%s,%s,%s,%s,%s)"""

HEADER_USUARIOS = ["id","cedula","usuario","nombre","apellido","ficha","password","email","nivel","turno","supervisor"]

USUARIOS = """ (`id`,`cedula`,`usuario`,`nombre`,`apellido`,`ficha`,`password`,`email`,`nivel`,`turno`,`supervisor`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

USUARIOS_ID = """ (`cedula`,`usuario`,`nombre`,`apellido`,`ficha`,`password`,`email`,`nivel`,`turno`,`supervisor`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

CONFIG = """ (`server_ip`,`server_port`,`server_usr`,`server_pw`,`printer1_name`,`printer2_name`,`data_source_type`,`com_port1`,`com_port2`,`mode_b1`,`mode_b2`,`mode_adobe`,`path_adobe`,`key`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

CONFIG_UPDATE = """ server_ip=%s,server_port=%s,server_usr=%s,server_pw=%s,printer1_name=%s,printer2_name=%s,data_source_type=%s,com_port1=%s,com_port2=%s,mode_b1=%s,mode_b2=%s,mode_adobe=%s,path_adobe=%s"""

HABLADORES = """ (`op`,`cantidad`,`posicion`,`observacion`,`producto`) values(%s,%s,%s,%s,%s)"""

HEADER_HABLADORES = ["op","cantidad","posicion","observacion","producto"]

# PIEZAS

PIEZAS = """ (`op`,`bultos_total`,`pieza_bulto`,`bulto_actual`,`caja_actual`,`paleta_total`,`codigo`,`paquetes`) values(%s,%s,%s,%s,%s,%s,%s,%s)"""

PROCESO_PIEZA = """ (`ticket`,`neto`,`n_bulto`,`n_caja`,`n_paleta`,`fecha_emision`,`op`,`ficha`,`hora`,`piezas`,`paquetes`) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

