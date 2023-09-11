import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import threading
import random
import time

class Proceso:
    def __init__(self, nombre, prioridad):
        self.nombre = nombre
        self.prioridad = prioridad
        self.estado = "activo"

class GestorProcesos:
    def __init__(self):
        self.nucleos = 0
        self.simulacion_en_ejecucion = False
        self.procesos = []

    def validar_prioridad(self, valor):
        try:
            prioridad = int(valor)
            return 1 <= prioridad <= 10
        except ValueError:
            return False

    def crear_proceso(self, nombre, prioridad):
        proceso = Proceso(nombre, prioridad)
        self.procesos.append(proceso)

    def simulacion_scheduler(self):
        while self.simulacion_en_ejecucion:
            if self.procesos:
                proceso = random.choice(self.procesos)
                tiempo_ejecucion = random.randint(1, 5)
                time.sleep(tiempo_ejecucion)
                nuevo_estado = random.choices(
                    ["preparado", "bloqueado", "terminado"],
                    weights=[0.9, 0.07, 0.03]
                )[0]
                proceso.estado = nuevo_estado

class InterfazGrafica:
    def __init__(self, ventana, gestor_procesos):
        self.ventana = ventana
        self.ventana.title("Simulador de Scheduler")
        self.gestor_procesos = gestor_procesos

        self.crear_interfaz()

    def crear_interfaz(self):
        # Etiqueta y entrada para el nombre del proceso
        self.nombre_label = ttk.Label(self.ventana, text="Nombre del Proceso:")
        self.nombre_label.pack()
        self.nombre_entry = ttk.Entry(self.ventana)
        self.nombre_entry.pack()

        # Etiqueta y entrada para la prioridad del proceso
        self.prioridad_label = ttk.Label(self.ventana, text="Prioridad:")
        self.prioridad_label.pack()
        self.prioridad_entry = ttk.Entry(self.ventana)
        self.prioridad_entry.pack()

        # Etiqueta para mostrar mensajes de error
        self.mensaje_error = tk.StringVar()
        self.mensaje_error_label = ttk.Label(self.ventana, textvariable=self.mensaje_error, foreground="red")
        self.mensaje_error_label.pack()

        # Botón para crear un nuevo proceso
        self.crear_proceso_button = ttk.Button(self.ventana, text="Crear Proceso", command=self.crear_proceso)
        self.crear_proceso_button.pack()

        # Etiqueta y entrada para la cantidad de núcleos de CPU
        self.nucleos_label = ttk.Label(self.ventana, text="Núcleos de CPU:")
        self.nucleos_label.pack()
        self.nucleos_entry = ttk.Entry(self.ventana)
        self.nucleos_entry.pack()

        # Botón para iniciar la simulación
        self.iniciar_simulacion_button = ttk.Button(self.ventana, text="Iniciar Simulación", command=self.iniciar_simulacion)
        self.iniciar_simulacion_button.pack()

        # Botón para detener la simulación
        self.detener_simulacion_button = ttk.Button(self.ventana, text="Detener Simulación", command=self.detener_simulacion)
        self.detener_simulacion_button.pack()

        # Etiqueta para mostrar el estado de la simulación
        self.estado_simulacion_label = ttk.Label(self.ventana, text="")
        self.estado_simulacion_label.pack()

        # Crear una tabla para mostrar los procesos y sus estados
        self.tabla_procesos = ttk.Treeview(self.ventana, columns=("Nombre", "Prioridad", "Estado"), show="headings")
        self.tabla_procesos.heading("Nombre", text="Nombre")
        self.tabla_procesos.heading("Prioridad", text="Prioridad")
        self.tabla_procesos.heading("Estado", text="Estado")
        self.tabla_procesos.pack()

        # Crear el área de registro de eventos
        self.registro_eventos = ScrolledText(self.ventana, wrap=tk.WORD, width=40, height=10)
        self.registro_eventos.pack()

    def validar_prioridad(self, valor):
        try:
            prioridad = int(valor)
            return 1 <= prioridad <= 10
        except ValueError:
            return False

    def crear_proceso(self):
        prioridad = self.prioridad_entry.get()
        if self.validar_prioridad(prioridad):
            prioridad = int(prioridad)
            nombre = self.nombre_entry.get()
            self.gestor_procesos.crear_proceso(nombre, prioridad)
            self.actualizar_tabla_procesos()
            self.nombre_entry.delete(0, "end")
            self.prioridad_entry.delete(0, "end")

    def actualizar_tabla_procesos(self):
        for i in self.tabla_procesos.get_children():
            self.tabla_procesos.delete(i)
        for proceso in self.gestor_procesos.procesos:
            self.tabla_procesos.insert("", "end", values=(proceso.nombre, proceso.prioridad, proceso.estado))

    def iniciar_simulacion(self):
        if not self.gestor_procesos.simulacion_en_ejecucion:
            self.gestor_procesos.nucleos = int(self.nucleos_entry.get())
            self.nucleos_entry.config(state="disabled")
            self.nombre_entry.config(state="disabled")
            self.prioridad_entry.config(state="disabled")
            self.estado_simulacion_label.config(text="Simulación en curso")
            for _ in range(self.gestor_procesos.nucleos):
                t = threading.Thread(target=self.gestor_procesos.simulacion_scheduler)
                t.start()
            self.gestor_procesos.simulacion_en_ejecucion = True

    def detener_simulacion(self):
        self.gestor_procesos.simulacion_en_ejecucion = False
        self.nucleos_entry.config(state="normal")
        self.nombre_entry.config(state="normal")
        self.prioridad_entry.config(state="normal")
        self.estado_simulacion_label.config(text="Simulación detenida")

    def registrar_evento(self, evento):
        self.registro_eventos.insert(tk.END, evento + "\n")
        self.registro_eventos.see(tk.END)

if __name__ == "__main__":
    ventana = tk.Tk()
    gestor_procesos = GestorProcesos()
    app = InterfazGrafica(ventana, gestor_procesos)
    ventana.mainloop()
