import tkinter as tk
from tkinter import ttk, messagebox
from database import Clientes, Remitos, Productos, session 

def ver_deudas(self):
    # Obtener el cliente seleccionado en la tabla
    seleccion = self.clientes_tree.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    
    # Obtener el nombre del cliente seleccionado
    nombre = self.clientes_tree.item(seleccion)['values'][0]
    # Llamar a la función para abrir la ventana de deudas
    abrir_ventana_deudas(self, nombre)

def abrir_ventana_deudas(self, nombre):
    # Obtener el cliente de la base de datos por el nombre
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    
    # Filtrar los remitos que no estén pagos
    remitos_no_pagos = [deuda for deuda in cliente.remitos if deuda.pago != 'SI']
    
    # Calcular el total de la deuda
    total_deuda = sum(deuda.total - (float(deuda.pago) if deuda.pago not in ["SI", "NO"] else 0) for deuda in remitos_no_pagos)

    # Verificar que el cliente tenga deudas
    if not remitos_no_pagos:
        messagebox.showinfo("Información", "El cliente no tiene deudas.")
        return
    
    # Crear una nueva ventana para mostrar las deudas
    self.ventana_deudas = tk.Toplevel()
    self.ventana_deudas.title("Deudas de " + nombre)

    frame_deudas = tk.Frame(self.ventana_deudas)
    frame_deudas.pack(fill='both', expand=True)
    
    frame_deudas_tree = tk.Frame(frame_deudas)
    frame_deudas_tree.pack(fill='x', pady=10)
    
    # Crear un Treeview para mostrar los remitos no pagos
    self.deudas_tree = ttk.Treeview(frame_deudas_tree, columns=('ID', 'Fecha', 'Fecha Pago', 'Total', 'Pago'), show='headings')
    self.deudas_tree.heading('ID', text='ID')
    self.deudas_tree.heading('Fecha', text='Fecha')
    self.deudas_tree.heading('Fecha Pago', text='Fecha Pago')
    self.deudas_tree.heading('Total', text='Total')
    self.deudas_tree.heading('Pago', text='Pago')
    self.deudas_tree.column('ID', width=30, anchor='center')
    self.deudas_tree.column('Fecha', width=150, anchor='center')
    self.deudas_tree.column('Fecha Pago', width=150, anchor='center')
    self.deudas_tree.column('Total', width=100, anchor='center')
    self.deudas_tree.column('Pago', width=100, anchor='center')
    self.deudas_tree.pack(pady=10, fill='x')
    
    # Scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(frame_deudas_tree, orient='vertical', command=self.deudas_tree.yview)
    self.deudas_tree.configure(yscroll=scrollbar.set)

    # Usar grid para organizar el Treeview y el Scrollbar
    self.deudas_tree.grid(row=0, column=0, sticky='nsew')
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Configurar el frame para expandir el Treeview
    frame_deudas_tree.grid_rowconfigure(0, weight=1)
    frame_deudas_tree.grid_columnconfigure(0, weight=1)
    
    # Insertar los remitos no pagos en la tabla
    for deuda in remitos_no_pagos:
        # Formatear la fecha del remito
        fecha_formateada = deuda.fecha.strftime("%d/%m/%Y %H:%M:%S")
        fecha_pago_formateada = deuda.fecha_pago.strftime("%d/%m/%Y %H:%M:%S")
        # Si el pago ya tiene un monto, restar el pago al total y formatear ambos
        if deuda.pago != "NO" and deuda.pago != "SI":
            pago_formateado = f"${float(deuda.pago):,.2f}"
            total_formateado = deuda.total - float(deuda.pago)
            total_formateado = f"${total_formateado:,.2f}"
        # Si el pago no tiene un monto, mostrar el total y el pago tal cual
        else:
            pago_formateado = deuda.pago
            total_formateado = f"${deuda.total:,.2f}"    
        # Insertar los valores en el Treeview
        self.deudas_tree.insert('', 'end', values=(
            deuda.id, 
            fecha_formateada, 
            fecha_pago_formateada,
            total_formateado, 
            pago_formateado
        ))

    
    # Crear una etiqueta para mostrar el total de la deuda
    self.etiqueta_total = tk.Label(self.ventana_deudas, text=f"Total de la Deuda: ${total_deuda:,.2f}")
    self.etiqueta_total.pack(pady=10)

    frame_botones = tk.Frame(self.ventana_deudas)
    frame_botones.pack(pady=10)

    # Crear un botón para actualizar los precios de los productos
    actualizar_deudas_button = ttk.Button(frame_botones, text="Actualizar Precios", command=lambda: actualizar_precios(self, nombre))
    actualizar_deudas_button.grid(row=0, column=0, padx=10)

    # Crear un botón para cancelar la deuda parcialmente
    cancelar_deuda_button = ttk.Button(frame_botones, text="Cancelar Parcial", command=lambda: cancelar_deuda(self, nombre))
    cancelar_deuda_button.grid(row=0, column=1, padx=10)

    # Crear un botón para cancelar el total de la deuda
    cancelar_total_button = ttk.Button(frame_botones, text="Cancelar Total", command=lambda: cancelar_total(self, nombre))
    cancelar_total_button.grid(row=0, column=2, padx=10)

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

        # Verificar si el producto se encuentra en la base de datos
        if nombre_producto in precios:
            # Actualizar el precio unitario y el total del detalle
            detalle.precio_unitario = precios[nombre_producto]
            detalle.total = detalle.cantidad * detalle.precio_unitario * (1 - detalle.descuento / 100)
        # Si el producto no se encuentra en la base de datos, mostrar un mensaje de advertencia
        else:
            messagebox.showwarning("Advertencia", f"El producto '{nombre_producto}' no se encuentra en la base de datos.", parent=self.ventana_deudas)
            continue

        # Calcular y actualizar el total del remito
        deuda.total = sum(detalle.total for detalle in deuda.detalles)

    # Confirmar la transacción
    session.commit()
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Los precios se han actualizado correctamente.", parent=self.ventana_deudas)
    # Actualizar la ventana de deudas
    actualizar_ventana_deudas(self, nombre)

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
    total_deuda = sum(deuda.total - (float(deuda.pago) if deuda.pago not in ["SI", "NO"] else 0) for deuda in remitos_no_pagos)

    # Insertar los remitos no pagos en la tabla
    for deuda in remitos_no_pagos:
        # Formatear la fecha del remito
        fecha_formateada = deuda.fecha.strftime("%d/%m/%Y %H:%M:%S")
        fecha_pago_formateada = deuda.fecha_pago.strftime("%d/%m/%Y %H:%M:%S")
        # Si el pago ya tiene un monto, restar el pago al total y formatear ambos
        if deuda.pago != "NO" and deuda.pago != "SI":
            pago_formateado = f"${float(deuda.pago):,.2f}"
            total_formateado = deuda.total - float(deuda.pago)
            total_formateado = f"${total_formateado:,.2f}"
        # Si el pago no tiene un monto, mostrar el total y el pago tal cual
        else:
            pago_formateado = deuda.pago
            total_formateado = f"${deuda.total:,.2f}"
        # Insertar los valores en el Treeview
        self.deudas_tree.insert('', 'end', values=(
            deuda.id, 
            fecha_formateada, 
            fecha_pago_formateada,
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
    
    # Obtener el ID del remito seleccionado
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
    if monto > deuda.total - (float(deuda.pago) if deuda.pago not in ["SI", "NO"] else 0):
        messagebox.showerror("Error", "El monto a cancelar no puede ser mayor al total de la deuda.", parent=self.ventana_cancelar_deuda)
        return
    
    # Solicitar confirmación para cancelar la deuda parcialmente
    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de cancelar ${monto:,.2f} de la deuda?", parent=self.ventana_cancelar_deuda)
    if not confirmacion:
        return

    # Si el pago ya tiene un monto, sumar el monto a cancelar al pago actual
    if deuda.pago != "NO":
        monto = float(deuda.pago) + monto
        deuda.pago = monto

    # Si el pago no tiene un monto, asignar el monto a cancelar al pago
    else:
        deuda.pago = monto

    # Confirmar la transacción
    session.commit()

    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Deuda cancelada exitosamente.", parent=self.ventana_cancelar_deuda)
    
    # Actualizar la ventana de deudas
    actualizar_ventana_deudas(self, nombre)

    # Cerrar la ventana de cancelar deuda
    self.ventana_cancelar_deuda.destroy()