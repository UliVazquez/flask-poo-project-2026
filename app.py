from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enviar-trabajo', methods=['POST', 'GET'])
def enviar_trabajo():
    return render_template('envia_trabajos.html')

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form["correo"]
        password = request.form["password"]

        # buscar organizador en la BD

    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)