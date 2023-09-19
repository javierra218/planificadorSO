import tkinter as tk
from tkinter import ttk
import threading
import random
import time
from tkinter.scrolledtext import ScrolledText
import matplotlib.pyplot as plt
import numpy as np
import ttkthemes  # Importa ttkthemes



# Variables globales para representar la simulación
nucleos = 0
simulacion_en_ejecucion = False
procesos = []
tabla_procesos = None
elementos_tabla = []

# Lista de núcleos disponibles
nucleos_disponibles = []

# Clase para representar un proceso


class Proceso:
    def __init__(self, nombre, prioridad):
        self.nombre = nombre
        self.prioridad = prioridad
        self.estado = "activo"  # El proceso comienza en estado activo
        self.nucleo = None  # Núcleo al que está asignado (inicialmente None)

# Función para validar la prioridad ingresada


def validar_prioridad(valor, prioridad_entry):
    try:
        prioridad = int(valor)
        if 1 <= prioridad <= 10:
            mensaje_error.set("")
            return True
        else:
            mensaje_error.set("La prioridad debe estar en el rango de 1 a 10.")
            return False
    except ValueError:
        mensaje_error.set(
            "La prioridad debe ser un número entero entre 1 y 10.")
        return False

# Función para activar los campos y crear la lista de núcleos disponibles


def activar_campos():
    # Declarar que estamos usando la variable global
    global nucleos, tabla_procesos, nucleos_disponibles
    nucleos = int(nucleos_entry.get())
    if nucleos > 0:
        nucleos_entry.config(state="disabled")
        nombre_entry.config(state="normal")
        prioridad_entry.config(state="normal")
        crear_proceso_button.config(state="normal")
        aceptar_button.config(state="disabled")  # Desactiva el botón "Aceptar"
        iniciar_simulacion_button.config(state="normal")

        # Crea la lista de núcleos disponibles
        nucleos_disponibles = ["Aleatorio"] + list(range(1, nucleos + 1))
        nucleo_combo["values"] = nucleos_disponibles
        # Establece "Aleatorio" como opción predeterminada
        nucleo_combo.current(0)

        # Crea la tabla de procesos (ahora dentro de esta función)
        crear_tabla_procesos()


# Función para crear la tabla de procesos
def crear_tabla_procesos():
    global tabla_procesos
    # Crea una tabla para mostrar los procesos y sus estados
    tabla_procesos = ttk.Treeview(ventana, columns=(
        "Nombre", "Prioridad", "Estado", "Núcleo"), show="headings")
    tabla_procesos.heading("Nombre", text="Nombre")
    tabla_procesos.heading("Prioridad", text="Prioridad")
    tabla_procesos.heading("Estado", text="Estado")
    tabla_procesos.heading("Núcleo", text="Núcleo")
    tabla_procesos.pack()

# Función para crear una nueva ventana para mostrar tablas por núcleo


def mostrar_tablas():
    global nucleos

    if nucleos == 0:
        return

    # Crea una nueva ventana para mostrar las tablas
    ventana_tablas = tk.Toplevel(ventana)
    ventana_tablas.title("Tablas de Procesos")

    # Crea un Notebook para las pestañas
    notebook = ttk.Notebook(ventana_tablas)
    notebook.pack(fill='both', expand='yes')

    # Crea una pestaña para cada núcleo
    for core in range(1, nucleos + 1):
        # Crear una tabla para el núcleo actual
        tabla_procesos_core = ttk.Treeview(notebook, columns=(
            "Nombre", "Prioridad", "Estado"), show="headings")
        tabla_procesos_core.heading("Nombre", text="Nombre")
        tabla_procesos_core.heading("Prioridad", text="Prioridad")
        tabla_procesos_core.heading("Estado", text="Estado")

        # Agregar los procesos del núcleo actual a la tabla
        for proceso in procesos:
            if proceso.nucleo == core:
                tabla_procesos_core.insert("", "end", values=(
                    proceso.nombre, proceso.prioridad, proceso.estado))

        # Añadir la pestaña al Notebook
        notebook.add(tabla_procesos_core, text=f"Núcleo {core}")

# Función para crear un nuevo proceso


def crear_proceso():
    # Obtiene el valor del campo de prioridad
    prioridad = prioridad_entry.get()
    nombre = nombre_entry.get()

    # Validar que el nombre del proceso no se repita
    nombres_procesos = [proceso.nombre for proceso in procesos]
    if nombre in nombres_procesos:
        mensaje_error.set("El nombre del proceso ya existe.")
        return

    if validar_prioridad(prioridad, prioridad_entry):
        # El valor es válido, continúa con la creación del proceso
        # Convierte la prioridad a entero si es válido
        prioridad = int(prioridad)

        # Obtener el núcleo seleccionado
        nucleo_seleccionado = nucleo_combo.get()
        if nucleo_seleccionado == "Aleatorio":
            nucleo_asignado = random.randint(1, nucleos)
        else:
            nucleo_asignado = int(nucleo_seleccionado)

        # Crear un nuevo proceso
        proceso = Proceso(nombre, prioridad)
        proceso.nucleo = nucleo_asignado

        # Agregar el proceso a la lista de procesos
        procesos.append(proceso)

        # Puedes actualizar la interfaz gráfica para mostrar los procesos creados
        actualizar_tabla_procesos()

        # Limpia los campos de entrada después de crear el proceso
        nombre_entry.delete(0, "end")
        prioridad_entry.delete(0, "end")


