from database import Acopios, session, Clientes
import datetime
from utils.remitos.guardar_remitos import guardar_remito
from utils.remitos.generar_remitos import generar_remito_excel
from tkinter import messagebox

def agregar_a_acopio(carrito, cliente):
    # Si no se seleccionó ningún cliente, anular la operación
    if not cliente:
        return

    # Obtener el ID del cliente seleccionado en la DB
    cliente_id = session.query(Clientes).filter(Clientes.nombre == cliente).first().id

    # Obtener la fecha actual
    fecha = datetime.datetime.now()

    # Obtener los productos en acopio del cliente
    acopios = session.query(Acopios).filter(Acopios.id_cliente == cliente_id).all()

    # Insertar los productos en la tabla de acopios
    for producto, cantidad, _, _ in carrito:
        cantidad = float(cantidad)
        if any(producto == a.producto for a in acopios):
            acopio = session.query(Acopios).filter(Acopios.id_cliente == cliente_id, Acopios.producto == producto).first()
            acopio.cantidad += cantidad
            acopio.fecha_modificacion = fecha
        
        else:
            acopio = Acopios(id_cliente=cliente_id, producto=producto, cantidad=cantidad, fecha=fecha)
            session.add(acopio)

    # Confirmar la transacción
    session.commit()

def descontar_de_acopio(carrito, cliente, imprimir):
    # Obtener el ID del cliente seleccionado en la DB
    cliente_id = session.query(Clientes).filter(Clientes.nombre == cliente).first().id

    # Obtener la fecha actual
    fecha = datetime.datetime.now()

    # Crear listas para los productos en deuda y los productos en acopio
    deuda_carrito = []
    acopio_carrito = []

    # Iterar sobre los productos en el carrito
    for producto, cantidad, descuento, precio in carrito:
        # Obtener el producto en acopio
        acopio = session.query(Acopios).filter(Acopios.id_cliente == cliente_id, Acopios.producto == producto).first()
        cantidad=float(cantidad)
        # Si el producto no se encuentra en acopio, sumarlo a la deuda
        if not acopio:
            deuda_carrito.append([producto, cantidad, descuento, precio])
        # Si la cantidad en acopio es menor a la cantidad a descontar, sumar la cantidad faltante a la deuda y borrar el producto de acopio
        elif acopio.cantidad < cantidad:
            cantidad_faltante = cantidad - acopio.cantidad
            deuda_carrito.append([producto, cantidad_faltante, descuento, precio])
            acopio_carrito.append([producto, acopio.cantidad, 0, 0])
            session.delete(acopio)
        # Si la cantidad en acopio es igual a la cantidad a descontar, borrar el producto de acopio
        elif acopio.cantidad == cantidad:
            session.delete(acopio)
            acopio_carrito.append([producto, cantidad, 0, 0])
        # Si la cantidad en acopio es mayor a la cantidad a descontar, restar la cantidad a descontar de la cantidad en acopio
        else:
            acopio.cantidad -= cantidad
            acopio.fecha_modificacion = fecha
            acopio_carrito.append([producto, cantidad, 0, 0]) 

    # Crear el remito de los productos descontados de acopio
    if acopio_carrito:
        guardar_remito(cliente, acopio_carrito, "De Acopio", False)
        generar_remito_excel(cliente, acopio_carrito, "De Acopio", imprimir)

    # Crear el remito de la deuda
    if deuda_carrito:
        messagebox.showwarning("Atención", "El cliente retiró productos que no se encuentran en acopio, o retiró más productos de los que tenía en acopio. Se creará un remito con los productos faltantes.")
        guardar_remito(cliente, deuda_carrito, "Retirado", True)
        generar_remito_excel(cliente, deuda_carrito, "Retirado", imprimir)

    # Confirmar la transacción
    session.commit()