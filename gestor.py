from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from models import db, Autor, Organizador, Trabajo
import os

class Gestor():
    def createDB(self):
        db.create_all()

    def crear_autor(self, nombre, apellido, mail):
        autor = Autor(name = nombre, surname = apellido, email = mail)
        if not autor.id:
            db.session.add(autor)
            db.session.commit()
    
    def generar_nombre_archivo(self, autor_id, titulo):
        fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
        titulo_limpio = secure_filename(titulo).replace(" ", "_")
        return f"{autor_id}_{titulo_limpio}_{fecha}.pdf"

    def verificar_autor_por_mail(self, email):
        return True if Autor.query.filter_by(email=email).first() else False

    def get_id_autor_por_mail(self, email):
        return Autor.query.filter_by(email=email).first().get_id()

    def subir_archivo(self, archivo, nombre_archivo, carpeta):
        ruta = os.path.join(carpeta, nombre_archivo)
        archivo.save(ruta)
        return ruta
    
    def crear_trabajo(self, titulo, res, ar, route, autorID):
        trabajo = Trabajo(title = titulo, desc = res, area = ar, estado = "Pendiente", ruta_archivo_pdf = route, autor_id = autorID)
        if not trabajo.id:
            db.session.add(trabajo)
            db.session.commit()
    
    def get_id_trabajo_por_ruta_archivo(self, ruta):
        return Trabajo.query.filter_by(ruta_archivo_pdf=ruta).first().get_id()