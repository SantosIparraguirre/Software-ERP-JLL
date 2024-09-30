# Software de gestión integral

## Descripción
Este proyecto es una aplicación de escritorio desarrollada en Python utilizando Tkinter para la interfaz gráfica y SQLAlchemy para la gestión de la base de datos. La aplicación está diseñada para una empresa de materiales de construcción y permite generar y guardar presupuestos, remitos, facturas y administrar clientes.

## Características
- **Interfaz intuitiva y amigable**: El diseño está pensado para facilitar el uso por parte de empleados de la empresa, con herramientas visuales claras y de fácil acceso.
- **Facilidad de expansión**: Estructura modular que permite agregar nuevas funcionalidades sin afectar el núcleo de la aplicación.
- **Listas de productos**: Seleccionar una línea de productos/proveedores para buscar sus productos.
- **Aumento de precios**: Permite aumentar los precios de los productos o la lista seleccionada, por el porcentaje ingresado.
- **Gestión de Carrito**: Añadir, eliminar, editar y visualizar productos en un carrito de compras.
- **Generación de Presupuestos y Remitos**: Facilita la creación de presupuestos y remitos, su almacenamiento en la base de datos, exportación a Excel e impresión.
- **Búsqueda y Filtros**: Búsqueda de productos por nombre, código o línea.
- **Productos Fuera de Lista**: Posibilidad de agregar productos que no están en la lista principal.
- **Lista de clientes**: Añadir, modificar y eliminar clientes.
- **Visualización de Presupuestos y Remitos**: Visualizar cada documento y sus detalles a través de la interfaz del cliente.
- **Sistema de deudas**: Capturar todos los remitos no pagos, calcular la deuda total, actualizar los precios de los productos, cancelar deuda parcial/total.
- **Sistema de acopios**: Agregar producto al acopio del cliente, descontar productos del mismo a través de un remito, generar un remito de deuda automáticamente si se excede la cantidad / retira un producto que no está en acopio.
- **Copia de seguridad**: Proceso automatizado para realizar un backup diario de la DB y subirlo a la nube.

## Librerias principales
- Tkinter
- SQLAlchemy
- Openpyxl
- ReportLab
- Pandas
- Pywin32

## Estructura del Proyecto
- `src/`: Contiene el código fuente de la aplicación.
- `src/utils/`: Contiene utilidades y funciones auxiliares.
- `src/icons/`: Contiene imágenes e íconos para la aplicación.

## Contacto

Si deseas colaborar con el proyecto, aportar dudas o sugerencias, puedes contactarme:

[LinkedIn](https://www.linkedin.com/in/santos-iparraguirre-b738a82b3/)

E-Mail: santosiparraguirrem@gmail.com