# Función para activar la simulación
def iniciar_simulacion():
    global simulacion_en_ejecucion, nucleos

    if not simulacion_en_ejecucion and nucleos > 0:
        # Deshabilita los botones y campos excepto "Detener Simulación"
        nucleos_entry.config(state="disabled")
        nombre_entry.config(state="disabled")
        prioridad_entry.config(state="disabled")
        crear_proceso_button.config(state="disabled")
        aceptar_button.config(state="disabled")
        iniciar_simulacion_button.config(state="disabled")
        detener_simulacion_button.config(state="normal")

        # Habilita el botón "Mostrar Tablas" al iniciar la simulación
        mostrar_tablas_button.config(state="normal")

        # Habilitar el boton grafica
        mostrar_grafica_button.config(state="normal")

        # Actualiza la etiqueta de estado de la simulación
        estado_simulacion_label.config(text="Simulación en curso")

        # Inicia la simulación en hilos separados para cada núcleo
        for _ in range(nucleos):
            t = threading.Thread(target=simulacion_scheduler)
            t.start()

        simulacion_en_ejecucion = True


# Función para detener la simulación
def detener_simulacion():
    global simulacion_en_ejecucion
    simulacion_en_ejecucion = False

    # Deshabilita los botones y campos excepto "Crear Proceso"
    nucleos_entry.config(state="disabled")
    nombre_entry.config(state="enable")
    prioridad_entry.config(state="enable")
    crear_proceso_button.config(state="enable")
    aceptar_button.config(state="disabled")
    iniciar_simulacion_button.config(state="enable")
    detener_simulacion_button.config(state="disabled")

    # Habilita el botón "Mostrar Tablas" después de detener la simulación
    mostrar_tablas_button.config(state="normal")

    # Actualiza la etiqueta de estado de la simulación
    estado_simulacion_label.config(text="Simulación detenida")

# Función para simular la asignación de procesos a los núcleos de CPU


def simulacion_scheduler():
    global simulacion_en_ejecucion
    print("Simulación iniciada")
    print(simulacion_en_ejecucion)
    while simulacion_en_ejecucion:
        print("Prueba")

        if procesos:
            proceso = random.choice(procesos)

            # Simula la asignación de CPU
            tiempo_ejecucion = random.randint(1, 5)
            time.sleep(tiempo_ejecucion)

            # Cambia el estado del proceso con las probabilidades especificadas
            nuevo_estado = random.choices(
                ["preparado", "bloqueado", "terminado"],
                weights=[0.9, 0.07, 0.03]
            )[0]

            if nuevo_estado != proceso.estado:
                evento = f"Proceso {proceso.nombre} cambió a estado {nuevo_estado}"
                ventana.after(0, lambda: registrar_evento(evento))

            proceso.estado = nuevo_estado

            # Actualiza la interfaz gráfica para reflejar el cambio de estado del proceso
            actualizar_tabla_procesos()
            ventana.update_idletasks()

# Función para actualizar la tabla de procesos en la interfaz gráfica


def actualizar_tabla_procesos():
    global tabla_procesos, elementos_tabla

    if tabla_procesos is None:
        return  # Si la tabla no está creada, no hacemos nada

    # Borrar los elementos anteriores de la tabla
    for i in elementos_tabla:
        tabla_procesos.delete(i)

    # Limpiar el registro de elementos anteriores
    elementos_tabla = []

    # Agregar los procesos actualizados a la tabla y registrar los elementos
    for proceso in procesos:
        nucleo = proceso.nucleo if proceso.nucleo is not None else "-"
        elemento = tabla_procesos.insert("", "end", values=(
            proceso.nombre, proceso.prioridad, proceso.estado, nucleo))
        elementos_tabla.append(elemento)


# Función para registrar eventos en el área de registro de eventos
def registrar_evento(evento):
    registro_eventos.insert(tk.END, evento + "\n")
    registro_eventos.see(tk.END)


