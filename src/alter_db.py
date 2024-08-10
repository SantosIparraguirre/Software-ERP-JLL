from database import engine
from sqlalchemy.sql import text

# Conectar a la base de datos y ejecutar la sentencia SQL para agregar la columna
with engine.connect() as connection:
    # Truncar la tabla clientes, es decir, borrar todos los registros con la sentencia truncate table
    connection.execute(text('DELETE FROM CLIENTES'))
    connection.commit()