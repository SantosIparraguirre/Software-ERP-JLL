import tkinter as tk
from tkinter import ttk, messagebox
from database import session
from database import Clientes
from PIL import Image, ImageTk

class ClientesApp(tk.Tk):
    def __init__(self, main_frame):
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

        # Actualizar la tabla de clientes
        self.actualizar_clientes()

    # Función para buscar un cliente
    def buscar_cliente(self):
        # Obtener el nombre del cliente a buscar
        nombre = self.nombre_buscar_var.get()
        # Buscar todos los nombres de clientes que contengan parte del nombre ingresado
        clientes = session.query(Clientes).filter(Clientes.nombre.like(f'%{nombre}%')).all()
        # Limpiar la tabla de clientes
        self.clientes_tree.delete(*self.clientes_tree.get_children())
        # Iterar sobre los clientes encontrados y agregarlos a la tabla de clientes
        for cliente in clientes:
            self.clientes_tree.insert('', 'end', values=(cliente.nombre, cliente.cuit, cliente.telefono, cliente.direccion))

    def agregar_cliente(self):
        # Obtener los datos del cliente ingresados por el usuario
        nombre = self.nombre_var.get()
        cuit = self.cuit_var.get()
        telefono = self.telefono_var.get()
        direccion = self.direccion_var.get()

        # Validar que el nombre no esté vacío
        if not nombre:
            messagebox.showerror("Error", "Ingresa un nombre.")
            return

        # Crear una instancia de la clase Cliente con los datos ingresados
        cliente = Clientes(nombre=nombre, cuit=cuit, telefono=telefono, direccion=direccion)
        # Agregar el cliente a la sesión
        session.add(cliente)
        # Confirmar la transacción
        session.commit()
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Cliente agregado exitosamente.")
        # Actualizar la tabla de clientes
        self.actualizar_clientes()

    # Función para actualizar la tabla de clientes
    def actualizar_clientes(self):
        # Limpiar la tabla de clientes
        self.clientes_tree.delete(*self.clientes_tree.get_children())
        # Obtener todos los clientes de la base de datos
        clientes = session.query(Clientes).all()
        # Iterar sobre los clientes y agregarlos a la tabla de clientes
        for cliente in clientes:
            self.clientes_tree.insert('', 'end', values=(cliente.nombre, cliente.cuit, cliente.telefono, cliente.direccion))

    # Función para eliminar un cliente
    def eliminar_cliente(self):
        # Obtener el cliente seleccionado en la tabla
        seleccion = self.clientes_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un cliente.")
            return
        # Obtener el nombre del cliente seleccionado
        nombre = self.clientes_tree.item(seleccion)['values'][0]
        # Buscar el cliente en la base de datos por el nombre
        cliente = session.query(Clientes).filter_by(nombre=nombre).first()
        # Eliminar el cliente de la sesión
        session.delete(cliente)
        # Confirmar la transacción
        session.commit()
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")
        # Actualizar la tabla de clientes
        self.actualizar_clientes()

    # Función para modificar un cliente
    def modificar_cliente(self):
        # Obtener el cliente seleccionado en la tabla
        seleccion = self.clientes_tree.selection()
        # Si no se seleccionó ningún cliente, mostrar un mensaje de error
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un cliente.")
            return
        
        # Obtener los datos del cliente seleccionado
        cliente_data = self.clientes_tree.item(seleccion)['values']
        # Llamar a la función abrir_ventana_modificacion con los datos del cliente seleccionado
        self.abrir_ventana_modificacion(cliente_data)

    def abrir_ventana_modificacion(self, cliente_data):
        # Crear una ventana secundaria para modificar el cliente
        ventana_mod = tk.Toplevel(self.main_frame)
        # Configurar el título y las dimensiones de la ventana
        ventana_mod.title("Modificar Cliente")
        ventana_mod.geometry("300x200")

        # Crear etiquetas y campos de entrada para los datos del cliente
        ttk.Label(ventana_mod, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
        # Establecer el valor del campo de entrada con el nombre del cliente seleccionado
        nombre_var = tk.StringVar(value=cliente_data[0])
        # Crear un campo de entrada con el nombre del cliente seleccionado
        ttk.Entry(ventana_mod, textvariable=nombre_var).grid(row=0, column=1, padx=5, pady=5)

        # Crear etiquetas y campos de entrada para el CUIT, teléfono y dirección del cliente
        ttk.Label(ventana_mod, text="CUIT:").grid(row=1, column=0, padx=5, pady=5)
        # Establecer el valor del campo de entrada con el CUIT del cliente seleccionado
        cuit_var = tk.StringVar(value=cliente_data[1])
        # Crear un campo de entrada con el CUIT del cliente seleccionado
        ttk.Entry(ventana_mod, textvariable=cuit_var).grid(row=1, column=1, padx=5, pady=5)

        # Crear etiquetas y campos de entrada para el teléfono y dirección del cliente
        ttk.Label(ventana_mod, text="Teléfono:").grid(row=2, column=0, padx=5, pady=5)
        # Establecer el valor del campo de entrada con el teléfono del cliente seleccionado
        telefono_var = tk.StringVar(value=cliente_data[2])
        # Crear un campo de entrada con el teléfono del cliente seleccionado
        ttk.Entry(ventana_mod, textvariable=telefono_var).grid(row=2, column=1, padx=5, pady=5)

        # Crear etiquetas y campos de entrada para la dirección del cliente
        ttk.Label(ventana_mod, text="Dirección:").grid(row=3, column=0, padx=5, pady=5)
        # Establecer el valor del campo de entrada con la dirección del cliente seleccionado
        direccion_var = tk.StringVar(value=cliente_data[3])
        # Crear un campo de entrada con la dirección del cliente seleccionado
        ttk.Entry(ventana_mod, textvariable=direccion_var).grid(row=3, column=1, padx=5, pady=5)

        # Botón para guardar los cambios
        ttk.Button(ventana_mod, text="Guardar Cambios", 
                   # Llamar a la función guardar_cambios con los datos del cliente seleccionado y la ventana secundaria
                command=lambda: self.guardar_cambios(cliente_data[0], nombre_var.get(), cuit_var.get(), 
                                                        telefono_var.get(), direccion_var.get(), ventana_mod)).grid(row=4, column=1, pady=10)

    def guardar_cambios(self, nombre_original, nuevo_nombre, nuevo_cuit, nuevo_telefono, nueva_direccion, ventana):
        # Buscar el cliente en la base de datos por el nombre original
        cliente = session.query(Clientes).filter_by(nombre=nombre_original).first()
        if cliente:
            # Actualizar los datos del cliente con los nuevos datos ingresados
            cliente.nombre = nuevo_nombre
            cliente.cuit = nuevo_cuit
            cliente.telefono = nuevo_telefono
            cliente.direccion = nueva_direccion
            # Confirmar la transacción
            session.commit()
            # Mostrar un mensaje de éxito
            messagebox.showinfo("Éxito", "Cliente modificado exitosamente.")
            # Actualizar la tabla de clientes
            self.actualizar_clientes()
            # Cerrar la ventana secundaria
            ventana.destroy()
        else:
            # Mostrar un mensaje de error si no se encontró el cliente
            messagebox.showerror("Error", "No se encontró el cliente.")