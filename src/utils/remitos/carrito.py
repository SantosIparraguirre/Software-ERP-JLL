from tkinter import messagebox

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
    descuento = f'{descuento_var.get()}%'

    if cantidad <= 0:
        messagebox.showerror("Error", "Ingresa una cantidad válida.")
        return

    # Agregar el producto al carrito y actualizar la lista de productos
    carrito.append((producto_nombre, cantidad, descuento, precio))

def actualizar_carrito(carrito_treeview, carrito):
    # Limpiar la lista de productos del carrito antes de insertar los productos actuales
    carrito_treeview.delete(*carrito_treeview.get_children())
    # Iterar sobre la lista de productos del carrito y agregarlos al treeview
    for item in carrito:
        producto, cantidad, descuento, precio = item
        carrito_treeview.insert('', 'end', values=(producto, cantidad, descuento, precio))

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

def eliminar_del_carrito(carrito, carrito_treeview):
    # Obtener el índice del producto seleccionado en el treeview del carrito
    seleccion = carrito_treeview.selection()
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un producto del carrito.")
        return
    
    index = carrito_treeview.index(seleccion)

    del carrito[index]