import tkinter as tk
from tkinter import ttk, messagebox
from database import Clientes, Presupuestos, DetallesPresupuestos, session

ventana_presupuestos = None

def ver_presupuestos(self, carrito):
    # Obtener el cliente seleccionado en la tabla
    seleccion = self.clientes_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    
    nombre = self.clientes_tree.item(seleccion)['values'][0]
    self.ventana_presupuestos = abrir_ventana_presupuestos(self, nombre, carrito)

def abrir_ventana_presupuestos(self, nombre, carrito):
    global ventana_presupuestos
    
    # Si la ventana de remitos ya está abierta, destruir la ventana actual y crear una nueva
    if ventana_presupuestos and ventana_presupuestos.winfo_exists():
        ventana_presupuestos.destroy()

    # Crear una ventana secundaria para ver los presupuestos del cliente
    ventana_presupuestos = tk.Toplevel()
    ventana_presupuestos.title("Presupuestos de " + nombre)
    ventana_presupuestos.geometry("900x550")

    # Crear un marco para los presupuestos
    frame_presupuestos = tk.Frame(ventana_presupuestos)
    frame_presupuestos.pack(fill='both', expand=True)

    # Crear un marco para la tabla de presupuestos y su scrollbar
    frame_presupuestos_tree = tk.Frame(frame_presupuestos)
    frame_presupuestos_tree.pack(fill='x', pady=10)

    # Crear una tabla para mostrar los presupuestos del cliente
    presupuestos_tree = ttk.Treeview(frame_presupuestos_tree, columns=('ID', 'Fecha', 'Total'), show='headings')
    presupuestos_tree.heading('ID', text='ID')
    presupuestos_tree.heading('Fecha', text='Fecha')
    presupuestos_tree.heading('Total', text='Total')
    presupuestos_tree.column('ID', width=180, anchor='center')
    presupuestos_tree.column('Fecha', width=300, anchor='center')
    presupuestos_tree.column('Total', width=400, anchor='center')
    presupuestos_tree.pack(side='left', fill='x')

    # Scrollbar para la tabla de presupuestos
    scrollbar_presupuestos = ttk.Scrollbar(frame_presupuestos_tree, orient=tk.VERTICAL, command=presupuestos_tree.yview)
    presupuestos_tree.configure(yscroll=scrollbar_presupuestos.set)
    scrollbar_presupuestos.pack(side='right', fill='y')

    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    for presupuesto in cliente.presupuestos:
        # Agregar los presupuestos del cliente a la tabla, formateando la fecha y el total como moneda
        presupuestos_tree.insert('', 'end', values=(presupuesto.id, presupuesto.fecha.strftime('%d/%m/%Y %H:%M:%S'), f"${presupuesto.total:,.2f}"))

    # Botón para eliminar el presupuesto seleccionado
    delete_presupuesto_button = ttk.Button(frame_presupuestos, text="Eliminar Presupuesto", command=lambda: eliminar_presupuesto(self, presupuestos_tree, nombre))
    # Posicionar el botón al centro del marco
    delete_presupuesto_button.pack(pady=10)

    # Botón para llevar el presupuesto al carrito
    add_to_cart_button = ttk.Button(frame_presupuestos, text="Agregar al Carrito", command=lambda: agregar_presupuesto(self, presupuestos_tree, nombre, carrito))
    # Posicionar el botón al centro del marco
    add_to_cart_button.pack(pady=10)

    # Crear un marco para la tabla de detalles y su scrollbar
    frame_detalles_tree = tk.Frame(frame_presupuestos)
    frame_detalles_tree.pack(fill='x', pady=10)

    # Crear un Treeview vacío para los detalles del presupuesto seleccionado
    detalles_tree = ttk.Treeview(frame_detalles_tree, columns=('Producto', 'Cantidad', 'Precio Unitario', 'Descuento', 'Total'), show='headings')
    detalles_tree.heading('Producto', text='Producto')
    detalles_tree.heading('Cantidad', text='Cantidad')
    detalles_tree.heading('Precio Unitario', text='Precio Unitario')
    detalles_tree.heading('Descuento', text='Descuento')
    detalles_tree.heading('Total', text='Total')
    detalles_tree.column('Producto', width=250, anchor='center')
    detalles_tree.column('Cantidad', width=100, anchor='center')
    detalles_tree.column('Precio Unitario', width=250, anchor='center')
    detalles_tree.column('Descuento', width=100, anchor='center')
    detalles_tree.column('Total', width=180, anchor='center')
    detalles_tree.pack(side='left', fill='x')

    # Scrollbar para la tabla de detalles
    scrollbar_detalles = ttk.Scrollbar(frame_detalles_tree, orient=tk.VERTICAL, command=detalles_tree.yview)
    detalles_tree.configure(yscroll=scrollbar_detalles.set)
    scrollbar_detalles.pack(side='right', fill='y')

    # Vincular el evento de selección del Treeview de presupuestos a la función ver_detalles_presupuesto
    presupuestos_tree.bind('<<TreeviewSelect>>', lambda event: ver_detalles_presupuesto(self, presupuestos_tree, detalles_tree))

    return ventana_presupuestos

