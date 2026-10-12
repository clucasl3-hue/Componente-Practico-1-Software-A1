from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
from views import EstudianteController, MateriaController, MatriculaController

# Controladores globales
estudiantes = EstudianteController()
materias = MateriaController()
matriculas = MatriculaController(estudiantes, materias)


def pausa():
    input("\nPresione Enter para continuar...")


def pedir_entero(etiqueta):
    try:
        return int(input(etiqueta))
    except ValueError:
        return None


def mostrar_resultado(exito, mensaje):
    if exito: imprimir_exito(mensaje)
    else: imprimir_error(mensaje)


def mostrar_lista(objetos, vacio="No hay registros todavía."):
    if not objetos:
        imprimir_info(vacio)
        return
    for obj in objetos:
        print(f"  {obj}")
    imprimir_info(f"Total: {len(objetos)}")


def mostrar_detalle(objeto):
    for clave, valor in objeto.a_diccionario().items():
        print(f"  {str(clave).replace('_', ' ').capitalize():<16}: {valor}")


# =====================================================================
# MENÚ ESTUDIANTES
# =====================================================================
def crear_estudiante():
    imprimir_titulo("CREAR ESTUDIANTE")
    datos = {
        "nombre": input("Nombre: "),
        "apellido": input("Apellido: "),
        "email": input("Email: "),
        "carnet": input("Carnet (ej. EST2026001): "),
        "carrera": input("Carrera: ")
    }
    mostrar_resultado(*estudiantes.crear(datos))
    pausa()

def listar_estudiantes():
    imprimir_titulo("LISTA DE ESTUDIANTES")
    mostrar_lista(estudiantes.leer(), "No hay estudiantes registrados.")
    pausa()

