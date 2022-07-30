# Para Importar todas las clases de Tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox # Importar de cuadros de alerta

import os # Directorio y cosas del sistema
from subprocess import run # Ejecutar comandos de terminal

import time # Importar libreria para fecha
import datetime # Importar libreria para fecha avanzada


root = Tk() # Crear la variable ventana
root.title("Programar apagado") # Título de la ventana
root.iconbitmap(os.path.dirname(__file__)+"\datos\logo.ico") # Mostrar icono
root.config(bg="black", pady=10, padx=20) # Poner fondo negro
root.resizable(False, False) # No permite cambiar el alto y ancho

# Posicionar en el centro de la pantalla
AnchoVentana = 400 # Ancho ventana
AltoVentana = 250 # Alto ventana
PosX = root.winfo_screenwidth() // 2 - AnchoVentana // 2 # Calcular posición horizontal
PosY = root.winfo_screenheight() // 2 - AltoVentana # Calcular posición vertical

root.geometry(str(AnchoVentana)+ "x" +str(AltoVentana)+ "+" +str(PosX)+ "+" +str(PosY)) # Tamaño de ventana y posición inicial


# Funciones-------------------------------------------------------------------


def Activar():
    global CuentaRegresiva, Final # Acceder a variables globales

    # Si el tiempo designado es mayor que 0
    if int(TxInputHora.get())+int(TxInputMin.get()) > 0:
        # Tiempo en minutos
        CuentaFinal=int(TxInputHora.get())*60+int(TxInputMin.get())

        # Fecha actual
        FechaActual=datetime.datetime.fromtimestamp(time.mktime(time.strptime(time.strftime("%Y/%m/%d", time.localtime()), "%Y/%m/%d"))) # Fecha
        HoraActual=time.localtime()[3]*60*60+time.localtime()[4]*60+time.localtime()[5] # Horas, Minutos y Segundo (En segundos)

        # Si es "A las"
        if SelectorBox.current() == 0:
            # Sumar 24 horas si la hora es anterior a la de ahora
            if HoraActual/60 > CuentaFinal: CuentaFinal+=1440
            # Sumar al día de hoy la hora a la que termina
            Final = FechaActual + datetime.timedelta(minutes=CuentaFinal)

        # Si es "Dentro de" Sumar a la fecha la hora actual y a la que termina
        else: Final = FechaActual + datetime.timedelta(minutes=CuentaFinal, seconds=HoraActual)

        CuentaRegresiva=True # Modificar estado
        
        BtnActivar.grid_forget() # Ocultar
        BtnDesactivar.grid(row="3", column="0", sticky="nswe", padx=75) # Mostrar

    else: messagebox.showerror(title="Error", message="No se ha espesificado el tiempo")


def Desactivar():
    global CuentaRegresiva # Acceder a variable global
    CuentaRegresiva=False # Modificar estado

    root.title("Programar apagado") # Cambiar título de la ventana
    Info.set("") # Info

    BtnDesactivar.grid_forget() # Ocultar
    BtnActivar.grid(row="3", column="0", sticky="nswe", padx=75) # Mostrar


# Comprobar contenido del input de horas
def SeeInputHora(event):
    # Comprueba que se pueda convertir en número, si no se puede cambiar valor a 0 para la hora
    try: int(TxInputHora.get())
    except ValueError: TxInputHora.set(0)
    
    # Si el numero es menor que 0
    if int(TxInputHora.get()) < 0: TxInputHora.set(0)

# Comprobar contenido del input de Minutos
def SeeInputMin(event):
    # Comprueba que se pueda convertir en número, si no se puede cambiar valor a 0 para los minutos
    try: int(TxInputMin.get())
    except ValueError: TxInputMin.set(0)

    # Si el numero es menor que 0
    if int(TxInputMin.get()) < 0: TxInputMin.set(0)


# Funciones-------------------------------------------------------------------
# Contenido-------------------------------------------------------------------


# Definir variables
CuentaRegresiva=False # Activar apagado
Final=None # Fecha en la que debe terminar

# 1 Fila -----------------------
# Frame
HoraNoti=Frame(root, bg="black", width=200, height=150) # Declarar y configurar
HoraNoti.grid(row="0", column="0",  sticky="nswe") # Mostrar
# Texto
Hora=StringVar(value="00:00")
text_1A=Label(HoraNoti, textvariable=Hora, bg="black", fg="white", font=("Roboto", 23, "bold")) # Declarar y configurar