def ver_detalles_presupuesto(self, presupuestos_tree, detalles_tree):
    # Obtener el presupuesto seleccionado en la tabla
    seleccion = presupuestos_tree.selection()
    # Si no se seleccionó ningún presupuesto, limpiar el Treeview de detalles
    if not seleccion:
        for item in detalles_tree.get_children():
            detalles_tree.delete(item)
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

def eliminar_presupuesto(self, presupuestos_tree, nombre):
    # Obtener el presupuesto seleccionado en la tabla
    seleccion = presupuestos_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un presupuesto.", parent=self.ventana_presupuestos)
        return

    # Obtener el ID del presupuesto seleccionado
    ID = presupuestos_tree.item(seleccion)['values'][0]

    # Mostrar un mensaje de confirmación para eliminar el presupuesto
    confirmacion = messagebox.askyesno(f"Eliminar Presupuesto", f"¿Estás seguro de eliminar el presupuesto {ID} de {nombre}?", parent=self.ventana_presupuestos)
    # Si el usuario no confirma, salir de la función
    if not confirmacion:
        return
    # Borrar los detalles del presupuesto
    session.query(DetallesPresupuestos).filter_by(id_presupuesto=ID).delete()
    # Buscar el presupuesto en la base de datos por la ID
    presupuesto = session.query(Presupuestos).filter_by(id=ID).first()
    # Eliminar el presupuesto de la sesión
    session.delete(presupuesto)
    # Confirmar la transacción
    session.commit()
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Presupuesto eliminado exitosamente.", parent=self.ventana_presupuestos)
    # Limpiar el Treeview de presupuestos
    for item in presupuestos_tree.get_children():
        presupuestos_tree.delete(item)
    # Volver a cargar los presupuestos del cliente
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    for presupuesto in cliente.presupuestos:
        presupuestos_tree.insert('', 'end', values=(presupuesto.id, presupuesto.fecha.strftime('%d/%m/%Y %H:%M:%S'), f"${presupuesto.total:,.2f}"))

def agregar_presupuesto(self, presupuestos_tree, nombre, carrito):
    # Obtener el presupuesto seleccionado en la tabla
    seleccion = presupuestos_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un presupuesto.", parent=self.ventana_presupuestos)
        return

    # Obtener el ID del presupuesto seleccionado
    ID = presupuestos_tree.item(seleccion)['values'][0]

    # Mostrar un mensaje de confirmación para agregar el presupuesto al carrito
    confirmacion = messagebox.askyesno(f"Agregar al Carrito", f"¿Estás seguro de agregar el presupuesto {ID} de {nombre} al carrito?", parent=self.ventana_presupuestos)
    # Si el usuario no confirma, salir de la función
    if not confirmacion:
        return

    # Obtener el presupuesto de la base de datos por la ID
    presupuesto = session.query(Presupuestos).filter_by(id=ID).first()

    # Limpiar el carrito antes de insertar los detalles del presupuesto
    carrito.clear()

    # Iterar sobre los detalles del presupuesto para agregarlos al carrito
    for detalle in presupuesto.detalles:
        carrito.append((detalle.producto, detalle.cantidad, f"{detalle.descuento}%", f"${detalle.precio_unitario:,.2f}"))
    
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Presupuesto agregado al carrito exitosamente.", parent=self.ventana_presupuestos)
