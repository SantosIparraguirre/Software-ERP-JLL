import datetime
from tkinter import messagebox
from database import session, Clientes, Remitos, DetallesRemitos

def guardar_remito(nombre_cliente, carrito, observaciones, deuda=False):
    try:
        # Si el remito es de deuda, no es necesario realizar las siguientes validaciones/operaciones
        if not deuda:
            if not nombre_cliente:
                messagebox.showerror("Error", "Selecciona un cliente.")
                return

            # Buscar el cliente en la base de datos
            cliente = session.query(Clientes).filter_by(nombre=nombre_cliente).first()

            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado en la base de datos.")
                return
            
            # Obtener las observaciones ingresadas por el usuario
            observaciones = observaciones.get().strip() if observaciones != "De Acopio" else observaciones

            # Preguntar al usuario si el remito se pagó o no, sólo si las observaciones son "Retirado"
            if observaciones == "Retirado":
                pago = messagebox.askyesno("Pago", "¿El remito se pagó?")
                pago = "SI" if pago else "NO"
            else:
                pago = "SI"

            if observaciones != "De Acopio":
                # Preguntar al usuario si desea guardar el remito
                guardar = messagebox.askyesno("Guardar", "¿Deseas guardar el remito?")
                if not guardar:
                    return
        
        else:
            cliente = session.query(Clientes).filter_by(nombre=nombre_cliente).first()
            pago = "NO"

        # Obtener la fecha actual
        fecha_actual = datetime.datetime.now()

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
            if type(precio) == str:
                precio = precio[1:].replace(',', '') if precio.startswith('$') else precio.replace(',', '')
                precio = float(precio) if precio else 0
            # Quitar el signo de porcentaje y convertir a flotante el descuento
            if type(descuento) == str:
                descuento = float(descuento[:-1]) if descuento.endswith('%') else float(descuento) if descuento else 0
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
        
        # Si el remito no es de deuda, mostrar un mensaje de éxito
        if not deuda:
            messagebox.showinfo("Éxito", "El remito se ha guardado correctamente en la base de datos.")
    
    except Exception as e:
        session.rollback()
        messagebox.showerror("Error", f"Ocurrió un error al guardar el remito: {str(e)}")