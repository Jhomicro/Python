import tkinter as tk
import threading
import os
from tkinter import ttk, font, messagebox, filedialog
from seccion.GeneradorQr import GeneradorQr, mostrar_imagen, FORMATO
from seccion.CUnidades import convertir_UNIDADES, UNIDADES
from seccion.CSeguras import contraseña_segura
from seccion.GCodBarras import generar_codigo_barras, EXTENSIONBARRAS, FORMATOBARRAS
from PIL import Image, ImageTk
from seccion.CalcFechaHora import (calcular_fecha_hora,
                                    convertir_zona_horaria,
                                    diferencia_entre_fechas,
                                    calcula_proxima_dia,
                                    calcular_amanecer_atardecer)
from seccion.BusDominios import (
    busqueda_disponibilidad_exhaustiva,
    formatear_resultado,
    informe_dominio,
    verificar_seguridad_dominio,
    monitoreo_expiracion,
)
from seccion.GeneradorFirmasElec import(
    generador_forma_texto,
    generar_pdf_firma
)
from seccion.GeneradorMapa import (
    generar_mapa_calor_basico,
    generar_mapa_calor_geografico,
    cargar_datos_csv,
    cargar_datos_json,
    guardar_configuracion,
    cargar_configuracion
)
import seccion.AdmininArchivos

from pytz import all_timezones, timezone
from datetime import datetime, timedelta
import platform
import locale

