import tkinter as tk
from tkinter import ttk, messagebox
from database import Clientes, Remitos, DetallesRemitos, session  

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
    remitos_tree = ttk.Treeview(frame_remitos, columns=('ID', 'Fecha', 'Fecha Pago', 'Total', 'Pago'), show='headings')
    remitos_tree.heading('ID', text='ID')
    remitos_tree.heading('Fecha', text='Fecha')
    remitos_tree.heading('Fecha Pago', text='Fecha Pago')
    remitos_tree.heading('Total', text='Total')
    remitos_tree.heading('Pago', text='Pago')
    remitos_tree.column('ID', width=30, anchor='center')
    remitos_tree.column('Fecha', width=150, anchor='center')
    remitos_tree.column('Fecha Pago', width=150, anchor='center')
    remitos_tree.column('Total', width=100, anchor='center')
    remitos_tree.column('Pago', width=100, anchor='center')
    remitos_tree.pack(pady=10, fill='x')

    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    for remito in cliente.remitos:
        # Formatear la fecha sin los decimales de los segundos
        fecha_formateada = remito.fecha.strftime("%d/%m/%Y %H:%M:%S")
        fecha_pago_formateada = remito.fecha_pago.strftime("%d/%m/%Y %H:%M:%S")
        # Insertar en el treeview los valores del remito, formateando el total y el pago como moneda
        if remito.pago != "NO" and remito.pago != "SI":
            pago_formateado = f"${float(remito.pago):,.2f}"
        else:
            pago_formateado = remito.pago
        remitos_tree.insert('', 'end', values=(remito.id, fecha_formateada, fecha_pago_formateada, f"${remito.total:,.2f}", pago_formateado))
    
    # Botón para eliminar remitos
    eliminar_remito_button = ttk.Button(frame_remitos, text="Eliminar Remito", command=lambda: eliminar_remito(self, remitos_tree, ventana_remitos))
    eliminar_remito_button.pack(pady=10)

    # Botón para modificar remitos
    modificar_remito_button = ttk.Button(frame_remitos, text="Modificar Remito", command=lambda: modificar_remito(self, remitos_tree))
    modificar_remito_button.pack(pady=10)

    # Crear un Treeview vacío para los detalles del remito seleccionado
    detalles_tree = ttk.Treeview(frame_remitos, columns=('Producto', 'Cantidad', 'Precio Unitario', 'Descuento', 'Total'), show='headings')
    detalles_tree.heading('Producto', text='Producto')
    detalles_tree.heading('Cantidad', text='Cantidad')
    detalles_tree.heading('Precio Unitario', text='Precio Unitario')
    detalles_tree.heading('Descuento', text='Descuento')
    detalles_tree.heading('Total', text='Total')
    detalles_tree.column('Producto', width=250, anchor='center')
    detalles_tree.column('Cantidad', width=50, anchor='center')
    detalles_tree.column('Precio Unitario', width=150, anchor='center')
    detalles_tree.column('Descuento', width=100, anchor='center')
    detalles_tree.column('Total', width=150, anchor='center')
    detalles_tree.pack(pady=10, fill='x')

    # Vincular el evento de selección del Treeview de remitos a la función ver_detalles_remito
    remitos_tree.bind('<<TreeviewSelect>>', lambda event: ver_detalles_remito(self, remitos_tree, detalles_tree))

def ver_detalles_remito(self, remitos_tree, detalles_tree):
    # Obtener el remito seleccionado en la tabla
    seleccion = remitos_tree.selection()
    if not seleccion:
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
        detalles_tree.insert('', 'end', values=(detalle.producto, detalle.cantidad, f"${detalle.precio_unitario:,.2f}", detalle.descuento, f"${detalle.total:,.2f}"))

def eliminar_remito(self, remitos_tree, ventana_remitos):
    # Obtener el remito seleccionado en la tabla
    seleccion = remitos_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un remito.", parent=ventana_remitos)
        return

    # Obtener el ID del remito seleccionado
    ID = remitos_tree.item(seleccion)['values'][0]
    # Buscar el remito en la base de datos por la ID
    remito = session.query(Remitos).filter_by(id=ID).first()
    # Preguntar al usuario si está seguro de eliminar el remito
    confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar el remito {ID}?", parent=ventana_remitos)
    if not confirmacion:
        return
    
    # Obtener el nombre del cliente del remito eliminado
    nombre_cliente = remito.cliente.nombre
    
    # Eliminar los detalles del remito
    session.query(DetallesRemitos).filter_by(id_remito=ID).delete()

    # Eliminar el remito
    session.query(Remitos).filter_by(id=ID).delete()

    # Confirmar la transacción
    session.commit()

    actualizar_remitos(self, remitos_tree, nombre_cliente)

    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Remito eliminado exitosamente.", parent=ventana_remitos)

