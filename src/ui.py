import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from reportlab.lib.pagesizes import letter
from sqlalchemy.orm import sessionmaker
from database_presupuestos import engine, Capea, Polietileno, Peirano, Latyn, Fusiogas, Chicote, H3, CañosPVC, PiezasPVC, Sigas, PPRosca, Awaduck, Amancofusion, Rotoplas
from openpyxl import load_workbook
import datetime

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
        self.geometry("1200x700")
        self.create_widgets()
        self.carrito = []
        self.ultimo_aumento = {}

    def create_widgets(self):
        # Menú lateral
        self.menu_lateral = tk.Frame(self, width=200, bg='gray')
        self.menu_lateral.pack(side='left', fill='y')

        # Botón para mostrar presupuestos
        self.presupuestos_button = ttk.Button(self.menu_lateral, text="Presupuestos", command=self.mostrar_presupuestos)
        self.presupuestos_button.pack(padx=10, pady=10)

        # Botón para mostrar clientes
        self.clientes_button = ttk.Button(self.menu_lateral, text="Clientes", command=self.mostrar_clientes)
        self.clientes_button.pack(padx=10, pady=10)

        # Frame principal
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(side='right', fill='both', expand=True)

        # Mostrar la sección de presupuestos por defecto
        self.mostrar_presupuestos()

    def mostrar_presupuestos(self):
        # Limpiar el main_frame antes de agregar nuevos widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Menú de selección de tablas
        self.tabla_label = ttk.Label(self.main_frame, text="Seleccioná una lista:")
        self.tabla_label.grid(column=0, row=0, padx=(10,2), pady=10)

        self.tabla_var = tk.StringVar()
        self.tabla_combobox = ttk.Combobox(self.main_frame, textvariable=self.tabla_var)
        self.tabla_combobox['values'] = list(tabla_clase_mapping.keys())
        self.tabla_combobox.bind("<<ComboboxSelected>>", self.update_productos)
        self.tabla_combobox.grid(column=1, row=0, padx=(0,5), pady=10)

        # Botón para aumentar precios
        self.aumentar_precios_button = ttk.Button(self.main_frame, text="Aumentar Precios", command=self.aumentar_precios)
        self.aumentar_precios_button.grid(column=2, row=0, columnspan=1, padx=(0,10), pady=10)

        # Información del último aumento
        self.ultimo_aumento_label = ttk.Label(self.main_frame, text="Último aumento: N/A")
        self.ultimo_aumento_label.grid(column=3, row=0, padx=1, pady=10)

        # Cuadro de búsqueda de productos
        self.busqueda_label = ttk.Label(self.main_frame, text="Buscar Producto:")
        self.busqueda_label.grid(column=0, row=2, padx=10, pady=10)

        self.busqueda_var = tk.StringVar()
        self.busqueda_entry = ttk.Entry(self.main_frame, textvariable=self.busqueda_var)
        self.busqueda_entry.grid(column=1, row=2, padx=(10, 2), pady=10)

        self.buscar_button = ttk.Button(self.main_frame, text="Buscar", command=self.buscar_producto)
        self.buscar_button.grid(column=2, row=2, padx=(0, 10), pady=10)

        # Campo de cantidad
        self.cantidad_label = ttk.Label(self.main_frame, text="Cantidad:")
        self.cantidad_label.grid(column=0, row=3, padx=10, pady=10)

        self.cantidad_var = tk.IntVar()
        self.cantidad_entry = ttk.Entry(self.main_frame, textvariable=self.cantidad_var)
        self.cantidad_entry.grid(column=1, row=3, padx=10, pady=10)

        # Campo de descuento
        self.descuento_label = ttk.Label(self.main_frame, text="Descuento (%):")
        self.descuento_label.grid(column=2, row=3, padx=10, pady=10)

        self.descuento_var = tk.DoubleVar()
        self.descuento_entry = ttk.Entry(self.main_frame, textvariable=self.descuento_var)
        self.descuento_entry.grid(column=3, row=3, padx=10, pady=10)

        # Botón para agregar al carrito
        self.add_button = ttk.Button(self.main_frame, text="Agregar al Carrito", command=self.agregar_al_carrito)
        self.add_button.grid(column=0, row=4, columnspan=3, padx=10, pady=10)

        # Tabla de productos
        self.productos_tree = ttk.Treeview(self.main_frame, columns=('Producto', 'Precio'), show='headings')
        self.productos_tree.heading('Producto', text='Producto')
        self.productos_tree.heading('Precio', text='Precio')
        self.productos_tree.grid(column=0, row=5, padx=10, pady=10, columnspan=2)

        # Listbox para mostrar el carrito
        self.carrito_listbox = tk.Listbox(self.main_frame, width=80)
        self.carrito_listbox.grid(column=2, row=5, columnspan=3, padx=10, pady=10, sticky='nsew')


        # Botón para borrar del carrito
        self.delete_button = ttk.Button(self.main_frame, text="Eliminar del Carrito", command=self.eliminar_del_carrito)
        self.delete_button.grid(column=0, row=8, columnspan=3, padx=10, pady=10)

        # Botón para generar el presupuesto
        self.generate_button = ttk.Button(self.main_frame, text="Generar Presupuesto", command=self.generar_presupuesto_excel)
        self.generate_button.grid(column=0, row=9, columnspan=3, padx=10, pady=10)

    def mostrar_clientes(self):
        # Limpiar el main_frame antes de agregar nuevos widgets
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Crear widgets específicos para la sección de clientes (a desarrollar)
        self.clientes_label = ttk.Label(self.main_frame, text="Sección de Clientes (en desarrollo)")
        self.clientes_label.grid(column=0, row=0, padx=10, pady=10)

    def update_productos(self, event):
        tabla = self.tabla_var.get()
        clase = tabla_clase_mapping[tabla]

        # Obtener el término de búsqueda
        search_term = self.busqueda_var.get().lower()

        productos = session.query(clase).all()
        self.productos_tree.delete(*self.productos_tree.get_children())
        for producto in productos:
            if search_term in producto.producto.lower():
                self.productos_tree.insert('', 'end', values=(producto.producto, producto.precio))

        # Actualizar la etiqueta de último aumento
        if tabla in self.ultimo_aumento:
            self.ultimo_aumento_label.config(text=f"Último aumento: {self.ultimo_aumento[tabla]}%")
        else:
            self.ultimo_aumento_label.config(text="Último aumento: N/A")

    def buscar_producto(self):
        search_term = self.busqueda_var.get().lower()
        tabla = self.tabla_var.get()
        clase = tabla_clase_mapping[tabla]

        productos = session.query(clase).all()
        self.productos_tree.delete(*self.productos_tree.get_children())
        for producto in productos:
            if search_term in producto.producto.lower():
                self.productos_tree.insert('', 'end', values=(producto.producto, producto.precio))

    def agregar_al_carrito(self):
        selected_item = self.productos_tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un producto.")
            return

        producto_nombre, precio = self.productos_tree.item(selected_item)['values']
        cantidad = self.cantidad_var.get()
        descuento = self.descuento_var.get()

        if cantidad <= 0:
            messagebox.showerror("Error", "Ingresa una cantidad válida.")
            return

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

    def generar_presupuesto_excel(self):
        # Solicitar ubicación para guardar el archivo Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return

        # Cargar la plantilla de Excel
        wb = load_workbook('./data/PLANTILLA PRESUPUESTO.xlsx')
        sheet = wb.active

        # Obtener la fecha actual
        fecha_actual = datetime.date.today().strftime("%d-%m-%Y")

        # Rellenar los datos generales del presupuesto

        # Fecha
        sheet.cell(row=3, column=6, value=fecha_actual)



        # Rellenar la plantilla con los datos del presupuesto
        fila_inicial = 11  # Fila donde comienzan los productos en la plantilla
        for item in self.carrito:
            producto, cantidad, descuento, precio = item
            cantidad = int(cantidad)
            precio = float(precio)
            precio_total = cantidad * precio * (1 - descuento / 100)
            descuento = float(descuento) / 100

            # Escribir los datos en las celdas correspondientes
            sheet.cell(row=fila_inicial, column=2, value=cantidad)
            sheet.cell(row=fila_inicial, column=3, value=producto)
            sheet.cell(row=fila_inicial, column=4, value=precio).number_format = '$ 0,0.00'
            sheet.cell(row=fila_inicial, column=5, value=descuento).number_format = '0.0%'
            sheet.cell(row=fila_inicial, column=6, value=precio_total).number_format = '$ 0,0.00'
            fila_inicial += 1

        # Guardar el archivo Excel
        wb.save(file_path)
        messagebox.showinfo("Éxito", f"Presupuesto generado en {file_path}")

    def aumentar_precios(self):
        tabla = self.tabla_var.get()
        if not tabla:
            messagebox.showerror("Error", "Selecciona una lista.")
            return

        aumento = simpledialog.askfloat("Aumentar Precios", "Ingrese el porcentaje de aumento (por ejemplo, 10 para un 10%):")
        if aumento is None or aumento <= 0:
            messagebox.showerror("Error", "Ingrese un porcentaje de aumento válido.")
            return

        clase = tabla_clase_mapping[tabla]
        productos = session.query(clase).all()
        for producto in productos:
            producto.precio *= (1 + aumento / 100)
        session.commit()

        self.ultimo_aumento[tabla] = aumento
        self.update_productos(None)
        messagebox.showinfo("Éxito", f"Los precios de {tabla} han sido aumentados en un {aumento}%.")

if __name__ == "__main__":
    app = PresupuestoApp()
    app.mainloop()
