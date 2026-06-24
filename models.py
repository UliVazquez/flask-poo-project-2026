from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Autor(db.Model):
    __tablename__= 'autor'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    trabajos = db.relationship('Trabajo', backref='autor', cascade='delete-orphan')

    def get_id(self):
        return self.id
    
    def get_nombre(self):
        return self.nombre
    
    def get_apellido(self):
        return self.apellido
    
    def get_email(self):
        return self.email
    
    def get_trabajos(self):
        return self.trabajos

class Trabajo(db.Model):
    __tablename__ = 'trabajo'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    resumen = db.Column(db.Text, nullable=False)
    area = db.Column(db.String(2), nullable=False)
    estado = db.Column(db.String(10), nullable=False)
    ruta_archivo_pdf = db.Column(db.String(255), nullable=False)
    autor_id = db.Column(db.Integer, db.ForeignKey('autor.id'))

    def get_id(self):
        return self.id
    
    def get_titulo(self):
        return self.titulo
    
    def get_resumen(self):
        return self.resumen
    
    def get_area(self):
        return self.area
    
    def get_ruta_archivo_pdf(self):
        return self.ruta_archivo_pdf

class Organizador(db.Model):
    pass