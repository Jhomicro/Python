import tkinter as tk
import time
import threading
import requests
import matplotlib.pyplot as plt
import datetime
from tkinter.ttk import Combobox  # Asegurarse de importar Combobox desde tkinter.ttk
from tkinter import messagebox

#TODO Api para el uso de Exchangerate API
API_URL = 'da765ae74f6a90e9b4be62d0'

#TODO Guardar el historial
historial = []

#TODO Monedas disponibles
monedas_disponibles = ["USD", "EUR", "GBP", "COP", "JPY", "AUD"]

#TODO Datos para los graficos
tasas=[]
tiempos=[]

#!URL base de api
def obtener_tasa_cambio(moneda_origen, moneda_destino):
    url=f"https://v6.exchangerate-api.com/v6/{API_URL}/latest/{moneda_origen}"

    try:
        response = requests.get(url)
        data = response.json()

        if data['result'] == 'success':
            tasa = data['conversion_rates'].get(moneda_destino)

            if tasa:
                return tasa
            else:
                print(f"No hay tasa de cambio disponible para la moneda {moneda_destino}")
                return None
        else:
            print("Error al obtener los datos")
            return None
    except Exception as e:
        print(f"Error al conectar con la API: {e}")
        return None


#? Función para realizar la conversión
def convertir_multiples_monedas(cantidad, moneda_origen, moneda_destino):
    tasa = obtener_tasa_cambio(moneda_origen, moneda_destino)
    if tasa:
        resultado = cantidad * tasa
        guardar_historial(cantidad, moneda_origen, moneda_destino, resultado)
        return resultado
    else:
        return None
#? Guardar conversiones en el historial
def guardar_historial(cantidad, moneda_origen, moneda_destino, resultado):
    historial.append(f"{cantidad} {moneda_origen} -> {resultado:.2f} {moneda_destino}")

#? Función para mostrar el historial

def mostrar_historial():
    if historial:
        print("Historial de conversiones:")
        for item in historial:
            print(item)
    else:
        print("El historial está vacío")

#? Función para mostrar gráficos de evolucion  de tasas
def mostrar_grafico():
    plt.plot(tiempos, tasas)
    plt.title("Gráfico evolución tasa de cambio")
    plt.xlabel("Tiempo (segundos)")
    plt.ylabel("Evolución tasa de cambio")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#? Función para monitorear y actualizar la tasa de cambio
def monitorear_tasas_periodicamente():
    while True:
        tasa = obtener_tasa_cambio("USD", "COP")
        if tasa:
            tasa_actual = tasa
            tasas.append(tasa_actual)
            tiempos.append(datetime.datetime.now())
            print(f"Tasa de cambio actual: {tasa_actual}")
            time.sleep(60) #!Actualizar el tiempo que se solicita mayos a un minuto

#? Función para ejecutar la actualización en segundo plano
def iniciar_monitoreo():
    threading.Thread(target=monitorear_tasas_periodicamente, daemon=True).start()

#? Función para realizar la conversión desde la interfaz gráfica

def realizar_conversion():
    try:
        cantidad = float(entry_cantidad.get())
        moneda_origen = combo_origen.get()
        moneda_destino = combo_destino.get()
        resultado = convertir_multiples_monedas(cantidad, moneda_origen, moneda_destino)

        if resultado:
            label_resultado.config(text=f"Resultado: {resultado:.2f} {moneda_destino}")
        else:
            label_resultado.config(text="Error al obtener el resultado")
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa una cantidad valida")

#? Función para mostrar el grafico en la gui
def mostrar_grafico_gui():
    mostrar_grafico()

#? Función para mostrar historial en la gui
def mostrar_historial_gui():
    mostrar_historial()

#? Función para mostrar monedas disponibles
def mostrar_monedas_disponibles():
    messagebox.showinfo("Monedas disponibles", " , ".join(monedas_disponibles))

#! Crear la interfaz gráfica
root = tk.Tk()
root.title("Conversor de divisas")
root.background = "#7cddbc"

#! Elementos de interfaz
tk.Label(root, text="Cantidad").grid(row=0, column=0)
entry_cantidad=tk.Entry(root)
entry_cantidad.grid(row = 0 , column= 1)

tk.Label(root, text="Moneda origen").grid(row=2, column=0)
combo_origen = Combobox(root, values=monedas_disponibles)
combo_origen.grid(row = 2, column = 1)
combo_origen.set("USD") #Valor por defecto

tk.Label(root, text="Moneda destino").grid(row=3, column=0)

combo_destino = Combobox(root, values=monedas_disponibles)
combo_destino.grid(row = 3, column = 1)
combo_destino.set("COP") #Valor por defecto

tk.Button(root, text="Convertir", command=realizar_conversion).grid(row=5, column=0, columnspan=2)

label_resultado = tk.Label(root, text="Resultado: ")
label_resultado.grid(row=6, column=0, columnspan=2)

tk.Button(root, text="Monedas disponibles", command=mostrar_monedas_disponibles).grid(row=7, column=0, columnspan=2)

tk.Button(root, text="Ver Historial", command=mostrar_historial_gui).grid(row=8, column=0, columnspan=2)
tk.Button(root, text="Ver Gráfico", command=mostrar_grafico_gui).grid(row=9, column=0, columnspan=2)

#! Iniciar el monitoreo de tasas en segundo plano
iniciar_monitoreo()

#! Ejecutar interfaz grafica
root.mainloop()