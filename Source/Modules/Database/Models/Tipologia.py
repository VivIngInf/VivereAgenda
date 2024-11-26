from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Double, Boolean, Date
from sqlalchemy.orm import sessionmaker
from ..Models.Base import Base
from datetime import date

class Tipologia(Base):
    __tablename__ = "Tipologia"

    ID_Tipologia = Column("ID_Tipologia", Integer, primary_key=True, nullable=False, autoincrement=True)
    nome = Column("Nome", String, nullable=False)
    
    def __init__(self, ID_Tipologia : int, nome : String):
        self.ID_Tipologia = ID_Tipologia
        self.nome = nome

    def __repr__(self):
        return f"{self.ID_Tipologia} {self.nome}"