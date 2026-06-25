from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class Autor(db.Model):
    __tablename__= 'autor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    trabajos = db.relationship('Trabajo', backref='autor', cascade='delete-orphan')

    def get_id(self):
        return self.id
    
    def get_nombre(self):
        return self.name
    
    def get_apellido(self):
        return self.surname
    
    def get_email(self):
        return self.email
    
    def get_trabajos(self):
        return self.trabajos

class Trabajo(db.Model):
    __tablename__ = 'trabajo'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    desc = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(2), nullable=False)
    estado = db.Column(db.String(10), nullable=False)
    ruta_archivo_pdf = db.Column(db.String(255), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'))

    def get_id(self):
        return self.id
    
    def get_titulo(self):
        return self.title
    
    def get_resumen(self):
        return self.desc
    
    def get_area(self):
        return self.area
    
    def get_ruta_archivo_pdf(self):
        return self.ruta_archivo_pdf

class Organizador(db.Model):
    __tablename__ = 'organizador'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.id
    
    def get_email(self):
        return self.email
    
class Evaluador(db.Model):
    __tablename__ = 'evaluador'
    
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(2), nullable=False)
    max_trabajos = db.Column(db.Integer, default=3)

class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'
    
    id = db.Column(db.Integer, primary_key=True)
    trabajo_id = db.Column(db.Integer, db.ForeignKey("trabajo.id"))
    evaluador_id = db.Column(db.Integer, db.ForeignKey("evaluador.id"))