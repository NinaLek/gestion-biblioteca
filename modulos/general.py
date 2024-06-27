import calendar, datetime as d, os

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def menu_inicio():
    op= validar_entero(5,"""
        SECCIONES:
1- LIBROS
2- SOCIOS
3- PRÉSTAMOS/DEVOLUCIONES
4- BÚSQUEDA DE LIBRO
5- RECOMENDAME UN LIBRO
0- FINALIZAR
opción: """)
    clear()
    return op


def verificar_fechas():
    while True:
        f = input('indique día (dd/mm/aaaa): ')
        dia,mes,anio = f.split('/')
        if anio.isdigit():
            anio = int(anio)
            if anio <= d.datetime.now().year and mes.isdigit():
                mes = int(mes)
                ult_dia_mes = calendar.monthrange(anio,mes)[1]
                if dia.isdigit() and int(dia)<=ult_dia_mes:
                    f = d.datetime.strptime(f,'%d/%m/%Y')
                    return f
        print('Fecha incorrecta.Inténtelo nuevamente')
                
def validar_entero(rango,dato ='opción: '):
    while True:
        n = input(dato)
        if n.isdigit():
            n=int(n)
            if 0 <= n <= rango:
                return n
            else:
                print('Incorrecto. fuera de rango')
        else:
            print('Incorrecto. no fue correcto')
            