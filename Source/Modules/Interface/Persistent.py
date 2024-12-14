from Modules.Database.Models.Utente import Utente
from Modules.Shared.Session import session
from Modules.Database.Connect import engine

from datetime import date

def CreatePersistent():

    # region Utente

    daniele = Utente(
        ID_Telegram="752154717",
        username="DanieleOrazio.Susino",
        email="danielino.susino@gg.it",
        isAdmin=True,
        isVerified=True,
    )

    andreaDePasquale = Utente(
        ID_Telegram="154366501",
        username="Andrea.Depasquale",
        email="andri.depis@vi.ing",
        isAdmin=True,
        isVerified=True,
    )

    session.add(daniele)
    session.add(andreaDePasquale)

    #endregion

    session.commit()