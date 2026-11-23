import sqlite3,time

db_path = "components/database/pesaje.db"
connection = None
try:
    connection = sqlite3.connect(db_path)
except:
    print("Error")
inicio=time.time()
for i in range(12):
    tableName = "bobinas"
    key="op"
    cursor = connection.cursor()
    statement = """SELECT * FROM """+ tableName + " WHERE " + key + "=?"
    cursor.execute(statement,(13118234,))
    table = cursor.fetchall()
    print(f"Table: {table}")
final=time.time()
tiempo=final-inicio

print(f"Tiempo total: {tiempo}")


tableName="proceso_bobina"
statement = """SELECT * FROM """ + tableName + " WHERE ticket=(SELECT MAX(ticket) FROM " + tableName + ")"
result= False
table = []

##print("statement: ",statement)
cursor.execute(statement) 
table = cursor.fetchall()
print(f"Ultimo ticket: {table}")
print(f"Numero de ticket: {table[0][0]}")
print(f"Tipo de archivo: {type(table[0][0])}")