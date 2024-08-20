import tkinter as tk
from tkinter import ttk, messagebox
from database import Clientes, Remitos, session  

def ver_remitos(self):
    # Obtener el cliente seleccionado en la tabla
    seleccion = self.clientes_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    
    nombre = self.clientes_tree.item(seleccion)['values'][0]
    abrir_ventana_remitos(self, nombre)

def abrir_ventana_remitos(self, nombre):
    # Crear una ventana secundaria para ver los remitos del cliente
    ventana_remitos = tk.Toplevel(self.main_frame)
    ventana_remitos.title("Remitos de " + nombre)
    ventana_remitos.geometry("900x500")

    # Crear un marco para los remitos
    frame_remitos = tk.Frame(ventana_remitos)
    frame_remitos.pack(fill='both', expand=True)

    # Crear una tabla para mostrar los remitos del cliente
    remitos_tree = ttk.Treeview(frame_remitos, columns=('ID', 'Fecha', 'Total', 'Pago'), show='headings')
    remitos_tree.heading('ID', text='ID')
    remitos_tree.heading('Fecha', text='Fecha')
    remitos_tree.heading('Total', text='Total')
    remitos_tree.heading('Pago', text='Pago')
    remitos_tree.column('ID', width=30, anchor='center')
    remitos_tree.column('Fecha', width=150, anchor='center')
    remitos_tree.column('Total', width=100, anchor='center')
    remitos_tree.column('Pago', width=100, anchor='center')
    remitos_tree.pack(pady=10, fill='x')

    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    for remito in cliente.remitos:

        # Formatear la fecha sin los decimales de los segundos
        fecha_formateada = remito.fecha.strftime("%d/%m/%Y %H:%M:%S")
        # Insertar en el treeview los valores del remito, formateando el total y el pago como moneda
        if remito.pago != "NO" and remito.pago != "SI":
            pago_formateado = f"${float(remito.pago):,.2f}"
        else:
            pago_formateado = remito.pago
        remitos_tree.insert('', 'end', values=(remito.id, fecha_formateada, f"${remito.total:,.2f}", pago_formateado))

    # Crear un Treeview vacío para los detalles del remito seleccionado
    detalles_tree = ttk.Treeview(frame_remitos, columns=('Producto', 'Cantidad', 'Precio Unitario', 'Total'), show='headings')
    detalles_tree.heading('Producto', text='Producto')
    detalles_tree.heading('Cantidad', text='Cantidad')
    detalles_tree.heading('Precio Unitario', text='Precio Unitario')
    detalles_tree.heading('Total', text='Total')
    detalles_tree.column('Producto', width=250, anchor='center')
    detalles_tree.column('Cantidad', width=50, anchor='center')
    detalles_tree.column('Precio Unitario', width=150, anchor='center')
    detalles_tree.column('Total', width=150, anchor='center')
    detalles_tree.pack(pady=10, fill='x')

    # Vincular el evento de selección del Treeview de remitos a la función ver_detalles_remito
    remitos_tree.bind('<<TreeviewSelect>>', lambda event: ver_detalles_remito(self, remitos_tree, detalles_tree))

def ver_detalles_remito(self, remitos_tree, detalles_tree):
    # Obtener el remito seleccionado en la tabla
    seleccion = remitos_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un remito.")
        return

    # Obtener el ID del remito seleccionado
    ID = remitos_tree.item(seleccion)['values'][0]
    # Llamar a la función mostrar_detalles_remito con el ID del remito y el Treeview de detalles
    mostrar_detalles_remito(self, ID, detalles_tree)

def mostrar_detalles_remito(self, ID, detalles_tree):
    # Limpiar el Treeview de detalles previo
    for item in detalles_tree.get_children():
        detalles_tree.delete(item)

    # Obtener el remito de la base de datos por la ID
    remito = session.query(Remitos).filter_by(id=ID).first()
    for detalle in remito.detalles:
        # Agregar los detalles del remito a la tabla de detalles, formateando los montos como moneda (separando miles y con dos decimales)
        detalles_tree.insert('', 'end', values=(detalle.producto, detalle.cantidad, f"${detalle.precio_unitario:,.2f}", f"${detalle.total:,.2f}"))