def mostrar_grafica_procesos_por_nucleo():
    if not procesos:
        return

    # Contar la cantidad de procesos por núcleo
    procesos_por_nucleo = {}
    for proceso in procesos:
        nucleo = proceso.nucleo
        if nucleo is not None:
            if nucleo in procesos_por_nucleo:
                procesos_por_nucleo[nucleo] += 1
            else:
                procesos_por_nucleo[nucleo] = 1

    # Crear la gráfica de barras
    nucleos = list(procesos_por_nucleo.keys())
    cantidad_procesos = list(procesos_por_nucleo.values())

    # Establecer ubicaciones de barras como valores enteros en el eje x
    x_pos = np.arange(len(nucleos))

    # Crear una figura con nombre personalizado
    fig = plt.figure("Uso General", figsize=(8, 6))

    # Utilizar una paleta de colores más sobria
    # Paleta de colores de Matplotlib
    colores = plt.cm.Paired(range(len(nucleos)))

    plt.bar(x_pos, cantidad_procesos, color=colores,
            edgecolor='black', linewidth=1.2)

    # Etiquetas de los ejes y título
    plt.xlabel('Núcleo de CPU', fontsize=12)
    plt.ylabel('Cantidad de Procesos', fontsize=12)
    plt.title('Distribución de Procesos en Núcleos de CPU', fontsize=14)

    # Estilo del grid
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Mostrar etiquetas en las barras
    for i, cantidad in enumerate(cantidad_procesos):
        plt.text(x_pos[i], cantidad + 0.2, str(int(cantidad)),
                 ha='center', fontsize=10)  # Formatear como entero

    # Etiquetas en el eje x
    plt.xticks(x_pos, nucleos)

    plt.tight_layout()
    plt.show()


##############################################################################################################################

# Crear la ventana principal con temas
ventana = ttkthemes.ThemedTk()
ventana.get_themes()  # Lista de temas disponibles
ventana.set_theme("ubuntu")  # Elige un tema (por ejemplo, "smog")
ventana.title("Simulador de Scheduler")

# Crear la ventana principal sin temaas
# ventana = tk.Tk()
# ventana.title("Simulador de Scheduler")
# # ventana.configure(bg="black")

# ventana['padx'] = '5'  # '5' espacio entre elementos horizontalmente
# ventana['pady'] = '5'  # '5' espacio entre elementos verticalmente

# Configuración de la ventana para que no se pueda redimensionar o maximizarla (True por defecto).
ventana.resizable(False, False)

# Etiqueta y entrada para la cantidad de núcleos de CPU
nucleos_label = ttk.Label(ventana, text="Núcleos de CPU:")
nucleos_label.pack()
nucleos_entry = ttk.Entry(ventana)
nucleos_entry.pack()

# Botón para aceptar la cantidad de núcleos y habilitar campos
aceptar_button = ttk.Button(ventana, text="Aceptar", command=activar_campos)
aceptar_button.pack()

# Etiqueta y entrada para el nombre del proceso (inicialmente desactivada)
nombre_label = ttk.Label(ventana, text="Nombre del Proceso:")
nombre_label.pack()
nombre_entry = ttk.Entry(ventana)
nombre_entry.pack()
nombre_entry.config(state="disabled")  # Inicialmente desactivada

# Etiqueta y entrada para la prioridad del proceso (inicialmente desactivada)
prioridad_label = ttk.Label(ventana, text="Prioridad:")
prioridad_label.pack()
prioridad_entry = ttk.Entry(ventana)
prioridad_entry.pack()
prioridad_entry.config(state="disabled")  # Inicialmente desactivada

# Etiqueta para mostrar mensajes de error
mensaje_error = tk.StringVar()
mensaje_error_label = ttk.Label(
    ventana, textvariable=mensaje_error, foreground="red")
mensaje_error_label.pack()

# Botón para crear un nuevo proceso (inicialmente desactivado)
crear_proceso_button = ttk.Button(
    ventana, text="Crear Proceso", command=crear_proceso)
crear_proceso_button.pack()
crear_proceso_button.config(state="disabled")  # Inicialmente desactivado

# Agregar la lista desplegable para seleccionar el núcleo
nucleo_label = ttk.Label(ventana, text="Núcleo:")
nucleo_label.pack()
nucleo_combo = ttk.Combobox(ventana, values=nucleos_disponibles)
nucleo_combo.pack()
# La lista desplegable es de solo lectura
nucleo_combo.config(state="readonly")

# Botón para iniciar la simulación (inicialmente desactivado)
iniciar_simulacion_button = ttk.Button(
    ventana, text="Iniciar Simulación", command=iniciar_simulacion)
iniciar_simulacion_button.pack()
iniciar_simulacion_button.config(state="disabled")  # Inicialmente desactivado

# Botón para detener la simulación (inicialmente desactivado)
detener_simulacion_button = ttk.Button(
    ventana, text="Detener Simulación", command=detener_simulacion)
detener_simulacion_button.pack()
detener_simulacion_button.config(state="disabled")  # Inicialmente desactivado

# Etiqueta para mostrar el estado de la simulación
estado_simulacion_label = ttk.Label(ventana, text="")
estado_simulacion_label.pack()

# Crear el área de registro de eventos
registro_eventos = ScrolledText(ventana, wrap=tk.WORD, width=40, height=10)
registro_eventos.pack()

# Botón para mostrar tablas por núcleo
mostrar_tablas_button = ttk.Button(
    ventana, text="Mostrar Tablas", command=mostrar_tablas)
mostrar_tablas_button.pack()
mostrar_tablas_button.config(state="disabled")  # Inicialmente desactivado

mostrar_grafica_button = ttk.Button(
    ventana, text="Mostrar Gráfica", command=mostrar_grafica_procesos_por_nucleo)
mostrar_grafica_button.pack()
mostrar_grafica_button.config(state="disable")


# Ejecutar la aplicación
ventana.mainloop()
