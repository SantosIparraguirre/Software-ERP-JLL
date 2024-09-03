import datetime
from tkinter import messagebox

def guardar_presupuesto(cliente_var, carrito, session, Clientes, Presupuestos, DetallesPresupuestos):
    try:
        # Obtener el nombre del cliente seleccionado
        nombre_cliente = cliente_var.get()

        if not nombre_cliente:
            messagebox.showerror("Error", "Selecciona un cliente.")
            return

        # Buscar el cliente en la base de datos
        cliente = session.query(Clientes).filter_by(nombre=nombre_cliente).first()

        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado en la base de datos.")
            return
        
        # Preguntar al usuario si desea guardar el presupuesto
        guardar = messagebox.askyesno("Guardar", "¿Deseas guardar el presupuesto?")
        if not guardar:
            return

        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()

        # Crear un nuevo presupuesto
        nuevo_presupuesto = Presupuestos(id_cliente=cliente.id, fecha=fecha_actual, total=0)

        # Agregar el presupuesto a la base de datos
        session.add(nuevo_presupuesto)
        session.commit()

        total_presupuesto = 0

        # Iterar sobre los elementos del carrito para agregarlos a los detalles del presupuesto
        for producto, cantidad, descuento, precio in carrito:
            cantidad = float(cantidad)
            # Quitamos el signo de pesos y las comas
            precio = precio[1:].replace(',', '') if precio else 0
            # Convertir el precio a flotante
            precio = float(precio) if precio else 0
            # Quitar el signo de porcentaje y convertir a flotante el descuento
            descuento = float(descuento[:-1]) if descuento else 0
            total = cantidad * precio * (1 - descuento / 100)
            detalle = DetallesPresupuestos(
                id_presupuesto=nuevo_presupuesto.id,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                descuento=descuento,
                total=total
            )
            total_presupuesto += total
            session.add(detalle)

        # Actualizar el total del presupuesto
        nuevo_presupuesto.total = total_presupuesto
        session.commit()

        messagebox.showinfo("Éxito", "El presupuesto se ha guardado correctamente en la base de datos.")
    
    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Ocurrió un error al guardar el presupuesto: {str(e)}")