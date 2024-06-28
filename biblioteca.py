from modulos import general as g, libros as l
print('----------------------------------¡Bienvenidos al servicio de gestión de la biblioteca!----------------------------------')

while True:
    op = g.menu_inicio() #Muestra las opciones generales y me va a pedir elegir una opción que va a quedar guardada en op
    match op:
        case 0: #Finalizar el programa
            print('----------------------------------Programa Finalizado----------------------------------')
            break
        case 1: #Sector de libros (Registrar, editar, eliminar)
            l.menu_libros() #Muestra opciones de registro, edición, eliminación y búsqueda         
        #case 2: #Sector de socios (Registrar, editar, eliminar)
         #   menu_socios() #Muestra opciones de registro, edición, e liminación y búsqueda
        #case 3:# Sector de préstamos (Registrar préstamo, devoluciones)
          #00  menu_prestamos_devoluciones()
        case 4:
            if not g.jsonVacio('libros.json'):
                print('BUSQUEDA DE LIBRO POR:')
                l.menu_buscar_libro() 
            else:
                print('No hay libros registrados aún')  