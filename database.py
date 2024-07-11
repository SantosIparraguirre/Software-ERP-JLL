from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
engine = create_engine('sqlite:///mi_empresa.db')
Session = sessionmaker(bind=engine)
session = Session()

class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)

class Factura(Base):
    __tablename__ = 'facturas'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    cliente = Column(String, nullable=False)
    total = Column(Float, nullable=False)
    productos = relationship("FacturaProducto", back_populates="factura")

class FacturaProducto(Base):
    __tablename__ = 'factura_productos'
    id = Column(Integer, primary_key=True)
    factura_id = Column(Integer, ForeignKey('facturas.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    factura = relationship("Factura", back_populates="productos")
    producto = relationship("Producto")

class Remito(Base):
    __tablename__ = 'remitos'
    id = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    cliente = Column(String, nullable=False)
    productos = relationship("RemitoProducto", back_populates="remito")

class RemitoProducto(Base):
    __tablename__ = 'remito_productos'
    id = Column(Integer, primary_key=True)
    remito_id = Column(Integer, ForeignKey('remitos.id'))
    producto_id = Column(Integer, ForeignKey('productos.id'))
    cantidad = Column(Integer, nullable=False)
    remito = relationship("Remito", back_populates="productos")
    producto = relationship("Producto")


# Crear las tablas
Base.metadata.create_all(engine)
