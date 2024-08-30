# Widget de productos

import tkinter as tk
from tkinter import ttk, messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from database import Productos, Categorias, session
from utils.remitos.productos import llenar_treeview_productos, update_productos, buscar_producto
from utils.productos.editar_celda import editar_celda
from utils.productos.agregar_producto import agregar_producto
from utils.productos.eliminar_producto import eliminar_producto
from utils.productos.precios import modificar_precios
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
        buscar_producto_label.place(x=250, y=120)

        # Crear un Entry para buscar productos
        self.busqueda_producto = tk.StringVar()
        self.buscar_producto_entry = ttk.Entry(self.main_frame, textvariable=self.busqueda_producto)
        self.buscar_producto_entry.place(x=347, y=120)

        # Vincular la tecla Enter con la función de buscar productos
        self.buscar_producto_entry.bind("<Return>", self.buscar_producto)

        # Botón para buscar productos
        # Cargar la imagen de búsqueda y redimensionarla
        original_search_image = Image.open("./icons/search.png")
        resized_search_image = original_search_image.resize((15, 15), Image.LANCZOS)
        self.search_image = ImageTk.PhotoImage(resized_search_image)

        # El botón llama a la función buscar_producto cuando se hace click
        self.buscar_button = ttk.Button(self.main_frame, image=self.search_image, command=self.buscar_producto)
        self.buscar_button.place(x=480, y=118)

        # Menú de selección de tablas (listas de precios)
        self.tabla_label = ttk.Label(self.main_frame, text="Filtrar por categoría:")
        # Empaquetar la etiqueta en el main_frame con place
        self.tabla_label.place(x=705, y=120)

        # Combobox para seleccionar la categoría

        # Obtener todas las categorías de la base de datos
        tablas = session.query(Categorias).all()

        tablas = [tabla.nombre for tabla in tablas]

        # StringVar para almacenar la tabla seleccionada
        self.tabla_var = tk.StringVar()
        # Combobox para seleccionar la tabla, textvariable es la variable que almacena la tabla seleccionada
        self.tabla_combobox = AutocompleteCombobox(self.main_frame, textvariable=self.tabla_var)
        # Establecer el ancho del combobox
        self.tabla_combobox.config(width=35)
        # Establecer la lista de opciones para el combobox
        self.tabla_combobox.set_completion_list(tablas)
        # Llamar a la función update_productos cuando se selecciona una tabla
        self.tabla_combobox.bind("<<ComboboxSelected>>", self.update_productos)
        # Llamar a la función update_productos cuando se presiona Enter
        self.tabla_combobox.bind("<Return>", self.update_productos)
        # Colocar el combobox en el main_frame
        self.tabla_combobox.place(x=818, y=120)


        # Crear una tabla para mostrar los productos
        self.productos_treeview = ttk.Treeview(self.main_frame, columns=('Codigo', 'Linea', 'Producto', 'Precio UD', 'ID'), show='headings')
        self.productos_treeview.heading('Codigo', text='Codigo')
        self.productos_treeview.heading('Linea', text='Linea')
        self.productos_treeview.heading('Producto', text='Producto')
        self.productos_treeview.heading('Precio UD', text='Precio UD')
        self.productos_treeview.heading('ID', text='ID')
        self.productos_treeview.column('Codigo', width=100, anchor='center')
        self.productos_treeview.column('Linea', width=200, anchor='center')
        self.productos_treeview.column('Producto', width=380, anchor='w')
        self.productos_treeview.column('Precio UD', width=120, anchor='center')
        self.productos_treeview.column('ID', width=0, stretch=tk.NO)
        self.productos_treeview.place(x=250, y=150)

        # Llamar a la función editar_celda cuando se hace doble clic en una celda
        self.productos_treeview.bind("<Double-1>", self.editar_celda)

        # Scrollbar para la tabla de productos
        scrollbar_productos = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.productos_treeview.yview)
        self.productos_treeview.configure(yscroll=scrollbar_productos.set)
        scrollbar_productos.place(x=1053, y=150, height=225)

        llenar_treeview_productos(self.productos_treeview, Productos)

        # Botón para agregar un producto
        add_producto_button = ttk.Button(self.main_frame, text="Agregar Producto", command=lambda: agregar_producto(self))
        add_producto_button.place(x=250, y=400)

        # Botón para eliminar un producto
        delete_producto_button = ttk.Button(self.main_frame, text="Eliminar Producto", command=lambda: eliminar_producto(self))
        delete_producto_button.place(x=370, y=400)

        # Botón para modificar los precios de los productos
        modificar_precios_button = ttk.Button(self.main_frame, text="Modificar Precios", command=lambda: modificar_precios(self.tabla_var, Productos, Categorias, self.update_productos))
        modificar_precios_button.place(x=500, y=400)


    def buscar_producto(self, event=None):
        buscar_producto(self.busqueda_producto, self.tabla_var, self.productos_treeview, Productos, Categorias)

    def update_productos(self, event=None):
        update_productos(self.tabla_var, self.productos_treeview, Productos, Categorias)

    def editar_celda(self, event=None):
        editar_celda(self, event)