def buscar_estudiante():
    imprimir_titulo("BUSCAR ESTUDIANTE")
    termino = input("Nombre, apellido, carnet o carrera: ")
    mostrar_lista(estudiantes.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_estudiante():
    imprimir_titulo("VER ESTUDIANTE POR ID")
    est = estudiantes.obtener(pedir_entero("Id: "))
    if not est: imprimir_error("No encontrado")
    else: mostrar_detalle(est)
    pausa()

def actualizar_estudiante():
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    id_est = pedir_entero("Id: ")
    est = estudiantes.obtener(id_est)
    if not est:
        imprimir_error("No encontrado")
        return pausa()

    print("Deje en blanco lo que no quiera cambiar.\n")
    cambios = {}
    for campo in ("nombre", "apellido", "email", "carnet", "carrera"):
        actual = getattr(est, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*estudiantes.actualizar(id_est, cambios))
    pausa()

def eliminar_estudiante():
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    id_est = pedir_entero("Id: ")
    est = estudiantes.obtener(id_est)
    if not est:
        imprimir_error("No encontrado")
        return pausa()

    if confirmar(f"¿Confirma eliminar a {est.nombre_completo()}?"):
        mostrar_resultado(*estudiantes.eliminar(id_est))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ MATERIAS
# =====================================================================
def crear_materia():
    imprimir_titulo("CREAR MATERIA")
    datos = {
        "nombre": input("Nombre: "),
        "codigo": input("Código (ej. MAT101): "),
        "creditos": input("Créditos: "),
        "cupos": input("Cupos (Enter para máximo 30): ")
    }
    mostrar_resultado(*materias.crear(datos))
    pausa()

def listar_materias():
    imprimir_titulo("LISTA DE MATERIAS")
    mostrar_lista(materias.leer(), "No hay materias registradas.")
    pausa()

def buscar_materia():
    imprimir_titulo("BUSCAR MATERIA")
    termino = input("Nombre o código: ")
    mostrar_lista(materias.buscar(termino), "Sin coincidencias.")
    pausa()

def ver_materia():
    imprimir_titulo("VER MATERIA POR ID")
    mat = materias.obtener(pedir_entero("Id: "))
    if not mat: imprimir_error("No encontrada")
    else: mostrar_detalle(mat)
    pausa()

def actualizar_materia():
    imprimir_titulo("ACTUALIZAR MATERIA")
    id_mat = pedir_entero("Id: ")
    mat = materias.obtener(id_mat)
    if not mat:
        imprimir_error("No encontrada")
        return pausa()

    cambios = {}
    for campo in ("nombre", "codigo", "creditos", "cupos"):
        actual = getattr(mat, campo)
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        if nuevo: cambios[campo] = nuevo

    mostrar_resultado(*materias.actualizar(id_mat, cambios))
    pausa()

def eliminar_materia():
    imprimir_titulo("ELIMINAR MATERIA")
    id_mat = pedir_entero("Id: ")
    mat = materias.obtener(id_mat)
    if not mat:
        imprimir_error("No encontrada")
        return pausa()

    if confirmar("¿Confirma eliminar esta materia?"):
        mostrar_resultado(*materias.eliminar(id_mat))
    else:
        imprimir_info("Operación cancelada")
    pausa()


# =====================================================================
# MENÚ MATRÍCULAS
# =====================================================================
def registrar_matricula():
    imprimir_titulo("REGISTRAR MATRÍCULA")
    imprimir_info("Estudiantes:")
    mostrar_lista(estudiantes.leer())
    imprimir_info("Materias:")
    mostrar_lista(materias.leer())

    datos = {
        "estudiante_id": pedir_entero("\nId del estudiante: "),
        "materia_id": pedir_entero("Id de la materia: "),
        "periodo": input("Periodo (ej. 2026-1): ")
    }
    if None in list(datos.values())[:2]:
        imprimir_error("Los IDs deben ser números enteros")
        return pausa()

    mostrar_resultado(*matriculas.crear(datos))
    pausa()

def listar_matriculas():
    imprimir_titulo("LISTA DE MATRÍCULAS")
    mostrar_lista(matriculas.leer(), "No hay matrículas registradas.")
    pausa()

def registrar_nota_matricula():
    imprimir_titulo("REGISTRAR NOTA")
    mostrar_lista(matriculas.leer())
    id_mat = pedir_entero("\nId de la matrícula: ")
    nota = input("Ingrese la nota (0 a 20): ")
    mostrar_resultado(*matriculas.registrar_nota(id_mat, nota))
    pausa()

def ver_certificado():
    imprimir_titulo("CERTIFICADO DE MATRÍCULA")
    texto = matriculas.certificado(pedir_entero("Id de la matrícula: "))
    if not texto: imprimir_error("No existe esa matrícula")
    else: print(texto)
    pausa()

def retirar_matricula():
    imprimir_titulo("RETIRAR MATRÍCULA")
    id_mat = pedir_entero("Id de la matrícula: ")
    if id_mat and confirmar("Se devolverá el cupo a la materia. ¿Confirma?"):
        mostrar_resultado(*matriculas.eliminar(id_mat))
    else:
        imprimir_info("Operación cancelada")
    pausa()

def resumen():
    imprimir_titulo("RESUMEN ACADÉMICO")
    print(f"  Estudiantes     : {len(estudiantes.leer())}")
    print(f"  Carreras        : {', '.join(estudiantes.carreras()) or '-'}")
    print(f"  Materias        : {len(materias.leer())}")
    sin_cupo = materias.materias_sin_cupo()
    print(f"  Materias llenas : {', '.join(m.nombre for m in sin_cupo) or 'ninguna'}")
    print(f"  Matrículas      : {len(matriculas.leer())}")
    aprobadas = sum(1 for m in matriculas.leer() if m.esta_aprobada())
    print(f"  Aprobadas       : {aprobadas}")
    pausa()


# =====================================================================
# CONFIGURACIÓN DE MENÚS (Diccionarios)
# =====================================================================
MENU_ESTUDIANTES = {
    "1": ("Crear estudiante", crear_estudiante),
    "2": ("Ver todos", listar_estudiantes),
    "3": ("Buscar", buscar_estudiante),
    "4": ("Ver por id", ver_estudiante),
    "5": ("Actualizar", actualizar_estudiante),
    "6": ("Eliminar", eliminar_estudiante),
    "0": ("Volver", None),
}

MENU_MATERIAS = {
    "1": ("Crear materia", crear_materia),
    "2": ("Ver todas", listar_materias),
    "3": ("Buscar", buscar_materia),
    "4": ("Ver por id", ver_materia),
    "5": ("Actualizar", actualizar_materia),
    "6": ("Eliminar", eliminar_materia),
    "0": ("Volver", None),
}

MENU_MATRICULAS = {
    "1": ("Registrar matrícula", registrar_matricula),
    "2": ("Ver todas", listar_matriculas),
    "3": ("Registrar nota", registrar_nota_matricula),
    "4": ("Ver certificado", ver_certificado),
    "5": ("Retirar matrícula", retirar_matricula),
    "0": ("Volver", None),
}


def ejecutar_menu(titulo, opciones):
    while True:
        imprimir_titulo(titulo)
        for tecla, (texto, _) in opciones.items():
            print(f"  {tecla}. {texto}")
        print()

        tecla = input("Opción: ").strip()
        if tecla not in opciones:
            imprimir_error("Opción no válida")
            pausa()
            continue

        _, funcion = opciones[tecla]
        if funcion is None: break
        funcion()


def main():
    while True:
        imprimir_titulo("SISTEMA ACADÉMICO")
        print("  1. Estudiantes")
        print("  2. Materias")
        print("  3. Matrículas")
        print("  4. Resumen")
        print("  0. Salir\n")

        tecla = input("Opción: ").strip()
        if tecla == "1": ejecutar_menu("ESTUDIANTES", MENU_ESTUDIANTES)
        elif tecla == "2": ejecutar_menu("MATERIAS", MENU_MATERIAS)
        elif tecla == "3": ejecutar_menu("MATRÍCULAS", MENU_MATRICULAS)
        elif tecla == "4": resumen()
        elif tecla == "0":
            imprimir_info("¡Hasta luego! 👋")
            break
        else:
            imprimir_error("Opción no válida")
            pausa()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")