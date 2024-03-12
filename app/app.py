from flask import Flask,render_template,redirect,url_for,flash, request,session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
#Creamos una instancia de la clase Flask

app = Flask(__name__)
app.secret_key = '150104'
#CONFIGURAR LA CONEXIÓN
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="AGENDA2024"

)
cursor = db.cursor()

@app.route('/password/<contraencrip>')
def encriptarcontra(contraencrip):
    #Generar un hash de la contraseña
    #encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'),bcrypt.gensalt())
    encriptar = generate_password_hash(contraencrip)
    valor = check_password_hash(encriptar,contraencrip)
    
    return "Encritado:{0} | coincidencia:{1}".format(encriptar,valor)

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        #verificar las credenciales del usuario
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')

        cursor = db.cursor()
        cursor.execute("SELECT usuarioper, contrasena FROM personas WHERE usuarioper = %s ", (username,))
        resultado = cursor.fetchone()

        if resultado or encriptarcontra(password) == resultado[1]:
            session['usuario']= username
            return redirect(url_for('lista'))
        else:
            error = 'Credenciales Invalidas. Porfavor intentarlo de nuevo'
            return render_template('login.html', error=error)    
        
    return render_template('login.html')

#Definir rutas

@app.route('/')
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    usuario =  cursor.fetchall()

    return render_template('index.html', personas=usuario)

@app.route('/Registrar' , methods=['GET','POST'] )
def registrar_usuario():
    if request.method == 'POST':
        Nombres = request.form.get('nombre')
        Apellidos = request.form.get('apellido')
        Email = request.form.get('correo')
        Direccion = request.form.get('direccion')
        Telefono = request.form.get('numero')
        Usuario = request.form.get('usuario')
        Contrasena = request.form.get('contrasena')

        Contrasenaencriptada = encriptarcontra(Contrasena)

    #insertar datos a la tabla personas

        cursor.execute("INSERT INTO personas(nombreper,apellidoper,emailper,direccionper,telefonoper,usuarioper,contrasena) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                       (Nombres,Apellidos,Email,Direccion,Telefono,Usuario,Contrasenaencriptada))
        db.commit()
        flash('Usuario creado correctamente','success')

    #En el caso de que sea una solicitud, redirige a la misma pagina
    #cuando el método es post
        return redirect(url_for('registrar_usuario'))

    #Método get, renderiza el formulario
    return render_template('Registrar.html')

@app.route('/Editar/<int:id>' ,methods = ['GET','POST'])
def editar_usuario(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombreperso = request.form.get('nombreperso')
        apellidoperso = request.form.get('apellidoperso')
        emailperso = request.form.get('emailperso')
        direccionperso = request.form.get('direccionperso')
        telefonoperso = request.form.get('telefonoperso')
        usuarioperso = request.form.get('usuarioperso')
        contraseñaperso = request.form.get('contraseñaperso')

    #sentencia para actualizar los datos
        sql = "UPDATE personas set nombreper=%s,apellidoper=%s,emailper=%s,direccionper=%s,telefonoper=%s,usuarioper=%s,contrasena=%s where polper=%s"
        cursor.execute(sql,(nombreperso,apellidoperso,emailperso,direccionperso,telefonoperso,usuarioperso,contraseñaperso,id))
        db.commit()

        return redirect(url_for('lista'))
    else:
        #obtener los datos de la persona que va a editar
        cursor = db.cursor()
        cursor.execute('SELECT * FROM personas WHERE polper = %s', (id,))
        data = cursor.fetchall()

        return render_template('Editar.html' , personas=data[0])

@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):

    cursor = db.cursor()
    cursor.execute('DELETE FROM personas WHERE polper = %s', (id,))
    db.commit()
    return redirect(url_for('lista'))

if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True,port=5005)