import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        database='user_company'
    )
    print("Conexión exitosa a la base de datos.")
    connection.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")