from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")

from gestor import Gestor
gestor = Gestor()

# index.html
@app.route("/")
def home():
    return render_template("index.html")

# login.html (login del organizador)
@app.route("/iniciar-sesion")
def iniciar_sesion():
    return render_template("login.html")

# lógica de inicio de sesión (organizador)
@app.route("/login", methods=["POST", "GET"])
def login():
    resultado = ""
    if request.method == "POST":
        session["correo"] = request.form["correo-org"]
        session["password"] = request.form["password-org"]
        flash("Has iniciado sesión correctamente.", "info")
        resultado = redirect(url_for("home"))
    else:
        resultado = render_template("error.html")
    return resultado

# lógica de cerrar sesión (organizador)
@app.route("/logout", methods=["POST", "GET"])
def logout():
    resultado = ""
    if request.method == "POST":
        if "correo" in session:
            session.pop("correo", None)
            session.pop("password", None)
            flash("Sesión cerrada con éxito.", "info")
            resultado = redirect(url_for("home"))
    else:
        resultado = render_template("error.html")
    return resultado

# lógica de asignar trabajos (organizador)
# TODO

# upload.html
@app.route("/cargar-trabajo", methods=["POST", "GET"])
def cargar_trabajo():
    resultado = ""
    if "correo" in session:
        resultado = render_template("error.html")
    else:
        resultado = render_template("upload.html")
    return resultado

# lógica de carga de archivo en base de datos
@app.route("/upload", methods = ["POST", "GET"])
def upload():
    resultado = ""
    if request.method == "POST":
        # Datos del trabajo
        titulo = request.form["titulo"]
        resumen = request.form["resumen"]
        area = request.form["area"]
        
        # Datos del autor
        apellido = request.form["apellido"]
        nombre = request.form["nombre"]
        email = request.form["correo"]
        archivo = request.files.get("archivo")
        
        band = gestor.verificar_autor_por_mail(email)
        
        if not band:
            gestor.crear_autor(nombre, apellido, email)
        
        nombre_archivo = gestor.generar_nombre_archivo(gestor.get_id_autor_por_mail(email), titulo)
        ruta = gestor.subir_archivo(archivo, nombre_archivo, app.config["UPLOAD_FOLDER"])
        gestor.crear_trabajo(titulo, resumen, area, ruta, gestor.get_id_autor_por_mail(email))
        flash(f"Archivo subido correctamente. ID Trabajo: {gestor.get_id_trabajo_por_ruta_archivo(ruta)}", "info")
        resultado = redirect(url_for("home"))
    else:
        resultado = render_template("error.html")
    return resultado

# programa principal
if __name__ == '__main__':
    with app.app_context():
        gestor.createDB()
        app.run(debug=True)