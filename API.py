from flask import Flask, request, jsonify
import pymysql.cursors

app = Flask(__name__)

# Configuración de la conexión a MariaDB
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='user_company',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    try:
        with connection.cursor() as cursor:
            # Verificar credenciales del usuario
            sql = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
            cursor.execute(sql, (email, password))
            user = cursor.fetchone()

            if user:
                return jsonify({"success": True, "user": user})
            else:
                return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/registrar-uso', methods=['POST'])
def registrar_uso():
    data = request.get_json()
    usuario_id = data.get('usuario_id')
    herramienta_id = data.get('herramienta_id')

    try:
        with connection.cursor() as cursor:
            # Registrar el uso de la herramienta
            sql = "INSERT INTO registros (usuario_id, herramienta_id) VALUES (%s, %s)"
            cursor.execute(sql, (usuario_id, herramienta_id))
            connection.commit()

            return jsonify({"success": True, "message": "Uso registrado correctamente"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/herramientas', methods=['GET'])
def obtener_herramientas():
    try:
        with connection.cursor() as cursor:
            # Obtener todas las herramientas
            sql = "SELECT * FROM herramientas"
            cursor.execute(sql)
            herramientas = cursor.fetchall()

            return jsonify({"success": True, "herramientas": herramientas})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)