from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Double, Boolean, Date
from sqlalchemy.orm import sessionmaker
from ..Models.Base import Base
from datetime import date

class Aula(Base):
    __tablename__ = "Aula"

    ID_Aula = Column("ID_Aula", CHAR(20), primary_key=True, nullable=False)
    
    num_Posti = Column("Num_Posti", Integer, default=0, nullable=False)
    has_Lavagna = Column("Has_Lavagna", Boolean, default=False, nullable=True)
    has_Proiettore = Column("Has_Proiettore", Boolean, default=False, nullable=True)

    Num_Edificio = Column("Num_Edificio", Integer, ForeignKey("Edificio.Num_Edificio"), nullable=False)


    def __init__(self, ID_Aula : String, num_Edificio : int, num_Posti : int, has_Lavagna : bool, has_Proiettore : bool):
        self.ID_Aula = ID_Aula
        self.num_Edificio = num_Edificio
        self.num_Posti = num_Posti
        self.has_Lavagna = has_Lavagna
        self.has_Proiettore = has_Proiettore

    def __repr__(self):
        return f"{self.ID_Aula} {self.num_Edificio} {self.num_Posti} {self.has_Lavagna} {self.has_Proiettore}"