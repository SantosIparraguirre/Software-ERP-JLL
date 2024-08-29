# Widget de productos

import tkinter as tk
from tkinter import ttk, messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from database import Productos, Categorias, session
from utils.remitos.productos import llenar_treeview_productos, update_productos, buscar_producto
from PIL import Image, ImageTk


class ProductosWidget(tk.Tk):
    def __init__(self, main_frame):
        # Inicializar la ventana del widget
        self.main_frame = main_frame
        
        # Logo de la empresa
        self.logo = tk.PhotoImage(file='./icons/logo.png')
        logo_label = ttk.Label(self.main_frame, image=self.logo)
        logo_label.pack(pady=10)

        # Crear etiqueta para buscar productos
        buscar_producto_label = ttk.Label(self.main_frame, text="Buscar Producto:")
        buscar_producto_label.place(x=250, y=100)

        # Crear un Entry para buscar productos
        self.busqueda_producto = tk.StringVar()
        self.buscar_producto_entry = ttk.Entry(self.main_frame, textvariable=self.busqueda_producto)
        self.buscar_producto_entry.place(x=350, y=100)

        # Vincular la tecla Enter con la función de buscar productos
        self.buscar_producto_entry.bind("<Return>", self.buscar_producto)

        # Botón para buscar productos
        # Cargar la imagen de búsqueda y redimensionarla
        original_search_image = Image.open("./icons/search.png")
        resized_search_image = original_search_image.resize((15, 15), Image.LANCZOS)
        self.search_image = ImageTk.PhotoImage(resized_search_image)

        # El botón llama a la función buscar_producto cuando se hace click
        self.buscar_button = ttk.Button(self.main_frame, image=self.search_image, command=self.buscar_producto)
        self.buscar_button.place(x=480, y=98)

        # Menú de selección de tablas (listas de precios)
        self.tabla_label = ttk.Label(self.main_frame, text="Filtrar por lista:")
        # Empaquetar la etiqueta en el main_frame con place
        self.tabla_label.place(x=600, y=100)

        # Combobox para seleccionar la categoría

        # Obtener todas las categorías de la base de datos
        tablas = session.query(Categorias).all()

        tablas = [tabla.nombre for tabla in tablas]

        # StringVar para almacenar la tabla seleccionada
        self.tabla_var = tk.StringVar()
        # Combobox para seleccionar la tabla, textvariable es la variable que almacena la tabla seleccionada
        self.tabla_combobox = AutocompleteCombobox(self.main_frame, textvariable=self.tabla_var)
        # Establecer la lista de opciones para el combobox
        self.tabla_combobox.set_completion_list(tablas)
        # Llamar a la función update_productos cuando se selecciona una tabla
        self.tabla_combobox.bind("<<ComboboxSelected>>", self.update_productos)
        # Llamar a la función update_productos cuando se presiona Enter
        self.tabla_combobox.bind("<Return>", self.update_productos)
        # Colocar el combobox en el main_frame
        self.tabla_combobox.place(x=680, y=100)


        # Crear una tabla para mostrar los productos
        self.productos_tree = ttk.Treeview(self.main_frame, columns=('Codigo', 'Linea', 'Producto', 'Precio UD'), show='headings')
        self.productos_tree.heading('Codigo', text='Codigo')
        self.productos_tree.heading('Linea', text='Linea')
        self.productos_tree.heading('Producto', text='Producto')
        self.productos_tree.heading('Precio UD', text='Precio UD')
        self.productos_tree.column('Codigo', width=100)
        self.productos_tree.column('Linea', width=100)
        self.productos_tree.column('Producto', width=400)
        self.productos_tree.column('Precio UD', width=200)
        self.productos_tree.place(x=250, y=150)

        # Scrollbar para la tabla de productos
        scrollbar_productos = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.productos_tree.yview)
        self.productos_tree.configure(yscroll=scrollbar_productos.set)
        scrollbar_productos.place(x=1053, y=150, height=225)

        llenar_treeview_productos(self.productos_tree, Productos)

        # # Botón para agregar un producto
        # add_producto_button = ttk.Button(self.productos_tab, text="Agregar Producto", command=self.agregar_producto)
        # add_producto_button.pack(pady=10)

        # # Botón para modificar un producto
        # modify_producto_button = ttk.Button(self.productos_tab, text="Modificar Producto", command=self.modificar_producto)
        # modify_producto_button.pack(pady=10)

        # # Botón para eliminar un producto
        # delete_producto_button = ttk.Button(self.productos_tab, text="Eliminar Producto", command=self.eliminar_producto)
        # delete_producto_button.pack(pady=10)

        # # Actualizar la tabla de productos
        # self.actualizar_productos()

    def buscar_producto(self, event=None):
        buscar_producto(self.busqueda_producto, self.tabla_var, self.productos_tree, Productos, Categorias)

    def update_productos(self, event=None):
        update_productos(self.tabla_var, self.productos_tree, Productos, Categorias)