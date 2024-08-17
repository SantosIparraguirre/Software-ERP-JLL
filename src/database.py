from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# Crear la base de datos
Base = declarative_base()

# Crear el motor de la base de datos SQLite
engine = create_engine('sqlite:///database.db')

# Crear una sesión
Session = sessionmaker(bind=engine)

# Variable de sesión para interactuar con la base de datos
session = Session()

# Crear la clase de la tabla de productos
class Productos(Base):
    __tablename__ = 'PRODUCTOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_categoria = Column(Integer, ForeignKey('CATEGORIAS.id'), nullable=False)
    codigo = Column(String)
    linea = Column(String)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    categoria = relationship('Categorias', back_populates='productos')

# Crear la clase de la tabla de categorías
class Categorias(Base):
    __tablename__ = 'CATEGORIAS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    productos = relationship('Productos', back_populates='categoria')

# Crear la clase de la tabla de clientes
class Clientes(Base):
    __tablename__ = 'CLIENTES'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    cuit = Column(String)
    telefono = Column(String)
    direccion = Column(String)
    presupuestos = relationship('Presupuestos', back_populates='cliente')
    remitos = relationship('Remitos', back_populates='cliente')
    acopios = relationship('Acopios', back_populates='cliente')

# Presupuestos
class Presupuestos(Base):
    __tablename__ = 'PRESUPUESTOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey ('CLIENTES.id'), nullable=False)
    fecha = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    cliente = relationship('Clientes', back_populates='presupuestos')
    detalles = relationship('DetallesPresupuestos', back_populates='presupuesto')

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
    presupuesto = relationship('Presupuestos', back_populates='detalles')

# Remitos
class Remitos(Base):
    __tablename__ = 'REMITOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey ('CLIENTES.id'), nullable=False)
    fecha = Column(DateTime, nullable=False)
    total = Column(Float, nullable=False)
    pago = Column(String, nullable=False)
    cliente = relationship('Clientes', back_populates='remitos')
    detalles = relationship('DetallesRemitos', back_populates='remito')

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
    remito = relationship('Remitos', back_populates='detalles')

# Acopios
class Acopios(Base):
    __tablename__ = 'ACOPIOS'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey('CLIENTES.id'), nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.datetime.now)
    fecha_modificacion = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    producto = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    cliente = relationship('Clientes', back_populates='acopios')


# Crear las tablas
Base.metadata.create_all(engine)