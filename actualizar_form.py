import tkinter as tk
from db import ejecutar_sql

def guardar_cliente(txt_nombre, txt_edad, id):
    nombre = txt_nombre.get() # (str)
    edad = int(txt_edad.get())
    sql = f"UPDATE cliente SET nombre='{nombre}', edad={edad} WHERE id = {id}"
    ejecutar_sql(sql)
    #print(sql)
    
def init_actualizar(contenedor_principal, id, nombre, edad):
    limpiar_form(contenedor_principal)
    
    label_nombre = tk.Label(contenedor_principal, text="Nombre")
    label_nombre.pack(pady=10)
    txt_nombre = tk.Entry(contenedor_principal)
    txt_nombre.insert(0, nombre)
    txt_nombre.pack(pady=10)
    
    label_edad = tk.Label(contenedor_principal, text="Edad")
    label_edad.pack(pady=10)
    txt_edad = tk.Entry(contenedor_principal)
    txt_edad.insert(0, edad)
    txt_edad.pack(pady=10)
    
    btn_guardar = tk.Button(
        contenedor_principal, 
        text="Actualizar Cliente",
        command=lambda: guardar_cliente(txt_nombre, txt_edad, id)
    )
    btn_guardar.pack(pady=10)
    
def limpiar_form(contenedor_principal):
    for e in contenedor_principal.winfo_children():
        e.destroy()