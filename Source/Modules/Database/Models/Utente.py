from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Double, Boolean, Date
from sqlalchemy.orm import sessionmaker
from ..Models.Base import Base
from datetime import date

class Utente(Base):
    __tablename__ = "Utente"

    ID_Telegram = Column("ID_Telegram", CHAR(9), primary_key=True, nullable=False)
    username = Column("Username", String, nullable=False)
    email = Column("Email", String, nullable=False)
    is_Admin = Column("Is_Admin", Boolean, default=False, nullable=True)
    is_Verified = Column("Is_Verified", Boolean, default=False, nullable=True)
    
    def __init__(self, ID_Telegram : str, username : str, email : str, isAdmin : bool, isVerified : bool):
        self.ID_Telegram = ID_Telegram
        self.username = username
        self.email = email
        self.isAdmin = isAdmin
        self.isVerified = isVerified

    def __repr__(self):
        return f"{self.ID_Telegram} {self.username} {self.email} {self.isAdmin} {self.isVerified}"