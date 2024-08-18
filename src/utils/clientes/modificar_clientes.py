from tkinter import messagebox
import tkinter as tk
from tkinter import ttk

def modificar_cliente(clientes_tree, abrir_ventana_modificacion):
    # Obtener el cliente seleccionado en la tabla
    seleccion = clientes_tree.selection()
    # Si no se seleccionó ningún cliente, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    
    # Obtener los datos del cliente seleccionado
    cliente_data = clientes_tree.item(seleccion)['values']
    # Llamar a la función abrir_ventana_modificacion con los datos del cliente seleccionado
    abrir_ventana_modificacion(cliente_data)

def abrir_ventana_modificacion(cliente_data, main_frame, guardar_cambios):
    # Crear una ventana secundaria para modificar el cliente
    ventana_mod = tk.Toplevel(main_frame)
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
            command=lambda: guardar_cambios(cliente_data[0], nombre_var.get(), cuit_var.get(), 
                                                telefono_var.get(), direccion_var.get(), ventana_mod)).grid(row=4, column=1, pady=10)

def guardar_cambios(nombre_original, nuevo_nombre, nuevo_cuit, nuevo_telefono, nueva_direccion, ventana, session, Clientes, actualizar_clientes):
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
        actualizar_clientes()
        # Cerrar la ventana secundaria
        ventana.destroy()
    else:
        # Mostrar un mensaje de error si no se encontró el cliente
        messagebox.showerror("Error", "No se encontró el cliente.")