import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database import session, Producto, Factura, FacturaProducto, Remito, RemitoProducto
import csv
from datetime import date

def agregar_producto():
    if validar_entradas():
        nombre = entry_nombre.get()
        cantidad = int(entry_cantidad.get())
        precio = float(entry_precio.get())
        nuevo_producto = Producto(nombre=nombre, cantidad=cantidad, precio=precio)
        session.add(nuevo_producto)
        session.commit()
        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado correctamente")
        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        actualizar_lista_productos()

def actualizar_lista_productos():
    for row in tree.get_children():
        tree.delete(row)
    productos = session.query(Producto).all()
    for producto in productos:
        tree.insert("", tk.END, values=(producto.nombre, producto.cantidad, producto.precio))

def buscar_producto():
    query = entry_busqueda.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    productos = session.query(Producto).filter(Producto.nombre.ilike(f"%{query}%")).all()
    for producto in productos:
        tree.insert("", tk.END, values=(producto.nombre, producto.cantidad, producto.precio))

def editar_producto():
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item[0], 'values')
        entry_nombre.delete(0, tk.END)
        entry_nombre.insert(0, item_values[0])
        entry_cantidad.delete(0, tk.END)
        entry_cantidad.insert(0, item_values[1])
        entry_precio.delete(0, tk.END)
        entry_precio.insert(0, item_values[2])
        boton_actualizar.config(state='normal')
        boton_agregar.config(state='disabled')

def actualizar_producto():
    if validar_entradas():
        nombre = entry_nombre.get()
        cantidad = int(entry_cantidad.get())
        precio = float(entry_precio.get())
        selected_item = tree.selection()[0]
        item_values = tree.item(selected_item, 'values')
        producto_actualizado = session.query(Producto).filter_by(nombre=item_values[0]).first()
        producto_actualizado.nombre = nombre
        producto_actualizado.cantidad = cantidad
        producto_actualizado.precio = precio
        session.commit()
        messagebox.showinfo("Éxito", f"Producto '{nombre}' actualizado correctamente")
        entry_nombre.delete(0, tk.END)
        entry_cantidad.delete(0, tk.END)
        entry_precio.delete(0, tk.END)
        boton_actualizar.config(state='disabled')
        boton_agregar.config(state='normal')
        actualizar_lista_productos()

def eliminar_producto():
    selected_item = tree.selection()
    if selected_item:
        item_values = tree.item(selected_item[0], 'values')
        session.query(Producto).filter_by(nombre=item_values[0]).delete()
        session.commit()
        tree.delete(selected_item)
        messagebox.showinfo("Éxito", f"Producto '{item_values[0]}' eliminado correctamente")

