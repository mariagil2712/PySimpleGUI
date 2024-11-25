import PySimpleGUI as sg
import csv

sg.theme('NeutralBlue')

# Archivos de participantes y eventos definidos
archivo_eventos = 'eventos.csv'
archivo_participantes = 'participantes.csv'

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
def cargar_eventos():
    with open(archivo_eventos, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        return [fila for fila in lector]

def cargar_participantes():
    with open(archivo_participantes, mode='r', newline='', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        return [fila for fila in lector]

def guardar_eventos():
    with open(archivo_eventos, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(eventos)

def guardar_participantes():
    with open(archivo_participantes, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(participantes)

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
    [sg.Listbox(values=[], size=(40, 10), key='klista2', enable_events=True), sg.Image(key="kfoto", size=(20,20))]
]

# Interfaz configuración
layoutconfiguracion = [
    [sg.Checkbox("Validar Aforo", key="kcheck1", default=True)],
    [sg.Checkbox("Solicitar imágenes", key="kcheck2", default=True)],
    [sg.Checkbox("Modificar registros", key="kcheck3", default=True)],
    [sg.Checkbox("Eliminar registros", key="kcheck4", default=True)],
    [sg.Button("Guardar")]
]

# Llamado layout principal
layout = [
    [sg.TabGroup([[sg.Tab("Eventos", layouteventos)], [sg.Tab("Participantes", layoutparticipantes)], [sg.Tab("Configuración", layoutconfiguracion)]])]
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
eventos = cargar_eventos()
participantes = cargar_participantes()

# Ventana 
window = sg.Window("COP 16 - Registro de eventos", layout, finalize=True)

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

# Acciones (bucle)
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break

    # Lógica Tab Eventos
    if event == "Agregar evento":
        evento = values["knombreevento"]
        if evento:
            eventos.append([values["knombreevento"], values["klugar"], values["kfecha"], values["khora"], values["kcupo"]])
            actualizar_listaE()
            actualizar_comboE()
            guardar_eventos()
        window["knombreevento"].update('')
        window["klugar"].update('')
        window["kfecha"].update('')
        window["khora"].update('')
        window["kcupo"].update('')
        window["kFileE"].update('')

    if event == "kmodificarE":
        if values["klista1"]:
            eventoseleccionado = values["klista1"][0]
            nuevoevento = values["knombreevento"]
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
        participante = values["knombrepersona"]
        if participante:
            evento_seleccionado = values["kcomboeventos"]
            tipopart = values["kcombotipopart"]
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

    if event == "kmodificarP":
        if values["klista2"]:
            participanteseleccionado = values["klista2"][0]
            nuevo_participante = values["knombrepersona"]
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
        validaraforo = values["kcheck1"]
        solicitarimagenes = values["kcheck2"]
        permitirmodificar = values["kcheck3"]
        permitireliminar = values["kcheck4"]
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

window.close()
