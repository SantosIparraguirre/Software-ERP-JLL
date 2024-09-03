from tkinter import messagebox
import tkinter as tk

def agregar_al_carrito(carrito, productos_tree, cantidad_var, descuento_var):
    # Obtener el producto seleccionado en la tabla de productos
    selected_item = productos_tree.selection()

    if not selected_item:
        messagebox.showerror("Error", "Selecciona un producto.")
        return

    # Obtener el nombre y precio del producto seleccionado a través del índice
    item = productos_tree.item(selected_item)
    producto_nombre = item['values'][2]
    precio = item['values'][3]
    # Obtener la cantidad y descuento ingresados por el usuario con el método get
    cantidad = cantidad_var.get()
    descuento = f'{descuento_var.get()}%' if descuento_var.get() > 0 else ''

    if cantidad <= 0.0:
        messagebox.showerror("Error", "Ingresa una cantidad válida.")
        return

    # Agregar el producto al carrito y actualizar la lista de productos
    carrito.append((producto_nombre, cantidad, descuento, precio))

def actualizar_carrito(carrito_treeview, carrito):
    # Limpiar la lista de productos del carrito antes de insertar los productos actuales
    carrito_treeview.delete(*carrito_treeview.get_children())
    # Iterar sobre la lista de productos del carrito y agregarlos al treeview
    for item in carrito:
        # Desempaquetar los valores del producto
        producto, cantidad, descuento, precio = item
        # Calcular el total del producto con descuento
        total = float(precio.replace('$', '').replace(',', '')) * float(cantidad) * (1 - float(descuento.replace('%', '')) / 100 if descuento else 1)
        # Insertar el producto en el treeview del carrito
        carrito_treeview.insert('', 'end', values=(producto, cantidad, descuento, precio, f'${total:,.2f}'))
    
    # Calcular el total del remito/presupuesto
    calcular_total(carrito, carrito_treeview)

# Función para calcular el total del remito/presupuesto
def calcular_total(carrito, carrito_treeview):
    # Si hay productos en el carrito, calcular el total del remito/presupuesto
    if carrito.__len__() > 0:
        # Verificar si el total ya está en el treeview
        if carrito_treeview.item(carrito_treeview.get_children()[-1])['values'][3] == 'Total:':
            carrito_treeview.delete(carrito_treeview.get_children()[-1])
        # Calcular el total del remito/presupuesto
        total_carrito = sum(float(item[3].replace('$', '').replace(',', '')) * float(item[1]) * (1 - float(item[2].replace('%', '')) / 100 if item[2] else 1) for item in carrito)
        # Añadir el total al treeview del carrito
        carrito_treeview.insert('', 'end', values=('', '', '', 'Total:', f'${total_carrito:,.2f}'))
        
def agregar_fuera_lista(carrito, producto_var, cantidad_fuera_lista_var, precio_var):
    # Obtener el nombre y precio del producto ingresados por el usuario
    producto = producto_var.get()
    # Obtener la cantidad y precio del producto ingresados por el usuario
    cantidad = cantidad_fuera_lista_var.get()
    # Obtener la cantidad y precio del producto ingresados por el usuario y formatearlo como moneda
    precio = f'${precio_var.get():,.2f}'

    # Validar que el producto y el precio no estén vacíos
    if not producto or not precio:
        messagebox.showerror("Error", "Ingresa un producto y un precio.")
        return

    # Agregar el producto a la lista de productos del carrito
    carrito.append((producto, cantidad, '0.0%', precio))
    # Limpiar los campos de entrada después de agregar el producto
    producto_var.set('')
    cantidad_fuera_lista_var.set('')
    precio_var.set('')

def eliminar_del_carrito(carrito, carrito_treeview):
    # Obtener el índice del producto seleccionado en el treeview del carrito
    seleccion = carrito_treeview.selection()

    # Si no se selecciona un producto, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un producto del carrito.")
        return

    # Obtener el nombre del producto seleccionado
    producto = carrito_treeview.item(seleccion)['values'][0]

    # Mostrar un mensaje de confirmación antes de eliminar el producto
    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar '{producto}' del carrito?")
    if not confirmacion:
        return
    
    # Obtener el índice del producto seleccionado
    index = carrito_treeview.index(seleccion)
    
    # Eliminar el producto del carrito
    del carrito[index]

def editar_celda(self, event):
    # Obtener la posición del clic y el ítem correspondiente
    row_id = self.carrito_treeview.identify_row(event.y)
    column_id = self.carrito_treeview.identify_column(event.x)

    if not row_id or not column_id:
        return
    
    # Si la celda es la de 'Total:', no permitir la edición
    if self.carrito_treeview.item(row_id)['values'][3] == 'Total:':
        return

    # Obtener valores actuales
    item = self.carrito_treeview.item(row_id)['values']
    column = int(column_id[1:]) - 1

    # Crear un Entry temporal
    x, y, width, height = self.carrito_treeview.bbox(row_id, column_id)
    entry = tk.Entry(self.carrito_treeview)
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, item[column])
    entry.focus()

    def guardar_edicion(event=None):
        # Obtener los valores actuales
        values = list(self.carrito_treeview.item(row_id, "values"))

        # Obtener el nuevo valor del entry
        new_value = entry.get()

        # Actualizar solo la columna seleccionada
        values[column] = new_value

        # Si se cambia la cantidad, el descuento o el precio, recalcular el total
        if column in [1, 2, 3]:  # Índices correspondientes a cantidad, descuento y precio
            cantidad = float(values[1])
            # Formatear el descuento para eliminar el signo de porcentaje
            descuento = float(values[2][:-1]) if values[2] else 0
            # Formatear el precio para eliminar el signo de dólar y las comas
            precio_unitario = float(values[3][1:].replace(",", ""))
            total = cantidad * precio_unitario * (1 - descuento / 100)
            values[4] = f"${total:,.2f}"  # Actualizar el total en la lista de valores
        
        # Si se cambia el total, recalcular el precio unitario
        elif column == 4:
            total = float(values[4][1:].replace(",", ""))
            cantidad = float(values[1])
            # Formatear el descuento para eliminar el signo de porcentaje
            descuento = float(values[2][:-1])
            precio_unitario = total / (cantidad * (1 - descuento / 100))
            values[3] = f"${precio_unitario:,.2f}"  # Actualizar el precio unitario en la lista de valores

        # Actualizar el treeview con los nuevos valores
        self.carrito_treeview.item(row_id, values=values)

        # Actualizar la lista original 'self.carrito' con los nuevos valores excepto el total
        index = int(self.carrito_treeview.index(row_id))
        self.carrito[index] = tuple(values[:4])  # No incluir el total en 'self.carrito'

        # Ocultar el entry después de guardar la edición
        entry.place_forget()

        # Calcular el total del remito/presupuesto
        calcular_total(self.carrito, self.carrito_treeview)

    entry.bind('<Return>', guardar_edicion)
    entry.bind('<FocusOut>', lambda event: entry.destroy())