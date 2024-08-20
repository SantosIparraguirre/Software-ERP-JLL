import tkinter as tk
from tkinter import ttk, messagebox
from database import Clientes, Remitos, Productos, session 

def ver_deudas(self):
    # Obtener el cliente seleccionado en la tabla
    seleccion = self.clientes_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    
    nombre = self.clientes_tree.item(seleccion)['values'][0]
    abrir_ventana_deudas(self, nombre)

def abrir_ventana_deudas(self, nombre):
    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    
    # Filtrar los remitos que no estén pagos
    remitos_no_pagos = [deuda for deuda in cliente.remitos if deuda.pago != 'SI']
    
    # Calcular el total de la deuda
    total_deuda = sum(deuda.total - float(deuda.pago) for deuda in remitos_no_pagos)
    
    # Crear una nueva ventana para mostrar las deudas
    self.ventana_deudas = tk.Toplevel()
    self.ventana_deudas.title("Deudas de " + nombre)
    
    # Crear un Treeview para mostrar los remitos no pagos
    self.deudas_tree = ttk.Treeview(self.ventana_deudas, columns=('ID', 'Fecha', 'Total', 'Pago'), show='headings')
    self.deudas_tree.heading('ID', text='ID')
    self.deudas_tree.heading('Fecha', text='Fecha')
    self.deudas_tree.heading('Total', text='Total')
    self.deudas_tree.heading('Pago', text='Pago')
    self.deudas_tree.column('ID', width=30, anchor='center')
    self.deudas_tree.column('Fecha', width=150, anchor='center')
    self.deudas_tree.column('Total', width=100, anchor='center')
    self.deudas_tree.column('Pago', width=100, anchor='center')
    self.deudas_tree.pack(pady=10, fill='x')
    
    # Insertar los remitos no pagos en la tabla
    for deuda in remitos_no_pagos:
        fecha_formateada = deuda.fecha.strftime("%d/%m/%Y %H:%M:%S")
        if deuda.pago != "NO" and deuda.pago != "SI":
            pago_formateado = f"${float(deuda.pago):,.2f}"
            total_formateado = deuda.total - float(deuda.pago)
            total_formateado = f"${total_formateado:,.2f}"
        else:
            pago_formateado = deuda.pago        
        self.deudas_tree.insert('', 'end', values=(
            deuda.id, 
            fecha_formateada, 
            total_formateado, 
            pago_formateado
        ))

    
    # Crear una etiqueta para mostrar el total de la deuda
    self.etiqueta_total = tk.Label(self.ventana_deudas, text=f"Total de la Deuda: ${total_deuda:,.2f}")
    self.etiqueta_total.pack(pady=10)

    # Crear un botón para actualizar los precios de los productos
    actualizar_deudas_button = ttk.Button(self.ventana_deudas, text="Actualizar Precios", command=lambda: actualizar_precios(self, nombre))
    actualizar_deudas_button.pack(pady=10)

    # Crear un botón para cancelar la deuda parcialmente
    cancelar_deuda_button = ttk.Button(self.ventana_deudas, text="Cancelar Parcial", command=lambda: cancelar_deuda(self, nombre))
    cancelar_deuda_button.pack(pady=10)

    # Crear un botón para cancelar el total de la deuda
    cancelar_total_button = ttk.Button(self.ventana_deudas, text="Cancelar Total", command=lambda: cancelar_total(self, nombre))
    cancelar_total_button.pack(pady=10)

# Función para actualizar los precios de los productos
def actualizar_precios(self, nombre):
    # Verificar que se haya seleccionado una deuda
    seleccion = self.deudas_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una deuda.", parent=self.ventana_deudas)
        return
    
    # Solicitar confirmación para actualizar los precios de los productos
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de actualizar los precios de los productos?", parent=self.ventana_deudas)
    if not confirmacion:
        return
    
    # Obtener el ID del remito seleccionado
    id_deuda = self.deudas_tree.item(seleccion)['values'][0]
    
    # Obtener el remito de la base de datos por el ID
    deuda = session.query(Remitos).get(id_deuda)

    # Obtener los nombres de los productos en los detalles del remito
    productos = [detalle.producto for detalle in deuda.detalles]

    # Obtener los productos de la base de datos por el nombre
    productos_db = session.query(Productos).filter(Productos.nombre.in_(productos)).all()

    # Crear un diccionario con los nombres de los productos y sus precios
    precios = {producto.nombre: producto.precio for producto in productos_db}

    # Actualizar los precios de los productos en los detalles del remito
    for detalle in deuda.detalles:
        nombre_producto = detalle.producto  # Capturar el nombre del producto
        if isinstance(nombre_producto, Productos):  # Si devuelve un objeto de Productos
            nombre_producto = nombre_producto.nombre  # Acceder al nombre real

        if nombre_producto in precios:
            detalle.precio_unitario = precios[nombre_producto]
            detalle.total = detalle.cantidad * detalle.precio_unitario * (1 - detalle.descuento / 100)
        else:
            messagebox.showwarning("Advertencia", f"El producto '{nombre_producto}' no se encuentra en la base de datos.")
            continue

    session.commit()
    messagebox.showinfo("Éxito", "Los precios se han actualizado correctamente.")


