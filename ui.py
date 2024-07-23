import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy.orm import sessionmaker
from database import engine, Capea, Polietileno, Peirano, Latyn, Fusiogas, Chicote, H3, Caños, PiezasPVC, Sigas, PPRosca, Awaduck, Amancofusion, Rotoplas

# Crear una sesión
Session = sessionmaker(bind=engine)
session = Session()

# Diccionario para mapear nombres de tablas a clases
tabla_clase_mapping = {
    'capea': Capea,
    'polietileno': Polietileno,
    'peirano': Peirano,
    'latyn': Latyn,
    'fusiogas': Fusiogas,
    'chicote': Chicote,
    'h3': H3,
    'caños pvc': Caños,
    'piezas pvc y losung': PiezasPVC,
    'sigas': Sigas,
    'pp rosca': PPRosca,
    'awaduck': Awaduck,
    'amanco fusion': Amancofusion,
    'rotoplas': Rotoplas
}

# Clase para la interfaz de presupuestos
class PresupuestoApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Presupuestos")
        self.geometry("800x600")
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
        self.tabla_label = ttk.Label(self.main_frame, text="Selecciona una Tabla:")
        self.tabla_label.grid(column=0, row=0, padx=10, pady=10)

        self.tabla_var = tk.StringVar()
        self.tabla_combobox = ttk.Combobox(self.main_frame, textvariable=self.tabla_var)
        self.tabla_combobox['values'] = list(tabla_clase_mapping.keys())
        self.tabla_combobox.bind("<<ComboboxSelected>>", self.update_productos)
        self.tabla_combobox.grid(column=1, row=0, padx=10, pady=10)

        # Cuadro de lista de productos
        self.producto_label = ttk.Label(self.main_frame, text="Selecciona un Producto:")
        self.producto_label.grid(column=0, row=1, padx=10, pady=10)

        self.productos_listbox = tk.Listbox(self.main_frame)
        self.productos_listbox.grid(column=1, row=1, padx=10, pady=10)

        # Campo de cantidad
        self.cantidad_label = ttk.Label(self.main_frame, text="Cantidad:")
        self.cantidad_label.grid(column=0, row=2, padx=10, pady=10)

        self.cantidad_var = tk.IntVar()
        self.cantidad_entry = ttk.Entry(self.main_frame, textvariable=self.cantidad_var)
        self.cantidad_entry.grid(column=1, row=2, padx=10, pady=10)

        # Campo de descuento
        self.descuento_label = ttk.Label(self.main_frame, text="Descuento (%):")
        self.descuento_label.grid(column=0, row=3, padx=10, pady=10)

        self.descuento_var = tk.DoubleVar()
        self.descuento_entry = ttk.Entry(self.main_frame, textvariable=self.descuento_var)
        self.descuento_entry.grid(column=1, row=3, padx=10, pady=10)

        # Botón para agregar al carrito
        self.add_button = ttk.Button(self.main_frame, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.add_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

        # Listbox para mostrar el carrito
        self.carrito_listbox = tk.Listbox(self.main_frame)
        self.carrito_listbox.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Botón para generar el presupuesto
        self.generate_button = ttk.Button(self.main_frame, text="Generar Presupuesto", command=self.generar_presupuesto)
        self.generate_button.grid(column=0, row=6, columnspan=2, padx=10, pady=10)

    def update_productos(self, event):
        # Actualizar la lista de productos según la tabla seleccionada
        tabla = self.tabla_var.get()
        clase = tabla_clase_mapping[tabla]
        productos = session.query(clase).all()
        self.productos_listbox.delete(0, tk.END)
        for producto in productos:
            self.productos_listbox.insert(tk.END, producto.producto)

    def agregar_al_carrito(self):
        producto_seleccionado = self.productos_listbox.get(tk.ACTIVE)
        cantidad = self.cantidad_var.get()
        descuento = self.descuento_var.get()

        if not producto_seleccionado:
            messagebox.showerror("Error", "Selecciona un producto.")
            return
        if cantidad <= 0:
            messagebox.showerror("Error", "Ingresa una cantidad válida.")
            return

        self.carrito.append((producto_seleccionado, cantidad, descuento))
        self.actualizar_carrito()

    def actualizar_carrito(self):
        self.carrito_listbox.delete(0, tk.END)
        for item in self.carrito:
            self.carrito_listbox.insert(tk.END, f"Producto: {item[0]}, Cantidad: {item[1]}, Descuento: {item[2]}%")

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
            producto, cantidad, descuento = item
            tabla = self.tabla_var.get()
            clase = tabla_clase_mapping[tabla]
            producto_info = session.query(clase).filter_by(producto=producto).first()
            precio = producto_info.precio
            precio_descuento = precio * (1 - descuento / 100)
            total_item = precio_descuento * cantidad
            total += total_item

            c.drawString(100, y, f"Producto: {producto}, Cantidad: {cantidad}, Precio unitario: {precio}, Total: {total_item:.2f}")
            y -= 20

        c.drawString(100, y - 20, f"Total: {total:.2f}")
        c.save()

        messagebox.showinfo("Información", "Presupuesto generado correctamente.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app = PresupuestoApp()
    app.mainloop()
