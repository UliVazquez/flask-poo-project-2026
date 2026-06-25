from models import db, Organizador, Evaluador, Trabajo, Asignacion

class Gestor():
    def createDB(self):
        db.create_all()
    
    def crear_trabajo(self, titulo, resumen, area, autor_nombre, autor_apellido, autor_email, nombre_seguro):
        trabajo = Trabajo(titulo = titulo, resumen = resumen, area = area, estado = "Pendiente", autor_nombre = autor_nombre, autor_apellido = autor_apellido, autor_email = autor_email, archivo_nombre = nombre_seguro)
        if not trabajo.id:
            db.session.add(trabajo)
            db.session.commit()
    
    def get_id_trabajo_por_nombre_archivo(self, nombre):
        return Trabajo.query.filter_by(archivo_nombre=nombre).first().get_id()
    
    def existe_organizador(self, email, clave):
        org = Organizador.query.filter_by(correo=email).first()
        b = False
        if org != None:
            b = org.verificar_clave(clave)
        return b

    def get_nombre_org_por_email(self, email):
        return Organizador.query.filter_by(correo=email).first().get_nombre()
    
    def get_apellido_org_por_email(self, email):
        return Organizador.query.filter_by(correo=email).first().get_apellido()
    
    def asignar_trabajos(self):
        trabajos_pendientes = Trabajo.query.filter_by(estado="Pendiente").all()
        i = 0
        for trabajo in trabajos_pendientes:
            if len(trabajo.get_asignaciones()) < 3:
                evaluadores_posibles = Evaluador.query.filter_by(area=trabajo.get_area()).all()
                j = 0
                while j < len(evaluadores_posibles):
                    evaluador = evaluadores_posibles[j]
                    # Puede evaluar si tiene menos asignaciones que su maximo de trabajos asignados
                    puede_evaluar = len(evaluador.get_asignaciones()) < evaluador.get_max_trabajos()
                    # Puede evaluar si no está asignado a este trabajo
                    ya_asignado = False
                    asignaciones_eval = evaluador.get_asignaciones()
                    k = 0
                    while k < len(asignaciones_eval) and not ya_asignado:
                        if asignaciones_eval[k].get_trabajo_id() == trabajo.get_id():
                            ya_asignado = True
                        k += 1
                    if puede_evaluar and not ya_asignado:
                        nueva = Asignacion(
                            trabajo_id=trabajo.get_id(),
                            evaluador_id=evaluador.get_id()
                        )
                        db.session.add(nueva)
                        db.session.commit()
                    # Dejar de buscar si el trabajo ya tiene 3 evaluadores
                    if len(trabajo.get_asignaciones()) >= 3:
                        j = len(evaluadores_posibles)  # fuerza salida del while
                    else:
                        j += 1
            i += 1