def cancelar_deuda(self, nombre):
    # Verificar que se haya seleccionado una deuda
    seleccion = self.deudas_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una deuda.", parent=self.ventana_deudas)
        return
    
    # Obtener el ID del remito seleccionado
    id_deuda = self.deudas_tree.item(seleccion)['values'][0]
    
    # Obtener el remito de la base de datos por el ID
    deuda = session.query(Remitos).get(id_deuda)

    # Abrir una nueva ventana para solicitar el monto a cancelar
    self.ventana_cancelar_deuda = tk.Toplevel()
    self.ventana_cancelar_deuda.title("Cancelar Deuda")

    # Crear una etiqueta para solicitar el monto a cancelar
    etiqueta_monto = tk.Label(self.ventana_cancelar_deuda, text="Monto a Cancelar:")
    etiqueta_monto.pack(pady=10)

    # Crear una entrada para ingresar el monto a cancelar
    monto_entry = ttk.Entry(self.ventana_cancelar_deuda)
    monto_entry.pack(pady=10)

    # Crear un botón para confirmar la cancelación de la deuda
    confirmar_cancelacion_button = ttk.Button(self.ventana_cancelar_deuda, text="Confirmar", command=lambda: confirmar_cancelacion(self, deuda, monto_entry, nombre))
    confirmar_cancelacion_button.pack(pady=10)

def actualizar_ventana_deudas(self, nombre):
    # Limpiar el Treeview
    for item in self.deudas_tree.get_children():
        self.deudas_tree.delete(item)
    
    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()

    # Filtrar los remitos que no estén pagos
    remitos_no_pagos = [deuda for deuda in cliente.remitos if deuda.pago != 'SI']

    # Calcular el total de la deuda
    total_deuda = sum(deuda.total - float(deuda.pago) for deuda in remitos_no_pagos)

    # Insertar los remitos no pagos en la tabla
    for deuda in remitos_no_pagos:
        fecha_formateada = deuda.fecha.strftime("%d/%m/%Y %H:%M:%S")
        if deuda.pago != "NO" and deuda.pago != "SI":
            pago_formateado = f"${float(deuda.pago):,.2f}"
            total_formateado = deuda.total - float(deuda.pago)
            total_formateado = f"${total_formateado:,.2f}"
        else:
            pago_formateado = deuda.pago        
        self.deudas_tree.insert('', 'end', values=(
            deuda.id, 
            fecha_formateada, 
            total_formateado, 
            pago_formateado
        ))

    # Actualizar la etiqueta del total de la deuda
    self.etiqueta_total.config(text=f"Total de la Deuda: ${total_deuda:,.2f}")

def cancelar_total(self, nombre):
    # Obtener el ID del remito seleccionado
    seleccion = self.deudas_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una deuda.", parent=self.ventana_deudas)
        return

    id_deuda = self.deudas_tree.item(seleccion)['values'][0]
    
    # Obtener el remito de la base de datos por el ID
    deuda = session.query(Remitos).get(id_deuda)

    # Solicitar confirmación para cancelar el total de la deuda
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar el total de la deuda?", parent=self.ventana_deudas)  
    if not confirmacion:
        return

    # Cancelar el total de la deuda
    deuda.pago = 'SI'
    session.commit()

    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Deuda cancelada exitosamente.", parent=self.ventana_deudas)

    # Actualizar la ventana de deudas
    actualizar_ventana_deudas(self, nombre)
    
def confirmar_cancelacion(self, deuda, monto_entry, nombre):
    # Obtener el monto a cancelar
    try:
        monto = float(monto_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Monto inválido.", parent=self.ventana_cancelar_deuda)
        return
    
    # Verificar que el monto a cancelar no sea mayor al total de la deuda
    if monto > deuda.total:
        messagebox.showerror("Error", "El monto a cancelar no puede ser mayor al total de la deuda.", parent=self.ventana_cancelar_deuda)
        return
    
    # Solicitar confirmación para cancelar la deuda parcialmente
    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de cancelar ${monto:,.2f} de la deuda?", parent=self.ventana_cancelar_deuda)
    if not confirmacion:
        return

    if deuda.pago != "NO":
        monto = float(deuda.pago) + monto
        deuda.pago = monto

    else:
        deuda.pago = monto

    session.commit()

    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Deuda cancelada exitosamente.", parent=self.ventana_cancelar_deuda)
    
    # Actualizar la ventana de deudas
    actualizar_ventana_deudas(self, nombre)

    # Cerrar la ventana de cancelar deuda
    self.ventana_cancelar_deuda.destroy()