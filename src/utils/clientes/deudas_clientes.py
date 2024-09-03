import tkinter as tk
from tkinter import ttk, messagebox
from database import Clientes, Remitos, Productos, session
import datetime

ventana_deudas = None

def obtener_cliente_por_nombre(nombre):
    return session.query(Clientes).filter_by(nombre=nombre).first()

def formatear_fecha(fecha):
    return fecha.strftime("%d/%m/%Y %H:%M:%S")

def insertar_remitos_no_pagos(treeview, remitos_no_pagos):
    for deuda in remitos_no_pagos:
        # Formatear la fecha
        fecha_formateada = formatear_fecha(deuda.fecha) if deuda.fecha else ''
        fecha_pago_formateada = formatear_fecha(deuda.fecha_pago) if deuda.fecha_pago else ''
        # Si el pago no es "NO" ni "SI", formatear el monto de pago como moneda
        if deuda.pago not in ["NO", "SI"]:
            total_formateado = f'${deuda.total:,.2f}'
            pago_formateado = f"${float(deuda.pago):,.2f}"
            deuda_formateado = f"${(deuda.total - float(deuda.pago)):,.2f}"
        # Si el pago es "NO", mostrar "NO" en lugar de un monto
        else:
            total_formateado = f"${deuda.total:,.2f}"
            pago_formateado = deuda.pago
            deuda_formateado = total_formateado
        # Insertar los datos en el Treeview
        treeview.insert('', 'end', values=(
            deuda.id, 
            fecha_formateada, 
            fecha_pago_formateada,
            total_formateado, 
            pago_formateado,
            deuda_formateado
        ))

def crear_treeview(parent):
    # Crear un Treeview con las columnas ID, Fecha, Fecha Pago, Total, Pago y Deuda
    treeview = ttk.Treeview(parent, columns=('ID', 'Fecha', 'Fecha Pago', 'Total', 'Pago', 'Deuda'), show='headings')
    # Propiedades de las columnas
    column_properties = {
        'ID': {'width': 30, 'anchor': 'center'},
        'Fecha': {'width': 150, 'anchor': 'center'},
        'Fecha Pago': {'width': 150, 'anchor': 'center'},
        'Total': {'width': 100, 'anchor': 'center'},
        'Pago': {'width': 100, 'anchor': 'center'},
        'Deuda': {'width': 100, 'anchor': 'center'}
    }
    # Configurar las cabeceras y las columnas
    for col in ['ID', 'Fecha', 'Fecha Pago', 'Total', 'Pago', 'Deuda']:
        treeview.heading(col, text=col)
        treeview.column(col, **column_properties.get(col, {}))
    # Empaquetar el Treeview
    treeview.pack(pady=10, fill='x')
    # Crear una scrollbar para el Treeview
    scrollbar = ttk.Scrollbar(parent, orient='vertical', command=treeview.yview)
    treeview.configure(yscroll=scrollbar.set)
    # Posicionar el Treeview y la scrollbar en el marco
    treeview.grid(row=0, column=0, sticky='nsew')
    scrollbar.grid(row=0, column=1, sticky='ns')
    # Configurar el marco para que se expanda con la ventana
    parent.grid_rowconfigure(0, weight=1)
    parent.grid_columnconfigure(0, weight=1)
    # Retornar el Treeview
    return treeview

def ver_deudas(self):
    # Obtener el cliente seleccionado en la tabla
    seleccion = self.clientes_tree.selection()
    # Si no se seleccionó ningún cliente, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    # Obtener el nombre del cliente seleccionado
    nombre = self.clientes_tree.item(seleccion)['values'][0]
    # Llamar a la función
    abrir_ventana_deudas(self, nombre)

