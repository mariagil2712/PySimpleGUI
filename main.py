import PySimpleGUI as sg
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

sg.theme('NeutralBlue')

# Cargar datos desde los CSV para pandas
participantes_df = pd.read_csv('participantes.csv')  
eventos_df = pd.read_csv('eventos.csv') 

def grafico_torta():
    tipo_participante = participantes_df.iloc[:, 4].value_counts()  # iloc para acceder por índice de columna
    fig, ax = plt.subplots(figsize=(6, 6)) 
    ax.pie(tipo_participante, labels=tipo_participante.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  
    return fig

def graficobarrasvertical():
    # Accede a la columna [6] de eventos_df (eventos)
    eventos = participantes_df.iloc[:, 6]  # Columna de eventos (índice 6)
    conteo_eventos = eventos.value_counts()

    fig, ax = plt.subplots()
    ax.bar(conteo_eventos.index, conteo_eventos.values)
    ax.set_xlabel('Eventos')
    ax.set_ylabel('Número de Participantes')
    ax.set_title('Participantes por Evento')
    return fig

# Función para dibujar el gráfico en pysimplegui (en su canvas)
def dibujargraficocanvas(fig, canvas_elem):
    canvas_elem.TKCanvas.delete('all')  # Limpiar canvas
    figura_canvas = FigureCanvasTkAgg(fig, canvas_elem.TKCanvas)
    figura_canvas.draw()
    figura_canvas.get_tk_widget().pack(fill='both', expand=True)

# Archivos de participantes, eventos y configuración definidos
archivo_eventos = "eventos.csv"
archivo_participantes = "participantes.csv"
archivo_configuracion = "configuracion.csv"

# Interfaz login
layoutlogin = [
    [sg.Text("Usuario:"), sg.Input(key="kusuario")],
    [sg.Text("Contraseña:"), sg.Input(key="kcontraseña", password_char='*')],
    [sg.Button("Iniciar Sesión")]
]

# Lista eventos
eventos = []

# Lista participantes
participantes = []

# Funciones para subir datos desde los archivos
def subir_eventos():
    with open(archivo_eventos, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        return [fila for fila in lector]

def subir_participantes():
    with open(archivo_participantes, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        return [fila for fila in lector]

def subir_configuracion():
    with open(archivo_configuracion, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        return [fila for fila in lector][0] 

def guardar_eventos():
    with open(archivo_eventos, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(eventos)

def guardar_participantes():
    with open(archivo_participantes, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(participantes)

def guardar_configuracion():
    with open(archivo_configuracion, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['true' if valor else 'false' for valor in configuracion])

# Interfaz eventos
layouteventos = [
    [sg.Text("Nombre evento:"), sg.InputText(key="knombreevento"), sg.Text("Lugar:"), sg.InputText(key="klugar")],
    [sg.Text("Fecha:"), sg.InputText(key="kfecha"), sg.Text("Hora:"), sg.InputText(key="khora")],
    [sg.Text("Cupo:"), sg.InputText(key="kcupo"), sg.Text("Imagen:"), sg.Input(key="kFileE", enable_events=True), sg.FileBrowse(key="kbrowse1")],
    [sg.Button("Agregar evento"), sg.Button("Modificar evento", key="kmodificarE"), sg.Button("Eliminar evento", key="keliminarE")],
    [sg.Listbox(values=[], size=(50, 10), key='klista1', enable_events=True), sg.Image(key="kimagen", size=(20,20))]
]

# Interfaz participantes
layoutparticipantes = [
    [sg.Text("Evento:"), sg.Combo([], key="kcomboeventos"), sg.Text("Nombre:"), sg.InputText(key="knombrepersona")],
    [sg.Text("Tipo Documento:"), sg.InputText(key="ktipdoc"), sg.Text("Número Documento:"), sg.InputText(key="knumdoc")],
    [sg.Text("Teléfono:"), sg.InputText(key="ktelefono"), sg.Text("Tipo participante:"), sg.Combo(["Estudiante", "Profesor", "Colaborador", "Visitante"], key="kcombotipopart")],
    [sg.Text("Dirección:"), sg.InputText(key="kdireccion"), sg.Text("Foto:"), sg.Input(key="kFileF", enable_events=True), sg.FileBrowse(key="kbrowse2")],
    [sg.Button("Agregar participante"), sg.Button("Modificar participante",key="kmodificarP"), sg.Button("Eliminar participante",key="keliminarP")],
    [sg.Listbox(values=[], size=(50, 10), key='klista2', enable_events=True), sg.Image(key="kfoto", size=(20,20))]
]

# Interfaz configuración
layoutconfiguracion = [
    [sg.Checkbox("Validar Aforo", key="kcheck1", default=True)],
    [sg.Checkbox("Solicitar imágenes", key="kcheck2", default=True)],
    [sg.Checkbox("Modificar registros", key="kcheck3", default=True)],
    [sg.Checkbox("Eliminar registros", key="kcheck4", default=True)],
    [sg.Button("Guardar")]
]

# Interfaz análisis
layoutanalisis = [
    [sg.Text("Participantes que fueron a todos los eventos")],
    [sg.Listbox(values=[], size=(40, 6), key='klista3', enable_events=True)],
    [sg.Text("Participantes que fueron a al menos un evento")],
    [sg.Listbox(values=[], size=(40, 6), key='klista4', enable_events=True)],
    [sg.Text("Participantes que fueron solo al primer evento")],
    [sg.Listbox(values=[], size=(40, 6), key='klista5', enable_events=True)],
    [sg.Button("Hacer análisis", key = "kanalisis")]
]

#Interfáz gráficos
layoutgraficos = [
    [sg.Text("Distribución de participantes por tipo de participante")],
    [sg.Canvas(key='canvas_torta')],
    [sg.Text("Participantes por evento")],
    [sg.Canvas(key='canvas_barras_vertical')],
    [sg.Button("Generar Gráficos")]
]


# Llamado layout principal
layout = [
    [sg.TabGroup([[sg.Tab("Eventos", layouteventos)], [sg.Tab("Participantes", layoutparticipantes)], [sg.Tab("Análisis", layoutanalisis)], [sg.Tab("Gráficos", layoutgraficos)],[sg.Tab("Configuración", layoutconfiguracion)]])]
]

# Se abre ventana de inicio de sesión Y se hace lectura del archivo csv
window_login = sg.Window("Bienvenido: Iniciar sesión", layoutlogin, margins=(10, 10))

usuarios = []

with open('usuarios.txt', 'r') as archivo_u:
    lector_csv1 = csv.reader(archivo_u)
    for fila in lector_csv1:
        usuarios.append(fila)

# Bucle de esa ventana y verificación de correspondencia entre usuario y contraseña
while True:
    event, values = window_login.read()

    if event == sg.WIN_CLOSED:
        exit()

    if event == "Iniciar Sesión":
        usuario = values['kusuario']
        contraseña = values['kcontraseña']
        if [usuario, contraseña] in usuarios:
            sg.popup("¡Bienvenido!")
            window_login.close() #de esta manera, si las condiciones se cumplen se cierra la ventana de inicio de sesión, continúa el código y entonces se abre la ventana normal (principal)
            break
        else:
            sg.popup("Usuario o contraseña incorrectos, vuelve a intentarlo") #si las condiciones no se cumplen, se muestra un mensaje de error y se sigue repitiendo hasta q sea necesario

# subir datos iniciales
eventos = subir_eventos()
participantes = subir_participantes()

# Ventana 
window = sg.Window("COP 16 - Registro de eventos", layout, finalize=True)
configuracion = [valor.lower() == 'true' for valor in subir_configuracion()] 
window['kcheck1'].update(value=configuracion[0])
window['kcheck2'].update(value=configuracion[1])
window['kcheck3'].update(value=configuracion[2])
window['kcheck4'].update(value=configuracion[3])

# Función para actualizar la lista de eventos
def actualizar_listaE():
    window["klista1"].update(eventos)

# Función para actualizar el combobox de eventos
def actualizar_comboE():
    nombreseventos = [evento[0] for evento in eventos]
    window["kcomboeventos"].update(values=nombreseventos)

# Función para actualizar la lista de participantes
def actualizar_listaP():
    window["klista2"].update(participantes)

actualizar_listaE()
actualizar_comboE()
actualizar_listaP()

#Función para participantes que fueron a todos los eventos
def parentodoseventos():
    partyeventos = set()  #evita duplicados!!
    for participante in participantes:
        listeyp = [p[6] for p in participantes if p[2] == participante[2]]
        if len(listeyp) == len(eventos):  # Si fue a todos los eventos
            partyeventos.add(participante[0])  
    return list(partyeventos) 

# Función para participantes que fueron a al menos un evento
def almenos1():
    partyeventos = set()  
    for participante in participantes:
        listeyp = [p[6] for p in participantes if p[2] == participante[2]]
        if listeyp:  # Si fue a al menos un evento
            partyeventos.add(participante[0])  
    return list(partyeventos) 

# Función para participantes que fueron solo al primer evento
def soloprimerevento():
    partyeventos = set() 
    for participante in participantes:
        listeyp = [p[6] for p in participantes if p[2] == participante[2]]
        if len(listeyp) == 1 and listeyp[0] == eventos[0][0]:  # Si solo fue al primer evento
            partyeventos.add(participante[0])  
    return list(partyeventos)  

# Acciones (bucle)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break

    # Lógica Tab análisis 
    if event == "kanalisis":
        partanalisis1 = parentodoseventos()
        partanalisis2 = almenos1()
        partanalisis3 = soloprimerevento()

        # Actualizamos las listbox correspondientes con los resultados
        window["klista3"].update(partanalisis1)
        window["klista4"].update(partanalisis2)
        window["klista5"].update(partanalisis3)
    
    # Lógica Tab Eventos
    if event == "Agregar evento":
        try:
            nombre_evento = values["knombreevento"]
            if not nombre_evento:
                raise ValueError("El nombre del evento no puede estar vacío.")

            if any(evento[0] == nombre_evento for evento in eventos):
                raise ValueError("Ya existe un evento con este nombre.")

            lugar = values["klugar"]
            fecha = values["kfecha"]
            hora = values["khora"]
            cupo = values["kcupo"]
            imagen = values["kFileE"]

            if not lugar or not fecha or not hora or not cupo:
                raise ValueError("Todos los campos deben ser completados.")

            if not cupo.isdigit():
                raise ValueError("El cupo debe ser un número válido (dígitos numericos).")

            eventos.append([nombre_evento, lugar, fecha, hora, cupo])
            guardar_eventos()
            actualizar_listaE()
            actualizar_comboE()
        except Exception as e:
            sg.popup_error(f"Error al agregar evento: {e}")

    if event == "kmodificarE":
        try:
            if values["klista1"]:
                eventoseleccionado = values["klista1"][0]
                nuevoevento = values["knombreevento"]
                lugar = values["klugar"]
                fecha = values["kfecha"]
                hora = values["khora"]
                cupo = values["kcupo"]
                imagen = values["kFileE"]
                if not nuevoevento or not lugar or not fecha or not hora or not cupo:
                    raise ValueError("Todos los campos deben ser completados.")
                if not cupo.isdigit():
                    raise ValueError("El cupo debe ser un número válido (dígitos numericos).")
                if nuevoevento:
                    index = eventos.index(eventoseleccionado)
                    eventos[index] = [nuevoevento, values["klugar"], values["kfecha"], values["khora"], values["kcupo"]]
                    actualizar_listaE()
                    actualizar_comboE()
                    guardar_eventos()
            window["knombreevento"].update('')
            window["klugar"].update('')
            window["kfecha"].update('')
            window["khora"].update('')
            window["kcupo"].update('')
            window["kFileE"].update('')

        except Exception as e:
            sg.popup_error(f"Error al modificar evento: {e}")
    
    if event == "keliminarE":
        if values["klista1"]:
            eventoseleccionado = values["klista1"][0]
            eventos.remove(eventoseleccionado)
            actualizar_comboE()
            actualizar_listaE()
            guardar_eventos()
            window["knombreevento"].update('')
            window["klugar"].update('')
            window["kfecha"].update('')
            window["khora"].update('')
            window["kcupo"].update('')
            window["kFileE"].update('')

    if event == "klista1":
        if values["klista1"]:
            eventoseleccionado = values["klista1"][0]
            window["knombreevento"].update(eventoseleccionado[0])
            window["klugar"].update(eventoseleccionado[1])
            window["kfecha"].update(eventoseleccionado[2])
            window["khora"].update(eventoseleccionado[3])
            window["kcupo"].update(eventoseleccionado[4])

    # Lógica Tab Participantes
    if event == "Agregar participante":
        try:
            participante = values["knombrepersona"]
            if participante:
                evento_seleccionado = values["kcomboeventos"]
                tipopart = values["kcombotipopart"]
                numdoc = values["knumdoc"]
                tipodoc = values["ktipdoc"]
                telefono = values["ktelefono"]
                direccion = values["kdireccion"]

                if not participante or not evento_seleccionado or not tipopart or not numdoc or not tipodoc or not telefono or not direccion:
                    raise ValueError("Todos los campos deben ser completados.")
                
                if any(participante[2] == numdoc for participante in participantes):
                    raise ValueError("Ya existe un participante con este número de documento.")
                                
                if not numdoc.isdigit():
                    raise ValueError("El número de documento debe ser válido (dígitos numericos).")
                    
                participantes.append([participante, values["ktipdoc"], values["knumdoc"], values["ktelefono"], tipopart, values["kdireccion"], evento_seleccionado])
                actualizar_listaP()
                guardar_participantes()
            window["knombrepersona"].update('')
            window["ktipdoc"].update('')
            window["knumdoc"].update('')
            window["ktelefono"].update('')
            window["kdireccion"].update('')
            window["kcomboeventos"].update('')
            window["kFileF"].update('')

        except Exception as e:
            sg.popup_error(f"Error al agregar participante: {e}")
    
    if event == "kmodificarP":
        try: 
            if values["klista2"]:
                participanteseleccionado = values["klista2"][0]
                nuevo_participante = values["knombrepersona"]
                evento_seleccionado = values["kcomboeventos"]
                tipopart = values["kcombotipopart"]
                numdoc = values["knumdoc"]
                tipodoc = values["ktipdoc"]
                telefono = values["ktelefono"]
                direccion = values["kdireccion"]
                
                if not nuevo_participante or not evento_seleccionado or not tipopart or not numdoc or not tipodoc or not telefono or not direccion:
                    raise ValueError("Todos los campos deben ser completados.")

                if not numdoc.isdigit():
                    raise ValueError("El número de documento debe ser válido (dígitos numericos).")
                    
                if nuevo_participante:
                    index = participantes.index(participanteseleccionado)
                    participantes[index] = [nuevo_participante, values["ktipdoc"], values["knumdoc"], values["ktelefono"], values["kcombotipopart"], values["kdireccion"]]
                    actualizar_listaP()
                    guardar_participantes()
            window["knombrepersona"].update('')
            window["ktipdoc"].update('')
            window["knumdoc"].update('')
            window["ktelefono"].update('')
            window["kdireccion"].update('')
            window["kcomboeventos"].update('')
            window["kFileF"].update('')

        except Exception as e:
            sg.popup_error(f"Error al modificar participante: {e}")
    
    if event == "keliminarP":
        if values["klista2"]:
            participanteseleccionado = values["klista2"][0]
            participantes.remove(participanteseleccionado)
            actualizar_listaP()
            guardar_participantes()
            window["knombrepersona"].update('')
            window["ktipdoc"].update('')
            window["knumdoc"].update('')
            window["ktelefono"].update('')
            window["kdireccion"].update('')
            window["kcomboeventos"].update('')
            window["kFileF"].update('')

    if event == "klista2":
        if values["klista2"]:
            participanteseleccionado = values["klista2"][0]
            window["knombrepersona"].update(participanteseleccionado[0])
            window["ktipdoc"].update(participanteseleccionado[1])
            window["knumdoc"].update(participanteseleccionado[2])
            window["ktelefono"].update(participanteseleccionado[3])
            window["kcombotipopart"].update(participanteseleccionado[4])
            window["kdireccion"].update(participanteseleccionado[5])
            window["kcomboeventos"].update(participanteseleccionado[6])

    # Lógica Tab Configuración
    if event == "Guardar":
        configuracion = [
            values['kcheck1'],
            values['kcheck2'],
            values['kcheck3'],
            values['kcheck4']
        ]       
        validaraforo = values["kcheck1"]
        solicitarimagenes = values["kcheck2"]
        permitirmodificar = values["kcheck3"]
        permitireliminar = values["kcheck4"]
        guardar_configuracion()
        sg.popup("Configuración guardada", title="Configuración")

        window["kbrowse1"].update(visible=solicitarimagenes)
        window["kbrowse2"].update(visible=solicitarimagenes)
        window["kFileE"].update(visible=solicitarimagenes)
        window["kFileF"].update(visible=solicitarimagenes)
        window["kimagen"].update(visible=solicitarimagenes)
        window["kfoto"].update(visible=solicitarimagenes)

        window["kmodificarE"].update(visible=permitirmodificar)
        window["kmodificarP"].update(visible=permitirmodificar)

        window["keliminarE"].update(visible=permitireliminar)
        window["keliminarP"].update(visible=permitireliminar)

    #Lógica Tab Gráficos
    if event == "Generar Gráficos":
        # Crear los gráficos
        fig_torta = grafico_torta()
        fig_barras_vertical = graficobarrasvertical()

        # Dibujar los gráficos en el canvas
        dibujargraficocanvas(fig_torta, window['canvas_torta'])
        dibujargraficocanvas(fig_barras_vertical, window['canvas_barras_vertical'])
        
window.close()
