import tkinter as tk
from tkinter import ttk
import threading
import random
import time
import re
import numpy as np
from tkinter.scrolledtext import ScrolledText

# Variables globales para representar la simulación
nucleos = 0
simulacion_en_ejecucion = False
procesos = []

# Clase para representar un proceso
class Proceso:
    def __init__(self, nombre, prioridad):
        self.nombre = nombre
        self.prioridad = prioridad
        self.estado = "activo"  # El proceso comienza en estado activo

# Función para validar la prioridad ingresada
def validar_prioridad(valor, prioridad_entry):
    # Valida que el valor ingresado sea un número entero dentro del rango deseado.
    try:
        prioridad = int(valor)
        if 1 <= prioridad <= 10:
            mensaje_error.set("")  # La entrada es válida, borra el mensaje de error
            return True
        else:
            # La entrada está fuera de rango, muestra un mensaje de error.
            mensaje_error.set("La prioridad debe estar en el rango de 1 a 10.")
            return False
    except ValueError:
        # La entrada no es un número entero, muestra un mensaje de error.
        mensaje_error.set("La prioridad debe ser un número entero entre 1 y 10.")
        return False



# Función para crear un nuevo proceso
def crear_proceso():
    # Obtiene el valor del campo de prioridad
    prioridad = prioridad_entry.get()

    if validar_prioridad(prioridad, prioridad_entry):
        # El valor es válido, continúa con la creación del proceso
        prioridad = int(prioridad)  # Convierte la prioridad a entero si es válido
        nombre = nombre_entry.get()
        
        # Crear un nuevo proceso
        proceso = Proceso(nombre, prioridad)
        
        # Agregar el proceso a la lista de procesos
        procesos.append(proceso)
        
        # Puedes actualizar la interfaz gráfica para mostrar los procesos creados
        actualizar_tabla_procesos()
        
        # Limpia los campos de entrada después de crear el proceso
        nombre_entry.delete(0, "end")
        prioridad_entry.delete(0, "end")

# Función que simula la asignación de procesos a los núcleos de CPU
def simulacion_scheduler():
    global simulacion_en_ejecucion

    while simulacion_en_ejecucion:
        if procesos:
            proceso = random.choice(procesos)

            # Simula la asignación de CPU con una distribución exponencial
            tiempo_ejecucion = int(np.random.exponential(scale=2))  # Ajusta la escala según tu necesidad
            time.sleep(tiempo_ejecucion)

            # Cambia el estado del proceso con las probabilidades especificadas
            nuevo_estado = random.choices(
                ["preparado", "bloqueado", "terminado"],
                weights=[0.9, 0.07, 0.03]
            )[0]

            if nuevo_estado != proceso.estado:
                # Si el estado ha cambiado, registra el evento
                evento = f"Proceso {proceso.nombre} cambió a estado {nuevo_estado}"
                registrar_evento(evento)

            proceso.estado = nuevo_estado

            # Actualiza la interfaz gráfica para reflejar el cambio de estado del proceso
            actualizar_tabla_procesos()
            ventana.update_idletasks()



# Función para actualizar la tabla de procesos en la interfaz gráfica
def actualizar_tabla_procesos():
    # Borrar todos los elementos actuales de la tabla
    for i in tabla_procesos.get_children():
        tabla_procesos.delete(i)

    # Agregar los procesos actualizados a la tabla
    for proceso in procesos:
        tabla_procesos.insert("", "end", values=(proceso.nombre, proceso.prioridad, proceso.estado))

# Función para iniciar la simulación
def iniciar_simulacion():
    global simulacion_en_ejecucion, nucleos

    if not simulacion_en_ejecucion:
        # Obtén la cantidad de núcleos de CPU ingresada por el usuario
        nucleos = int(nucleos_entry.get())

        # Deshabilita los controles relevantes
        nucleos_entry.config(state="disabled")
        nombre_entry.config(state="disabled")
        prioridad_entry.config(state="disabled")
        crear_proceso_button.config(state="disabled")

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

    # Reactiva los controles deshabilitados
    nucleos_entry.config(state="normal")
    nombre_entry.config(state="normal")
    prioridad_entry.config(state="normal")
    crear_proceso_button.config(state="normal")

    # Actualiza la etiqueta de estado de la simulación
    estado_simulacion_label.config(text="Simulación detenida")

def registrar_evento(evento):
    registro_eventos.insert(tk.END, evento + "\n")
    registro_eventos.see(tk.END)  # Desplaza automáticamente al final del registro


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Scheduler")

# Etiqueta y entrada para el nombre del proceso
nombre_label = ttk.Label(ventana, text="Nombre del Proceso:")
nombre_label.pack()
nombre_entry = ttk.Entry(ventana)
nombre_entry.pack()

# Etiqueta y entrada para la prioridad del proceso
prioridad_label = ttk.Label(ventana, text="Prioridad:")
prioridad_label.pack()
prioridad_entry = ttk.Entry(ventana)
prioridad_entry.pack()

# Etiqueta para mostrar mensajes de error
mensaje_error = tk.StringVar()
mensaje_error_label = ttk.Label(ventana, textvariable=mensaje_error, foreground="red")
mensaje_error_label.pack()

# Botón para crear un nuevo proceso
crear_proceso_button = ttk.Button(ventana, text="Crear Proceso", command=crear_proceso)
crear_proceso_button.pack()

# Etiqueta y entrada para la cantidad de núcleos de CPU
nucleos_label = ttk.Label(ventana, text="Núcleos de CPU:")
nucleos_label.pack()
nucleos_entry = ttk.Entry(ventana)
nucleos_entry.pack()

# Botón para iniciar la simulación
iniciar_simulacion_button = ttk.Button(ventana, text="Iniciar Simulación", command=iniciar_simulacion)
iniciar_simulacion_button.pack()


# Botón para detener la simulación
detener_simulacion_button = ttk.Button(ventana, text="Detener Simulación", command=detener_simulacion)
detener_simulacion_button.pack()

# Etiqueta para mostrar el estado de la simulación
estado_simulacion_label = ttk.Label(ventana, text="")
estado_simulacion_label.pack()

# Crear una tabla para mostrar los procesos y sus estados
tabla_procesos = ttk.Treeview(ventana, columns=("Nombre", "Prioridad", "Estado"), show="headings")
tabla_procesos.heading("Nombre", text="Nombre")
tabla_procesos.heading("Prioridad", text="Prioridad")
tabla_procesos.heading("Estado", text="Estado")
tabla_procesos.pack()

# Crear el área de registro de eventos
registro_eventos = ScrolledText(ventana, wrap=tk.WORD, width=40, height=10)
registro_eventos.pack()

# Ejecutar la aplicación
ventana.mainloop()

