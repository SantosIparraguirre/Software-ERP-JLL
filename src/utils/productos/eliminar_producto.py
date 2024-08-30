from tkinter import messagebox
from database import session, Productos

# Función para eliminar productos de la base de datos
def eliminar_producto(self):
    # Obtener el producto seleccionado
    seleccion = self.productos_treeview.selection()
    
    # Si no se selecciona un producto, mostrar un mensaje de error
    if not seleccion:
        messagebox.showerror("Error", "Selecciona un producto.")
        return
    
    # Obtener el ID del producto seleccionado
    ID = self.productos_treeview.item(seleccion)['values'][4]

    # Obtener el nombre del producto seleccionado
    producto = self.productos_treeview.item(seleccion)['values'][2]
    
    # Mostrar un mensaje de confirmación antes de eliminar el producto
    confirmacion = messagebox.askyesno("Confirmar", f"¿Estás seguro de eliminar '{producto}' de la lista?")
    if not confirmacion:
        return
    
    # Eliminar el producto de la base de datos
    session.query(Productos).filter_by(id=ID).delete()

    # Confirmar los cambios en la base de datos
    session.commit()
    
    # Actualizar la tabla de productos
    self.update_productos()