def abrir_ventana_deudas(self, nombre):
    global ventana_deudas
    # Si la ventana de deudas ya está abierta, cerrarla
    if ventana_deudas and tk.Toplevel.winfo_exists(ventana_deudas):
        ventana_deudas.destroy()
    # Obtener el cliente de la base de datos por el nombre
    cliente = obtener_cliente_por_nombre(nombre)
    # Filtrar los remitos del cliente que no han sido pagados
    remitos_no_pagos = [deuda for deuda in cliente.remitos if deuda.pago != 'SI']
    # Calcular el total de la deuda
    total_deuda = sum(deuda.total - (float(deuda.pago) if deuda.pago not in ["SI", "NO"] else 0) for deuda in remitos_no_pagos)
    # Si el cliente no tiene deudas, mostrar un mensaje informativo y retornar
    if not remitos_no_pagos:
        messagebox.showinfo("Información", "El cliente no tiene deudas.")
        return
    # Crear una ventana secundaria para mostrar las deudas del cliente
    ventana_deudas = tk.Toplevel()
    # Configurar el título de la ventana
    ventana_deudas.title("Deudas de " + nombre)
    # Configurar las dimensiones de la ventana
    frame_deudas = tk.Frame(ventana_deudas)
    frame_deudas.pack(fill='both', expand=True)
    # Crear un marco para la tabla de deudas y su scrollbar
    frame_deudas_tree = tk.Frame(frame_deudas)
    frame_deudas_tree.pack(fill='x', pady=10)
    # Crear un Treeview para mostrar las deudas del cliente
    self.deudas_tree = crear_treeview(frame_deudas_tree)
    # Insertar los remitos no pagos en el Treeview
    insertar_remitos_no_pagos(self.deudas_tree, remitos_no_pagos)
    # Crear una etiqueta para mostrar el total de la deuda
    self.etiqueta_total = tk.Label(ventana_deudas, text=f"Total de la Deuda: ${total_deuda:,.2f}")
    self.etiqueta_total.pack(pady=10)
    # Crear un marco para los botones
    frame_botones = tk.Frame(ventana_deudas)
    frame_botones.pack(pady=10)
    # Crear botones para actualizar precios, cancelar parcial y cancelar total
    ttk.Button(frame_botones, text="Actualizar Precios", command=lambda: actualizar_precios(self, nombre, ventana_deudas)).grid(row=0, column=0, padx=10)
    ttk.Button(frame_botones, text="Cancelar Parcial", command=lambda: cancelar_deuda(self, nombre, ventana_deudas)).grid(row=0, column=1, padx=10)
    ttk.Button(frame_botones, text="Cancelar Total", command=lambda: cancelar_total(self, nombre, ventana_deudas)).grid(row=0, column=2, padx=10)

def actualizar_precios(self, nombre, ventana_deudas):
    # Obtener la selección del Treeview
    seleccion = self.deudas_tree.selection()
    # Si no se seleccionó ninguna deuda, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una deuda.", parent=ventana_deudas)
        return
    # Preguntar al usuario si está seguro de actualizar los precios
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de actualizar los precios de los productos?", parent=ventana_deudas)
    # Si el usuario no confirma, retornar
    if not confirmacion:
        return
    # Obtener el ID de la deuda seleccionada
    id_deuda = self.deudas_tree.item(seleccion)['values'][0]
    # Buscar la deuda en la base de datos por el ID
    deuda = session.query(Remitos).get(id_deuda)
    # Obtener los nombres de los productos de la deuda
    productos = [detalle.producto for detalle in deuda.detalles]
    # Buscar los productos en la base de datos por el nombre
    productos_db = session.query(Productos).filter(Productos.nombre.in_(productos)).all()
    # Crear un diccionario con los precios de los productos
    precios = {producto.nombre: producto.precio for producto in productos_db}
    # Iterar sobre los detalles de la deuda
    for detalle in deuda.detalles:
        # Obtener el nombre del producto
        nombre_producto = detalle.producto
        # Si el producto está en el diccionario de precios, actualizar el precio unitario y el total
        if nombre_producto in precios:
            detalle.precio_unitario = precios[nombre_producto]
            detalle.total = detalle.cantidad * detalle.precio_unitario * (1 - detalle.descuento / 100)
        # Si el producto no está en la base de datos, mostrar un mensaje de advertencia
        else:
            messagebox.showwarning("Advertencia", f"El producto '{nombre_producto}' no se encuentra en la base de datos.", parent=ventana_deudas)
            continue
        # Actualizar el total de la deuda
        deuda.total = sum(detalle.total for detalle in deuda.detalles)
    # Confirmar la transacción
    session.commit()
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Los precios se han actualizado correctamente.", parent=ventana_deudas)
    # Actualizar la ventana de deudas
    actualizar_ventana_deudas(self, nombre)

