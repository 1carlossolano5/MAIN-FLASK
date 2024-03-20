from flask import Flask,render_template,redirect,url_for,flash, request,session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import base64 
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

@app.route('/lista')
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

        cursor.execute("INSERT INTO personas(nombreper,apellidoper,emailper,direccionper,telefonoper,usuarioper,contrasena,rol) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
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

##-------------Lista de canciones----------##

@app.route("/LISTAR")
def list_song(): 
    cursor = db.cursor()
    cursor.execute("SELECT titulo,artista,genero,precio,duracion,lanzamiento,img FROM canciones")
    canciones = cursor.fetchall()

    if canciones:
        cancioneslist = []
        for cancion in canciones:
            #Convertir la imagen formato base64
            imagen = base64.b64encode(cancion[6].decode('utf-8'))
            #agregar los datos de la cancion a la lista
            cancioneslist.append({
                'titulo':cancion[0],
                'artista':cancion[1],
                'genero':cancion[2],
                'precio':cancion[3],
                'duracion':cancion[4],
                'lanzamiento':cancion[5],
                'imagen':imagen,
            })
    
        return render_template("LISTAR.html", canciones = cancioneslist)
    else:
        return print("Canciones no encontradas")
    

##-------------Registro Canciones----------##

@app.route("/REGISTRO", methods =['GET', 'POST'])
def add_song():
    cursor = db.cursor()
    if request.method == 'POST':
        Titulo = request.form.get('titulo')  
        Artista = request.form.get('artista')
        Genero = request.form.get('genero')
        Precio = request.form.get('precio')
        Duracion = request.form.get('duracion')
        Fecha = request.form.get('fecha')
        Imagen = request.form.get('image')



        cursor.execute("INSERT INTO canciones (titulo, artista, genero, precio, duracion, lanzamiento,img)VALUES(%s,%s,%s,%s,%s,%s,%s)",(Titulo,Artista,Genero,Precio,Duracion,Fecha,Imagen))
        return redirect(url_for('add_song'))
    db.commit()
    return render_template("REGISTRO.html")


##----------Actualizar Canciones--------##

@app.route("/ACTUALIZAR/<int:id>", methods=["POST", "GET"])
def update_song(id):
    cursor = db.cursor()
    if request.method == "POST":
        Titulou = request.form.get('Titu')  
        Artistau = request.form.get('Arti')
        Generou = request.form.get('Gene')
        Preciou = request.form.get('Preci')
        Duracionu = request.form.get('Dura')
        Fechau = request.form.get('Lanz')
        Imagenu = request.form.get('Imagen')

        cursor.execute("update canciones set titulo=%s, artista=%s, genero=%s, precio=%s, duracion=%s, lanzamiento=%s,img=%s where id_can=%s",(Titulou,Artistau,Generou,Preciou,Duracionu,Fechau,Imagenu,id))
        db.commit()
        return redirect(url_for('list_song'))
    else:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM canciones WHERE id_can =%s", (id,))
        data = cursor.fetchall()
        return render_template("ACTUALIZAR.html", cancion=data[0])
    
##------------Eliminar Canciones-----------##
    
@app.route("/Eliminar_cancion/<int:id>", methods=["GET"])
def delete_song(id):
    cursor = db.cursor()
    if request.method == "GET":
        cursor.execute( "delete from canciones where id_can=%s" , (id,))
        db.commit()
        return redirect(url_for("list_song"))
    
##------------------------------------##


if __name__ == '__main__':
    app.add_url_rule('/',view_func=login)
    app.run(debug=True,port=5005)

##------------------------------------##