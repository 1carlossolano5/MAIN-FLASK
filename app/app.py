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


##-------------Contraseña---------------##
cursor = db.cursor()

@app.route('/password/<contraencrip>')
def encriptarcontra(contraencrip):
    #Generar un hash de la contraseña
    #encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'),bcrypt.gensalt())
    encriptar = generate_password_hash(contraencrip)
    valor = check_password_hash(encriptar,contraencrip)
    
    #return "Encritado:{0} | coincidencia:{1}".format(encriptar,valor)
    return valor

##-------------Login---------------##

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        #verificar las credenciales del usuario
        usuario = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')

        cursor = db.cursor()
        sql = "SELECT usuarioper, contrasena, Rol FROM personas WHERE usuarioper = %s"
        cursor.execute(sql,(usuarios,))
        usuarios = cursor.fetchone()

        if usuarios and check_password_hash(usuarios['contraper'], password):
            session['usuario']= usuarios['usuarioper']
            session['rol']= usuarios['Rol']

            # De acuerdo al rol asignado las url
            if usuario['Rol']=='administrador':
               return redirect(url_for('lista'))
            else:
                 return redirect(url_for('mostrar_canciones'))
        else:
            print("Credenciales invalidas")
            print("Credeciales invalidas. por favor intentarlo de nuevo")
            return render_template('login.html',)    
        
    return render_template('login.html')

##-------------Logout---------------##


@app.route('/logout')
def logout():
    #Eliminar el usuario de la sesión
    session.pop('usuario', None)

    print("La sesion se cerro correctamente")
    return redirect/url_for(('login'))


##-------------Rutas---------------##

#Definir rutas

@app.route('/')
def lista():
    cursor = db.cursor()
    cursor.execute('SELECT * FROM personas')
    usuario =  cursor.fetchall()

    return render_template('index.html', personas=usuario)

##-------------Registrar----------##

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
        Rol = request.form.get('Rol')

        Contrasenaencriptada = generate_password_hash(Contrasena)

        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM personas WHERE usuarioper = %s OR emailper= %s", (Usuario, Email))
        existing_user = cursor.fetchone()

        if existing_user:
            print('El usuario o correo ya existe')
            return render_template('Registrar.html')

        cursor.execute("INSERT INTO personas(nombreper,apellidoper,emailper,direccionper,telefonoper,usuarioper,contrasena,rol) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                       (Nombres,Apellidos,Email,Direccion,Telefono,Usuario,Contrasenaencriptada,Rol))
        db.commit()
        flash('Usuario creado correctamente','success')

    #En el caso de que sea una solicitud, redirige a la misma pagina
    #cuando el método es post
        return redirect(url_for('registrar_usuario'))

    #Método get, renderiza el formulario
    return render_template('Registrar.html')

##-------------Editar---------------##

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
    

##-------------Eliminar---------------##

@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):

    cursor = db.cursor()
    cursor.execute('DELETE FROM personas WHERE polper = %s', (id,))
    db.commit()
    return redirect(url_for('lista'))

##-------------Registro Canciones--------##

@app.route('/Registro', methods=['GET', 'POST'])
def registro_cancion():
    if request.method == 'POST':
       Titulo = request.form.get('titulo')
       Artista = request.form.get('artista')
       Genero = request.form.get('genero')
       Precio = request.form.get('precio')
       Duracion = request.form.get('duracion')
       Lanzamiento = request.form.get('lanzamiento')

       cursor = db.cursor()
       cursor.execute(
           "SELECT * FROM canciones WHERE titulo = %s or artista = %s", (Titulo,Artista))
       cursor.execute("INSERT INTO personas(titulo,artista,genero,precio,duracion,lanzamiento) VALUES (%s,%s,%s,%s,%s,%s)",
        (Titulo,Artista,Genero,Precio,Duracion,Lanzamiento))
       db.commit()

       return redirect(url_for('registrar_cancion'))  # Redirigir a la página principal
    return render_template("Registro.html")

##----------Actualizar Canciones--------##

@app.route('/actualizar/<int:id>',methods=['GET', 'POST'])
def editar_cancion(id):
    cursor = db.cursor()
    if request.method == 'POST':
        titulo = request.form.get('titulo')
        artista = request.form.get('artista')
        genero = request.form.get('genero')
        precio = request.form.get('precio')
        duracion = request.form.get('duracion')
        lanzamiento = request.form.get('lanzamiento')

        sql = "UPDATE canciones set titulo=%s,artista=%s,genero=%s,precio=%s,duracion=%s,lanzamiento=%s, where id_can=%s"
        cursor.execute(sql,(titulo,artista,genero,precio,duracion,lanzamiento,id)) 
        db.commit()
        
        return redirect(url_for('listar'))
    
    else: 
        cursor = db.cursor()
        cursor.execute('SELECT * FROM canciones WHERE id_canciones=%s' ,(id,))
        data = cursor.fetchall()

        return render_template('actualizar.html', canciones=data[0])
    
##------------Eliminar Canciones-----------##
    
@app.route("/eliminar/<int:id>", methods=['GET'])
def eliminar_cancion(id):

    cursor = db.cursor()
    cursor.execute('DELETE FROM canciones WHERE id_cancion = %s', (id,))
    db.commit()
    return redirect(url_for('listar'))

##------------------------------------##


if __name__ == '__main__':
    app.add_url_rule('/',view_func=lista)
    app.run(debug=True,port=5005)

##------------------------------------##