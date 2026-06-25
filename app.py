from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os

app = Flask(__name__)
app.config.from_pyfile("config.py")

# Configuración para la subida de archivos 
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads') 
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True) 

# se importa aquí para evitar importación circular
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
        email = request.form["correo-org"]
        clave = request.form["password-org"]
        existe = gestor.existe_organizador(email, clave)
        if existe:
            session["correo"] = email
            session["nombre"] = gestor.get_nombre_org_por_email(email)
            session["apellido"] = gestor.get_apellido_org_por_email(email)
            flash("Sesión iniciada con éxito.", "info")
            resultado = redirect(url_for("home"))
        else:
            flash("Correo electrónico y/o contraseña incorrectos.", "warning")
            resultado = redirect(url_for("iniciar_sesion"))
    else:
        resultado = render_template("error.html", mensaje="ERROR: No puede acceder aquí.")
    return resultado

# lógica de cerrar sesión (organizador)
@app.route("/logout", methods=["POST", "GET"])
def logout():
    resultado = ""
    if request.method == "POST":
        if "correo" in session:
            session.pop("correo", None)
            session.pop("nombre", None)
            session.pop("apellido", None)
            flash("Sesión cerrada con éxito.", "info")
            resultado = redirect(url_for("home"))
    else:
        resultado = render_template("error.html", mensaje="ERROR: No puede acceder aquí.")
    return resultado

# lógica de asignar trabajos (organizador)
@app.route("/asignar", methods=["POST", "GET"])
def asignar():
    resultado = ""
    if request.method == "POST":
        mensaje = gestor.asignar_trabajos()
        flash("Tarea finalizada.", "info")
        resultado = redirect(url_for("home"))
    else:
        resultado = render_template("error.html", mensaje="ERROR: No puede acceder aquí.")
    return resultado

# upload.html
@app.route("/cargar-trabajo", methods=["POST", "GET"])
def cargar_trabajo():
    resultado = ""
    if "correo" in session:
        resultado = render_template("error.html", mensaje = "ERROR: No puede acceder como organizador.")
    else:
        resultado = render_template("upload.html")
    return resultado

# lógica de carga de archivo en base de datos
@app.route("/upload", methods = ["POST", "GET"])
def upload():
    resultado = ""
    if request.method == "POST":
        titulo = request.form["titulo"]
        resumen = request.form["resumen"]
        area = request.form["area"]
        print(area)
        autor_nombre = request.form["nombre"]
        autor_apellido = request.form["apellido"]
        autor_email = request.form["correo"]
        archivo = request.files.get("archivo")
        if archivo and archivo.filename:
            if archivo.filename.endswith(".pdf"):
                nombre_seguro = secure_filename(archivo.filename)
                ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], nombre_seguro)
                archivo.save(ruta_completa)
                gestor.crear_trabajo(titulo, resumen, area, autor_nombre, autor_apellido, autor_email, nombre_seguro)
                flash(f"Archivo subido. ID Trabajo: {gestor.get_id_trabajo_por_nombre_archivo(nombre_seguro)}", "info")
                resultado = redirect(url_for("cargar_trabajo"))
            else:
                flash("Error: el archivo debe estar en formato PDF.", "warning")
                resultado = redirect(url_for("cargar_trabajo"))
    else:
        resultado = render_template("error.html", mensaje="ERROR: No puede acceder aquí")
    return resultado

# programa principal
if __name__ == '__main__':
    with app.app_context():
        gestor.createDB()
        app.run(debug=True)