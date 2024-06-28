from .general import validar_entero, jsonVacio, clear
from .prestamos import realizar_prestamo
import json, os, datetime
libros = []
id_libro = 0

def menu_libros():
    cargar_libros_json()#nos traemos el libros.json
    op = validar_entero(4,"""
Sección LIBROS:
1- Registrar
2- Editar
3- Eliminar
Opción: """)
    
def registrar_libro():
    nuevo = True
    titulo = input('Título: ').capitalize()
    autor = input('Autor: ').capitalize()
    editorial = input('editorial: ').capitalize()
    for libro in libros:
        if libro['titulo'] == titulo and libro['autor'] == autor and libro['editorial']== editorial:
            nuevo=False
            op= input('Libro registrado. ¿Le gustaría agregar un ejemplar? (S/N)').capitalize()
            if op == 'S':
                modificar_cantidad(libro['id_libro'])
                break
    if nuevo == True:
        idAuto()
        genero = input('Genero: ').capitalize()
        anio_publicacion = validar_entero(datetime.datetime.now().year,'Año de publicación: ')
        cantidad_disponible = validar_entero(1000,'Cantidad de ejemplares disponibles: ')
        l = {
            "id_libro":id_libro,
            "titulo":titulo,
            "autor":autor,
            "editorial":editorial,
            "anio_publicacion":anio_publicacion,
            "genero":genero,
            "cantidad_disponible": cantidad_disponible,
            "estado":'Activo'
        }
        libros.append(l)
        editar_libro_json(libros)#escribo la lista actualizada en el json también


def editar_libro(id):
    op = validar_entero(6,"""
Qué dato desea editar:
                        1- Título
                        2- Autor
                        3- Editorial
                        4- Género
                        5- Año de publicación
                        6- Cantidad disponible
                        0- Volver
                        Opción: """)
    if op != 0:
        match op:
            case 1: 
                categoria = 'titulo'
                dato = input('Nuevo título: ')
            case 2:
                categoria = 'autor'
                dato = input('Nuevo autor: ')
            case 3:
                categoria = 'editorial'
                dato = input('Nueva editorial: ')
            case 4: 
                categoria = 'genero'
                dato = input('Nuevo género: ')
            case 5:
                categoria = 'anio_publicacion'
                dato = validar_entero(datetime.datetime.now().year, 'Nuevo año de publicación')
            case 6:
                categoria = 'cantidad_disponible'
                dato = validar_entero(1000, 'Cantidad disponible: ')
        modificar_datos(id, categoria,dato)
        clear()
        print('Datos actualizados:')
        mostrar_libro(id)
        input('Dato modificado exitosamente. Presione Enter para continuar')

def modificar_datos(id,cat,dato):
    libros[id-1][cat] == dato
    editar_libro_json()

def modificar_cantidad(id):
    libros[id-1]['cantidad_disponible'] +=1
    editar_libro_json(libros)


def busqueda_libro():
    cargar_libros_json() #Acá sólo entra si hay libros registrados
    op = validar_entero(5,"""
BUSQUEDA DE LIBRO POR:
                        1- Título
                        2- Autor
                        3- Editorial
                        4- Género
                        5- Id
                        0- Volver
                        Opción: """)
    if op != 0:
        match op:
            case 1: 
                categoria = 'titulo'
                dato = input('Título buscado: ')
            case 2:
                categoria = 'autor'
                dato = input('Autor buscado: ')
            case 3:
                categoria = 'editorial'
                dato = input('Editorial buscada: ')
            case 4: 
                categoria = 'genero'
                dato = input('Género buscado: ')
            case 5:
                id_l_elegido = validar_entero(len(libros), 'Ingrese el id del libro: ')
        if op != 5:
            id_l_elegido = buscar_datos_libros(dato, categoria)
        mostrar_libro(id_l_elegido)
        accion = validar_entero(3,"""
                                ¿Qué desea hacer?
                                1- Realizar un préstamo
                                2- Editarlo
                                3- Eliminarlo
                                0- Volver
                                Opcion: """)
        match accion:
            case 1:   
                realizar_prestamo(id_l_elegido) #se encargará préstamos
            case 2:
                editar_libro(id_l_elegido)
            case 3:
                eliminar_libro(id_l_elegido)


def mostrar_libro(id): #únicamente muestra el libro
    print(f"""
        Libro elegido:
        Id_Libro: {libros[id-1]['id_libro']}
        Título: {libros[id-1]['titulo']}
        Autor: {libros[id-1]['autor']}
        Editorial: {libros[id-1]['editorial']}
        Género: {libros[id-1]['genero']}
        Año de publicación: {libros[id-1]['anio_publicacion']}
        Cantidad disponible: {libros[id-1]['cantidad_disponible']}""")

def buscar_datos_libros(dato, categoria): #buscar y devolver el id (si es -1 es porque no estaba)
    for libro in libros:
        if libro[categoria]==dato and libro['estado']=='Activo':
            print(f"""Título: {libro['titulo']} ||Autor: {libro['autor']} ||Editorial: {libro['editorial']} """)
    id = validar_entero(len(libros), 'Ingrese el id del libro elegido (0- Volver): ')
    return id
              



#manipulación de json

def cargar_libros_json():
    global libros
    global id_libro
    if not jsonVacio('libros.json'):
        with open('libros.json','r',encoding='utf-8') as l:
            libros = json.load(l)
            id_libro = libros[-1]['id_libro']


def editar_libro_json():
    global libros
    with open('libros.json','w',encoding='utf-8') as l:
        json.dump(libros,l,indent=4, ensure_ascii=False)


def idAuto():
    global id_libro
    id_libro +=1