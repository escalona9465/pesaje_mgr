from importlib.resources import path
import sqlite3,time
from cryptography.fernet import Fernet

# key = b'B-8jec8Y8UPWfBWLMxvck2NwMCl8eqEb4uGA-Ms4zlQ='

class DBCypher():
    def __init__(self,DBPath) -> None:
        self.db_path = DBPath

    def encryptDB(self):
        fernet = Fernet(self.readKey())
        with open(self.db_path, 'rb') as file:
            original = file.read()
            encrypted = fernet.encrypt(original)
        with open(self.db_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)

    def decryptDB(self):
        fernet = Fernet(self.readKey())
        with open(self.db_path, 'rb') as enc_file:
            encrypted = enc_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(self.db_path, 'wb') as dec_file:
            dec_file.write(decrypted)

    def readKey(self):
        return b's69FfUDlS3PKvxlCsigAzKs0hhYRSoTzcfyKiRPYJ3s='

    def setPath(self,path):
        self.db_path = path

class DBHandler():
    def __init__(self,dbPath) -> None:
        self.dbPath = dbPath
        self.connection = None
        if self.connect():
            pass
            print("Success connecting to database")
            self.cursor = self.connection.cursor()
        else:
            pass
            print("Fail trying to connect to database")

    # columns = [type1:field1,type2:field2,type3:field3,...,typen:filedn]
    # statement = "CREATE TABLE IF NOT EXISTS tabla1(unix REAL, fecha TEXT, palabraclave TEXT, valor REAL)
    def createTable(self,tableName,types,fields):
        statement = "CREATE TABLE IF NOT EXISTS "+tableName + "("
        for k in range(len(types)):
            if k < (len(types)-1):
                statement = statement + fields[k] + " " + types[k] + ","
            else:
                statement = statement + fields[k] + " " + types[k] + ")"
        result = False
        try:
            self.cursor.execute(statement)
            result = True
        except Exception as e:
            print(e)
            pass
        return result

        
    # keyValue is inserted on values at the end of sentense
    def updateValue(self,tableName,keyValue,keyUbicacion):
        # check first if data lenght match width the table to store data...
        #print(f"Usuario: {keyValue}. Password: {keyUbicacion}.")
        statement = "UPDATE "+tableName +" SET "+keyValue[0]+" = ? WHERE "+ keyUbicacion[0] + "=?;"
        result = False
        try:
            #print("statement: ",statement)
            self.cursor.execute(statement,(keyValue[1],keyUbicacion[1],)) 
            self.connection.commit()
            result = True
            #print("query success:",statement)
        except Exception as e:
            print(e)  
            pass
        return result

    def deleteRow(self,tableName,key,keyValue):
        # check first if data lenght match width the table to store data...
        statement = "DELETE FROM "+tableName +" WHERE "+key +" = ?" 
        result = False
        try:
            ##print("statement: ",statement)
            self.cursor.execute(statement,(keyValue,)) 
            self.connection.commit()
            result = True
            #print("query success:",statement)
        except Exception as e:
            print(e) 
            pass 
        return result        
    def obtenerImpresora(self,tipo):
        if tipo == "etiquetadora":
            statement = f'SELECT printer2_name FROM config_proceso'
            result = False
            try:
                self.cursor.execute(statement) 
                table = self.cursor.fetchall()
                result = True
            except Exception as e:
                print(e)
        return result,table
    def updateRow(self,tableName,headerUpdate,configUpdate,key):
        # check first if data lenght match width the table to store data...
        statement = "UPDATE "+tableName +" SET "+headerUpdate+" WHERE "+key +" = ?" 
        result = False
        try:
            #print("statement: ",statement)
            self.cursor.execute(statement,configUpdate) 
            self.connection.commit()
            result = True
            #print("query success:",statement)
        except Exception as e:
            print(e) 
            pass 
        return result
    
    def actualizar_fila(self,tablename,filtro,valores):
        result = False
        if tablename == "productos":
            try:
                self.cursor.execute(f'UPDATE {tablename} SET producto=?,peso_max=?,peso_min=? WHERE codigo_producto=?',(valores[0],valores[1],valores[2],filtro))
                self.connection.commit()
                result = True
            except Exception as e:
                print(e)
        elif tablename == "paletas":
            try:
                self.cursor.execute(f'UPDATE {tablename} SET nombre=?,peso=? WHERE id=?',(valores[0],valores[1],filtro))
                self.connection.commit()
                result = True
            except Exception as e:
                print(e)
        return result

    # row = [value1,value2,value3,...,valuen]
    def insertRow(self,tableName,header,values):
        # check first if data lenght match width the table to store data...
        statement = "INSERT INTO "+tableName + header
        result = False
        try:
            ##print("statement: ",statement)
            self.cursor.execute(statement,values) 
            self.connection.commit()
            result = True
            #print("query success:",statement)
        except Exception as e:
            print(e)
            pass  
        return result

    def insertarFila(self,tablename,valores):
        if tablename == "paletas":
            self.cursor.execute(f'INSERT INTO {tablename} ("id","nombre","peso")  values(?,?,?)',valores)
        self.connection.commit()


    def insertValue(self):
        pass

    def obtenerUltimaFila(self,table_name,filtro):
       self.cursor.execute(f'SELECT * FROM {table_name} ORDER BY {filtro} DESC LIMIT 1')
       tabla = self.cursor.fetchone()
       return tabla

    def getLastRow(self,table,columnId):
        statement = """SELECT * FROM """+table+""" WHERE """+columnId+""" = (SELECT MAX("""+columnId+""") FROM """+table+""");"""
        result = False
        table = []
        try:
            ##print("statement: ",statement)
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement)
        except Exception as e:
            pass
            print(e)  
        return result,table
    
    def getBobinasPallet_(self,op_,nPallet_):
        statement = """SELECT * FROM proceso_bobina WHERE (op="""+str(op_)+""" and n_paleta="""+str(nPallet_)+""")"""
        result = False
        table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    def sumarColumnaPesoBobinas(self,columna,filtro1,valor1,filtro2=None,valor2=None):
        statement = f"SELECT SUM({columna}) AS suma_total FROM proceso_bobina WHERE ({filtro1}={valor1} and {filtro2}={valor2})"
        result = False
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchone()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    def sumarpesoycantidadbobinas(self,op):
        statement = f"SELECT SUM(peso_neto) AS suma_total, COUNT(*) AS cantidad FROM proceso_bobina WHERE op='{op}'"
        result = False
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchone()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return table

    def actualizarColumna(self,tableName,columnaName,columnaValue,filtro,valor):
        statement = f"UPDATE {tableName}  SET {columnaName}=? WHERE {filtro}=?;"
        result = False
        try:
            #print("statement: ",statement)
            self.cursor.execute(statement,(columnaValue,valor,)) 
            self.connection.commit()
            result = True
            #print("query success:",statement)
        except Exception as e:
            print(e)  
            pass
        return result

    def getLastPalletOp(self,op):
        statement = f"SELECT * FROM proceso_bobina WHERE op='{op}' ORDER BY n_paleta DESC"
        result = False
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchone()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return table

    def getBobinasPalletDeleted_(self,op_,nPallet_):
        statement = """SELECT * FROM proceso_bobina_eliminados WHERE (op="""+op_+""" and n_paleta="""+nPallet_+""")"""
        result = False
        table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table


    def getTable(self,tableName,nivel=None):
        initTime = time.time()
        #print("Init breakpoint at => 0 ")
        statement = """SELECT * FROM """+ tableName
        result = False
        table = []
        if nivel == "supervisor":
            statement = """SELECT * FROM """+ tableName + """ WHERE nivel == 'SUPERVISOR'"""
            result = False
            table = []
        elif nivel == "operador":
            statement = """SELECT * FROM """+ tableName + """ WHERE nivel == 'OPERADOR'"""
            result = False
            table = []
        elif nivel == "all":
            statement = """SELECT * FROM """+ tableName
            result = False
            table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    def getTable_1(self,tablename,columna):
        #print(sqlite3.sqlite_version)
        # Configurar el cursor para devolver solo valores
        #self.cursor.row_factory = lambda cursor, row: row[0]
        statement = f'SELECT {columna} FROM {tablename}'
        result = False
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        self.cursor.row_factory = None
        return result,table
    
    def getTable_2(self,tablename,columna):
        # Configurar el cursor para devolver solo valores
        self.cursor.row_factory = lambda cursor, row: row[0]
        statement = f'SELECT {columna} FROM {tablename} ORDER BY ROWID DESC LIMIT 1000;'
        result = False
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        self.cursor.row_factory = None
        return result,table
    
    def getTable_new(self,tablename,columna):
        if tablename == "paletas":
            statement = f'SELECT {columna} FROM {tablename}'
            result = False
            
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    
    def gettablebytwo(self,tablename,condicion1,condicion2,valor1,valor2):
        statement = f"""SELECT * FROM {tablename} WHERE (UPPER({condicion1}) = UPPER('{valor1}') and UPPER({condicion2}) = UPPER('{valor2}'))"""
        result = False
        #print(statement)
        table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    def getTable_andOrder(self,tableName,columna_orden):
        initTime = time.time()
        #print("Init breakpoint at => 0 ")
        statement = f"SELECT * FROM {tableName} ORDER BY {columna_orden} ASC"
        result = False
        table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    def ultimoticket(self,tableName):
        statement = """SELECT * FROM """ + tableName + " WHERE ticket=(SELECT MAX(ticket) FROM " + tableName + ")"
        result= False
        table = []
        try:
            ##print("statement: ",statement)
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement," result: ",table)
        except Exception as e:
            pass
            print(e)
        return table
    
    def productByRow(self,oprow):
        producto="'" + str(oprow[8]) + "'"
        #print(f"Producto nuevo: {producto}")
        statement = """SELECT * FROM productos WHERE codigo_producto="""+producto
        result = False
        table = []
        try:
            ##print("statement: ",statement)
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement," result: ",table)
        except Exception as e:
            pass
            print(e)
        return table
    
    def clientID(self,clientid):
        statement = """SELECT * FROM clientes WHERE id="""+str(clientid)
        result = False
        table = []
        try:
            ##print("statement: ",statement)
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement," result: ",table)
        except Exception as e:
            pass
            print(e)
        return table
    
    def samecoils(self,op):
        statement = """SELECT * FROM proceso_bobina WHERE op="""+op
        result = False
        table = []
        try:
            ##print("statement: ",statement)
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement," result: ",table)
        except Exception as e:
            pass
            print(e)
        return table
    
    def getcoilsOP(self,op):
        statement = """SELECT * FROM proceso_bobina WHERE op="""+op
        result = False
        table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    def samecoilsPallet(self,op,actualpallet):
        statement = """SELECT * FROM proceso_bobina WHERE (op="""+str(op)+""" and n_paleta="""+str(actualpallet)+""")"""
        result = False
        table = []
        try:
            #print("statement: ",statement)
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement," result: ",table)
        except Exception as e:
            pass
            print(e)
        #print(f"Tabla en samecoilsPallet: {table}")
        return table

    def getProductFromCodeDB(self,code):
        producto="'" + str(code) + "'"
        #print(f"Producto nuevo: {producto}")
        statement = """SELECT * FROM productos WHERE codigo_producto="""+producto
        result = False
        table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return table

    def getTableByRow(self,tableName,key,value):
        statement = """SELECT * FROM """+ tableName + " WHERE " + key + "=?" 
        result = False
        table = []
        try:
            #print("statement: ",statement)
            self.cursor.execute(statement,(value,)) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement," result: ",table)
        except Exception as e:
            pass
            print(e)
        return result,table

    def getTableBy2Rows(self,tableName,key1,value1,key2,value2):
        statement = """SELECT * FROM """+ tableName + " WHERE " + key1 + "=? AND " + key2 + "=?"
        row = []
        try:
            #print("statement: ",statement)
            self.cursor.execute(statement,(value1,value2,)) 
            row = self.cursor.fetchall()
            #print("query success:",statement," result: ",table)
        except Exception as e:
            pass
            print(e)
        return row

    def getCustomTable(self,header,tableName):
        initTime = time.time()
        #print("Init breakpoint at => 0 ")
        statement = """SELECT """+header+""" FROM """+ tableName
        result = False
        table = []
        try:
            self.cursor.execute(statement) 
            table = self.cursor.fetchall()
            result = True
            #print("query success:",statement,"\n",table)
        except Exception as e:
            pass
            print(e)
        #print("breakpoint FETCH TABLE at=>",time.time()-initTime)
        return result,table
    
    def Obtenter_Tabla_condicionada(self,table_name,columnas,where):
        if table_name == "proceso_bobina":
            statement = f"""SELECT {columnas} FROM {table_name} WHERE {where}"""
        #☻print(statement)
        table = []
        try:
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table

    def getProduct_by(self,columna,filtro,valor=None):
        if filtro == "ALL":
            statement = f"""SELECT {columna} FROM productos"""
        else:
            statement = f"""SELECT {columna} FROM productos WHERE {filtro} = {valor}"""
        table = []
        try:
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table
        
    def execute(self,statement):
        try:
            self.cursor.execute(statement)
        except Exception as e:
            pass
            #print("No se pudo ejecutar la sentencia SQL, ",e)


    def obtenerTabla_unique(self,table_name,filtro):
        statement = f'SELECT DISTINCT {filtro} FROM {table_name}'
        table = []
        try:
            self.cursor.execute(statement)
            table = self.cursor.fetchall()
        except Exception as e:
            print(e)
        return table
    
    def connect(self):
        result = False
        try:
            self.connection = sqlite3.connect(self.dbPath)#, Password="tutankamon")
            result = True
        except Exception as e:
            pass
            print(e)
        return result

    def close(self):
        result = False
        try:
            self.connection.commit()
            self.cursor.close()
            self.connection.close() 
            result = True  
        except Exception as e:
            pass
            print(e)
        return result      
