from tkinter import messagebox, simpledialog
from database import session

def modificar_precios(tabla_var, Productos, Categorias, update_productos_callback):
    # Obtener la categoría seleccionada por el usuario
    categoria_seleccionada = tabla_var.get()

    # Verificar si hay una lista seleccionada
    if not categoria_seleccionada:
        # Mostrar un mensaje de error si no hay una lista seleccionada
        messagebox.showerror("Error", "Selecciona una lista de productos.")
        return

    # Solicitar el porcentaje de aumento al usuario
    porcentaje_aumento = simpledialog.askfloat("Modificar Precios", "Ingrese el porcentaje (por ejemplo, 10 para un 10%):")
    # Si el usuario ingresó un porcentaje
    if porcentaje_aumento is not None:

        # Obtener el ID de la categoría seleccionada
        categoria_seleccionada = session.query(Categorias).filter_by(nombre=categoria_seleccionada).first().id

        # Obtener todos los productos de la categoría seleccionada
        productos = session.query(Productos).filter_by(id_categoria=categoria_seleccionada).all()

        # # Guardar los precios anteriores antes de aumentarlos
        # precios_anteriores.clear()  # Limpiar la lista antes de guardar nuevos precios
        # precios_anteriores.extend([(producto.nombre, producto.precio) for producto in productos])

        # Iterar sobre los productos y aumentar el precio según el porcentaje ingresado
        for producto in productos:
            producto.precio *= (1 + porcentaje_aumento / 100)

        # Confirmar los cambios en la base de datos
        session.commit()

        # Actualizar la lista de productos en la interfaz de usuario
        update_productos_callback()

        # Mostrar un mensaje de éxito al usuario con el porcentaje de aumento y la categoría seleccionada
        messagebox.showinfo("Éxito", f"Los precios de la lista {categoria_seleccionada} han sido modificados en un {porcentaje_aumento}%.")

def deshacer_ultimo_aumento(tabla_var, precios_anteriores, Categorias, Productos):
    # Verificar si hay precios anteriores guardados
    if not precios_anteriores:
        # Mostrar un mensaje de error si no hay precios anteriores guardados
        messagebox.showwarning("Error", "No hay modificaciones previas para deshacer.")
        return

    # Obtener la categoría seleccionada por el usuario
    categoria_seleccionada = tabla_var.get()

    # Obtener el ID de la categoría seleccionada
    categoria_seleccionada = session.query(Categorias).filter_by(nombre=categoria_seleccionada).first().id

    # Iterar sobre los productos y revertir el último aumento de precio
    for nombre_producto, precio_anterior in precios_anteriores:
        # Obtener el producto por el nombre y la categoría
        producto = session.query(Productos).filter_by(nombre=nombre_producto, id_categoria=categoria_seleccionada).first()
        # Si el producto existe, revertir el precio al precio anterior
        if producto:
            producto.precio = precio_anterior

    # Confirmar los cambios en la base de datos
    session.commit()
    # Mostrar un mensaje de éxito al usuario
    messagebox.showinfo("Éxito", "Última modificación revertida exitosamente.")
    # Limpiar la lista de precios anteriores
    precios_anteriores.clear() 