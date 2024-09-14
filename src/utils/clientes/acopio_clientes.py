from tkinter import messagebox
from tkinter import Toplevel, ttk
from database import Acopios, Clientes, session

ventana_acopio = None

def ver_acopio(self):
    # Obtener el cliente seleccionado
    seleccion = self.clientes_tree.selection()

    # Si no se seleccionó ningún cliente, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un cliente.")
        return
    
    # Obtener el nombre del cliente seleccionado
    nombre = self.clientes_tree.item(seleccion)['values'][0]

    self.ventana_acopio = abrir_ventana_acopio(nombre)

def abrir_ventana_acopio(nombre):
    global ventana_acopio

    # Si la ventana de acopio ya está abierta, borrarla
    if ventana_acopio and ventana_acopio.winfo_exists():
        ventana_acopio.destroy()

    # Crear una nueva ventana
    ventana_acopio = Toplevel()
    ventana_acopio.title(f"Acopio de {nombre}")

    # Crear un Treeview para mostrar los productos en acopio
    acopio_tree = ttk.Treeview(ventana_acopio, columns=("producto", "cantidad", "fecha", "fecha_modificación"), selectmode="browse")
    acopio_tree.heading("#0", text="ID")
    acopio_tree.heading("producto", text="Producto")
    acopio_tree.heading("cantidad", text="Cantidad")
    acopio_tree.heading("fecha", text="Fecha")
    acopio_tree.heading("fecha_modificación", text="Fecha de modificación")
    acopio_tree.column("#0", width=0, stretch=False)
    acopio_tree.column("producto", anchor="center", width=300)
    acopio_tree.column("cantidad", anchor="center", width=70)
    acopio_tree.column("fecha", anchor="center", width=150)
    acopio_tree.column("fecha_modificación", anchor="center", width=150)
    acopio_tree.pack(padx=10, pady=10, fill="both", expand=True)

    # Obtener el cliente seleccionado en la tabla
    cliente = session.query(Clientes).filter_by(nombre=nombre).first()
    # Obtener los productos en acopio del cliente
    acopio = session.query(Acopios).filter_by(id_cliente=cliente.id).all()
    # Agregar los productos en acopio al Treeview con la fecha formateada
    for producto in acopio:
        acopio_tree.insert('', 'end', text=producto.id, values=(producto.producto, 
                                                                producto.cantidad, 
                                                                producto.fecha.strftime('%d/%m/%Y %H:%M:%S'), 
                                                                producto.fecha_modificacion.strftime('%d/%m/%Y %H:%M:%S') if producto.fecha_modificacion else ""))
    
    return ventana_acopio