text_1A.grid(row="0", column="0",  sticky="nswe") # Mostrar
# Texto
Info=StringVar()
text_1B=Label(HoraNoti, textvariable=Info, bg="black", fg="#999999", font=("Roboto", 13)) # Declarar y configurar
text_1B.grid(row="1", column="0",  sticky="nswe") # Mostrar

# 2 Fila -----------------------
# Frame
Form=LabelFrame(root, text="Programar para apagar", font=("Roboto", 11, "bold"), width=200, bg="black", fg="white", labelanchor='n', pady=15) # Declarar y configurar
Form.grid(row="1", column="0",  sticky="nswe", pady=20, padx=20) # Mostrar

# Selector
SelectorBox=ttk.Combobox(Form, state="readonly", values=["A las", "Dentro de"], font=("Roboto", 11)) # Declarar y configurar
SelectorBox.current(0) # Definir opción predeterminada
SelectorBox.grid(row="0", column="0", sticky="nsw", padx=15) # Mostrar

# Frame Inputs
FrameInputs=Frame(Form, bg="white") # Declarar y configurar
FrameInputs.grid(row="0", column="1", sticky="nswe", padx=15) # Mostrar
# Hora
TxInputHora=StringVar(value="0")
InputHora=Entry(FrameInputs, textvariable=TxInputHora, bg="white", font=("Roboto", 11), width=3, justify='center') # Declarar y configurar
InputHora.grid(row="0", column="0", sticky="nsw") # Mostrar
# Texto
text_2A=Label(FrameInputs, text=":", font=("Roboto", 11, "bold")) # Declarar y configurar
text_2A.grid(row="0", column="1", sticky="nswe") # Mostrar
# Minutos
TxInputMin=StringVar(value="0")
InputMin=Entry(FrameInputs, textvariable=TxInputMin, bg="white", font=("Roboto", 11), width=3, justify='center') # Declarar y configurar
InputMin.grid(row="0", column="2", sticky="nse") # Mostrar

# 3 Fila -----------------------
# Botón Desactivar
BtnDesactivar=Button(root, text="Cancelar", font=("Roboto", 11, "bold"), pady=5, padx=5, bg="black", fg="red", command=Desactivar) # Declarar y configurar
# Botón Activar
BtnActivar=Button(root, text="Programar", font=("Roboto", 11, "bold"), pady=5, padx=5, bg="black", fg="white", command=Activar) # Declarar y configurar
BtnActivar.grid(row="3", column="0", sticky="nswe", padx=75) # Mostrar


# Configuración de columnas
root.columnconfigure(0, weight=True)
HoraNoti.columnconfigure(0, weight=True)


# Contenido-------------------------------------------------------------------
# Funciones al iniciarse------------------------------------------------------


# Actualizar hora
def times():
    Hora.set(time.strftime("%H:%M:%S")) # Info

    # Si está activada la cuenta atrás
    if CuentaRegresiva:
        Ahora=datetime.datetime.fromtimestamp(time.mktime(time.localtime())) # Fecha y hora actual

        root.title("Se apagará en "+str(Final - Ahora)) # Cambiar título de la ventana

        # Si es para el mismo día
        if time.strftime('%Y-%m-%d', time.localtime(Ahora.timestamp())) == time.strftime('%Y-%m-%d', time.localtime(Final.timestamp())):
            Info.set("Programado para apagarse a las "+str(time.strftime('%H:%M', time.localtime(Final.timestamp())))) # Info
        # Si es para el día siguiente
        else: Info.set("Programado para apagarse el "+str(time.strftime('%d %B, %H:%M', time.localtime(Final.timestamp())))) # Info
        
        # El tiempo actual ha llegado al mismo o mayor que la cuenta final
        if Ahora >= Final:
            run("shutdown -s -t 0") # Apagar equipo
            Desactivar()
    
    text_1A.after(500,times) # Llamar dentro de 500 milisegundos
times()


# Eventos
# Dejar el foco
InputHora.bind('<FocusOut>', SeeInputHora) # Input Hora
InputMin.bind('<FocusOut>', SeeInputMin) # Input Minutos

# Lanzar función de desactivar
def OFF(event): Desactivar()
# Dejar el foco
InputHora.bind('<KeyRelease>', OFF) # Input Hora
InputMin.bind('<KeyRelease>', OFF) # Input Minutos
# Soltar clic del raton
SelectorBox.bind('<Button>', OFF) # Selector

# Lanzar función de activar
def ON(event): Activar()
# Al soltar enter
root.bind('<KeyRelease-Return>', ON) # Ventana


# Funciones al iniciarse------------------------------------------------------


root.mainloop() # Abrir ventana