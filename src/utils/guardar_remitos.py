import datetime
from tkinter import messagebox

def guardar_remito(cliente_var, carrito, session, Clientes, Remitos, DetallesRemitos):
    try:
        # Preguntar al usuario si el remito se pagó o no
        pago = messagebox.askyesno("Pago", "¿El remito se pagó?")
        pago = "SI" if pago else "NO"

        # Obtener el nombre del cliente seleccionado
        nombre_cliente = cliente_var.get()

        # Buscar el cliente en la base de datos
        cliente = session.query(Clientes).filter_by(nombre=nombre_cliente).first()

        if not cliente:
            messagebox.showerror("Error", "Cliente no encontrado en la base de datos.")
            return

        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()

        # Crear un nuevo remito
        nuevo_remito = Remitos(id_cliente=cliente.id, fecha=fecha_actual, pago=pago, total=0)

        # Agregar el remito a la base de datos
        session.add(nuevo_remito)
        session.commit()

        total_remito = 0

        # Iterar sobre los elementos del carrito para agregarlos a los detalles del remito
        for producto, cantidad, descuento, precio in carrito:
            cantidad = int(cantidad)
            precio = float(precio)
            descuento = float(descuento)
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