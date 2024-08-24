from database import session

def update_productos(tabla_var, productos_tree, Productos, Categorias, event=None):
    categoria_seleccionada = tabla_var.get()
    
    # Obtener los productos de la categoría seleccionada
    productos = (
        session.query(Productos)
        .join(Categorias)
        .filter(Categorias.nombre == categoria_seleccionada)
        .all()
    )
    
    # Limpiar el treeview actual
    for item in productos_tree.get_children():
        productos_tree.delete(item)
    
    # Insertar los nuevos productos en el treeview
    for producto in productos:
        precio = f'${producto.precio:,.2f}' if producto.precio else ''
        productos_tree.insert('', 'end', values=(
            producto.codigo,
            producto.linea,
            producto.nombre,
            precio
        ))

def buscar_producto(busqueda_var, tabla_var, productos_tree, Productos, Categorias):
    # Obtener el término de búsqueda y convertirlo a minúsculas
    search_term = busqueda_var.get().lower()

    categoria_seleccionada = tabla_var.get()

    # Obtener los productos de la categoría seleccionada
    productos = (
        session.query(Productos)
        .join(Categorias)
        .filter(Categorias.nombre == categoria_seleccionada)
        .all()
    )

    # Limpiar la tabla de productos antes de insertar aquellos que coincidan con el término de búsqueda
    productos_tree.delete(*productos_tree.get_children())

    for producto in productos:
        # Verificar que los atributos no sean None antes de llamar a lower()
        nombre = producto.nombre.lower() if producto.nombre else ''
        codigo = producto.codigo.lower() if producto.codigo else ''
        linea = producto.linea.lower() if producto.linea else ''
        
        # Si la búsqueda está contenida en el nombre del producto, insertar el producto en la tabla
        if search_term in nombre or search_term in codigo or search_term in linea:
            precio = f'${producto.precio:,.2f}' if producto.precio else ''
            productos_tree.insert('', 'end', values=(producto.codigo, producto.linea, producto.nombre, precio))