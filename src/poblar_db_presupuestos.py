import pandas as pd

# Importar las clases de los modelos
from database import session, Vasser, Capea, Polietileno, Peirano, Latyn, Fusiogas, Chicote, H3, CañosPVC, PiezasPVC, Sigas, PPRosca, Awaduck, Amancofusion, Rotoplas

# Ruta del archivo Excel
file_path = 'productos.xlsx'

# Diccionario para mapear nombres de hojas a clases (tablas)
sheet_class_mapping = {
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

# Cargar y poblar datos desde cada hoja del Excel
for sheet_name, cls in sheet_class_mapping.items():
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    for _, row in df.iterrows():
        producto = cls(producto=row['PRODUCTO'], precio=row['PRECIO'])
        session.add(producto)

# Cargar los datos de vasser
df = pd.read_excel(file_path, sheet_name='VASSER')
for _, row in df.iterrows():
    producto = Vasser(codigo=row['Codigo'], linea=row['Linea'], producto=row['Descripcion'], precio=row['Precio'])
    session.add(producto)

# Confirmar la transacción
session.commit()

# Cerrar la sesión
session.close()