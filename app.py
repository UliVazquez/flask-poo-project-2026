from flask import Flask, redirect, url_for, render_template, request, session

app = Flask(__name__)
app.secret_key = "profeapruebemeporfavor"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload')
def enviar_trabajo():
    return render_template('upload.html')

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)