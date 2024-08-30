import tkinter as tk
from tkinter import ttk, messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from database import session, Productos, Categorias, Clientes, Presupuestos, DetallesPresupuestos, Remitos, DetallesRemitos
from PIL import Image, ImageTk
from clientes import ClientesWidget
from productos import ProductosWidget
from utils.remitos.carrito import agregar_al_carrito, actualizar_carrito, agregar_fuera_lista, eliminar_del_carrito, editar_celda
from utils.remitos.productos import update_productos, buscar_producto, llenar_treeview_productos
from utils.remitos.guardar_remitos import guardar_remito
from utils.remitos.generar_remitos import generar_remito_excel
from utils.remitos.guardar_presupuestos import guardar_presupuesto
from utils.remitos.generar_presupuestos import generar_presupuesto_excel


# Clase para la interfaz
class RemitosApp(tk.Tk):
    def __init__(self):
        # Inicializar la ventana principal
        super().__init__()
        # Título de la ventana
        self.title("Constructora Jose Luis Lopez")
        # Geometría de la ventana
        self.geometry("1300x600")
        # Bloquear el tamaño de la ventana
        self.resizable(False, False)
        # Crear los widgets con la función create_widgets
        self.create_widgets()
        # Lista para almacenar los productos del carrito
        self.carrito = []
        # Lista para almacenar los precios anteriores antes de un aumento
        self.precios_anteriores = []

    def create_widgets(self):
        # Menú superior
        # Frame para el menú superior con un alto de 50 y color de fondo gris
        self.menu_superior = tk.Frame(self, height=50, bg='gray')
        # Empaquetar el frame en la ventana principal en la parte superior y que se expanda en el eje x
        self.menu_superior.pack(side='top', fill='x')

        # Botón para mostrar remitos
        self.remitos_button = ttk.Button(self.menu_superior, text="Remitos", command=self.mostrar_remitos)
        self.remitos_button.pack(side='left', padx=10, pady=10)

        # Botón para mostrar clientes
        self.clientes_button = ttk.Button(self.menu_superior, text="Clientes", command=self.mostrar_clientes)
        self.clientes_button.pack(side='left', padx=10, pady=10)

        # Botón para mostrar listas de precios de productos
        self.listas_precios_button = ttk.Button(self.menu_superior, text="Productos", command=self.mostrar_productos)
        self.listas_precios_button.pack(side='left', padx=10, pady=10)

        # Frame principal
        self.main_frame = tk.Frame(self)
        # Empaquetar el frame principal en la ventana principal
        self.main_frame.pack(side='top', fill='both', expand=True)


    def mostrar_remitos(self):
        # Limpiar el main_frame antes de agregar nuevos widgets para evitar superposiciones
        for widget in self.main_frame.winfo_children():
            # Destruir el widget
            widget.destroy()

        # Etiqueta para el nombre del cliente
        self.cliente_label = ttk.Label(self.main_frame, text="Nombre del Cliente:")
        self.cliente_label.place(x=10, y=10)
        
        # Combobox para seleccionar el cliente
        self.cliente_var = tk.StringVar()
        self.cliente_combobox = AutocompleteCombobox(self.main_frame, textvariable=self.cliente_var)
        # Establecer la lista de opciones para el combobox con los nombres de los clientes
        self.cliente_combobox.set_completion_list(self.obtener_nombres_clientes())
        self.cliente_combobox.place(x=135, y=10)

        # Menú de selección de tablas (listas de precios)
        self.tabla_label = ttk.Label(self.main_frame, text="Filtrar por categoría:")
        # Empaquetar la etiqueta en el main_frame con place
        self.tabla_label.place(x=10, y=70)

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
        self.tabla_combobox.place(x=135, y=70)

        # Etiqueta de búsqueda
        self.busqueda_label = ttk.Label(self.main_frame, text="Buscar un producto:")
        self.busqueda_label.place(x=10, y=130)

        # Campo de búsqueda
        # StringVar para almacenar el valor ingresado en el campo de búsqueda 
        self.busqueda_var = tk.StringVar()
        # Entry para ingresar el término de búsqueda, textvariable es la variable que almacena el valor ingresado
        self.busqueda_entry = ttk.Entry(self.main_frame, textvariable=self.busqueda_var)
        self.busqueda_entry.place(x=135, y=130)

        # Vincular la tecla Enter con la función buscar_producto
        self.busqueda_entry.bind("<Return>", self.buscar_producto)

        # Botón para buscar productos
        # Cargar la imagen de búsqueda y redimensionarla
        original_search_image = Image.open("./icons/search.png")
        resized_search_image = original_search_image.resize((15, 15), Image.LANCZOS)
        self.search_image = ImageTk.PhotoImage(resized_search_image)

        # El botón llama a la función buscar_producto cuando se hace click
        self.buscar_button = ttk.Button(self.main_frame, image=self.search_image, command=self.buscar_producto)
        self.buscar_button.place(x=270, y=128)

        # Tabla de productos
        # Treeview con las columnas Producto y Precio
        self.productos_tree = ttk.Treeview(self.main_frame, columns=('Codigo', 'Linea', 'Producto', 'Precio UD'), show='headings')
        # Encabezados de las columnas
        self.productos_tree.heading('Codigo', text='Codigo')
        self.productos_tree.heading('Linea', text='Linea')
        self.productos_tree.heading('Producto', text='Producto')
        self.productos_tree.heading('Precio UD', text='Precio UD')
        # Ancho de las columnas
        self.productos_tree.column('Codigo', anchor='center', width=50)
        self.productos_tree.column('Linea', anchor='center', width=70)
        self.productos_tree.column('Producto', width=350)
        self.productos_tree.column('Precio UD', anchor='center', width=100)
        self.productos_tree.place(x=10, y=160)

        # Scrollbar para la tabla de productos
        # Scrollbar en el eje vertical que se conecta con la tabla de productos y se mueve con ella
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.productos_tree.yview)
        # Configurar la scrollbar para que se mueva junto con la tabla de productos en el eje y (vertical)
        self.productos_tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=582, y=162, relheight=0.40)

        # Llamar a la función llenar_treeview_productos para mostrar los productos en la tabla
        llenar_treeview_productos(self.productos_tree, Productos)

        # Etiqueta de cantidad
        self.cantidad_label = ttk.Label(self.main_frame, text="Cantidad:")
        self.cantidad_label.place(x=10, y=400)

        # Campo de cantidad
        # IntVar para almacenar el valor ingresado en el campo de cantidad 
        self.cantidad_var = tk.IntVar()
        # Entry para ingresar la cantidad, textvariable es la variable que almacena el valor ingresado
        self.cantidad_entry = ttk.Entry(self.main_frame, textvariable=self.cantidad_var)
        self.cantidad_entry.place(x=115, y=400)
        # Llamar a la función agregar_al_carrito cuando se presiona Enter
        self.cantidad_entry.bind("<Return>", self.agregar_al_carrito)

        # Etiqueta de descuento
        self.descuento_label = ttk.Label(self.main_frame, text="Descuento (%):")
        self.descuento_label.place(x=10, y=430)

        # Campo de descuento
        # DoubleVar para almacenar el valor ingresado en el campo de descuento
        self.descuento_var = tk.DoubleVar()
        # Entry para ingresar el descuento, textvariable es la variable que almacena el valor ingresado
        self.descuento_entry = ttk.Entry(self.main_frame, textvariable=self.descuento_var)
        self.descuento_entry.place(x=115, y=430)
        # Llamar a la función agregar_al_carrito cuando se presiona Enter
        self.descuento_entry.bind("<Return>", self.agregar_al_carrito)

        # Botón para agregar al carrito
        # El botón llama a la función agregar_al_carrito cuando se hace click
        self.add_button = ttk.Button(self.main_frame, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.add_button.place(x=260, y=398)

        # Logo de la empresa
        # Cargar la imagen del logo y redimensionarla
        # original_logo = Image.open("./icons/logo.png")
        # resized_logo = original_logo.resize((600, 100), Image.LANCZOS)
        # self.logo = ImageTk.PhotoImage(resized_logo)
        # Etiqueta para mostrar el logo
        self.logo = ImageTk.PhotoImage(file="./icons/logo.png")
        self.logo_label = ttk.Label(self.main_frame, image=self.logo)
        self.logo_label.place(x=375, y=30)

        # Carrito

        # Agregar productos fuera de lista
        # Etiqueta de productos fuera de lista
        self.productos_fuera_lista_label = ttk.Label(self.main_frame, text="PRODUCTOS FUERA DE LISTA")
        self.productos_fuera_lista_label.place(x=990, y=10)

        # Etiqueta para nombre del producto
        self.producto_label = ttk.Label(self.main_frame, text="Producto:")
        self.producto_label.place(x=970, y=40)

        # Campo para ingresar el nombre del producto
        self.producto_var = tk.StringVar()
        self.producto_entry = ttk.Entry(self.main_frame, textvariable=self.producto_var)
        self.producto_entry.place(x=1035, y=40)

        # Etiqueta para cantidad del producto
        self.cantidad_fuera_lista_label = ttk.Label(self.main_frame, text="Cantidad:")
        self.cantidad_fuera_lista_label.place(x=970, y=70)

        # Campo para ingresar la cantidad del producto
        self.cantidad_fuera_lista_var = tk.IntVar()
        self.cantidad_fuera_lista_entry = ttk.Entry(self.main_frame, textvariable=self.cantidad_fuera_lista_var)
        self.cantidad_fuera_lista_entry.place(x=1035, y=70)

        # Etiqueta para precio del producto
        self.precio_label = ttk.Label(self.main_frame, text="Precio:")
        self.precio_label.place(x=970, y=100)

        # Campo para ingresar el precio del producto
        self.precio_var = tk.DoubleVar()
        self.precio_entry = ttk.Entry(self.main_frame, textvariable=self.precio_var)
        self.precio_entry.place(x=1035, y=100)

        # Llamar a la función agregar_fuera_lista cuando se presiona Enter
        self.precio_entry.bind("<Return>", self.agregar_fuera_lista)

        # Botón para agregar productos fuera de lista
        self.add_fuera_lista_button = ttk.Button(self.main_frame, text="Agregar al Carrito", command=self.agregar_fuera_lista)
        self.add_fuera_lista_button.place(x=1170, y=68)

        # Etiqueta "CARRITO"
        self.carrito_label = ttk.Label(self.main_frame, text="CARRITO")
        self.carrito_label.place(x=890, y=133)

        # Botón para borrar del carrito
        # El botón llama a la función eliminar_del_carrito cuando se hace click
        self.delete_button = ttk.Button(self.main_frame, text="Eliminar Producto", command=self.eliminar_del_carrito)
        self.delete_button.place(x=965, y=130)


        # Botón para limpiar el carrito
        self.clear_button = ttk.Button(self.main_frame, text="Limpiar Carrito", command=self.limpiar_carrito)
        self.clear_button.place(x=1080, y=130)

        # Treeview para mostrar los productos del carrito
        self.carrito_treeview = ttk.Treeview(self.main_frame, columns=('Producto', 'Cantidad', 'Descuento', 'Precio UD', 'Total'), show='headings')
        # Encabezados de las columnas
        self.carrito_treeview.heading('Producto', text='Producto')
        self.carrito_treeview.heading('Cantidad', text='Cantidad')
        self.carrito_treeview.heading('Descuento', text='Descuento')
        self.carrito_treeview.heading('Precio UD', text='Precio UD')
        self.carrito_treeview.heading('Total', text='Total')
        # Ancho de las columnas
        self.carrito_treeview.column('Producto', width=340)
        self.carrito_treeview.column('Cantidad', anchor='center', width=60)
        self.carrito_treeview.column('Descuento', anchor='center', width=70)
        self.carrito_treeview.column('Precio UD', anchor='center', width=100)
        self.carrito_treeview.column('Total', anchor='center', width=100)
        self.carrito_treeview.place(x=600, y=160)

        # Actualizar la lista de productos del carrito
        self.actualizar_carrito()

        # Vincular el evento Double-1 (doble clic) con la función editar_celda
        self.carrito_treeview.bind("<Double-1>", self.editar_celda)
        # Vincular la tecla suprimir con la función eliminar_del_carrito
        self.carrito_treeview.bind("<Delete>", self.eliminar_del_carrito)

        # Scrollbar para la lista de productos del carrito
        # Scrollbar en el eje vertical que se conecta con la lista de productos del carrito y se mueve con ella
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.carrito_treeview.yview)
        # Configurar la scrollbar para que se mueva junto con la lista de productos del carrito en el eje y (vertical)
        self.carrito_treeview.configure(yscroll=scrollbar.set)
        scrollbar.place(x=1273, y=162, relheight=0.40)

        # Combobox de observaciones
        # Tres opciones para las observaciones
        observaciones = ["Retirado", "A retirar", "Devolución"]
        # Etiqueta para seleccionar la observación
        self.observaciones_label = ttk.Label(self.main_frame, text="Observaciones:")
        self.observaciones_label.place(x=600, y=402)
        # StringVar para almacenar la observación seleccionada
        self.observaciones_var = tk.StringVar()
        # Combobox para seleccionar la observación, textvariable es la variable que almacena la observación seleccionada
        self.observaciones_combobox = ttk.Combobox(self.main_frame, textvariable=self.observaciones_var, values=observaciones, width=12)
        self.observaciones_combobox.place(x=690, y=402)

        # Botón para guardar el presupuesto en la base de datos
        self.save_presupuesto_button = ttk.Button(self.main_frame, text="Guardar Presupuesto", command=self.guardar_presupuesto)
        self.save_presupuesto_button.place(x=860, y=400)

        # Botón para guardar el remito en la base de datos
        self.save_remito_button = ttk.Button(self.main_frame, text="Guardar Remito", command=self.guardar_remito)
        self.save_remito_button.place(x=990, y=400)

    # Funciones para interactuar con la base de datos y la interfaz

    # Obtener los nombres de los clientes de la base de datos
    def obtener_nombres_clientes(self):
        clientes = session.query(Clientes.nombre).all()
        return [cliente[0] for cliente in clientes]

    # # Funciones para interactuar con la base de datos y la interfaz
    # def modificar_precios(self):
    #     # Llamar a la función modificar_precios con la tabla seleccionada, los precios anteriores y las clases de Productos y Categorias
    #     modificar_precios(self.tabla_var, self.precios_anteriores, Categorias, Productos)
    #     # Actualizar la lista de productos
    #     self.update_productos(None)

    # Función para agregar productos fuera de lista al carrito
    def agregar_fuera_lista(self, event=None):
        # Llamar a la función agregar_fuera_lista con el carrito, el nombre del producto, la cantidad, y el precio
        agregar_fuera_lista(self.carrito, self.producto_var, self.cantidad_fuera_lista_var, self.precio_var)
        # Actualizar la lista de productos del carrito
        self.actualizar_carrito()

    # Función para actualizar la lista de productos
    def update_productos(self, event=None):
        # Llamar a la función update_productos con la tabla seleccionada, la tabla de productos, las clases de Productos y Categorias, y el evento
        update_productos(self.tabla_var, self.productos_tree, Productos, Categorias, event)

    # Función para buscar un producto en la lista de productos
    def buscar_producto(self, event=None):
        # Llamar a la función buscar_producto con el término de búsqueda, la tabla seleccionada, la tabla de productos, las clases de Productos y Categorias
        buscar_producto(self.busqueda_var, self.tabla_var, self.productos_tree, Productos, Categorias)

    # Funciones para interactuar con el carrito
    def agregar_al_carrito(self, event=None):
        # Llamar a la función agregar_al_carrito con el carrito, la tabla de productos, la cantidad y el descuento
        agregar_al_carrito(self.carrito, self.productos_tree, self.cantidad_var, self.descuento_var)
        # Actualizar la lista de productos del carrito
        self.actualizar_carrito()

    # Función para actualizar la lista de productos del carrito
    def actualizar_carrito(self):
        # Llamar a la función actualizar_carrito con el treeview del carrito y la lista de productos del carrito
        actualizar_carrito(self.carrito_treeview, self.carrito)

    # Funciones para interactuar con el carrito
    def eliminar_del_carrito(self, event=None):
        # Llamar a la función eliminar_del_carrito con el carrito y el treeview del carrito
        eliminar_del_carrito(self.carrito, self.carrito_treeview)
        # Actualizar la lista de productos del carrito
        self.actualizar_carrito()

    # Función para limpiar el carrito
    def limpiar_carrito(self):
        # Mostrar un mensaje de confirmación antes de limpiar el carrito
        confirmacion = messagebox.askyesno("Confirmar", "¿Estás seguro de limpiar el carrito?")
        if not confirmacion:
            return
        # Limpiar la lista de productos del carrito
        self.carrito = []
        # Actualizar la lista de productos del carrito
        self.actualizar_carrito()
    
    # Función para editar una celda del carrito
    def editar_celda(self, event=None):
        # Llamar a la función editar_celda con el evento
        editar_celda(self, event)

    # Función para guardar el remito en la base de datos
    def guardar_remito(self):
        # Llamar a la función guardar_remito con el cliente seleccionado, el carrito, la sesión y las clases de Clientes, Remitos y DetallesRemitos
        guardar_remito(self.cliente_var, self.carrito, session, Clientes, Remitos, DetallesRemitos) 
        # Llamar a la función generar_remito_excel con el cliente seleccionado, el carrito, la sesión y las clases de Clientes
        generar_remito_excel(self.cliente_var, self.carrito, self.observaciones_var, session, Clientes)

    # Función para guardar el presupuesto en la base de datos
    def guardar_presupuesto(self):
        # Llamar a la función guardar_presupuesto con el cliente seleccionado, el carrito, la sesión y las clases de Clientes, Presupuestos y DetallesPresupuestos
        guardar_presupuesto(self.cliente_var, self.carrito, session, Clientes, Presupuestos, DetallesPresupuestos)
        # Llamar a la función generar_presupuesto_excel con el cliente seleccionado, el carrito, la sesión y las clases de Clientes
        generar_presupuesto_excel(self.cliente_var, self.carrito, session, Clientes)

    # Función para mostrar los clientes
    def mostrar_clientes(self):
        # Limpiar el main_frame antes de agregar nuevos widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Crear una instancia de ClientesWidget y agregar sus widgets al main_frame
        self.clientes_app = ClientesWidget(self.main_frame)     

    # Función para mostrar las listas de precios de productos
    def mostrar_productos(self):
        # Limpiar el main_frame antes de agregar nuevos widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Crear una instancia de ProductosWidget y agregar sus widgets al main_frame
        self.productos_app = ProductosWidget(self.main_frame)

# Función principal para ejecutar la aplicación
# Si el script se ejecuta directamente, se crea una instancia de la clase RemitosApp y se llama al método mainloop
if __name__ == "__main__":
    app = RemitosApp()
    app.mainloop()
