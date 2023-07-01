import json

from flask import Flask, request,jsonify
import jwt
import datetime
app = Flask(__name__)
from flask_mysqldb import MySQL
from werkzeug.security import check_password_hash,generate_password_hash
from flask_cors import CORS,cross_origin
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'escuela_bolivariano'
app.config['SECRET_KEY'] = 'sadddddddddd15csa545sc1a54a5c5s'
mysql = MySQL(app)
CORS(app, resources={r"/*": {"origins": "*"}})


def ObtenerDatosPost():
    request_data = request.data

    request_data = json.loads(request_data.decode('utf-8'))

    return request_data

@app.route('/empleados',methods=['GET'])
@cross_origin()
def get_empleados():
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM empleados")
    empleados = cur.fetchall()
    return jsonify(empleados)

@app.route('/registrar_empleados',methods=['POST'])
@cross_origin()
def registrar_empleado():
    if request.method == 'POST':
        data = request.get_json()
        nombres = data['nombres']
        apellidos = data['apellidos']
        cedula = data['cedula']
        codigoCargo = data['codigo_cargo']
        titulo = data['titulo']
        fechaNacimiento = data['fecha_nacimiento']
        fechaIngreso = data['fecha_ingreso']
        codigoDependencia = data['codigo_dependencia']
        dependencia = data['dependencia']
        estado = data['estado']
        patologias = data['patologias']
        direccion = data['direccion']
        telefono = data['telefono']
        nivel = data['nivel']

        cur = mysql.connection.cursor()
        cur.execute(f"INSERT INTO empleados(nombres,apellidos,cedula,codigo_cargo,titulo,fecha_nacimiento,fecha_ingreso,codigo_dependencia,cargo,dependencia,estado,patologias,direccion,telefono,correo,nivel) VALUES ('{nombres}','{apellidos}','{cedula}','{codigoCargo}','{titulo}','{fechaNacimiento}','{fechaIngreso}','{codigoDependencia}','{dependencia}','{estado}','{patologias}','{direccion}','{telefono}','{nivel}')")
        mysql.connection.commit()
        cur.close()
        return jsonify({"status": "success", "message": "Empleado registrado"})

@app.route('/empleado/<id>')
def mostrar_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute(f"SELECT * FROM empleados WHERE id = '{id}'")
    empleado = cur.fetchall()
    return jsonify(empleado)

@app.route('/delete/<id>',methods=['DELETE'])
def eliminar_empleado(id):
    cur = mysql.connection.cursor()
    cur.execute(f"DELETE FROM empleados WHERE id = '{id}'")
    mysql.connection.commit()
    return "Usuario eliminado satisfactoriamente"

@app.route('/empleado_edit/<id>',methods =["POST"])
def editar_empleado(id):
    nombres = request.form['nombres']
    apellidos = request.form['apellidos']
    cedula = request.form['cedula']

    cur = mysql.connection.cursor()
    ejecucion = cur.execute(f'UPDATE empleados SET nombres = "{nombres}",apellidos="{apellidos}",cedula = "{cedula}" WHERE id = "{id}"')
    print(ejecucion)
    mysql.connection.commit()
    return "La base de datos ha sido actualizada"


@app.route('/register',methods=['POST'])
@cross_origin()
def register():
    if request.method == 'POST':
        data = request.get_json()
        usuario = data['usuario']
        password = data['password']

        cur = mysql.connection.cursor()
        password = generate_password_hash(password)
        cur.execute(f'INSERT INTO usuarios(usuario,password) VALUES ("{usuario}","{password}") ')
        return "Usuario creado satisfactoriamente"


@app.route('/login',methods = ['POST'])
@cross_origin()
def login():
    if request.method == 'POST':
        try:

            data = request.get_json()
            usuario = data['usuario']
            password = data['password']
            print(usuario,data)
            cur = mysql.connection.cursor()
            cur.execute(f'SELECT * FROM usuarios WHERE usuario = "{usuario}"')
            usuariodb = cur.fetchall()
            print(usuariodb)
            hashedPassword = usuariodb[0][2]
            checked_password = check_password_hash(hashedPassword,password)
            print(checked_password)
            if checked_password == True:
                print("Password pass")
                token = jwt.encode({'user' : usuariodb[0][1],'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=24)},app.config['SECRET_KEY'])
                print(token)
                return jsonify({"token" : token})
            else:
                return jsonify({'message' : "Password Incorrecta"})
        except:
            return jsonify({'message' :"Usuario no encontrado"})
    return jsonify({'message': "No post reque"})

@app.route('/constancias/constancia_trabajo',methods=['POST'])
@cross_origin()
def constancia_trabajo():
    print("Executed")
    if request.method == 'POST':
        try:
            print("Executed2")
            data = request.get_json()
            print(data)
            usuario = data['usuario']
            password = data['password']
            print(usuario,password)
            #fechaActual = obtenerFechaActual()
            #print(fechaActual)
            #ProcesarFechaActual(request_data=request_data, fechaActual=fechaActual)
            #generarPdf(contenido=request_data, templateName="constanciaTrabajo")
            #return f'Constancia Enviada al correo {request_data["correo"]}'
            return "Constancia enviada"
        except:
            return "No se pudo procesar la información pruebe su conexion a internet o el correo destinatario"

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port=4000,debug=True)
