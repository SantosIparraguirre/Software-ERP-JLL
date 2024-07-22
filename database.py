from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///productos.db')
Session = sessionmaker(bind=engine)
session = Session()

class Capea(Base):
    __tablename__ = 'capea'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Polietileno(Base):
    __tablename__ = 'polietileno'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Peirano(Base):
    __tablename__ = 'peirano'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Latyn(Base):
    __tablename__ = 'latyn'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Fusiogas(Base):
    __tablename__ = 'fusiogas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Chicote(Base):
    __tablename__ = 'chicote'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class H3(Base):
    __tablename__ = 'h3'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Caños(Base):
    __tablename__ = 'caños'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class PiezasPVC(Base):
    __tablename__ = 'piezas pvc y losung'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Sigas(Base):
    __tablename__ = 'sigas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class PPRosca(Base):
    __tablename__ = 'pprosca'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Awaduck(Base):
    __tablename__ = 'awaduck'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Amancofusion(Base):
    __tablename__ = 'amanco fusion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

class Rotoplas(Base):
    __tablename__ = 'rotoplas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    producto = Column(String, nullable=False)
    precio = Column(Float, nullable=False)

# Crear las tablas
Base.metadata.create_all(engine)
