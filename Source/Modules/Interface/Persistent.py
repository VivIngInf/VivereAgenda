from Modules.Database.Models.Utente import Utente
from Modules.Shared.Session import session
from Modules.Database.Connect import engine

from datetime import date

def CreatePersistent():

    #region Utente

    #endregion

    session.commit()