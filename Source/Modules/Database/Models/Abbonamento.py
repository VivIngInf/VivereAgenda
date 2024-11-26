from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Double, Boolean, Date
from sqlalchemy.orm import sessionmaker
from ..Models.Base import Base
from datetime import date

class Abbonamento(Base):
    __tablename__ = "Abbonamento"

    ID_Abbonamento = Column("ID_Abbonamento", Integer, nullable=False, autoincrement=True, primary_key=True)
    ID_Telegram = Column("ID_Telegram", CHAR(9), ForeignKey("Utente.ID_Telegram"), nullable=False)
    ID_Tipologia = Column("ID_Tipologia", Integer, ForeignKey("Tipologia.ID_Tipologia"), nullable=False)
    
    def __init__(self, ID_Telegram : String, ID_Tipologia : int):
        self.ID_Telegram = ID_Telegram
        self.ID_Tipologia = ID_Tipologia

    def __repr__(self):
        return f"{self.ID_Telegram} {self.ID_Tipologia}"