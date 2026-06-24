from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile("config.py")

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
        resultado = redirect(url_for("error.html"))
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
@app.route("/upload", methods=["POST", "GET"])
def enviar_trabajo():
    resultado = ""
    if "correo" in session:
        resultado = render_template("error.html")
    else:
        resultado = render_template("upload.html")
    return resultado

# lógica de carga de archivo en base de datos
# TODO

# programa principal
if __name__ == '__main__':
    app.run(debug=True)