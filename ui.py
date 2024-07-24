import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import sessionmaker
from database import engine, Capea, Polietileno, Peirano, Latyn, Fusiogas, Chicote, H3, CañosPVC, PiezasPVC, Sigas, PPRosca, Awaduck, Amancofusion, Rotoplas

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Diccionario para mapear nombres de tablas a clases
tabla_clase_mapping = {
    'CAPEA': Capea,
    'POLIETILENO': Polietileno,
    'PEIRANO': Peirano,
    'LATYN': Latyn,
    'FUSIOGAS': Fusiogas,
    'CHICOTE': Chicote,
    'H3': H3,
    'CAÑOS PVC': CañosPVC,
    'PIEZAS PVC Y LOSUNG': PiezasPVC,
    'SIGAS': Sigas,
    'PP ROSCA': PPRosca,
    'AWADUCK': Awaduck,
    'AMANCO FUSION': Amancofusion,
    'ROTOPLAS': Rotoplas
}

# Clase para la interfaz de presupuestos
class PresupuestoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Presupuestos")
        self.geometry("1000x600")
        self.create_widgets()
        self.carrito = []

    def create_widgets(self):
        # Menú lateral
        self.menu_lateral = tk.Frame(self, width=200, bg='gray')
        self.menu_lateral.pack(side='left', fill='y')

        # Frame principal
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side='right', fill='both', expand=True)

        # Menú de selección de tablas
        self.tabla_label = ttk.Label(self.main_frame, text="Seleccioná una lista:")
        self.tabla_label.grid(column=0, row=0, padx=10, pady=10)

        self.tabla_var = tk.StringVar()
        self.tabla_combobox = ttk.Combobox(self.main_frame, textvariable=self.tabla_var)
        self.tabla_combobox['values'] = list(tabla_clase_mapping.keys())
        self.tabla_combobox.bind("<<ComboboxSelected>>", self.update_productos)
        self.tabla_combobox.grid(column=1, row=0, padx=10, pady=10)

        # Botón para aumentar precios
        self.aumentar_precios_button = ttk.Button(self.main_frame, text="Aumentar Precios", command=self.aumentar_precios)
        self.aumentar_precios_button.grid(column=2, row=0, columnspan=1, padx=10, pady=10)
        
        # Información del último aumento
        self.ultimo_aumento_label = ttk.Label(self.main_frame, text="Último aumento: N/A")
        self.ultimo_aumento_label.grid(column=3, row=0, padx=10, pady=10)

        # Cuadro de búsqueda de productos
        self.busqueda_label = ttk.Label(self.main_frame, text="Buscar Producto:")
        self.busqueda_label.grid(column=0, row=2, padx=10, pady=10)

        self.busqueda_var = tk.StringVar()
        self.busqueda_entry = ttk.Entry(self.main_frame, textvariable=self.busqueda_var)
        self.busqueda_entry.grid(column=1, row=2, padx=10, pady=10)

        self.buscar_button = ttk.Button(self.main_frame, text="Buscar", command=self.buscar_producto)
        self.buscar_button.grid(column=2, row=2, padx=10, pady=10)

        # Cuadro de lista de productos
        self.producto_label = ttk.Label(self.main_frame, text="Seleccioná un producto:")
        self.producto_label.grid(column=0, row=3, padx=10, pady=10)

        self.productos_listbox = tk.Listbox(self.main_frame, width=75)
        self.productos_listbox.grid(column=1, row=3, padx=10, pady=10, columnspan=2)

        # Campo de cantidad
        self.cantidad_label = ttk.Label(self.main_frame, text="Cantidad:")
        self.cantidad_label.grid(column=0, row=4, padx=10, pady=10)

        self.cantidad_var = tk.IntVar()
        self.cantidad_entry = ttk.Entry(self.main_frame, textvariable=self.cantidad_var)
        self.cantidad_entry.grid(column=1, row=4, padx=10, pady=10)

        # Campo de descuento
        self.descuento_label = ttk.Label(self.main_frame, text="Descuento (%):")
        self.descuento_label.grid(column=0, row=5, padx=10, pady=10)

        self.descuento_var = tk.DoubleVar()
        self.descuento_entry = ttk.Entry(self.main_frame, textvariable=self.descuento_var)
        self.descuento_entry.grid(column=1, row=5, padx=10, pady=10)

        # Botón para agregar al carrito
        self.add_button = ttk.Button(self.main_frame, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.add_button.grid(column=0, row=6, columnspan=3, padx=10, pady=10)

        # Listbox para mostrar el carrito
        self.carrito_listbox = tk.Listbox(self.main_frame, width=100)
        self.carrito_listbox.grid(column=0, row=7, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Botón para borrar del carrito
        self.delete_button = ttk.Button(self.main_frame, text="Eliminar del Carrito", command=self.eliminar_del_carrito)
        self.delete_button.grid(column=0, row=8, columnspan=3, padx=10, pady=10)

        # Botón para generar el presupuesto
        self.generate_button = ttk.Button(self.main_frame, text="Generar Presupuesto", command=self.generar_presupuesto)
        self.generate_button.grid(column=0, row=9, columnspan=3, padx=10, pady=10)

    def update_productos(self, event):
        tabla = self.tabla_var.get()
        clase = tabla_clase_mapping[tabla]

        # Obtener el término de búsqueda
        search_term = self.busqueda_var.get().lower()

        productos = session.query(clase).all()
        self.productos_listbox.delete(0, tk.END)
        for producto in productos:
            if search_term in producto.producto.lower():
                self.productos_listbox.insert(tk.END, f"{producto.producto} - Precio: {producto.precio}")



    def buscar_producto(self):
        search_term = self.busqueda_var.get().lower()
        tabla = self.tabla_var.get()
        clase = tabla_clase_mapping[tabla]

        productos = session.query(clase).all()
        self.productos_listbox.delete(0, tk.END)
        for producto in productos:
            if search_term in producto.producto.lower():
                self.productos_listbox.insert(tk.END, f"{producto.producto} - Precio: {producto.precio}")



    def filtrar_productos(self, tabla, busqueda):
        clase = tabla_clase_mapping[tabla]
        productos = session.query(clase).filter(clase.producto.contains(busqueda)).all()
        self.productos_listbox.delete(0, tk.END)
        for producto in productos:
            self.productos_listbox.insert(tk.END, producto.producto)

    def agregar_al_carrito(self):
        producto_seleccionado = self.productos_listbox.get(tk.ACTIVE)
        if not producto_seleccionado:
            messagebox.showerror("Error", "Selecciona un producto.")
            return

        # Extraer el nombre del producto (antes del guión)
        producto_nombre = producto_seleccionado.split(" - ")[0]

        cantidad = self.cantidad_var.get()
        descuento = self.descuento_var.get()

        if cantidad <= 0:
            messagebox.showerror("Error", "Ingresa una cantidad válida.")
            return

        # Obtener el precio del producto
        tabla = self.tabla_var.get()
        clase = tabla_clase_mapping[tabla]
        producto_info = session.query(clase).filter_by(producto=producto_nombre).first()
        precio = producto_info.precio

        self.carrito.append((producto_nombre, cantidad, descuento, precio))
        self.actualizar_carrito()




    def actualizar_carrito(self):
        self.carrito_listbox.delete(0, tk.END)
        for item in self.carrito:
            producto, cantidad, descuento, precio = item
            self.carrito_listbox.insert(tk.END, f"Producto: {producto}, Cantidad: {cantidad}, Descuento: {descuento}%, Precio: {precio}")


    def eliminar_del_carrito(self):
        seleccion = self.carrito_listbox.curselection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona un producto del carrito.")
            return

        self.carrito.pop(seleccion[0])
        self.actualizar_carrito()

    def generar_presupuesto(self):
    # Solicitar ubicación para guardar el archivo PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not file_path:
            return
    
    # Crear el PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 50, "Presupuesto")
        y = height - 100

        total = 0
        for item in self.carrito:
            producto, cantidad, descuento, precio = item
            precio_descuento = precio * (1 - descuento / 100)
            total_item = precio_descuento * cantidad
            total += total_item

            c.drawString(100, y, f"Producto: {producto}, Cantidad: {cantidad}, Precio: {precio}, Descuento: {descuento}%, Total: {total_item:.2f}")
            y -= 20

        c.drawString(100, y - 20, f"Total: {total:.2f}")
        c.save()

        messagebox.showinfo("Información", "Presupuesto generado correctamente.")


    def aumentar_precios(self):
        porcentaje = tk.simpledialog.askfloat("Aumentar Precios", "Ingresa el porcentaje de aumento de precios (%):")
        if porcentaje is None or porcentaje <= 0:
            messagebox.showerror("Error", "Ingresa un porcentaje válido.")
            return

        tabla = self.tabla_var.get()
        clase = tabla_clase_mapping[tabla]

        productos = session.query(clase).all()
        for producto in productos:
            producto.precio *= (1 + porcentaje / 100)
        session.commit()

        messagebox.showinfo("Información", "Precios aumentados correctamente.")
        self.update_productos(None)

# Ejecutar la aplicación
if __name__ == "__main__":
    try:
        app = PresupuestoApp()
        app.mainloop()
    except Exception as e:
        with open("error.log", "w") as f:
            f.write(str(e))
    input("Presiona Enter para salir...")
