from datetime import datetime, timedelta
import random
from tqdm import tqdm

# Importa tus modelos
from database import Remitos, DetallesRemitos, Clientes, session

# Función para generar un remito aleatorio
def generar_remito(cliente_id):
    fecha = datetime.now() - timedelta(days=random.randint(1, 365))
    fecha_pago = fecha + timedelta(days=random.randint(1, 30))
    total = round(random.uniform(100, 1000), 2)
    metodos_pago = ['SI', 'NO']
    
    return Remitos(
        id_cliente=cliente_id,
        fecha=fecha,
        fecha_pago=fecha_pago,
        total=total,
        pago=random.choice(metodos_pago)
    )

# Función para generar detalles de remito aleatorios
def generar_detalles_remito():
    productos = ['Producto A', 'Producto B', 'Producto C', 'Producto D']
    cantidad = random.randint(1, 10)
    precio_unitario = round(random.uniform(10, 100), 2)
    descuento = round(random.uniform(0, 10), 2)
    total = round((cantidad * precio_unitario) - descuento, 2)
    
    return DetallesRemitos(
        producto=random.choice(productos),
        cantidad=cantidad,
        precio_unitario=precio_unitario,
        descuento=descuento,
        total=total
    )

# Obtener todos los IDs de clientes
cliente_ids = [id[0] for id in session.query(Clientes.id).all()]

# Generar 25.000 remitos
num_remitos = 25000
batch_size = 1000

for i in tqdm(range(0, num_remitos, batch_size), desc="Generando remitos"):
    for _ in range(batch_size):
        nuevo_remito = generar_remito(random.choice(cliente_ids))
        session.add(nuevo_remito)
        session.flush()  # Esto asigna un ID al remito
        
        # Generar entre 1 y 5 detalles por remito
        for _ in range(random.randint(1, 5)):
            detalle = generar_detalles_remito()
            detalle.id_remito = nuevo_remito.id
            session.add(detalle)
    
    # Commit cada lote
    session.commit()

print(f"Se han creado {num_remitos} remitos con sus respectivos detalles.")

# Cerrar la sesión
session.close()