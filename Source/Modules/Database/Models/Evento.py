from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Double, Boolean, Date, Time
from sqlalchemy.orm import sessionmaker
from ..Models.Base import Base
from datetime import date

class Evento(Base):
    __tablename__ = "Evento"

    ID_Evento = Column("ID_Evento", Integer, primary_key=True, nullable=False, autoincrement=True)

    nome = Column("Nome", String, default=None, nullable=False)
    giorno = Column("Hiorno", Date, default=None, nullable=False)
    orario_Inizio = Column("Orario_Inizio", Time, default=None, nullable=False) 
    orario_Fine = Column("Orario_Fine", Time, default=None, nullable=False) 
    ID_Msg = Column("ID_Msg", Integer, default=None, nullable=False)
    is_Verified = Column("Is_Verified", Boolean, default=False, nullable=True)
    

    ref_Aula = Column("Ref_Aula", CHAR(20), ForeignKey("Aula.ID_Aula"), nullable=False)
    ref_Tipologia = Column("Ref_Tipologia", Integer, ForeignKey("Tipologia.ID_Tipologia"), nullable=False)


    def __init__(self, ID_Evento : int, nome : String, giorno : Date, orario_Inizio : Time, orario_Fine : Time, ID_Msg : int, is_Verified : bool):
        self.ID_Evento = ID_Evento
        self.nome = nome
        self.giorno = giorno
        self.orario_Inizio = orario_Inizio
        self.orario_Fine = orario_Fine
        self.ID_Msg = ID_Msg
        self.is_Verified = is_Verified

    def __repr__(self):
        return f"{self.ID_Evento} {self.nome} {self.giorno} {self.orario_Inizio} {self.orario_Fine} {self.ID_Msg} {self.is_Verified}"