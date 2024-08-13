import pandas as pd
from database_v2 import Productos, Categorias, session

# Ruta del archivo Excel
file_path = 'productos.xlsx'

# Diccionario para mapear nombres de hojas a IDs de categoría
sheet_category_mapping = {
    'CAPEA': 'Capea',
    'POLIETILENO': 'Polietileno',
    'PEIRANO': 'Peirano',
    'LATYN': 'Latyn',
    'FUSIOGAS': 'Fusiogas',
    'CHICOTE': 'Chicote',
    'H3': 'H3',
    'CAÑOS PVC': 'Caños PVC',
    'PIEZAS PVC Y LOSUNG': 'Piezas PVC y Losung',
    'SIGAS': 'Sigas',
    'PP ROSCA': 'PP Rosca',
    'AWADUCK': 'Awaduck',
    'AMANCO FUSION': 'Amanco Fusion',
    'ROTOPLAS': 'Rotoplas',
    'VASSER': 'Vasser'
}

# Crear categorías si no existen
for category_name in sheet_category_mapping.values():
    categoria = session.query(Categorias).filter_by(nombre=category_name).first()
    if not categoria:
        nueva_categoria = Categorias(nombre=category_name)
        session.add(nueva_categoria)
session.commit()

# Cargar y poblar datos desde cada hoja del Excel
for sheet_name, category_name in sheet_category_mapping.items():
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    categoria = session.query(Categorias).filter_by(nombre=category_name).first()
    
    for _, row in df.iterrows():
        if sheet_name == 'VASSER':
            producto = Productos(
                codigo=row.get('Codigo', ''),
                linea=row.get('Linea', ''),
                nombre=row['Descripcion'],
                precio=row['Precio'],
                id_categoria=categoria.id
            )
        else:
            producto = Productos(
                nombre=row['PRODUCTO'],
                precio=row['PRECIO'],
                id_categoria=categoria.id
            )
        session.add(producto)

# Confirmar la transacción
session.commit()

# Cerrar la sesión
session.close()