import tkinter as tk
from tkinter import ttk
from database import session, Categorias, Productos

def agregar_producto(self, event=None):
    # Verificar si se seleccionó una categoría
    if not self.tabla_var.get():
        tk.messagebox.showerror("Error", "Por favor, selecciona una categoría.")
        return

    # Crear una nueva ventana
    new_window = tk.Toplevel()
    new_window.title("Agregar Producto")

    # Obtener el nombre de la categoría seleccionada
    nombre_categoria = self.tabla_var.get()

    # Obtener el ID de la categoría seleccionada
    categoria_id = session.query(Categorias).filter_by(nombre=nombre_categoria).first().id

    # Crear etiquetas y campos de entrada para el código, línea, nombre y precio del producto
    ttk.Label(new_window, text="Código:").grid(row=0, column=0, padx=10, pady=5)
    codigo_entry = ttk.Entry(new_window)
    codigo_entry.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(new_window, text="Línea:").grid(row=1, column=0, padx=10, pady=5)
    linea_entry = ttk.Entry(new_window)
    linea_entry.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(new_window, text="Nombre:").grid(row=2, column=0, padx=10, pady=5)
    nombre_entry = ttk.Entry(new_window)
    nombre_entry.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(new_window, text="Precio UD:").grid(row=3, column=0, padx=10, pady=5)
    precio_ud_entry = ttk.Entry(new_window)
    precio_ud_entry.grid(row=3, column=1, padx=10, pady=5)

    # Función para agregar el producto a la base de datos
    def submit_producto():
        codigo = codigo_entry.get()
        linea = linea_entry.get()
        nombre = nombre_entry.get()
        precio_ud = precio_ud_entry.get()
        # Si falta nombre o precio, mostrar un mensaje de error
        if not nombre or not precio_ud:
            tk.messagebox.showerror("Error", "Por favor, ingresa el nombre y el precio del producto.", parent=new_window)
            return
        # Crear un nuevo producto con los datos ingresados
        producto = Productos(codigo=codigo, linea=linea, nombre=nombre, precio=precio_ud, id_categoria=categoria_id)
        # Agregar el producto a la base de datos
        session.add(producto)
        session.commit()
        # Mostrar un mensaje de éxito
        tk.messagebox.showinfo("Éxito", f"{nombre} agregado a la categoría {nombre_categoria}", parent=new_window)
        new_window.destroy()
        # Actualizar la tabla de productos
        self.update_productos()

    # Add a submit button
    submit_button = ttk.Button(new_window, text="Agregar", command=submit_producto)
    submit_button.grid(row=4, column=0, columnspan=2, pady=10)