# Clase principal de la aplicación
class HerramientasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Herramientas")
        self.root.geometry("900x880+300+0")
        self.historial = []  # Historial compartido
        self.unidades = UNIDADES
        self.formato = FORMATO
        self.extensionBarras = EXTENSIONBARRAS
        self.formatoBarras = FORMATOBARRAS

        # Colores
        self.bgPrincipal = "#1E1E2F"
        self.bgPrimario = "#1F6FEB"
        self.bgSecundario = "#E0245E"
        self.Bordes = "#161B22"
        self.TextoPrincipal = "#C9D1D9"
        self.textoSecundario = "#8B949E"
        self.bgLateral = "#242424"
        self.Acentos = "#2EA043"
        self.Hover = "#58A6FF"

        # Fuentes
        self.titulo_font = font.Font(family="Montserrat", size=22, weight="bold")
        self.texto_font = font.Font(family="Montserrat", size=15)

        # Configuración de la ventana
        self.root.config(bg=self.bgPrincipal)
        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame del menú lateral
        self.menu_frame = tk.Frame(self.root, bg=self.bgLateral, width=200)
        self.menu_frame.pack(side="left" ,fill="y")

        # Área de contenido
        self.content_frame = tk.Frame(self.root, bg=self.bgPrincipal)
        self.content_frame.pack(side="right", fill="both", expand=True)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Botones del menú
        menu_buttons = [
            ("Conversor de unidades", self.mostrar_conversor_unidades),
            ("Generador de códigos QR", self.mostrar_generador_qr),
            ("Generador de contraseñas seguras", self.mostrar_contraseña_segura),
            ("generador de códigos de barras", self.mostrar_diagrama_barras),
            ("calculadora de fecha y hora", self.mostrar_calculadora_fecha_hora),
            ("herramienta de búsqueda de dominios", self.mostrar_busqueda_dominios),
            ("Generador de firma electrónica", self.mostrar_firma_electronica),
            ("Generador de mapas", self.generador_mapa_calor),
            ("Administrador de archivos", self.mostrar_administrado_archivos)
        ]

        for text, command in menu_buttons:
            btn = tk.Button(
                self.menu_frame,
                text=text,
                command=command,
                bg=self.bgSecundario,
                fg=self.TextoPrincipal,
                font=self.texto_font,
                relief="flat",
                height=2
            )
            btn.pack(fill="x", pady=5)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.Hover))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.bgSecundario))

    def limpiar_contenido(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def mostrar_error(self, message):
        messagebox.showerror("Error", message)
    def mostrar_conversor_unidades(self):
        self.limpiar_contenido()

        # Título
        tk.Label(
            self.content_frame,
            text="Conversor de Unidades",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.titulo_font
        ).pack(pady=20)

        # Selección de categoría
        tk.Label(
            self.content_frame,
            text="Categoría:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack()

        categorias = list(self.unidades.keys())
        categoria_seleccionada = tk.StringVar(value=list(self.unidades.keys())[0])
        combobox_categorias = ttk.Combobox(
            self.content_frame,
            values=categorias,
            textvariable=categoria_seleccionada,
            state="readonly",
            font=self.texto_font
        )
        combobox_categorias.pack(pady=5)

        # Selección de unidades
        lbl_unidad_origen = tk.StringVar()
        lbl_unidad_destino = tk.StringVar()

        tk.Label(
            self.content_frame,
            text="Unidad de Origen:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack()
        combo_origen = ttk.Combobox(
            self.content_frame,
            textvariable=lbl_unidad_origen,
            state="readonly",
            font=self.texto_font
        )
        combo_origen.pack(pady=5)

        tk.Label(
            self.content_frame,
            text="Unidad de Destino:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack()
        combo_destino = ttk.Combobox(
            self.content_frame,
            textvariable=lbl_unidad_destino,
            state="readonly",
            font=self.texto_font
        )
        combo_destino.pack(pady=5)

        # Entrada de cantidad
        tk.Label(
            self.content_frame,
            text="Cantidad:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack()
        entry_cantidad = tk.Entry(
            self.content_frame,
            font=self.texto_font,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal
        )
        entry_cantidad.pack(pady=5)

        # Resultado
        lbl_resultado = tk.Label(
            self.content_frame,
            text="Resultado: ",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        lbl_resultado.pack(pady=10)

        def actualizar_unidades(*args):
            categoria = categoria_seleccionada.get()
            opciones = list(self.unidades.get(categoria, {}).keys())
            combo_origen["values"] = opciones
            combo_destino["values"] = opciones
            if opciones:
                lbl_unidad_origen.set(opciones[0])
                lbl_unidad_destino.set(opciones[0])

        def convertir():
            try:
                cantidad = float(entry_cantidad.get())
                origen = lbl_unidad_origen.get()
                destino = lbl_unidad_destino.get()
                categoria = categoria_seleccionada.get()
                resultado = convertir_UNIDADES(cantidad, origen, destino, categoria)

                if resultado.is_integer():
                    lbl_resultado.config(text= f"Resultado {int(resultado)}")
                else:
                    lbl_resultado.config(text= f"Resultado {resultado:.6f}")

            except ValueError as e:
                self.mostrar_error(str(e))

        combobox_categorias.bind("<<ComboboxSelected>>", actualizar_unidades)
        actualizar_unidades()

        tk.Button(
            self.content_frame,
            text="Convertir",
            command=convertir,
            bg=self.Acentos,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=10)

    #Generador de QR
    def mostrar_generador_qr(self):
        self.limpiar_contenido()

        tk.Label(
            self.content_frame,
            text="Generador de Códigos QR",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.titulo_font
        ).pack(pady=20)

        tk.Label(
            self.content_frame,
            text="Introduce el texto para generar el código QR:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack()

        entry_texto = tk.Entry(
            self.content_frame,
            font=self.texto_font,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal
        )
        entry_texto.pack(pady=5)

        tk.Label(
            self.content_frame,
            text= "Seleccione el tipo de formato:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack()

        formatos = list(self.formato)
        formatos_seleccionado = tk.StringVar(value=formatos[0])

        combobox_formato = ttk.Combobox(
            self.content_frame,
            values=formatos,
            textvariable=formatos_seleccionado,
            state="readonly",
            font=self.texto_font
        )
        combobox_formato.pack(pady=5)

        #Espacio para la vista previa del QR
        lbl_vista_previa = tk.Label(
            self.content_frame,
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        lbl_vista_previa.pack(pady=10)

        def generar_qr():
            texto = entry_texto.get()
            if texto:
                formato = formatos_seleccionado.get()
                resultado = GeneradorQr(texto, formato = formato)
                if "Codigo generado correctamente" in resultado:
                    #Ruta del archivo generado
                    archivo_generado = resultado.split(":")[1].strip()

                    #Mostrar la imagen generada
                    try:
                        img= Image.open(archivo_generado)
                        img_tk= mostrar_imagen(img)
                        lbl_vista_previa.config(image=img_tk)
                        lbl_vista_previa.image = img_tk
                    except Exception as e:
                        self.mostrar_error(str(e))
                messagebox.showinfo("QR Generado", f"QR generado con éxito: {resultado}")
                self.historial.append(texto)
            else:
                messagebox.showwarning("Advertencia", "Introduce un texto válido.")

        tk.Button(
            self.content_frame,
            text="Generar QR",
            command=generar_qr,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=10)

    #Generador de contraseñas seguras
    def mostrar_contraseña_segura(self):
        self.limpiar_contenido()

        self.vars = []
        self.estados=[]

        #Etiqueta principal
        tk.Label(
            self.content_frame,
            text="Contraseñas Seguras",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.titulo_font
            ).pack(pady=20)

        tk.Label(
            self.content_frame,
            text="Nombre del archivo:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack()

        self.entry_nombre_archivo = tk.Entry(
            self.content_frame,
            font=self.texto_font,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal
        )
        self.entry_nombre_archivo.pack(pady=5)

        #Entrada de logitud
        tk.Label(
            self.content_frame,
            text="Introduce la longitud de la contraseña:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack()

        self.entry_longitud = tk.Entry(
            self.content_frame,
            font=self.texto_font,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal
            )
        self.entry_longitud.pack(pady=5)

        #Etiqueta de opciones
        tk.Label(
            self.content_frame,
            text="Seleccione las caracteristicas deseadas:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack()

        #Crear un diccionario para asociar las opciones con sus estados
        self.opciones_vars = {
            "incluir_minusculas": tk.BooleanVar(value=False),
            "incluir_mayusculas": tk.BooleanVar(value=False),
            "incluir_numeros": tk.BooleanVar(value=False),
            "incluir_simbolos": tk.BooleanVar(value=False)
        }

        # Crear los checkbuttons y asociarlos con los variables booleanas
        for opcion,var in self.opciones_vars.items():
            texto= opcion.replace("_", " ").capitalize()
            check = tk.Checkbutton(
                self.content_frame,
                text=texto,
                compound="left",
                bg=self.bgPrincipal,
                fg=self.TextoPrincipal,
                font=self.texto_font,
                variable=var
                )
            check.pack(anchor="w", pady=10, padx=10)
            self.vars.append(var)

        #Generar contraseña
        tk.Button(
            self.content_frame,
            text="Generar Contraseña",
            command=self.generar_contrasena,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)


    def generar_contrasena(self):
        try:
            longitud = int(self.entry_longitud.get())
            nombre = self.entry_nombre_archivo.get()
            if longitud > 0:
                # Obtener las opciones seleccionadas
                opciones = {opcion: var.get() for opcion, var in self.opciones_vars.items()}
                print("Opciones seleccionadas: ", opciones)
                # Crear la contraseña
                contrasena = contraseña_segura(longitud,
                                                incluir_minusculas=opciones["incluir_minusculas"],
                                                incluir_mayusculas=opciones["incluir_mayusculas"],
                                                incluir_numeros=opciones["incluir_numeros"],
                                                incluir_simbolos=opciones["incluir_simbolos"],
                                                nombre=nombre)
                messagebox.showinfo("Contraseña Generada", f"Contraseña generada: {contrasena}")
            else:
                messagebox.showwarning("Advertencia", "Introduce una longitud válida.")
        except ValueError as e:
            self.mostrar_error(str(e))

    # Crear diagrama de barras
    def mostrar_diagrama_barras(self):
        self.limpiar_contenido()

        self.datos=[]
        self.historial=[]

        # Etiqueta principal
        tk.Label(
            self.content_frame,
            text="Diagrama de Barras",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.titulo_font
            ).pack(pady=20)

        tk.Label(
            self.content_frame,
            text="Ingrese el nombre de la carpeta:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack()

        self.entry_nombre_carpeta = tk.Entry(
            self.content_frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
        )
        self.entry_nombre_carpeta.pack(pady=5)

        tk.Label(
            self.content_frame,
            text="Ingresa el nombre del archivo:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack()

        self.entry_nombre_archivo = tk.Entry(
            self.content_frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            )
        self.entry_nombre_archivo.pack(pady=5)

        tk.Label(
            self.content_frame,
            text="Ingresa los datos separados por comas:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            ).pack()

        self.entry_datos = tk.Entry(
            self.content_frame,
            font=self.texto_font,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            )
        self.entry_datos.pack(pady=5)

        # Formato

        tk.Label(
            self.content_frame,
            text="Seleccione la extensión deseado:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack()

        extension_Barras = list(self.extensionBarras)
        extensiones_Barras_seleccionado = tk.StringVar(value=extension_Barras[1])

        combobox_extension_formatobarras = ttk.Combobox(
            self.content_frame,
            values=extension_Barras,
            textvariable=extensiones_Barras_seleccionado,
            state="readonly",
            font=self.texto_font
        )
        combobox_extension_formatobarras.pack(pady=5)

        tk.Label(
            self.content_frame,
            text="Ingrese el formato deseado",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack()

        formato_barras = list(self.formatoBarras)
        formato_barras_seleccionado = tk.StringVar(value=formato_barras[0])

        combobox_formato_formatobarras = ttk.Combobox(
            self.content_frame,
            values=formato_barras,
            textvariable=formato_barras_seleccionado,
            state="readonly",
            font=self.texto_font
        )
        combobox_formato_formatobarras.pack(pady=5)

        def generar_diagrama_barras():
            texto = self.entry_datos.get()
            nombre_archivo = self.entry_nombre_archivo.get()
            nombre_carpeta = self.entry_nombre_carpeta.get()
            extension = extensiones_Barras_seleccionado.get()
            formato = formato_barras_seleccionado.get()
            if texto and nombre_archivo:

                try:
                    generar_codigo_barras(texto = texto,
                                        formato = formato,
                                        carpeta_salida = nombre_carpeta,
                                        nombre_archivo=nombre_archivo,
                                        extension=extension)
                    messagebox.showinfo("Diagrama Generado", f"Diagrama generado en {nombre_carpeta}/{nombre_archivo}.{extension}")
                except ValueError as e:
                    self.mostrar_error(str(e))
            else:
                messagebox.showwarning("Advertencia", "Por favor, llene todos los campos.")

        tk.Button(
            self.content_frame,
            text="Generar Diagrama",
            command=generar_diagrama_barras,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=20)

    #Calculadora de fecha y hora
    def mostrar_calculadora_fecha_hora(self):
        self.limpiar_contenido()

        #Etiqueta principal
        tk.Label(
            self.content_frame,
            text="Calculadora de Fecha y Hora",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.titulo_font
            ).pack(pady=20)

        #Etiquetas de ayuda
        tk.Label(
            self.content_frame,
            text="Fecha base (YYYY-MM-DD HH:MM:SS):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        self.label_hora_local = tk.Label(
            self.content_frame,
            text="Hora local: ",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.label_hora_local.pack(pady=1)

        self.label_fecha_local=tk.Label(
            self.content_frame,
            text="Fecha local: ",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.label_fecha_local.pack(pady=1)

        self.mostrar_fecha_local()

        #Crear notebook
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(expand=1, fill="both", pady=10)

        #Crear frames para cada tab
        tab_calcular_fecha_hora=tk.Frame(self.notebook, bg=self.bgPrincipal, )
        tab_zona_horaria= tk.Frame(self.notebook, bg=self.bgPrincipal, )
        tab_calcular_diferencia = tk.Frame(self.notebook, bg=self.bgPrincipal, )
        tab_proxima_dia = tk.Frame(self.notebook, bg=self.bgPrincipal, )
        tab_amanecer_atardecer = tk.Frame(self.notebook, bg=self.bgPrincipal, )

        #Añadir los frames al notebook
        self.notebook.add(tab_calcular_fecha_hora, text="Calcular Fecha y Hora")
        self.notebook.add(tab_zona_horaria, text="Zona Horaria")
        self.notebook.add(tab_calcular_diferencia, text="Diferencia entre Fechas")
        self.notebook.add(tab_proxima_dia, text="Próximo Día")
        self.notebook.add(tab_amanecer_atardecer, text="Amanecer y Atardecer")

        #!----------------Contenido tap 1 : Calcular Fecha y Hora----------------

        #Entrada de fecha base
        tk.Label(
            tab_calcular_fecha_hora,
            text="Ingresa la fecha base",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            ).pack()

        #Campo de entrada de fecha base
        self.entry_fecha_base = tk.Entry(
            tab_calcular_fecha_hora,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_fecha_base.pack()

        #Etiqueta de tiempo en días
        tk.Label(
            tab_calcular_fecha_hora,
            text="Tiempo en días:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de tiempo en días
        self.entry_tiempo_dias = tk.Entry(
            tab_calcular_fecha_hora,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_tiempo_dias.pack()

        #Etiqueta de tiempo en horas
        tk.Label(
            tab_calcular_fecha_hora,
            text="Tiempo en horas:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de tiempo en horas
        self.entry_tiempo_horas = tk.Entry(
            tab_calcular_fecha_hora,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_tiempo_horas.pack()

        #Etiqueta de tiempo en minutos
        tk.Label(
            tab_calcular_fecha_hora,
            text="Tiempo en minutos:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de tiempo en minutos
        self.entry_tiempo_minutos = tk.Entry(
            tab_calcular_fecha_hora,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_tiempo_minutos.pack()

        #Botón para calcular la nueva fecha
        self.button_calcular_diferencia = tk.Button(
                tab_calcular_fecha_hora,
                text="Calcular Diferencia",
                command=self.calcular_nueva_fecha,
                bg=self.bgPrimario,
                fg=self.TextoPrincipal,
                font=self.texto_font
            ).pack(pady=10)

        #resultado en calcular la fecha y hora
        self.label_resultado = tk.Label(
            tab_calcular_fecha_hora,
            text="Fecha calculada: ",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.label_resultado.pack(pady=20)

        #!----------------Contenido tap 2 : Zona Horaria----------------

        #Etiquetas de ayuda
        tk.Label(
            tab_zona_horaria,
            text="Fecha y hora (YYYY-MM-DD HH:MM:SS):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de zona horaria
        self.entry_zona_horaria = tk.Entry(
            tab_zona_horaria,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_zona_horaria.pack()

        #Etiqueta de zona horaria origen
        tk.Label(
            tab_zona_horaria,
            text="Zona Horaria de Origen:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        #Menú de selección de zona horaria origen
        self.combo_zona_origen = ttk.Combobox(
            tab_zona_horaria,
            values=all_timezones,
            width=30,
            font=self.texto_font
        )
        self.combo_zona_origen.pack(pady=10)

        #Etiqueta de zona horaria destino
        tk.Label(
            tab_zona_horaria,
            text="Zona Horaria de Destino:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        #Menú de selección de zona horaria destino
        self.combo_zona_destino = ttk.Combobox(
            tab_zona_horaria,
            values=all_timezones,
            width=30,
            font=self.texto_font
        )
        self.combo_zona_destino.pack(pady=10)

        #Botón para convertir zona horaria
        self.button_convertir_zona = tk.Button(
            tab_zona_horaria,
            text="Convertir Zona Horaria",
            command=self.convertir_zona,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.button_convertir_zona.pack(pady=10)

        #Resultado de la conversión
        self.label_zona_convertida = tk.Label(
            tab_zona_horaria,
            text="",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.label_zona_convertida.pack(pady=20)

        #!----------------Contenido tap 3 : Diferencia entre Fechas----------------
        #Etiquetas de ayuda
        tk.Label(
            tab_calcular_diferencia,
            text="Fecha inicio (YYYY-MM-DD HH:MM:SS):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de fecha inicio
        self.entry_fecha_inicio = tk.Entry(
            tab_calcular_diferencia,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_fecha_inicio.pack()
        #Etiquetas de ayuda para la fecha objetivo
        tk.Label(
            tab_calcular_diferencia,
            text="Fecha objetivo (YYYY-MM-DD HH:MM:SS):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de fecha fin
        self.entry_fecha_objetivo = tk.Entry(
            tab_calcular_diferencia,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_fecha_objetivo.pack()

        #Etiqueta para la unidad
        tk.Label(
            tab_calcular_diferencia,
            text="Unidad de diferencia (días, horas, minutos, segundos):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Menú de selección de unidad
        self.unidad_var = tk.StringVar()
        self.unidad_var.set("segundos") #Valor por defecto
        self.combo_unidad = ttk.Combobox(
            tab_calcular_diferencia,
            textvariable=self.unidad_var,
            values=["días", "horas", "minutos", "segundos"],
            width=30,
            state="readonly",
            font=self.texto_font
            )
        self.combo_unidad.pack(pady=10)

        #Botón para calcular la diferencia
        self.button_calcular_diferencia = tk.Button(
            tab_calcular_diferencia,
            text="Calcular Diferencia",
            command=self.calcular_diferencia,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.button_calcular_diferencia.pack(pady=10)

        #Resultado de la diferencia
        self.label_resultado_diferencia = tk.Label(
            tab_calcular_diferencia,
            text="La diferencia es  ",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.label_resultado_diferencia.pack(pady=20)

        #!----------------Contenido tap 4 : Próximo Día----------------

        #Etiquetas de ayuda
        tk.Label(
            tab_proxima_dia,
            text="Fecha de inicio (YYYY-MM-DD HH:MM:SS):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de fecha
        self.entry_fecha_proximo_dia = tk.Entry(
            tab_proxima_dia,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_fecha_proximo_dia.pack()

        #Etiqueta para el día objetivo
        tk.Label(
            tab_proxima_dia,
            text="Día objetivo:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        #Menú de selección de día objetivo
        self.combo_dia_objetivo = ttk.Combobox(
            tab_proxima_dia,
            values=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sábado", "Domingo"],
            font=self.texto_font
        )
        self.combo_dia_objetivo.pack(pady=10)

        #Botón para calcular proximo día
        self.button_calcular_proximo_dia = tk.Button(
            tab_proxima_dia,
            text="Calcular Próximo Día",
            command=self.calcular_proximo_dia,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.button_calcular_proximo_dia.pack(pady=10)
        #Resultado de la nueva fecha
        self.label_resultado_proximo_dia = tk.Label(
            tab_proxima_dia,
            text="Proximo día es: ",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.label_resultado_proximo_dia.pack(pady=20)

        #!----------------Contenido tap 5 : Amanecer y Atardecer----------------
        #Etiquetas de ayuda
        tk.Label(
            tab_amanecer_atardecer,
            text="Fecha (YYYY-MM-DD):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)
        #Campo de entrada de fecha
        self.entry_amanecer_atardecer = tk.Entry(
            tab_amanecer_atardecer,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_amanecer_atardecer.pack()
        #Etiqueta de ayuda para la latitud
        tk.Label(
            tab_amanecer_atardecer,
            text="Latitud (Ej. 40.7128):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10
        )
        #Campo de entrada de latitud
        self.entry_lat = tk.Entry(
            tab_amanecer_atardecer,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_lat.pack()
        #Etiqueta de ayuda para la longitud
        tk.Label(
            tab_amanecer_atardecer,
            text="Longitud (Ej. -74.0060):",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10
        )
        #Campo de entrada de longitud
        self.entry_lon = tk.Entry(
            tab_amanecer_atardecer,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_lon.pack()
        #Boton para calcular amanecer y atardecer
        self.button_calcular_amanecer_atardecer = tk.Button(
            tab_amanecer_atardecer,
            text="Calcular Amanecer y Atardecer",
            command=self.calcular_amanecer_atardecer,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.button_calcular_amanecer_atardecer.pack(pady=10)
        #Resultado de amanecer y atardecer
        self.label_resultado_amanecer_atardecer = tk.Label(
            tab_amanecer_atardecer,
            text="Amanecer y Atardecer: ",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.label_resultado_amanecer_atardecer.pack(pady=20)

    def mostrar_fecha_local(self):
        #Obtener la hora y fecha local
        hora_local = datetime.now().strftime("%I:%M:%S %p")
        fecha_local = datetime.now().strftime("%d-%m-%Y")
        #Actualizar el label con la fecha y hora
        self.label_hora_local.config(text = f"Hora local: {hora_local}")
        self.label_fecha_local.config(text = f"Fecha local: {fecha_local}")
        #Actualizar cada segundo
        self.content_frame.after(1000, self.mostrar_fecha_local)

    def calcular_nueva_fecha(self):
        fecha_base = self.entry_fecha_base.get()
        try:
            tiempo_dias = int(self.entry_tiempo_dias.get())
            tiempo_horas = int(self.entry_tiempo_horas.get())
            tiempo_minutos = int(self.entry_tiempo_minutos.get())
            nueva_fecha = calcular_fecha_hora(fecha_inicio_str= fecha_base, dias= tiempo_dias, horas=tiempo_horas, minutos= tiempo_minutos)
            self.label_resultado.config(text = f"Fecha calculada: {nueva_fecha.strftime('%Y-%m-%d %H:%M:%S')}")
        except ValueError as e:
            self.mostrar_error(str(e))

    def convertir_zona(self):
        fecha_hora_str = self.entry_zona_horaria.get()
        zona_horaria_origen = self.combo_zona_origen.get()
        zona_horaria_destino = self.combo_zona_destino.get()

        try:
            fecha_hora = datetime.strptime(fecha_hora_str, "%Y-%m-%d %H:%M:%S")
            fecha_convertida = convertir_zona_horaria(fecha_hora= fecha_hora, zona_origen= zona_horaria_origen, zona_destino= zona_horaria_destino)
            self.label_zona_convertida.config(text = f"Fecha y hora convertida: {fecha_convertida.strftime('%Y-%m-%d %H:%M:%S')}")
        except Exception as e:
            self.mostrar_error(str(e))

    def calcular_diferencia(self):
        #Calcular los valores de entrada
        fecha_inicio = self.entry_fecha_inicio.get()
        fecha_fin = self.entry_fecha_objetivo.get()
        unidad_tiempo = self.unidad_var.get()

        try:
            #Llamar a la función para calcular la diferencia
            diferencia = diferencia_entre_fechas(fecha_inicio_str=fecha_inicio, dia_objetivo = fecha_fin, unidad= unidad_tiempo)
            self.label_resultado_diferencia.config(text = f"La diferencia es {diferencia} {unidad_tiempo}")
        except Exception as e:
            self.mostrar_error(str(e))

    def calcular_proximo_dia(self):
        fecha_proximo = self.entry_fecha_proximo_dia.get()
        try:

            sistema = platform.system().lower()

            if sistema == "windows":
                locale.setlocale(locale.LC_TIME, "Spanish" or "spanish_america")
            else:
                locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

            dia_objetivo_str = self.combo_dia_objetivo.get()
            dias = {
                "Lunes": 0,
                "Martes": 1,
                "Miercoles": 2,
                "Jueves": 3,
                "Viernes": 4,
                "Sábado": 5,
                "Domingo": 6
            }
            dia_objetivo = dias[dia_objetivo_str] #Obtener el valor correspodiente del diccionario

            proxima_fecha = calcula_proxima_dia(fecha_inicio_str=fecha_proximo, dia_objetivo=dia_objetivo)
            proximo_dia_nombre = proxima_fecha.strftime('%A')
            self.label_resultado_proximo_dia.config(
                text = f"Proximo día es: {proxima_fecha.strftime('%Y-%m-%d')} ({proximo_dia_nombre})")
        except Exception as e:
            self.mostrar_error(str(e))
        except Exception as e:
            self.mostrar_error(str(e))

    def calcular_amanecer_atardecer(self):
        fecha_str = self.entry_amanecer_atardecer.get()
        lat = float(self.entry_lat.get())
        lon = float(self.entry_lon.get())

        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            amanecer, atardecer = calcular_amanecer_atardecer(fecha=fecha, lat=lat, lon=lon)
            self.label_resultado_amanecer_atardecer.config(text = f"Amanecer: {amanecer.strftime('%H:%M:%S')}\nAtardecer: {atardecer.strftime('%H:%M:%S')}")
        except Exception as e:
            self.mostrar_error(str(e))

    # ----------------- SECCIÓN MOSTRAR DOMINIOS-------------------!

    """
    busqueda_disponibilidad_exhaustiva,
    buscar_MultitLD,
    sugerir_dominios_alternativos,
    informe_dominio,
    verificar_seguridad_dominio,
    consulta_masiva,
    generar_reporte_personalizado,
    """
    def mostrar_busqueda_dominios(self):
        self.limpiar_contenido()

        #Etiqueta principal
        tk.Label(
            self.content_frame,
            text="Búsqueda de Dominios",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=20)

        #Crear Notebook
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(expand=1, fill="both", pady=10)

        # Crear frames para cada tab
        self.tab_busqueda_dominio = tk.Frame(self.notebook, bg=self.bgPrincipal)
        self.tab_verificacion_seguridad = tk.Frame(self.notebook, bg=self.bgPrincipal)
        self.tab_monitoreo_seguridad = tk.Frame(self.notebook, bg=self.bgPrincipal)
        self.tab_informe_detallado = tk.Frame(self.notebook, bg=self.bgPrincipal)

        #Añadir los frames al notebooks
        self.notebook.add(self.tab_busqueda_dominio, text="Busqueda de dominio")
        self.notebook.add(self.tab_verificacion_seguridad, text="Verificación de Seguridad")
        self.notebook.add(self.tab_monitoreo_seguridad, text="Monitoreo de Expiración")
        self.notebook.add(self.tab_informe_detallado, text="Informe Detallado")

        #! -------------Contenido tap 1: Busuqeda de dominio---------------
        #Etiqueta de ayuda
        tk.Label(
            self.tab_busqueda_dominio,
            text="Introduce el dominio a buscar:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        self.entry_dominio= tk.Entry(
            self.tab_busqueda_dominio,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_dominio.pack()

        #Spiner de carga
        self.spiner_dominio = ttk.Progressbar(
            self.tab_busqueda_dominio,
            mode="indeterminate",
            length=200
        )

        #Botón para buscar el dominio
        self.boton_busqueda_dominio = tk.Button(
            self.tab_busqueda_dominio,
            command=self.iniciar_busqueda_dominio,
            text="Buscar",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
        )
        self.boton_busqueda_dominio.pack(pady=10)

        self.resultado_text = tk.Text(
            self.tab_busqueda_dominio,
            wrap="word",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            height=10,
        )
        self.resultado_text.pack( fill="both", expand=True)

        #! -------------Contenido tap 2: Verificación de Seguridad--------------
        #Etiqueta de ayuda
        tk.Label(
            self.tab_verificacion_seguridad,
            text="Introduce el dominio a verificar:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        self.entry_dominio_seguridad= tk.Entry(
            self.tab_verificacion_seguridad,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_dominio_seguridad.pack()

        #Botón para verificar la seguridad del dominio
        self.boton_verificacion_seguridad = tk.Button(
            self.tab_verificacion_seguridad,
            text="Verificar",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.iniciar_verificacion_seguridad
        )
        self.boton_verificacion_seguridad.pack(pady=10)

        #! --------------- Contenido tab 3: Monitoreo de expiración
        #Etiqueta de ayuda
        tk.Label(
            self.tab_monitoreo_seguridad,
            text="Introduce el dominio a monitorear:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        #Campo de entrada de monitoreo de expiración
        self.entry_dominio_monitoreo= tk.Entry(
            self.tab_monitoreo_seguridad,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_dominio_monitoreo.pack()

        #Botton de monitoreo de expiración
        self.boton_monitoreo_seguridad = tk.Button(
            self.tab_monitoreo_seguridad,
            text="Iniciar monitoreo",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.iniciar_monitoreo
        )
        self.boton_monitoreo_seguridad.pack(pady=10)

        #! --------------- Contenido tab 4: Informe Detallado--------------
        #Etiqueta de ayuda
        tk.Label(
            self.tab_informe_detallado,
            text="Generar informe detallado de un dominio:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        #Campo de entrada de informe detallado
        self.entry_dominio_informe_detallado= tk.Entry(
            self.tab_informe_detallado,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_dominio_informe_detallado.pack()

        # Botón para generar informe detallado
        self.boton_informe_detallado = tk.Button(
            self.tab_informe_detallado,
            text="Generar informe",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.generar_informe
        )
        self.boton_informe_detallado.pack(pady=10)

    #Metodos Funcionales

    def iniciar_busqueda_dominio(self):
        dominio = self.entry_dominio.get()
        if not dominio:
            self.mostrar_resultado("Debes introducir un dominio")
            return

        #Mostrar el spinner
        self.spiner_dominio.pack(pady=10)
        self.spiner_dominio.start()
        self.mostrar_resultado("Buscando dominio...")

        #Ejecutar la busqueda en un hilo separado
        hilo = threading.Thread(target=self.buscar_dominio, args=(dominio,))
        hilo.start()
    def buscar_dominio(self, dominio):
        try:
            resultado = busqueda_disponibilidad_exhaustiva(dominio=dominio)
            # Actualiza el resultado en la gui (Usar 'after' para evitar problemas con hilos)
            self.content_frame.after(0, self.actualizar_resultado_dominio, resultado)
        except Exception as e:
            self.content_frame.after(0, self.actualizar_resultado_dominio,f"Error: {str(e)}")

    def iniciar_verificacion_seguridad(self):
        dominio = self.entry_dominio_seguridad.get()
        if not dominio:
            self.mostrar_resultado("Debes introducir un dominio")
            return
        resultado = verificar_seguridad_dominio(dominio)
        self.mostrar_resultado(resultado)
    def iniciar_monitoreo(self):
        dominio = self.entry_dominio_monitoreo.get()
        if not dominio:
            self.mostrar_resultado("Debes introducir un dominio")
            return
        resultado = monitoreo_expiracion(dominio)
        self.mostrar_resultado(resultado)
    def generar_informe(self):
        dominio= self.entry_dominio_informe_detallado.get()
        if not dominio:
            self.mostrar_resultado("Debes introducir un dominio")
            return
        resultado = informe_dominio(dominio)
        self.mostrar_resultado(resultado)
    def mostrar_resultado(self, resultado):
        #Limpia el cuadro de texto y agregar el nuevo resultado
        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, resultado)

        self.resultado_text.delete(1.0, tk.END)
        self.resultado_text.insert(tk.END, str(resultado))
    def actualizar_resultado_dominio(self, resultado):
        #Detener el spiner
        self.spiner_dominio.stop()
        self.spiner_dominio.pack_forget()

        # Formatear y mostrar resultado
        texto_formateado = formatear_resultado(resultado)
        self.mostrar_resultado(texto_formateado)

    #----------------Mostrar firma electronica-------------!
    def mostrar_firma_electronica(self):
        # Mostrar la firma electrónica
        self.limpiar_contenido()
        #Titulo principal
        tk.Label(
            self.content_frame,
            text="Firma electrónica",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=10)

        #Etiquetas y entrada de nombre
        tk.Label(
            self.content_frame,
            text="Nombre y Apellido:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=5)
        self.entry_nombre_firma_electronica = tk.Entry(
            self.content_frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_nombre_firma_electronica.pack(pady=5)

        #Etiqueta y entrada de cargo
        tk.Label(
            self.content_frame,
            text="Cargo a la firma:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=5)
        self.entry_cargo_firma_electronica = tk.Entry(
            self.content_frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_cargo_firma_electronica.pack(pady=5)

        #Etiqueta de nombre del archivo
        tk.Label(
            self.content_frame,
            text="Nombre del archivo:",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            ).pack(pady=5)
        self.entry_archivo_firma_electronica = tk.Entry(
            self.content_frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.entry_archivo_firma_electronica.pack(pady=5)
        #Etiqueta de respuesta
        self.resultado_label = tk.Label(
            self.content_frame,
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
            )
        self.resultado_label.pack(pady=5)

        #Botón para generar la firma PNG
        self.boton_generar_firma = tk.Button(
            self.content_frame,
            text="Generar firma PNG",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.generar_firma_png
            )
        self.boton_generar_firma.pack(pady=10)
        #Botón para generar pdf
        self.boton_generar_pdf = tk.Button(
            self.content_frame,
            text="Generar PDF",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.generar_firma_pdf
            )
        self.boton_generar_pdf.pack(pady=10)
    def obtener_archivo_con_extension(self, archivo, extension_requerida):
        if not archivo.lower().startswith(extension_requerida):
            archivo+=extension_requerida
            return archivo
    def generar_firma_png (self):
        nombre_firma= self.entry_nombre_firma_electronica.get()
        cargo= self.entry_cargo_firma_electronica.get()
        archivo= self.entry_archivo_firma_electronica.get()

        if nombre_firma and cargo and archivo:
            archivo_con_extension= self.obtener_archivo_con_extension(archivo, ".png")
            #Generar la firma en PNG
            try:
                generador_forma_texto(nombre_firma,cargo,archivo_con_extension)
            except Exception as e:
                self.resultado_label.config(text=f"Error al generar la firma: {str(e)}")
        else:
            self.resultado_label.config(text="Debes introducir nombre de firma, cargo y archivo")
    def generar_firma_pdf(self):
        # Generar la firma en PDF
        nombre_fima = self.entry_nombre_firma_electronica.get()
        cargo = self.entry_cargo_firma_electronica.get()
        archivo = self.entry_archivo_firma_electronica.get()
        archivo_con_extension= self.obtener_archivo_con_extension(archivo, ".pdf")

        if nombre_fima and cargo and archivo:
            try:
                generar_pdf_firma(nombre_fima, cargo, archivo_con_extension)
            except Exception as e:
                self.resultado_label.config(text=f"Error al generar la firma: {str(e)}")
        else:
            self.resultado_label.config(text="Debes introducir nombre de firma, cargo y archivo")
    # Crear notebooks dinamicos
    def generar_notebook(self, tabs):
        """
        Crear notebook dinamico con tabs
        """
        self.notebook = ttk.Notebook(self.content_frame)
        self.notebook.pack(expand=1, fill="both", pady=5)

        # Crear frames dinamicamente
        self.tabs={}
        for tab_name in tabs:
            frame = tk.Frame(self.notebook, bg=self.bgPrincipal)
            self.notebook.add(frame, text=tab_name)
            self.tabs[tab_name] = frame
    # Función para mostrar los tab generados
    def mostrar_tab(self, tab_name):
        """
        Muestra un todos los tabs creados
        :Param tab_name: Nombre del tab al que se quiere añadir contenido.
        """
        if tab_name in self.tabs:
            tab_index = list(self.tabs.keys()).index(tab_name)
            self.notebook.select(tab_index)
        else:
            print(f"El tab '{tab_name}' no existe")
    # Añadir contenido al tab
    def añadir_contenido_a_tab(self, tab_name, configurar_funcion):
        """
        Añade contenido a un tab
        @param tab_name: Nombre del tab
        @param configurar_tab: Función que recibe el frame del tab para configurarlo
        """
        if tab_name in self.tabs:
            frame = self.tabs[tab_name]
            configurar_funcion(frame)
        else:
            print(f"El tab {tab_name} no existe")

    #----------------Pestaña de Generar mapa de calor-------------!
    def generador_mapa_calor(self):
        # Limpiar contenido
        self.limpiar_contenido()
        #Crear tabs
        tabs=["Mapa Basico", "Mapa Geográfico"]
        self.generar_notebook(tabs)
        
        # Añadir contenido a los tabs
        self.añadir_contenido_a_tab("Mapa Basico", self.configurar_tab_mapa_basico)
        self.añadir_contenido_a_tab("Mapa Geográfico", self.configurar_tab_mapa_geografico)

    def configurar_tab_mapa_basico(self, frame):
        """
        Configurar el contenido del tab mapa basico
        """
        tk.Label(
            frame,
            text="Mapa de calor basico",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=10)
        #Nombre del archivo
        tk.Label(
            frame,
            text="Nombre del archivo",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=5)
        self.entry_nombre_archivo = tk.Entry(
            frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
        )
        self.entry_nombre_archivo.pack(pady=5)
        # Campo para el archivo CSV
        tk.Label(
            frame,
            text="Archivo de datos CSV",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=5)
        tk.Button(
            frame,
            text="Seleccionar archivo",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.datos_cargados_csv
        ).pack(pady=5)

        #Campo para paleta de colores
        tk.Label(
            frame,
            text="Paleta de colores",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=5)
        self.entry_paleta_colores = tk.Entry(
            frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
        )
        self.entry_paleta_colores.pack(pady=5)
        tk.Button(
            frame,
            text="Generar mapa de calor",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.generador_mapa_basico_datos
        ).pack(pady=5)
        self.resultado_label_mapa = tk.Label(
            frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.resultado_label_mapa.pack(pady=5)

    def configurar_tab_mapa_geografico(self, frame):
        """
        Configura el contenido del tab de mapa geografico
        """
        #Titulo
        tk.Label(
            frame,
            text="Mapa de calor de calor geográfico",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=10)
        #Nombre del archivo
        tk.Label(
            frame,
            text="Nombre del archivo",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=5)
        self.entry_nombre_archivo_geografico = tk.Entry(
            frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
        )
        self.entry_nombre_archivo_geografico.pack(pady=5)
        #Archivo de datos csv
        tk.Label(
            frame,
            text="Archivo de datos CSV",
            bg=self.bgPrincipal,
            fg=self.TextoPrincipal,
            font=self.texto_font
        ).pack(pady=10)
        tk.Button(
            frame,
            text="Seleccionar archivo",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.datos_cargados_csv
        ).pack(pady=5)
        tk.Button(
            frame,
            text="Generar mapa de calor",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.generar_mapa_geografico
        ).pack(pady=10)
        self.resultado_label_mapa_geografico = tk.Label(
            frame,
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font
        )
        self.resultado_label_mapa_geografico.pack(pady=5)

    def generador_mapa_basico_datos(self):
        archivo = self.entry_nombre_archivo.get()
        paleta_colores=self.entry_paleta_colores.get()
        if not hasattr(self, 'datos_csv'):
            self.resultado_label_mapa.config(text="Error: No se han cargado datos csv")
            return
        if not archivo:
            self.resultado_label_mapa.config(text="Error: Ingrese un nombre de archivo de salida")
            return
        if not paleta_colores:
            paleta_colores = "viridis"
        try:
            #Generar el mapa de calor
            resultado = generar_mapa_calor_basico(datos= self.datos_csv.values, nombre_archivo=archivo, paleta= paleta_colores)
            self.resultado_label_mapa.config(text=resultado)
        except Exception as e:
            self.resultado_label_mapa.config(text=f"Error al generar el mapa: {str(e)}")
    def datos_cargados_csv(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
        if archivo:
            try:
                self.datos_csv = cargar_datos_csv(archivo)
                messagebox.showinfo("Exito","Datos cargados correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar los datos de CSV: {str(e)}")
        else:
            self.resultado_label_mapa.config(text="Error: No se ha seleccionado un archivo CSV")
    def generar_mapa_geografico(self):
        archivo = self.entry_nombre_archivo_geografico.get()
        if not hasattr(self, "datos_csv"):
            messagebox.showerror("Error", " Error: No se ha cargado correctamente los datos")
            return
        if not archivo:
            messagebox.showerror("Error", "Error: Ingrese un nombre de archivo de salida")
            return
        if not archivo:
            archivo = "Mapa de calor.html"
        try:
            coordenadas = list(zip(self.datos_csv["Latitud"], self.datos_csv["Longitud"]))
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el mapa geográfico: {str(e)}")
        #LLamar a la función
        try:
            resultado = generar_mapa_calor_geografico(coordenadas, archivo)
            messagebox.showinfo("Exito", f"Mapa generado correctamente en {archivo}")
            self.resultado_label_mapa_geografico.config(resultado)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el mapa geográfico: {str(e)}")
    
    #---------------------- Mostrar administrador de archivos-------------------
    def mostrar_administrado_archivos(self):
        self.limpiar_contenido()
        #Crear el arbol de directorios
        self.tree = ttk.Treeview(self.content_frame)
        self.tree.heading("#0", text="Directorio y archivos", anchor="w")
        self.tree.pack(fill="both", expand=True)
        #Barra de desplazamiento
        self.scrollbar = ttk.Scrollbar(
            self.content_frame,
            orient="vertical",
            command=self.tree.yview
            )
        self.scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        #Crear botones de acción
        self.boton_crear_archivo = tk.Button(
            self.content_frame,
            text="Crear archivo",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.crear_archivo
        )
        self.boton_crear_archivo.pack(padx=5, pady=5, side="top")

        self.boton_eliminar= tk.Button(
            self.content_frame,
            text="Eliminar archivo",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.eliminar_archivo
        )
        self.boton_eliminar.pack(padx=5, pady=5, side="top")

        self.boton_copiar = tk.Button(
            self.content_frame,
            text="Copiar archivo",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.copiar_archivo
        )
        self.boton_copiar.pack(padx=5, pady=5, side="top")

        self.boton_mover = tk.Button(
            self.content_frame,
            text="Mover archivo",
            bg=self.bgPrimario,
            fg=self.TextoPrincipal,
            font=self.texto_font,
            command=self.mover_archivo
        )
        # LLenar el arbol inicial con el directorio actual
        self.directorio_actual= os.getcwd()
        self.listar_directorio(self.directorio_actual)
        # Bind para detectar clic en los nodos
        self.tree.bind("<ButtonRelease-1>", self.on_tree_item_select)

    def on_tree_item_select(self, event):
        item = self.tree.selection()
        if item:
            ruta = self.tree.item(item[0], "text")
            if os.path.isdir(ruta):  # Solo carga directorios
                self.listar_directorio(ruta)
        else:
            self.abrir_archivo(ruta)
    #Funciones de uso
    def listar_directorio(self, ruta):
        self.tree.delete(*self.tree.get_children()) # Limpiar el arbol
        nodo_raiz=self.tree.insert("", "end", text=ruta, open=True)
        for root, dirs, files in seccion.AdmininArchivos.listar_archivos(ruta):
            if root == ruta:
                parent_id=nodo_raiz
            else:
                parent_id=self.tree.insert(nodo_raiz, "end", text=root, open=False)
            # Insertar directorios como nodos hijos
            for directorio in dirs:
                self.tree.insert(parent_id, "end", text=directorio, open=False)
            for archivo in files:
                self.tree.insert(parent_id, "end", text=archivo, open=False)

    def abrir_archivo(self, ruta):
    # Verifica que el archivo sea un archivo de texto
        if os.path.exists(ruta):
            if ruta.endswith(".txt"):
                # Crear una nueva ventana para mostrar el contenido del archivo
                ventana_archivo = tk.Toplevel(self.content_frame)
                ventana_archivo.title(f"Abrir archivo: {ruta}")
                # Crea un widget Text para mostrar el contenido
                text_widget = tk.Text(ventana_archivo, wrap="word", height=20, width=50)
                text_widget.pack(expand=True, fill="both")
                # Leer el contenido del archivo
                try:
                    with open(ruta, 'r') as archivo:
                        contenido = archivo.read()
                        text_widget.insert(tk.END, contenido)
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo abrir el archivo: {str(e)}")
            else:
                messagebox.showwarning("Archivo no soportado", "Solo se pueden abrir archivos de texto.")
        else:
            messagebox.showerror("Error", "El archivo no existe.")
    def crear_archivo(self):
        ruta = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")], title="Crear archivo")
        if ruta:
            seccion.AdmininArchivos.crear_archivo(ruta)
            messagebox.showinfo("Exito", f"Archivo creado: {ruta}")
            self.listar_directorio(self.directorio_actual)
    def eliminar_archivo(self):
        item_seleccionado=self.tree.focus()
        if item_seleccionado:
            ruta = self.tree.item(item_seleccionado, "text")
            try:
                seccion.AdmininArchivos.eliminar_archivo(ruta)
                messagebox.showinfo("Exito", f"Archivo eliminado: {ruta}")
                self.listar_directorio(self.directorio_actual)
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar el archivo: {str(e)}")
        else:
            messagebox.showerror("Error", "No se ha seleccionado un archivo")
    def copiar_archivo(self):
        ruta_origen = filedialog.askopenfilename(title="Seleccionar archivo a copiar")
        ruta_destino = filedialog.asksaveasfilename(title="Seleccionar carpeta de destino")
        if ruta_origen and ruta_destino:
            try:
                seccion.AdmininArchivos.copiar_archivo(ruta_origen, ruta_destino)
                messagebox.showinfo("Exito", f"Archivo copiado: {ruta_origen} a {ruta_destino}")
                self.listar_directorio(self.directorio_actual)
            except Exception as e:
                messagebox.showerror("Error", f"Error al copiar el archivo: {str(e)}")
        else:
            messagebox.showerror("Error", "No se ha seleccionado un archivo o carpeta")
    def mover_archivo(self):
        ruta_origen= filedialog.askopenfilename(title="Seleccionar archivo a mover")
        ruta_destino= filedialog.askopenfilename(title="Seleccionar directorio de destino")
        if ruta_origen and ruta_destino:
            try:
                seccion.AdmininArchivos.mover_archivo(ruta_origen, ruta_destino)
                messagebox.showinfo("Exito", f"Archivo movido: {ruta_origen} a {ruta_destino}")
                self.listar_directorio(self.directorio_actual)
            except Exception as e:
                messagebox.showerror("Error", f"Error al mover el archivo: {str(e)}")
        else:
            messagebox.showerror("Error", "No se ha seleccionado un archivo o directorio")

# Programa principal
if __name__ == "__main__":
    root = tk.Tk()
    app = HerramientasApp(root)
    root.mainloop()
