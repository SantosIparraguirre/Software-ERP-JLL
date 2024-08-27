from database import session

# Llenar treeview con todos los productos
def llenar_treeview_productos(productos_tree, Productos):
    # Obtener todos los productos
    productos = session.query(Productos).all()
    
    # Limpiar el treeview antes de insertar los productos
    for item in productos_tree.get_children():
        productos_tree.delete(item)
    
    # Insertar los productos en el treeview
    for producto in productos:
        precio = f'${producto.precio:,.2f}' if producto.precio else ''
        productos_tree.insert('', 'end', values=(producto.codigo, producto.linea, producto.nombre, precio))

def update_productos(tabla_var, productos_tree, Productos, Categorias, event=None):
    # Limpiar el treeview actual
    for item in productos_tree.get_children():
        productos_tree.delete(item)

    categoria_seleccionada = tabla_var.get()
    
    # Si no se seleccionó una categoría, llenar el treeview con todos los productos
    if not categoria_seleccionada:
        # Limpiar el treeview
        llenar_treeview_productos(productos_tree, Productos)
        return
    
    else:
        # Obtener los productos de la categoría seleccionada
        productos = (
            session.query(Productos)
            .join(Categorias)
            .filter(Categorias.nombre == categoria_seleccionada)
            .all()
        )
    
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

    # Separar la búsqueda por palabras clave
    search_terms = search_term.split()

    # Obtener la categoría seleccionada
    categoria_seleccionada = tabla_var.get()

    # Si no se seleccionó una categoría, buscar en todos los productos
    if not categoria_seleccionada:
        productos = session.query(Productos).all()
    # Si se seleccionó una categoría, buscar solo en los productos de esa categoría
    else:
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
        if all(term in nombre or term in codigo or term in linea for term in search_terms):
            precio = f'${producto.precio:,.2f}' if producto.precio else ''
            productos_tree.insert('', 'end', values=(producto.codigo, producto.linea, producto.nombre, precio))