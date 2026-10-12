from abc import ABC, abstractmethod
import os

from models import Estudiante, Materia, Matricula
from shared.json_manager import GestorJSON
from shared.herramientas import es_email_valido

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


class CrudBase(ABC):
    @abstractmethod
    def leer(self): pass
    @abstractmethod
    def obtener(self, id_registro): pass
    @abstractmethod
    def buscar(self, texto): pass
    @abstractmethod
    def siguiente(self): pass
    @abstractmethod
    def crear(self, datos): pass
    @abstractmethod
    def actualizar(self, id_registro, datos): pass
    @abstractmethod
    def eliminar(self, id_registro): pass


class EstudianteController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "estudiantes.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Estudiante.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([e.a_diccionario() for e in self.lista])

    def carnets_registrados(self, excepto_id=None):
        return {e.carnet.upper() for e in self.lista if e.id != excepto_id and e.carnet}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "apellido", "email", "carnet"):
                if str(datos.get(campo, "")).strip() == "":
                    return f"El campo {campo} es obligatorio"

        if "email" in datos:
            email = str(datos["email"]).strip().lower()
            if not es_email_valido(email): return f"Email inválido: '{email}'"
            if email in {e.email for e in self.lista if e.id != id_actual}:
                return "Ese email ya está registrado"

        if "carnet" in datos:
            carnet = str(datos["carnet"]).strip().upper()
            if carnet in self.carnets_registrados(id_actual):
                return f"El carnet '{carnet}' ya está asignado"
        return None

    def leer(self): return self.lista

    def obtener(self, id_est):
        for e in self.lista:
            if e.id == id_est: return e
        return None

    def buscar(self, t):
        t = t.strip().lower()
        if not t: return []
        return [e for e in self.lista if t in e.nombre.lower() or t in e.apellido.lower() or t in e.carnet.lower()]

    def siguiente(self):
        return max([e.id for e in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        est = Estudiante(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["apellido"]).strip().title(), str(datos["email"]).strip().lower(),
            str(datos["carnet"]).strip().upper(), str(datos.get("carrera", "")).strip().title()
        )
        self.lista.append(est)
        self.guardar()
        return True, f"Estudiante creado: {est.etiqueta()}"

    def actualizar(self, id_est, datos):
        est = self.obtener(id_est)
        if not est: return False, "No existe el estudiante"
        error = self.validar(datos, id_est)
        if error: return False, error
        for k, v in datos.items():
            val = str(v).strip()
            if k in ("nombre", "apellido", "carrera"): val = val.title()
            elif k == "email": val = val.lower()
            elif k == "carnet": val = val.upper()
            setattr(est, k, val)
        self.guardar()
        return True, f"Estudiante {id_est} actualizado"

    def eliminar(self, id_est):
        est = self.obtener(id_est)
        if not est: return False, "No existe"
        self.lista.remove(est)
        self.guardar()
        return True, f"Estudiante {id_est} eliminado"

    def carreras(self):
        return sorted({e.carrera for e in self.lista if e.carrera})


class MateriaController(CrudBase):
    def __init__(self, archivo=None):
        ruta = archivo or os.path.join(DATA_DIR, "materias.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Materia.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([m.a_diccionario() for m in self.lista])

    def codigos_registrados(self, excepto_id=None):
        return {m.codigo.upper() for m in self.lista if m.id != excepto_id}

    def validar(self, datos, id_actual=None):
        if id_actual is None:
            for campo in ("nombre", "codigo", "creditos"):
                if str(datos.get(campo, "")).strip() == "": return f"El campo {campo} es obligatorio"
        if "codigo" in datos:
            cod = str(datos["codigo"]).strip().upper()
            if cod in self.codigos_registrados(id_actual): return f"El código '{cod}' ya existe"
        return None

    def leer(self): return self.lista
    def obtener(self, id_mat):
        for m in self.lista:
            if m.id == id_mat: return m
        return None

    def buscar(self, t):
        t = t.strip().lower()
        return [m for m in self.lista if t in m.nombre.lower() or t in m.codigo.lower()]

    def siguiente(self):
        return max([m.id for m in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        mat = Materia(
            self.siguiente(), str(datos["nombre"]).strip().title(),
            str(datos["codigo"]).strip().upper(), int(datos["creditos"]),
            int(datos["cupos"]) if str(datos.get("cupos", "")).strip() != "" else Materia.CUPOS_MAXIMOS
        )
        self.lista.append(mat)
        self.guardar()
        return True, f"Materia creada: {mat.etiqueta()}"

    def actualizar(self, id_mat, datos):
        mat = self.obtener(id_mat)
        if not mat: return False, "No existe"
        error = self.validar(datos, id_mat)
        if error: return False, error
        if "nombre" in datos: mat.nombre = str(datos["nombre"]).strip().title()
        if "codigo" in datos: mat.codigo = str(datos["codigo"]).strip().upper()
        if "creditos" in datos: mat.creditos = int(datos["creditos"])
        if "cupos" in datos and str(datos["cupos"]).strip() != "": mat.cupos = int(datos["cupos"])
        self.guardar()
        return True, f"Materia {id_mat} actualizada"

    def eliminar(self, id_mat):
        mat = self.obtener(id_mat)
        if not mat: return False, "No existe"
        self.lista.remove(mat)
        self.guardar()
        return True, f"Materia eliminada"

    def materias_sin_cupo(self):
        return [m for m in self.lista if not m.hay_cupo()]


class MatriculaController(CrudBase):
    def __init__(self, estudiantes, materias, archivo=None):
        self.estudiantes = estudiantes
        self.materias = materias
        ruta = archivo or os.path.join(DATA_DIR, "matriculas.json")
        self.gestor = GestorJSON(ruta)
        self.lista = [Matricula.desde_diccionario(d) for d in self.gestor.leer()]

    def guardar(self):
        self.gestor.guardar([mat.a_diccionario() for mat in self.lista])

    def validar(self, datos):
        try:
            est_id = int(datos.get("estudiante_id", 0))
            mat_id = int(datos.get("materia_id", 0))
        except (TypeError, ValueError):
            return "IDs inválidos"
        if not self.estudiantes.obtener(est_id): return "No existe el estudiante"
        materia = self.materias.obtener(mat_id)
        if not materia: return "No existe la materia"
        periodo = str(datos.get("periodo", "")).strip()
        if not periodo: return "El periodo es obligatorio"
        for mat in self.lista:
            if mat.estudiante_id == est_id and mat.materia_id == mat_id and mat.periodo == periodo:
                return "Ya está matriculado en esta materia para este periodo"
        if not materia.hay_cupo(): return "No hay cupos"
        return None

    def leer(self): return self.lista
    def obtener(self, id_mat):
        for m in self.lista:
            if m.id == id_mat: return m
        return None

    def buscar(self, t):
        return [mat for mat in self.lista if t.strip() in mat.periodo]

    def siguiente(self):
        return max([mat.id for mat in self.lista], default=0) + 1

    def crear(self, datos):
        error = self.validar(datos)
        if error: return False, error
        materia = self.materias.obtener(int(datos["materia_id"]))
        mat = Matricula(self.siguiente(), int(datos["estudiante_id"]), materia.id, str(datos["periodo"]).strip(), 0.0)
        materia.ocupar_cupo()
        self.materias.guardar()
        self.lista.append(mat)
        self.guardar()
        return True, f"Matrícula #{mat.id} registrada"

    def actualizar(self, id_mat, datos): return False, "No se modifica"

    def eliminar(self, id_mat):
        mat = self.obtener(id_mat)
        if not mat: return False, "No existe"
        materia = self.materias.obtener(mat.materia_id)
        if materia:
            materia.liberar_cupo()
            self.materias.guardar()
        self.lista.remove(mat)
        self.guardar()
        return True, "Matrícula retirada"

    def registrar_nota(self, id_mat, nota):
        mat = self.obtener(id_mat)
        if not mat: return False, "No existe"
        if not Materia.es_nota_valida(nota): return False, "Nota inválida (0-20)"
        mat.nota = float(nota)
        self.guardar()
        return True, "Nota registrada"

    def certificado(self, id_mat):
        mat = self.obtener(id_mat)
        if not mat: return None
        est = self.estudiantes.obtener(mat.estudiante_id)
        materia = self.materias.obtener(mat.materia_id)
        texto = f"CERTIFICADO #{mat.id}   periodo: {mat.periodo}\n"
        texto += f"Estudiante: {est.nombre_completo() if est else 'N/A'}   ({est.carnet if est else 'N/A'})\n"
        texto += f"Materia   : {materia.nombre if materia else 'N/A'}\n"
        texto += "-" * 40 + f"\nNota: {mat.nota}\nEstado: {mat.estado()}"
        return texto