def modificar_remito(self, remitos_tree):
    # Obtener el remito seleccionado en la tabla
    seleccion = remitos_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un remito.")
        return

    # Obtener el ID del remito seleccionado
    ID = remitos_tree.item(seleccion)['values'][0]
    # Llamar a la función abrir_ventana_modificacion_remito con el ID del remito seleccionado
    abrir_ventana_modificacion_remito(self, ID)

def abrir_ventana_modificacion_remito(self, ID):
    # Crear una ventana secundaria para modificar el remito
    ventana_mod_remito = tk.Toplevel(self.main_frame)
    ventana_mod_remito.title("Modificar Remito")
    ventana_mod_remito.geometry("300x200")

    # Crear etiquetas y campos de entrada para los datos del remito
    ttk.Label(ventana_mod_remito, text="Fecha:").grid(row=0, column=0, padx=5, pady=5)
    # Obtener la fecha del remito seleccionado
    fecha = session.query(Remitos).filter_by(id=ID).first().fecha
    # Formatear la fecha como string
    fecha_str = fecha.strftime("%d/%m/%Y %H:%M:%S")
    # Crear un campo de entrada con la fecha del remito seleccionado
    fecha_var = tk.StringVar(value=fecha_str)
    ttk.Entry(ventana_mod_remito, textvariable=fecha_var).grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(ventana_mod_remito, text="Total:").grid(row=1, column=0, padx=5, pady=5)
    # Obtener el total del remito seleccionado
    total = session.query(Remitos).filter_by(id=ID).first().total
    # Formatear el total como string
    total_str = f"{total:.2f}"
    # Crear un campo de entrada con el total del remito seleccionado
    total_var = tk.StringVar(value=total_str)
    ttk.Entry(ventana_mod_remito, textvariable=total_var).grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(ventana_mod_remito, text="Pago:").grid(row=2, column=0, padx=5, pady=5)
    # Obtener el pago del remito seleccionado
    pago = session.query(Remitos).filter_by(id=ID).first().pago
    # Crear un campo de entrada con el pago del remito seleccionado
    pago_var = tk.StringVar(value=pago)
    ttk.Entry(ventana_mod_remito, textvariable=pago_var).grid(row=2, column=1, padx=5, pady=5)

    # Botón para guardar los cambios
    ttk.Button(ventana_mod_remito, text="Guardar Cambios", 
               # Llamar a la función guardar_cambios_remito con el ID del remito seleccionado y la ventana secundaria
               command=lambda: guardar_cambios_remito(ID, fecha_var.get(), total_var.get(), pago_var.get(), ventana_mod_remito)).grid(row=3, column=1, pady=10)
    
def guardar_cambios_remito(ID, nueva_fecha, nuevo_total, nuevo_pago, ventana_mod_remito):
    # Buscar el remito en la base de datos por la ID
    remito = session.query(Remitos).filter_by(id=ID).first()
    if remito:
        # Actualizar los datos del remito con los nuevos datos ingresados
        remito.fecha = nueva_fecha
        remito.total = float(nuevo_total)
        remito.pago = nuevo_pago
        # Confirmar la transacción
        session.commit()
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Remito modificado exitosamente.")
        # Cerrar la ventana secundaria
        ventana_mod_remito.destroy()

def actualizar_remitos(self, remitos_tree, nombre):
    # Limpiar el Treeview de remitos previo
    for item in remitos_tree.get_children():
        remitos_tree.delete(item)

    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()

    # Insertar en el Treeview los valores actualizados del remito
    for remito in cliente.remitos:
        fecha_formateada = remito.fecha.strftime("%d/%m/%Y %H:%M:%S")
        fecha_pago_formateada = remito.fecha_pago.strftime("%d/%m/%Y %H:%M:%S")
        if remito.pago != "NO" and remito.pago != "SI":
            pago_formateado = f"${float(remito.pago):,.2f}"
        else:
            pago_formateado = remito.pago
        remitos_tree.insert('', 'end', values=(remito.id, fecha_formateada, fecha_pago_formateada, f"${remito.total:,.2f}", pago_formateado))
