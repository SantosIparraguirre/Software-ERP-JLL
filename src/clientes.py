# Interfaz gráfica para la gestión de clientes

import tkinter as tk
from tkinter import ttk, messagebox
from database import session, Clientes, Presupuestos, DetallesPresupuestos, Remitos, DetallesRemitos
from PIL import Image, ImageTk
from utils.clientes.gestion_clientes import buscar_cliente, agregar_cliente, actualizar_clientes, eliminar_cliente
from utils.clientes.modificar_clientes import abrir_ventana_modificacion, guardar_cambios, modificar_cliente
from utils.clientes.presupuestos_clientes import ver_presupuestos, abrir_ventana_presupuestos, ver_detalles_presupuesto, mostrar_detalles_presupuesto
from utils.clientes.remitos_clientes import ver_remitos, abrir_ventana_remitos, ver_detalles_remito, mostrar_detalles_remito
from utils.clientes.deudas_clientes import ver_deudas

# Clase para la aplicación de gestión de clientes
class ClientesApp(tk.Tk):
    def __init__(self, main_frame):
        # Inicializar la ventana de la aplicación
        self.main_frame = main_frame

        # Etiqueta para buscar un cliente
        self.buscar_label = ttk.Label(self.main_frame, text="BUSCAR CLIENTE")
        self.buscar_label.place(x=90, y=10)

        # Etiqueta para el nombre del cliente a buscar
        self.nombre_buscar_label = ttk.Label(self.main_frame, text="Nombre:")
        self.nombre_buscar_label.place(x=10, y=40)

        # Campo para ingresar el nombre del cliente a buscar
        self.nombre_buscar_var = tk.StringVar()
        self.nombre_buscar_entry = ttk.Entry(self.main_frame, textvariable=self.nombre_buscar_var)
        self.nombre_buscar_entry.place(x=80, y=40)

        # Botón para buscar el cliente
        # Cargar y redimensionar la imagen del botón de búsqueda
        original_search_image = Image.open("./icons/search.png")
        resized_search_image = original_search_image.resize((15, 15), Image.LANCZOS)
        self.search_image = ImageTk.PhotoImage(resized_search_image)

        # El botón llama a la función buscar_cliente cuando se hace click
        self.buscar_cliente_button = ttk.Button(self.main_frame, image=self.search_image, command=self.buscar_cliente)
        self.buscar_cliente_button.place(x=220, y=38)

        # Etiqueta para agregar un cliente
        self.cliente_label = ttk.Label(self.main_frame, text="AGREGAR CLIENTE")
        self.cliente_label.place(x=85, y=70)

        # Etiqueta para el nombre del cliente
        self.nombre_label = ttk.Label(self.main_frame, text="Nombre:")
        self.nombre_label.place(x=10, y=100)

        # Campo para ingresar el nombre del cliente
        self.nombre_var = tk.StringVar()
        self.nombre_entry = ttk.Entry(self.main_frame, textvariable=self.nombre_var)
        self.nombre_entry.place(x=80, y=100)

        # Etiqueta para el CUIT del cliente
        self.cuit_label = ttk.Label(self.main_frame, text="CUIT:")
        self.cuit_label.place(x=10, y=130)

        # Campo para ingresar el CUIT del cliente
        self.cuit_var = tk.StringVar()
        self.cuit_entry = ttk.Entry(self.main_frame, textvariable=self.cuit_var)
        self.cuit_entry.place(x=80, y=130)

        # Etiqueta para el teléfono del cliente
        self.telefono_label = ttk.Label(self.main_frame, text="Teléfono:")
        self.telefono_label.place(x=10, y=160)

        # Campo para ingresar el teléfono del cliente
        self.telefono_var = tk.StringVar()
        self.telefono_entry = ttk.Entry(self.main_frame, textvariable=self.telefono_var)
        self.telefono_entry.place(x=80, y=160)

        # Etiqueta para la dirección del cliente
        self.direccion_label = ttk.Label(self.main_frame, text="Dirección:")
        self.direccion_label.place(x=10, y=190)

        # Campo para ingresar la dirección del cliente
        self.direccion_var = tk.StringVar()
        self.direccion_entry = ttk.Entry(self.main_frame, textvariable=self.direccion_var)
        self.direccion_entry.place(x=80, y=190)

        # Botón para agregar el cliente
        # El botón llama a la función agregar_cliente cuando se hace click
        self.add_cliente_button = ttk.Button(self.main_frame, text="Agregar Cliente", command=self.agregar_cliente)
        self.add_cliente_button.place(x=100, y=220)
    
        # Etiqueta para mostrar los clientes
        self.clientes_label = ttk.Label(self.main_frame, text="CLIENTES")
        self.clientes_label.place(x=580, y=10)

        # Tabla de clientes
        # Treeview con las columnas Nombre, CUIT, Teléfono y Dirección
        self.clientes_tree = ttk.Treeview(self.main_frame, columns=('Nombre', 'CUIT', 'Teléfono', 'Dirección'), show='headings')
        # Encabezados de las columnas
        self.clientes_tree.heading('Nombre', text='Nombre')
        self.clientes_tree.heading('CUIT', text='CUIT')
        self.clientes_tree.heading('Teléfono', text='Teléfono')
        self.clientes_tree.heading('Dirección', text='Dirección')
        # Ancho de las columnas
        self.clientes_tree.column('Nombre', width=200)
        self.clientes_tree.column('CUIT', width=100)
        self.clientes_tree.column('Teléfono', width=100)
        self.clientes_tree.column('Dirección', width=200)
        self.clientes_tree.place(x=300, y=40)

        # Scrollbar para la tabla de clientes
        # Scrollbar en el eje vertical que se conecta con la tabla de clientes y se mueve con ella
        scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.clientes_tree.yview)
        # Configurar la scrollbar para que se mueva junto con la tabla de clientes en el eje y (vertical)
        self.clientes_tree.configure(yscroll=scrollbar.set)
        scrollbar.place(x=903, y=40, relheight=0.32)

        # Botón para eliminar un cliente
        # El botón llama a la función eliminar_cliente cuando se hace click
        self.delete_cliente_button = ttk.Button(self.main_frame, text="Eliminar Cliente", command=self.eliminar_cliente)
        self.delete_cliente_button.place(x=940, y=50)

        # Botón para modificar un cliente
        # El botón llama a la función modificar_cliente cuando se hace click
        self.modify_cliente_button = ttk.Button(self.main_frame, text="Modificar Cliente", command=self.modificar_cliente)
        self.modify_cliente_button.place(x=940, y=80)

        # Botón para ver los presupuestos de un cliente
        # El botón llama a la función ver_presupuestos cuando se hace click
        self.ver_presupuestos_button = ttk.Button(self.main_frame, text="Ver Presupuestos", command=self.ver_presupuestos)
        self.ver_presupuestos_button.place(x=940, y=110)

        # Botón para ver los remitos de un cliente
        # El botón llama a la función ver_remitos cuando se hace click
        self.ver_remitos_button = ttk.Button(self.main_frame, text="Ver Remitos", command=self.ver_remitos)
        self.ver_remitos_button.place(x=940, y=140)

        # Botón para ver las deudas de un cliente
        # El botón llama a la función ver_deudas cuando se hace click
        self.ver_deudas_button = ttk.Button(self.main_frame, text="Ver Deudas", command=self.ver_deudas)
        self.ver_deudas_button.place(x=940, y=170)

        # Actualizar la tabla de clientes
        self.actualizar_clientes()

    # Funciones importadas de los módulos de utilidades

    # Función para buscar un cliente
    def buscar_cliente(self):
        # Llamar a la función buscar_cliente con el nombre del cliente a buscar, la tabla de clientes, la sesión y la clase Clientes
        buscar_cliente(self.nombre_buscar_var, self.clientes_tree, session, Clientes)

    # Función para agregar un cliente
    def agregar_cliente(self):
        # Llamar a la función agregar_cliente con los datos del cliente a agregar, la sesión y la clase Clientes
        agregar_cliente(self.nombre_var, self.cuit_var, self.telefono_var, self.direccion_var, session, Clientes)
        # Actualizar la tabla de clientes
        self.actualizar_clientes()

    # Función para actualizar la tabla de clientes
    def actualizar_clientes(self):
        # Llamar a la función actualizar_clientes con la tabla de clientes, la sesión y la clase Clientes
        actualizar_clientes(self.clientes_tree, session, Clientes)

    # Función para eliminar un cliente
    def eliminar_cliente(self):
        # Llamar a la función eliminar_cliente con la tabla de clientes, la sesión, la clase Clientes y la clase Presupuestos
        eliminar_cliente(self.clientes_tree, session, Clientes, Presupuestos)
        # Actualizar la tabla de clientes
        self.actualizar_clientes()

    # Función para modificar un cliente
    def modificar_cliente(self):
        # Llamar a la función modificar_cliente con la tabla de clientes, la función abrir_ventana_modificacion y la función guardar_cambios
        modificar_cliente(self.clientes_tree,
                          # Función para abrir la ventana de modificación de un cliente con los datos del cliente seleccionado y la ventana principal
                           lambda cliente_data: abrir_ventana_modificacion(
                               cliente_data, 
                               self.main_frame, 
                               lambda nombre_original, 
                               nuevo_nombre, 
                               nuevo_cuit, 
                               nuevo_telefono, 
                               nueva_direccion, 
                # Función para guardar los cambios realizados en la ventana de modificación de un cliente con los datos del cliente seleccionado 
                               ventana: guardar_cambios(
                                        nombre_original,
                                        nuevo_nombre,
                                        nuevo_cuit,
                                        nuevo_telefono,
                                        nueva_direccion,
                                        ventana,
                                        session,
                                        Clientes, 
                                        self.actualizar_clientes)))

    # Función abrir la ventana de modificación
    def abrir_ventana_modificacion(self, cliente_data):
        # Llamar a la función abrir_ventana_modificacion con los datos del cliente seleccionado, la ventana principal y la función para guardar los cambios
        abrir_ventana_modificacion(
            cliente_data,
            self.main_frame, 
            lambda nombre_original, 
            nuevo_nombre, 
            nuevo_cuit, 
            nuevo_telefono, 
            nueva_direccion, 
            # Función para guardar los cambios realizados en la ventana de modificación de un cliente con los datos del cliente seleccionado
            ventana: guardar_cambios(
                nombre_original, 
                nuevo_nombre, 
                nuevo_cuit, 
                nuevo_telefono, 
                nueva_direccion, 
                ventana, 
                session, 
                Clientes, 
                self.actualizar_clientes))
    
    # Función para guardar los cambios realizados en la ventana de modificación
    def guardar_cambios(self, nombre_original, nuevo_nombre, nuevo_cuit, nuevo_telefono, nueva_direccion, ventana):
        # Llamar a la función guardar_cambios con los datos del cliente seleccionado, la ventana de modificación, la sesión, la clase Clientes y la función para actualizar la tabla de clientes
        guardar_cambios(nombre_original, nuevo_nombre, nuevo_cuit, nuevo_telefono, nueva_direccion, ventana, session, Clientes, self.actualizar_clientes)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def ver_presupuestos(self):
        # Llamar a la función ver_presupuestos
        ver_presupuestos(self)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def abrir_ventana_presupuestos(self, nombre):
        # Llamar a la función abrir_ventana_presupuestos con el nombre del cliente
        abrir_ventana_presupuestos(self, nombre)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def ver_detalles_presupuesto(self, presupuestos_tree, detalles_tree):
        # Llamar a la función ver_detalles_presupuesto con la tabla de presupuestos y la tabla de detalles
        ver_detalles_presupuesto(self, presupuestos_tree, detalles_tree)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def mostrar_detalles_presupuesto(self, ID, detalles_tree):
        # Llamar a la función mostrar_detalles_presupuesto con el ID del presupuesto y la tabla de detalles
        mostrar_detalles_presupuesto(self, ID, detalles_tree)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def ver_remitos(self):
        # Llamar a la función ver_remitos
        ver_remitos(self)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def abrir_ventana_remitos(self, nombre):
        # Llamar a la función abrir_ventana_remitos con el nombre del cliente
        abrir_ventana_remitos(self, nombre)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def ver_detalles_remito(self, remitos_tree, detalles_tree):
        # Llamar a la función ver_detalles_remito con la tabla de remitos y la tabla de detalles
        ver_detalles_remito(self, remitos_tree, detalles_tree)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def mostrar_detalles_remito(self, ID, detalles_tree):
        # Llamar a la función mostrar_detalles_remito con el ID del remito y la tabla de detalles
        mostrar_detalles_remito(self, ID, detalles_tree)

    # Funciones para ver los presupuestos, remitos y deudas de un cliente
    def ver_deudas(self):
        # Llamar a la función ver_deudas
        ver_deudas(self)