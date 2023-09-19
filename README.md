# Simulador de Scheduler

## Descripción General

Este proyecto es un simulador de asignación de procesos a núcleos de CPU desarrollado en Python utilizando las bibliotecas tkinter y matplotlib. El simulador permite configurar la cantidad de núcleos de CPU, crear procesos con nombres, prioridades y asignaciones de núcleo, ejecutar una simulación en la que los procesos cambian de estado y se asignan a los núcleos de CPU de manera aleatoria, y visualizar tablas y gráficos relacionados con la asignación de procesos.

## Requisitos

- Python 3.x
- Biblioteca tkinter (incluida en la biblioteca estándar de Python)
- Biblioteca matplotlib (puede instalarse con `pip install matplotlib`)

## Ejecución

1. Clona o descarga este repositorio a tu máquina local.

2. Abre una terminal o línea de comandos.

3. Navega al directorio donde se encuentra el archivo `schedulerFinal.py`.

4. Ejecuta el siguiente comando para iniciar la aplicación:

```bash
python schedulerFinal.py
```

## Funcionalidades

- **Especificar la Cantidad de Núcleos**: Ingresa la cantidad de núcleos de CPU disponibles para la simulación y haz clic en "Aceptar" para habilitar los campos de entrada de proceso.

- **Crear un Proceso**: Ingresa un nombre y una prioridad para el proceso y haz clic en "Crear Proceso" para crear uno nuevo.

- **Iniciar Simulación**: Una vez que se han creado los procesos, haz clic en "Iniciar Simulación" para comenzar la simulación. Los procesos cambiarán de estado y se asignarán a los núcleos de CPU de manera aleatoria.

- **Detener Simulación**: Puedes detener la simulación en cualquier momento haciendo clic en "Detener Simulación".

- **Mostrar Tablas**: Haz clic en "Mostrar Tablas" para ver tablas que muestran los procesos asignados a cada núcleo de CPU.

- **Mostrar Gráfica**: Haz clic en "Mostrar Gráfica" para generar una gráfica de barras que muestra la distribución de procesos en los núcleos de CPU.




