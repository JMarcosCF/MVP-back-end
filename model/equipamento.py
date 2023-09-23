from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

class Equipamento(Base):
    __tablename__ = 'equipamento'

    id = Column("pk_equipamento", Integer, primary_key=True)
    modelo = Column(String(140), unique=True)
    fabricante = Column(String(100), unique=False)
    

    def __init__(self, modelo:str, fabricante:str):
        """

        Cria um equipamento

        Argumentos:
            modelo: modelo do equipamento
            fabricante: fabricante do equipamento
        """

        self.modelo = modelo
        self.fabricante = fabricante