import tkinter.messagebox as messagebox
from sqlalchemy import func

def buscar_cliente(nombre_buscar_var, clientes_tree, session, Clientes):
    # Obtener el nombre del cliente a buscar
    nombre = nombre_buscar_var.get()
    # Buscar todos los nombres de clientes que contengan parte del nombre ingresado
    clientes = session.query(Clientes).filter(Clientes.nombre.like(f'%{nombre}%')).all()
    # Limpiar la tabla de clientes
    clientes_tree.delete(*clientes_tree.get_children())
    # Iterar sobre los clientes encontrados y agregarlos a la tabla de clientes
    for cliente in clientes:
        clientes_tree.insert('', 'end', values=(cliente.nombre, cliente.cuit, cliente.telefono, cliente.direccion))

def agregar_cliente(nombre_var, cuit_var, telefono_var, direccion_var, session, Clientes):
    # Obtener los datos del cliente ingresados por el usuario
    nombre = nombre_var.get().strip()
    cuit = cuit_var.get().strip()
    telefono = telefono_var.get().strip()
    direccion = direccion_var.get().strip()

    # Validar que el nombre no esté vacío
    if not nombre:
        messagebox.showerror("Error", "Ingresa un nombre.")
        return
    
    # Validar que el nombre no esté repetido 
    cliente = session.query(Clientes).filter(func.lower(Clientes.nombre) == nombre.lower()).first()
    if cliente:
        messagebox.showerror("Error", "Ya existe un cliente con el mismo nombre.")
        return

    # Crear una instancia de la clase Cliente con los datos ingresados
    cliente = Clientes(nombre=nombre, cuit=cuit, telefono=telefono, direccion=direccion)
    # Agregar el cliente a la sesión
    session.add(cliente)
    # Confirmar la transacción
    session.commit()
    # Mostrar un mensaje de éxito
    messagebox.showinfo("Éxito", "Cliente agregado exitosamente.")

def actualizar_clientes(clientes_tree, session, Clientes):
    # Limpiar la tabla de clientes
    clientes_tree.delete(*clientes_tree.get_children())
    # Obtener todos los clientes de la base de datos
    clientes = session.query(Clientes).all()
    # Ordenarlos alfabeticamente
    clientes = sorted(clientes, key=lambda x: x.nombre)
    # Iterar sobre los clientes y agregarlos a la tabla de clientes
    for cliente in clientes:
        clientes_tree.insert('', 'end', values=(cliente.nombre, cliente.cuit, cliente.telefono, cliente.direccion))

def eliminar_cliente(clientes_tree, session, Clientes, Presupuestos):
    try:
        # Obtener el cliente seleccionado en la tabla
        seleccion = clientes_tree.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un cliente.")
            return
        # Obtener el nombre del cliente seleccionado
        nombre = clientes_tree.item(seleccion)['values'][0]
        # Preguntar al usuario si está seguro de eliminar el cliente
        confirmacion = messagebox.askyesno("Confirmación", f"¿Estás seguro de eliminar al cliente {nombre}?")
        if not confirmacion:
            return
        # Buscar el cliente en la base de datos por el nombre
        cliente = session.query(Clientes).filter_by(nombre=nombre).first()
        
        # Eliminar los presupuestos relacionados con el cliente
        session.query(Presupuestos).filter_by(id_cliente=cliente.id).delete()
        
        # Eliminar el cliente de la sesión
        session.delete(cliente)
        # Confirmar la transacción
        session.commit()
        # Mostrar un mensaje de éxito
        messagebox.showinfo("Éxito", "Cliente eliminado exitosamente.")

    except Exception:
        session.rollback()
        messagebox.showerror("Error", "No se puede eliminar el cliente porque tiene presupuestos o remitos asociados.")