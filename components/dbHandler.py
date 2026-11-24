import os
import time
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


class DBCypher():
    """Kept for backward compatibility with imports; file encryption is not used with MySQL."""
    def __init__(self, DBPath=None) -> None:
        self.db_path = DBPath

    def encryptDB(self):
        pass

    def decryptDB(self):
        pass

    def readKey(self):
        return b's69FfUDlS3PKvxlCsigAzKs0hhYRSoTzcfyKiRPYJ3s='

    def setPath(self, path):
        self.db_path = path


class DBHandler():
    _NUMERIC_NULLABLE_COLUMNS = {
        "bobinas": {"bobinas_paleta"},
        "habladores": {"posicion"},
        "productos": {"peso_max", "peso_min"},
    }

    def __init__(self, dbPath=None) -> None:
        self.dbPath = dbPath
        self.database = self._resolve_database_name(dbPath)
        self.connection = None
        self.cursor = None
        if self.connect():
            print(f"Success connecting to MySQL database: {self.database}")
        else:
            print(f"Fail trying to connect to MySQL database: {self.database}")

    @staticmethod
    def _resolve_database_name(dbPath):
        """Maps legacy SQLite paths or logical names ('pesaje', 'piezas') to env-configured MySQL DB names."""
        pesaje_db = os.getenv("MYSQL_DB_PESAJE", "pesaje")
        piezas_db = os.getenv("MYSQL_DB_PIEZAS", "piezas")
        if not dbPath:
            return pesaje_db
        normalized = str(dbPath).replace("\\", "/").lower()
        if "piezas" in normalized:
            return piezas_db
        if "pesaje" in normalized:
            return pesaje_db
        return str(dbPath)

    def _ensure_connection(self):
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        else:
            try:
                self.connection.ping(reconnect=True, attempts=3, delay=1)
            except Exception:
                self.connect()

    def connect(self):
        result = False
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                port=int(os.getenv("MYSQL_PORT", "3306")),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", ""),
                database=self.database,
                charset="utf8mb4",
                autocommit=False,
            )
            self.cursor = self.connection.cursor(buffered=True)
            result = True
        except Exception as e:
            print(e)
        return result

    def createTable(self, tableName, types, fields):
        statement = f"CREATE TABLE IF NOT EXISTS `{tableName}` ("
        cols = []
        for k in range(len(types)):
            cols.append(f"`{fields[k]}` {types[k]}")
        statement += ", ".join(cols) + ")"
        result = False
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            self.connection.commit()
            result = True
        except Exception as e:
            print(e)
        return result

    @staticmethod
    def _clean_empty_to_none(val):
        if isinstance(val, str) and val.strip() == "":
            return None
        return val

    def _sanitize_values_for_header(self, tableName, header, values):
        nullable_cols = self._NUMERIC_NULLABLE_COLUMNS.get(tableName)
        if not nullable_cols:
            return values
        vals = list(values)
        # Extract column names from header (e.g. "(`op`,`tara`,...) values(...)" or "col1=%s,col2=%s")
        import re
        cols_part = header.split("values")[0] if "values" in header.lower() else header
        cols = re.findall(r"`?([a-zA-Z0-9_]+)`?\s*(?:,|\)|=)", cols_part)
        for idx, col in enumerate(cols):
            if idx < len(vals) and col in nullable_cols:
                vals[idx] = self._clean_empty_to_none(vals[idx])
        return tuple(vals) if isinstance(values, tuple) else vals

    def updateValue(self, tableName, keyValue, keyUbicacion):
        statement = f"UPDATE `{tableName}` SET `{keyValue[0]}` = %s WHERE `{keyUbicacion[0]}` = %s"
        result = False
        val = keyValue[1]
        if keyValue[0] in self._NUMERIC_NULLABLE_COLUMNS.get(tableName, set()):
            val = self._clean_empty_to_none(val)
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (val, keyUbicacion[1]))
            self.connection.commit()
            result = True
        except Exception as e:
            print(e)
        return result

    def deleteRow(self, tableName, key, keyValue):
        statement = f"DELETE FROM `{tableName}` WHERE `{key}` = %s"
        result = False
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (keyValue,))
            self.connection.commit()
            result = True
        except Exception as e:
            print(e)
        return result

    def obtenerImpresora(self, tipo):
        result = False
        table = []
        if tipo == "etiquetadora":
            statement = "SELECT printer2_name FROM config_proceso"
            try:
                self._ensure_connection()
                self.cursor.execute(statement)
                table = self.cursor.fetchall()
                result = True
            except Exception as e:
                print(e)
        return result, table

    def updateRow(self, tableName, headerUpdate, configUpdate, key):
        statement = f"UPDATE `{tableName}` SET {headerUpdate} WHERE `{key}` = %s"
        result = False
        try:
            self._ensure_connection()
            sanitized = self._sanitize_values_for_header(tableName, headerUpdate, configUpdate)
            self.cursor.execute(statement, sanitized)
            self.connection.commit()
            result = True
        except Exception as e:
            print(e)
        return result

    def actualizar_fila(self, tablename, filtro, valores):
        result = False
        if tablename == "productos":
            try:
                self._ensure_connection()
                peso_max = self._clean_empty_to_none(valores[1])
                peso_min = self._clean_empty_to_none(valores[2])
                self.cursor.execute(
                    f"UPDATE `{tablename}` SET producto=%s, peso_max=%s, peso_min=%s WHERE codigo_producto=%s",
                    (valores[0], peso_max, peso_min, filtro),
                )
                self.connection.commit()
                result = True
            except Exception as e:
                print(e)
        elif tablename == "paletas":
            try:
                self._ensure_connection()
                self.cursor.execute(
                    f"UPDATE `{tablename}` SET nombre=%s, peso=%s WHERE id=%s",
                    (valores[0], valores[1], filtro),
                )
                self.connection.commit()
                result = True
            except Exception as e:
                print(e)
        return result

    def insertRow(self, tableName, header, values):
        statement = f"INSERT INTO `{tableName}` {header}"
        result = False
        try:
            self._ensure_connection()
            sanitized = self._sanitize_values_for_header(tableName, header, values)
            self.cursor.execute(statement, sanitized)
            self.connection.commit()
            result = True
        except Exception as e:
            print(e)
        return result

    def insertarFila(self, tablename, valores):
        if tablename == "paletas":
            self._ensure_connection()
            self.cursor.execute(
                f"INSERT INTO `{tablename}` (`id`, `nombre`, `peso`) VALUES (%s, %s, %s)",
                valores,
            )
            self.connection.commit()

    def insertValue(self):
        pass

    def obtenerUltimaFila(self, table_name, filtro):
        self._ensure_connection()
        self.cursor.execute(f"SELECT * FROM `{table_name}` ORDER BY `{filtro}` DESC LIMIT 1")
        tabla = self.cursor.fetchone()
        return tabla

    def getLastRow(self, tableName, columnId):
        statement = f"SELECT * FROM `{tableName}` WHERE `{columnId}` = (SELECT MAX(`{columnId}`) FROM `{tableName}`)"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def getBobinasPallet_(self, op_, nPallet_):
        statement = "SELECT * FROM proceso_bobina WHERE op = %s AND n_paleta = %s"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (op_, nPallet_))
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def sumarColumnaPesoBobinas(self, columna, filtro1, valor1, filtro2=None, valor2=None):
        statement = f"SELECT SUM(`{columna}`) AS suma_total FROM proceso_bobina WHERE `{filtro1}` = %s AND `{filtro2}` = %s"
        result = False
        table = None
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (valor1, valor2))
            table = self.cursor.fetchone()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def sumarpesoycantidadbobinas(self, op):
        statement = "SELECT SUM(peso_neto) AS suma_total, COUNT(*) AS cantidad FROM proceso_bobina WHERE op = %s"
        table = None
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (op,))
            table = self.cursor.fetchone()
        except Exception as e:
            print(e)
        return table

    def actualizarColumna(self, tableName, columnaName, columnaValue, filtro, valor):
        statement = f"UPDATE `{tableName}` SET `{columnaName}` = %s WHERE `{filtro}` = %s"
        result = False
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (columnaValue, valor))
            self.connection.commit()
            result = True
        except Exception as e:
            print(e)
        return result

    def getLastPalletOp(self, op):
        statement = "SELECT * FROM proceso_bobina WHERE op = %s ORDER BY n_paleta DESC LIMIT 1"
        table = None
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (op,))
            table = self.cursor.fetchone()
        except Exception as e:
            print(e)
        return table

    def getBobinasPalletDeleted_(self, op_, nPallet_):
        statement = "SELECT * FROM proceso_bobina_eliminados WHERE op = %s AND n_paleta = %s"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (op_, nPallet_))
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def getTable(self, tableName, nivel=None):
        statement = f"SELECT * FROM `{tableName}`"
        if nivel == "supervisor":
            statement = f"SELECT * FROM `{tableName}` WHERE nivel = 'SUPERVISOR'"
        elif nivel == "operador":
            statement = f"SELECT * FROM `{tableName}` WHERE nivel = 'OPERADOR'"
        elif nivel == "all":
            statement = f"SELECT * FROM `{tableName}`"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def getTable_1(self, tablename, columna):
        statement = f"SELECT {columna} FROM `{tablename}`"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def getTable_2(self, tablename, columna):
        statement = f"SELECT `{columna}` FROM `{tablename}` ORDER BY `{columna}` DESC LIMIT 1000"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = [row[0] for row in self.cursor.fetchall()]
            result = True
        except Exception as e:
            print(e)
        return result, table

    def getTable_new(self, tablename, columna):
        result = False
        table = []
        if tablename == "paletas":
            statement = f"SELECT {columna} FROM `{tablename}`"
            try:
                self._ensure_connection()
                self.cursor.execute(statement)
                table = self.cursor.fetchall()
                result = True
            except Exception as e:
                print(e)
        return result, table

    def gettablebytwo(self, tablename, condicion1, condicion2, valor1, valor2):
        statement = f"SELECT * FROM `{tablename}` WHERE (UPPER(`{condicion1}`) = UPPER(%s) AND UPPER(`{condicion2}`) = UPPER(%s))"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (valor1, valor2))
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def getTable_andOrder(self, tableName, columna_orden):
        statement = f"SELECT * FROM `{tableName}` ORDER BY `{columna_orden}` ASC"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def ultimoticket(self, tableName):
        statement = f"SELECT * FROM `{tableName}` WHERE ticket = (SELECT MAX(ticket) FROM `{tableName}`)"
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def productByRow(self, oprow):
        statement = "SELECT * FROM productos WHERE codigo_producto = %s"
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (str(oprow[8]),))
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def clientID(self, clientid):
        statement = "SELECT * FROM clientes WHERE id = %s"
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (clientid,))
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def samecoils(self, op):
        statement = "SELECT * FROM proceso_bobina WHERE op = %s"
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (op,))
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def getcoilsOP(self, op):
        statement = "SELECT * FROM proceso_bobina WHERE op = %s"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (op,))
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def samecoilsPallet(self, op, actualpallet):
        statement = "SELECT * FROM proceso_bobina WHERE op = %s AND n_paleta = %s"
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (op, actualpallet))
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def getProductFromCodeDB(self, code):
        statement = "SELECT * FROM productos WHERE codigo_producto = %s"
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (str(code),))
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def getTableByRow(self, tableName, key, value):
        statement = f"SELECT * FROM `{tableName}` WHERE `{key}` = %s"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (value,))
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def getTableBy2Rows(self, tableName, key1, value1, key2, value2):
        statement = f"SELECT * FROM `{tableName}` WHERE `{key1}` = %s AND `{key2}` = %s"
        row = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement, (value1, value2))
            row = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return row

    def getCustomTable(self, header, tableName):
        statement = f"SELECT {header} FROM `{tableName}`"
        result = False
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
            result = True
        except Exception as e:
            print(e)
        return result, table

    def Obtenter_Tabla_condicionada(self, table_name, columnas, where):
        table = []
        if table_name == "proceso_bobina":
            statement = f"SELECT {columnas} FROM `{table_name}` WHERE {where}"
            try:
                self._ensure_connection()
                self.cursor.execute(statement)
                table = self.cursor.fetchall()
            except Exception as e:
                print(e)
        return table

    def getProduct_by(self, columna, filtro, valor=None):
        if filtro == "ALL":
            statement = f"SELECT {columna} FROM productos"
        else:
            statement = f"SELECT {columna} FROM productos WHERE `{filtro}` = %s"
        table = []
        try:
            self._ensure_connection()
            if filtro == "ALL":
                self.cursor.execute(statement)
            else:
                self.cursor.execute(statement, (valor,))
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def execute(self, statement):
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            self.connection.commit()
        except Exception as e:
            print(e)

    def obtenerTabla_unique(self, table_name, filtro):
        statement = f"SELECT DISTINCT `{filtro}` FROM `{table_name}`"
        table = []
        try:
            self._ensure_connection()
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def close(self):
        result = False
        try:
            if self.connection and self.connection.is_connected():
                self.connection.commit()
                if self.cursor:
                    self.cursor.close()
                self.connection.close()
            result = True
        except Exception as e:
            print(e)
        return result
