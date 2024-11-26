from mysql.connector import cursor, connect, MySQLConnection

from .Session import session
from sqlalchemy import select, func, distinct, literal
from sqlalchemy.orm import aliased, load_only
from sqlalchemy.sql import exists
from ..Database.Models.Utente import Utente
from ..Database.Models.Tipologia import Tipologia
from ..Database.Models.Evento import Evento
from ..Database.Models.Edificio import Edificio
from ..Database.Models.Aula import Aula
from ..Database.Models.Abbonamento import Abbonamento

import datetime
from os import environ

from datetime import date, datetime, time

def InsertUser(idTelegram : str, username : str, email : str, isAdmin : bool, isVerified : bool):

    utente = Utente(
        ID_Telegram=idTelegram,
        username=username,
        email=email,
        isAdmin=isAdmin,
        isVerified=isVerified
    )
    
    session.add(utente)
    session.commit()
    
def CheckUserExists(idTelegram : str) -> bool:
    query = session.query(Utente).filter(Utente.ID_Telegram == f"{idTelegram}")
    exists = session.query(query.exists()).scalar()

    return bool(exists)

def SetIsVerifiedUser(idTelegram : str, isVerified : bool):
    if not CheckUserExists(idTelegram=idTelegram):
        return

    user: Utente = session.query(Utente).filter(Utente.ID_Telegram == f"{idTelegram}").one()
    user.isVerified = isVerified

    session.commit()

# ----

def InsertEdificio(numEdificio : int, comune : str):

    edificio = Edificio(
        Num_Edificio = numEdificio,
        comune = comune
    )
    
    session.add(edificio)
    session.commit()

# ----

def InsertAula(idAula : str, numEdificio : int, numPosti : int, hasLavagna : bool, hasProiettore : bool):
    
    aula = Aula(
        ID_Aula=idAula,
        num_Edificio=numEdificio,
        num_Posti=numPosti,
        has_Lavagna=hasLavagna,
        has_Proiettore=hasProiettore
    )

    session.add(aula)
    session.commit()

# ----

def InsertTipologia(idTipologia : int, nome : str):

    tipologia = Tipologia(
        ID_Tipologia = idTipologia,
        nome = nome
    )

    session.add(tipologia)
    session.commit(tipologia)

# ----

def InsertAbbonamento(idTelegram : str, idTipologia : int):

    abbonamento = Abbonamento(
        ID_Telegram=idTelegram,
        ID_Tipologia=idTipologia
    )

    session.add(abbonamento)
    session.commit()

# ----

def InsertEvento(idEvento : int, nome : str, giorno : date, orarioInizio : time, orarioFine : time, idMsg : int, isVerified : bool):

    evento = Evento(
        ID_Evento=idEvento,
        nome=nome,
        giorno=giorno,
        orario_Inizio=orarioInizio,
        orario_Fine=orarioFine,
        ID_Msg=idMsg,
        is_Verified=isVerified
    )

    session.add(evento)
    session.commit(evento)

def CheckEventExists(idEvento : int) -> bool:
    query = session.query(Evento).filter(Evento.ID_Evento == f"{idEvento}")
    exists = session.query(query.exists()).scalar()

    return bool(exists)

def SetIsVerifiedEvent(idEvento : int, isVerified : bool):
    if not CheckEventExists(idEvento=idEvento):
        return

    user: Evento = session.query(Evento).filter(Evento.ID_Evento == f"{idEvento}").one()
    user.isVerified = isVerified

    session.commit()