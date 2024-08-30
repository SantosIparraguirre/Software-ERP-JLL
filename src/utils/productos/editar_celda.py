import tkinter as tk
from tkinter import messagebox
from database import session, Productos

def editar_celda(self, event):
    # Obtener la posición del clic y el ítem correspondiente
    row_id = self.productos_treeview.identify_row(event.y)
    column_id = self.productos_treeview.identify_column(event.x)

    if not row_id or not column_id:
        return

    # Obtener valores actuales
    item = self.productos_treeview.item(row_id)['values']
    column = int(column_id[1:]) - 1

    # Crear un Entry temporal
    x, y, width, height = self.productos_treeview.bbox(row_id, column_id)
    entry = tk.Entry(self.productos_treeview)
    entry.place(x=x, y=y, width=width, height=height)
    entry.insert(0, item[column])
    entry.focus()

    def guardar_edicion(event=None):
        # Obtener los valores actuales
        values = list(self.productos_treeview.item(row_id, "values"))

        # Obtener el ID del producto seleccionado
        ID = values[4]

        # Obtener el nuevo valor del entry
        new_value = entry.get()

        # Actualizar solo la columna seleccionada
        values[column] = new_value

        # Obtener el producto de la base de datos
        producto = session.query(Productos).filter_by(id=ID).first()

        # Actualizar el producto con los nuevos valores
        if column == 0:
            # Si el código es None, no actualizarlo
            if new_value == 'None':
                entry.place_forget()
                return
            producto.codigo = new_value
        elif column == 1:
            producto.linea = new_value
        elif column == 2:
            producto.nombre = new_value
        elif column == 3:
            # Si el precio contiene comas, eliminarlas
            new_value = new_value.replace(",", "")
            # Si el precio contiene un signo de dólar, eliminarlo
            if new_value.startswith('$'):
                new_value = new_value[1:]
            producto.precio = float(new_value)
        
        # Confirmar los cambios en la base de datos
        session.commit()

        # Actualizar el treeview con los nuevos valores
        self.productos_treeview.item(row_id, values=values)

        # Ocultar el entry después de guardar la edición
        entry.place_forget()

    entry.bind('<Return>', guardar_edicion)
    entry.bind('<FocusOut>', lambda event: entry.destroy())