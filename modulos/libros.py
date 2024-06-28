from .general import validar_entero, jsonVacio, clear
from .prestamos import realizar_prestamo_desde_libros
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
    0- Volver
    Opción: """)
    clear()
    match op:
        case 1:
            registrar_libro()
        case 2: 
            menu_editar_libro()
        case 3:
            menu_eliminar_libro()

    
def registrar_libro():
    nuevo = True
    titulo = input('Título: ').title()
    autor = input('Autor: ').title()
    editorial = input('Editorial: ').title()
    for libro in libros:
        if libro['titulo'] == titulo and libro['autor'] == autor and libro['editorial']== editorial:
            nuevo=False
            op= input('Libro registrado. ¿Le gustaría agregar un ejemplar? (S/N)').capitalize()
            if op == 'S':
                modificar_cantidad(libro['id_libro'])
                break
    if nuevo == True:
        idAuto()
        genero = input('Genero: ').title()
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
        editar_libros_json()#escribo la lista actualizada en el json también
        input('Libro agregado correctamente. Enter para continuar')
        clear()

def menu_editar_libro():
    print('Búsqueda de libro a editar por:')
    id = busqueda_libro()
    editar_libro(id)


def editar_libro(id):
    print('Qué dato desea editar:')
    op = validar_entero(6,"""
                        1- Título
                        2- Autor
                        3- Editorial
                        4- Género
                        5- Año de publicación
                        6- Cantidad disponible
                        0- Volver
                        Opción: """)
    clear()
    if op != 0:
        match op:
            case 1: 
                categoria = 'titulo'
                dato = input('Nuevo título: ').title()
            case 2:
                categoria = 'autor'
                dato = input('Nuevo autor: ').title()
            case 3:
                categoria = 'editorial'
                dato = input('Nueva editorial: ')
            case 4: 
                categoria = 'genero'
                dato = input('Nuevo género: ').title()
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
        clear()

def modificar_datos(id,cat,dato):
    cargar_libros_json()
    libros[id-1][cat] = dato
    editar_libros_json()

def modificar_cantidad(id):
    libros[id-1]['cantidad_disponible'] +=1
    editar_libros_json()

def menu_buscar_libro():
    id = busqueda_libro()
    accion_encontrado(id)

def busqueda_libro():
    cargar_libros_json() #Acá sólo entra si hay libros registrados
    op = validar_entero(5,"""
                        1- Título
                        2- Autor
                        3- Editorial
                        4- Género
                        5- Id
                        0- Volver
                        Opción: """)
    clear()
    if op != 0:
        match op:
            case 1: 
                categoria = 'titulo'
                dato = input('Título buscado: ').title()
            case 2:
                categoria = 'autor'
                dato = input('Autor buscado: ').title()
            case 3:
                categoria = 'editorial'
                dato = input('Editorial buscada: ').title()
            case 4: 
                categoria = 'genero'
                dato = input('Género buscado: ').title()
            case 5:
                id_l_elegido = validar_entero(len(libros), 'Ingrese el id del libro: ')
        if op != 5:
            id_l_elegido = buscar_datos_libros(dato, categoria)
        mostrar_libro(id_l_elegido)
        input('Presione Enter para continuar')
        clear()
        return id_l_elegido

def accion_encontrado(id):   
    accion = validar_entero(3,"""
                                ¿Qué desea hacer?
                                1- Realizar un préstamo
                                2- Editarlo
                                3- Eliminarlo
                                0- Volver
                                Opcion: """)
    clear()
    match accion:
        case 1:   
            realizar_prestamo_desde_libros(id) #se encargará préstamos
        case 2:
            editar_libro(id)
        case 3:
            eliminar_libro(id)


def mostrar_libro(id): #únicamente muestra el libro
    #libros = cargar_libros_json()
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
            print(f"""Id: {libro['id_libro']} ||Título: {libro['titulo']} ||Autor: {libro['autor']} ||Editorial: {libro['editorial']} """)
    id = validar_entero(len(libros), 'Ingrese el id del libro elegido (0- Volver): ')
    return id
              
def menu_eliminar_libro():
    print('Buscar libro a eliminar por:')
    id = busqueda_libro()
    eliminar_libro(id)

def eliminar_libro(id):
    libros[id-1]['estado'] = 'Eliminado'
    editar_libros_json()
    input('Libro eliminado correctamente')
    clear()

#manipulación de json

def cargar_libros_json():
    global libros
    global id_libro
    if not jsonVacio('libros.json'):
        with open('libros.json','r',encoding='utf-8') as li:
            libros = json.load(li)
            id_libro = libros[-1]['id_libro']
        return libros

def editar_libros_json():
    with open('libros.json','w',encoding='utf-8') as l:
        json.dump(libros,l,indent=4, ensure_ascii=False)
    

def idAuto():
    global id_libro
    id_libro +=1