from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear la base de datos
Base = declarative_base()

# Crear el motor de la base de datos SQLite
engine = create_engine('sqlite:///productos.db')

# Crear una sesión
Session = sessionmaker(bind=engine)

# Variable de sesión para interactuar con la base de datos
session = Session()

# Tablas de la base de datos

# Clientes
class Clientes(Base):
    __tablename__ = 'CLIENTES'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    cuit = Column(String, nullable=False)

# Presupuestos
class Presupuestos(Base):
    __tablename__ = 'PRESUPUESTOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey ('CLIENTES.id'), nullable=False)
    fecha = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    cliente = relationship('Clientes')

# Detalles de presupuestos
class DetallesPresupuestos(Base):
    __tablename__ = 'DETALLES_PRESUPUESTOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_presupuesto = Column(Integer, ForeignKey ('PRESUPUESTOS.id'), nullable=False)
    producto = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    descuento = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    presupuesto = relationship('Presupuestos')

# Remitos
class Remitos(Base):
    __tablename__ = 'REMITOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey ('CLIENTES.id'), nullable=False)
    fecha = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    cliente = relationship('Clientes')

# Detalles de remitos
class DetallesRemitos(Base):
    __tablename__ = 'DETALLES_REMITOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_remito = Column(Integer, ForeignKey ('REMITOS.id'), nullable=False)
    producto = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    descuento = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    remito = relationship('Remitos')

class Vasser(Base):
    __tablename__ = 'VASSER'
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String, nullable=False)
    linea = Column(String, nullable=False)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Capea(Base):
    __tablename__ = 'CAPEA'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Polietileno(Base):
    __tablename__ = 'POLIETILENO'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Peirano(Base):
    __tablename__ = 'PEIRANO'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Latyn(Base):
    __tablename__ = 'LATYN'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Fusiogas(Base):
    __tablename__ = 'FUSIOGAS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Chicote(Base):
    __tablename__ = 'CHICOTE'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class H3(Base):
    __tablename__ = 'H3'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class CañosPVC(Base):
    __tablename__ = 'CAÑOS PVC'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class PiezasPVC(Base):
    __tablename__ = 'PIEZAS PVC Y LOSUNG'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Sigas(Base):
    __tablename__ = 'SIGAS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class PPRosca(Base):
    __tablename__ = 'PP ROSCA'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Awaduck(Base):
    __tablename__ = 'AWADUCK'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Amancofusion(Base):
    __tablename__ = 'AMANCO FUSION'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Rotoplas(Base):
    __tablename__ = 'ROTOPLAS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

# Crear las tablas
Base.metadata.create_all(engine)