def exportar_inventario():
    productos = session.query(Producto).all()
    with open('inventario.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Cantidad", "Precio"])
        for producto in productos:
            writer.writerow([producto.nombre, producto.cantidad, producto.precio])
    messagebox.showinfo("Éxito", "Inventario exportado correctamente a 'inventario.csv'")

def validar_entradas():
    try:
        nombre = entry_nombre.get()
        cantidad = int(entry_cantidad.get())
        precio = float(entry_precio.get())
        if not nombre:
            raise ValueError("El nombre no puede estar vacío")
        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa")
        if precio < 0:
            raise ValueError("El precio no puede ser negativo")
        return True
    except ValueError as e:
        messagebox.showerror("Error de validación", str(e))
        return False

def crear_factura():
    productos_seleccionados = []
    for item in tree.selection():
        item_values = tree.item(item, 'values')
        producto = session.query(Producto).filter_by(nombre=item_values[0]).first()
        cantidad = int(item_values[1])
        precio = float(item_values[2])
        productos_seleccionados.append((producto, cantidad, precio))

    if productos_seleccionados:
        total = sum([p[1] * p[2] for p in productos_seleccionados])
        nueva_factura = Factura(fecha=date.today(), cliente="Cliente Genérico", total=total)
        session.add(nueva_factura)
        session.commit()
        for producto, cantidad, precio in productos_seleccionados:
            factura_producto = FacturaProducto(factura_id=nueva_factura.id, producto_id=producto.id, cantidad=cantidad, precio_unitario=precio)
            session.add(factura_producto)
        session.commit()
        messagebox.showinfo("Éxito", "Factura creada correctamente")

def crear_remito():
    productos_seleccionados = []
    for item in tree.selection():
        item_values = tree.item(item, 'values')
        producto = session.query(Producto).filter_by(nombre=item_values[0]).first()
        cantidad = int(item_values[1])
        productos_seleccionados.append((producto, cantidad))

    if productos_seleccionados:
        nuevo_remito = Remito(fecha=date.today(), cliente="Cliente Genérico")
        session.add(nuevo_remito)
        session.commit()
        for producto, cantidad in productos_seleccionados:
            remito_producto = RemitoProducto(remito_id=nuevo_remito.id, producto_id=producto.id, cantidad=cantidad)
            session.add(remito_producto)
        session.commit()
        messagebox.showinfo("Éxito", "Remito creado correctamente")

def ver_facturas():
    facturas = session.query(Factura).all()
    for factura in facturas:
        print(f"Factura ID: {factura.id}, Fecha: {factura.fecha}, Cliente: {factura.cliente}, Total: {factura.total}")
        for producto in factura.productos:
            print(f" - Producto: {producto.producto.nombre}, Cantidad: {producto.cantidad}, Precio Unitario: {producto.precio_unitario}")

def ver_remitos():
    remitos = session.query(Remito).all()
    for remito in remitos:
        print(f"Remito ID: {remito.id}, Fecha: {remito.fecha}, Cliente: {remito.cliente}")
        for producto in remito.productos:
            print(f" - Producto: {producto.producto.nombre}, Cantidad: {producto.cantidad}")


def iniciar_interfaz():
    global entry_nombre, entry_cantidad, entry_precio, tree, entry_busqueda, boton_actualizar, boton_agregar
    app = tk.Tk()
    app.title("Gestión de Stock")
    app.geometry("800x600")

    # Frame de Búsqueda
    frame_busqueda = ttk.LabelFrame(app, text="Buscar Producto")
    frame_busqueda.pack(padx=10, pady=10, fill="x")
    ttk.Label(frame_busqueda, text="Buscar por Nombre").grid(row=0, column=0, padx=5, pady=5)
    entry_busqueda = ttk.Entry(frame_busqueda)
    entry_busqueda.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(frame_busqueda, text="Buscar", command=buscar_producto).grid(row=0, column=2, padx=5, pady=5)

    # Frame de Formulario
    frame_formulario = ttk.LabelFrame(app, text="Agregar/Editar Producto")
    frame_formulario.pack(padx=10, pady=10, fill="x")

    ttk.Label(frame_formulario, text="Nombre del Producto").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = ttk.Entry(frame_formulario)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Cantidad").grid(row=1, column=0, padx=5, pady=5)
    entry_cantidad = ttk.Entry(frame_formulario)
    entry_cantidad.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Precio").grid(row=2, column=0, padx=5, pady=5)
    entry_precio = ttk.Entry(frame_formulario)
    entry_precio.grid(row=2, column=1, padx=5, pady=5)

    boton_agregar = ttk.Button(frame_formulario, text="Agregar Producto", command=agregar_producto)
    boton_agregar.grid(row=3, column=0, padx=5, pady=10)

    boton_actualizar = ttk.Button(frame_formulario, text="Actualizar Producto", command=actualizar_producto)
    boton_actualizar.grid(row=3, column=1, padx=5, pady=10)
    boton_actualizar.config(state='disabled')

    # Frame de Lista de Productos
    frame_lista = ttk.LabelFrame(app, text="Lista de Productos")
    frame_lista.pack(padx=10, pady=10, fill="both", expand=True)

    columnas = ("Nombre", "Cantidad", "Precio")
    style = ttk.Style()
    style.configure("Treeview.Heading", anchor="center")
    style.configure("Treeview", rowheight=25)
    tree = ttk.Treeview(frame_lista, columns=columnas, show="headings", style="Treeview")
    for col in columnas:
        tree.heading(col, text=col, anchor="center")
        tree.column(col, anchor="center")
    tree.pack(padx=5, pady=5, fill="both", expand=True)

    ttk.Button(app, text="Eliminar Producto", command=eliminar_producto).pack(pady=5)
    ttk.Button(app, text="Exportar Inventario", command=exportar_inventario).pack(pady=5)
    ttk.Button(app, text="Editar Producto", command=editar_producto).pack(pady=5)
    ttk.Button(app, text="Crear Factura", command=crear_factura).pack(pady=5)
    ttk.Button(app, text="Crear Remito", command=crear_remito).pack(pady=5)
    ttk.Button(app, text="Ver Facturas", command=ver_facturas).pack(pady=5)
    ttk.Button(app, text="Ver Remitos", command=ver_remitos).pack(pady=5)

    actualizar_lista_productos()

    app.mainloop()

