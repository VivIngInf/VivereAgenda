from Modules.Database.Models.Utente import Utente
from Modules.Database.Models.Tipologia import Tipologia
from Modules.Database.Models.Evento import Evento
from Modules.Database.Models.Edificio import Edificio
from Modules.Database.Models.Aula import Aula
from Modules.Database.Models.Abbonamento import Abbonamento
from Modules.Database.Models.Base import Base
from Modules.Database.Connect import engine

# Siccome tutti i modelli generano da Base,
# possiamo invocare la generazione di base
# e tutti i modelli verranno generati
def CreateAll():
    Base.metadata.create_all(bind=engine)