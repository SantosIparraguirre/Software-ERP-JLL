import datetime
from tkinter import messagebox

def guardar_remito(cliente_var, carrito, observaciones, session, Clientes, Remitos, DetallesRemitos):
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

        # Preguntar al usuario si el remito se pagó o no
        pago = messagebox.askyesno("Pago", "¿El remito se pagó?")
        pago = "SI" if pago else "NO"

        # Preguntar al usuario si desea guardar el remito
        guardar = messagebox.askyesno("Guardar", "¿Deseas guardar el remito?")
        if not guardar:
            return

        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()

        # Obtener las observaciones ingresadas por el usuario
        observaciones = observaciones.get().strip()

        # Crear un nuevo remito
        nuevo_remito = Remitos(id_cliente=cliente.id, fecha=fecha_actual, pago=pago, total=0, observacion=observaciones)

        # Agregar el remito a la base de datos
        session.add(nuevo_remito)
        session.commit()

        total_remito = 0

        # Iterar sobre los elementos del carrito para agregarlos a los detalles del remito
        for producto, cantidad, descuento, precio in carrito:
            cantidad = float(cantidad)
            # Quitamos el signo de pesos y las comas
            precio = precio[1:].replace(',', '') if precio else 0
            precio = float(precio) if precio else 0
            # Quitar el signo de porcentaje y convertir a flotante el descuento
            descuento = float(descuento[:-1]) if descuento else 0
            total = cantidad * precio * (1 - descuento / 100)
            detalle = DetallesRemitos(
                id_remito=nuevo_remito.id,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=precio,
                descuento=descuento,
                total=total
            )
            total_remito += total
            session.add(detalle)

        # Actualizar el total del remito
        nuevo_remito.total = total_remito
        session.commit()

        messagebox.showinfo("Éxito", "El remito se ha guardado correctamente en la base de datos.")
    
    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Ocurrió un error al guardar el remito: {str(e)}")