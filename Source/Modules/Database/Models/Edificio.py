from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Double, Boolean, Date
from sqlalchemy.orm import sessionmaker
from ..Models.Base import Base
from datetime import date

class Edificio(Base):
    __tablename__ = "Edificio"

    Num_Edificio = Column("Num_Edificio", Integer, primary_key=True, nullable=False)
    comune = Column("Comune", String, nullable=False)
    can_Ask = Column("Can_Ask", Boolean, nullable=False, default=False)
    
    def __init__(self, Num_Edificio : int, comune : String, can_Ask : bool):
        self.Num_Edificio = Num_Edificio
        self.comune = comune
        self.can_Ask = can_Ask

    def __repr__(self):
        return f"{self.Num_Edificio} {self.comune} {self.can_Ask}"