def cancelar_deuda(self, nombre, ventana_deudas):
    # Obtener la selección del Treeview
    seleccion = self.deudas_tree.selection()
    # Si no se seleccionó ninguna deuda, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una deuda.", parent=ventana_deudas)
        return
    # Obtener el ID de la deuda seleccionada
    id_deuda = self.deudas_tree.item(seleccion)['values'][0]
    # Buscar la deuda en la base de datos por el ID
    deuda = session.query(Remitos).get(id_deuda)
    # Crear una ventana secundaria para cancelar la deuda
    self.ventana_cancelar_deuda = tk.Toplevel()
    self.ventana_cancelar_deuda.title("Cancelar Deuda")
    # Tamaño de la ventana
    self.ventana_cancelar_deuda.geometry("300x200")
    # Etiqueta y campo de entrada para el monto a cancelar
    tk.Label(self.ventana_cancelar_deuda, text="Monto a Cancelar:").pack(pady=10)
    monto_entry = ttk.Entry(self.ventana_cancelar_deuda)
    monto_entry.pack(pady=10)
    # Botón para confirmar la cancelación
    ttk.Button(self.ventana_cancelar_deuda, text="Confirmar", command=lambda: confirmar_cancelacion(self, deuda, monto_entry, nombre)).pack(pady=10)

def actualizar_ventana_deudas(self, nombre):
    # Limpiar el Treeview de deudas
    for item in self.deudas_tree.get_children():
        self.deudas_tree.delete(item)
    # Obtener el cliente de la base de datos por el nombre
    cliente = obtener_cliente_por_nombre(nombre)
    # Filtrar los remitos del cliente que no han sido pagados
    remitos_no_pagos = [deuda for deuda in cliente.remitos if deuda.pago != 'SI']
    # Calcular el total de la deuda
    total_deuda = sum(deuda.total - (float(deuda.pago) if deuda.pago not in ["SI", "NO"] else 0) for deuda in remitos_no_pagos)
    # Insertar los remitos no pagos en el Treeview
    insertar_remitos_no_pagos(self.deudas_tree, remitos_no_pagos)
    # Actualizar la etiqueta con el total de la deuda
    self.etiqueta_total.config(text=f"Total de la Deuda: ${total_deuda:,.2f}")

def cancelar_total(self, nombre, ventana_deudas):
    # Obtener la selección del Treeview
    seleccion = self.deudas_tree.selection()
    # Si no se seleccionó ninguna deuda, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona una deuda.", parent=ventana_deudas)
        return
    # Obtener el ID de la deuda seleccionada
    id_deuda = self.deudas_tree.item(seleccion)['values'][0]
    # Buscar la deuda en la base de datos por el ID
    deuda = session.query(Remitos).get(id_deuda)
    # Mostrar un mensaje de confirmación para cancelar la deuda
    confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar el total de la deuda?", parent=ventana_deudas)
    # Si el usuario no confirma, retornar
    if not confirmacion:
        return
    # Actualizar el monto de pago de la deuda
    deuda.pago = 'SI'
    # Actualizar la fecha de pago de la deuda
    deuda.fecha_pago = datetime.datetime.now()
    # Confirmar la transacción
    session.commit()
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Deuda cancelada exitosamente.", parent=ventana_deudas)
    # Actualizar la ventana de deudas
    actualizar_ventana_deudas(self, nombre)

def confirmar_cancelacion(self, deuda, monto_entry, nombre):
    # Obtener el monto ingresado por el usuario
    try:
        monto = float(monto_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Monto inválido.", parent=self.ventana_cancelar_deuda)
        return
    # Validar que el monto a cancelar no sea mayor al total de la deuda
    if monto > deuda.total - (float(deuda.pago) if deuda.pago not in ["SI", "NO"] else 0):
        messagebox.showerror("Error", "El monto a cancelar no puede ser mayor al total de la deuda.", parent=self.ventana_cancelar_deuda)
        return
    # Mostrar un mensaje de confirmación para cancelar la deuda
    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de cancelar ${monto:,.2f} de la deuda?", parent=self.ventana_cancelar_deuda)
    # Si el usuario no confirma, retornar
    if not confirmacion:
        return
    # Actualizar el monto de pago de la deuda
    deuda.pago = float(deuda.pago) + monto if deuda.pago != "NO" else monto
    # Actualizar la fecha de pago de la deuda
    deuda.fecha_pago = datetime.datetime.now()
    # Confirmar la transacción
    session.commit()
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Deuda cancelada exitosamente.", parent=self.ventana_cancelar_deuda)
    # Actualizar la ventana de deudas
    actualizar_ventana_deudas(self, nombre)
    # Cerrar la ventana secundaria
    self.ventana_cancelar_deuda.destroy()