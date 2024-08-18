# presupuestos.py

import tkinter as tk
from tkinter import ttk, messagebox
from database import Clientes, Presupuestos, session

def ver_presupuestos(self):
    # Obtener el cliente seleccionado en la tabla
    seleccion = self.clientes_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    
    nombre = self.clientes_tree.item(seleccion)['values'][0]
    abrir_ventana_presupuestos(self, nombre)

def abrir_ventana_presupuestos(self, nombre):
    # Crear una ventana secundaria para ver los presupuestos del cliente
    ventana_presupuestos = tk.Toplevel(self.main_frame)
    ventana_presupuestos.title("Presupuestos de " + nombre)
    ventana_presupuestos.geometry("900x500")

    # Crear un marco para los presupuestos
    frame_presupuestos = tk.Frame(ventana_presupuestos)
    frame_presupuestos.pack(fill='both', expand=True)

    # Crear una tabla para mostrar los presupuestos del cliente
    presupuestos_tree = ttk.Treeview(frame_presupuestos, columns=('ID', 'Fecha', 'Total'), show='headings')
    presupuestos_tree.heading('ID', text='ID')
    presupuestos_tree.heading('Fecha', text='Fecha')
    presupuestos_tree.heading('Total', text='Total')
    presupuestos_tree.column('ID', width=50, anchor='center')
    presupuestos_tree.column('Fecha', width=200, anchor='center')
    presupuestos_tree.column('Total', width=100, anchor='center')
    presupuestos_tree.pack(pady=10, fill='x')

    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    for presupuesto in cliente.presupuestos:
        # Agregar los presupuestos del cliente a la tabla, formateando la fecha y el total como moneda
        presupuestos_tree.insert('', 'end', values=(presupuesto.id, presupuesto.fecha.strftime('%d/%m/%Y %H:%M:%S'), f"${presupuesto.total:,.2f}"))

    # Crear un Treeview vacío para los detalles del presupuesto seleccionado
    detalles_tree = ttk.Treeview(frame_presupuestos, columns=('Producto', 'Cantidad', 'Precio Unitario', 'Descuento', 'Total'), show='headings')
    detalles_tree.heading('Producto', text='Producto')
    detalles_tree.heading('Cantidad', text='Cantidad')
    detalles_tree.heading('Precio Unitario', text='Precio Unitario')
    detalles_tree.heading('Descuento', text='Descuento')
    detalles_tree.heading('Total', text='Total')
    detalles_tree.column('Producto', width=250, anchor='center')
    detalles_tree.column('Cantidad', width=50, anchor='center')
    detalles_tree.column('Precio Unitario', width=150, anchor='center')
    detalles_tree.column('Descuento', width=50, anchor='center')
    detalles_tree.column('Total', width=150, anchor='center')
    detalles_tree.pack(pady=10, fill='x')

    # Vincular el evento de selección del Treeview de presupuestos a la función ver_detalles_presupuesto
    presupuestos_tree.bind('<<TreeviewSelect>>', lambda event: ver_detalles_presupuesto(self, presupuestos_tree, detalles_tree))

def ver_detalles_presupuesto(self, presupuestos_tree, detalles_tree):
    # Obtener el presupuesto seleccionado en la tabla
    seleccion = presupuestos_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un presupuesto.")
        return

    # Obtener el ID del presupuesto seleccionado
    ID = presupuestos_tree.item(seleccion)['values'][0]
    # Llamar a la función mostrar_detalles_presupuesto con el ID del presupuesto y el Treeview de detalles
    mostrar_detalles_presupuesto(self, ID, detalles_tree)

def mostrar_detalles_presupuesto(self, ID, detalles_tree):
    # Limpiar el Treeview de detalles previo
    for item in detalles_tree.get_children():
        detalles_tree.delete(item)

    # Obtener el presupuesto de la base de datos por la ID
    presupuesto = session.query(Presupuestos).filter_by(id=ID).first()
    for detalle in presupuesto.detalles:
        # Agregar los detalles del presupuesto a la tabla de detalles, formateando los montos como moneda (separando miles y con dos decimales)
        detalles_tree.insert('', 'end', values=(detalle.producto, detalle.cantidad, f"${detalle.precio_unitario:,.2f}", detalle.descuento, f"${detalle.total:,.2f}"))