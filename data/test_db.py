from database import database  # Importa el objeto de conexión a la base de datos

cursor = database.cursor()     # Crea un cursor para ejecutar consultas SQL
cursor.execute("SHOW TABLES;") # Ejecuta la consulta para mostrar todas las tablas de la base de datos

for table in cursor.fetchall(): # Recorre los resultados de la consulta
    print(table)                # Imprime el nombre de cada tabla encontrada

cursor.close()                  # Cierra el cursor para liberar recursos