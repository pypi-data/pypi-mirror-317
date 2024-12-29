from enum import Enum


class SchoolStatus(str, Enum):
    Public = 'Public'
    Prive_LAIC = 'Privé Laïc'
    Prive_CONFESSIONNEL = 'Privé confessionnel'
    Communautaire = 'Communautaire'


class RegionPedagogique(str, Enum):
    RP29 = "RP29"
    RP28 = "RP28"
    RP60 = "RP60"
    RP61 = "RP61"


class TypePollution(str, Enum):
    SONORE = "Sonore"
    ATMOSPHERIQUE = "Atmosphérique"


class SourceEau(str, Enum):
    EAU_COURANTE = "Eau courante"
    PUITS = "Puits"
    FORAGE = "Forage"
    CITERNE = "Citerne"


class SourceElectricity(str, Enum):
    SBEE = "SBEE"
    SOLAIRE = "Solaire"


class SchoolPropertyTitle(str, Enum):
    TITRE_FONCIER = "Titre foncier"
    ACTE_DE_DONATION = "Acte de donation"
    ACTE_AUTORITE_TERRITORIALE = "Acte de l'autorité chargée de l'administration territoriale"
    CONTRAT_LOCATION = "Contrat de location entre l'école et un propriétaire"


class StudiesLevel(str, Enum):
    CI = "CI"
    CP = "CP"
    CE1 = "CE1"
    CE2 = "CE2"
    CM1 = "CM1"
    CM2 = "CM2"


class LocalType(str, Enum):
    SALLE = "Salle"
    BUREAU = "Bureau"
    MAGASIN = "Magasin"
    LATRINE = "Latrine"
    CUISINE = "Cuisine"
    BIBLIOTHEQUE = "Bibliothèque"
    LOGEMENT = "Logement"
    SALLE_INFORMATIQUE = "Salle informatique"


class Distance(str, Enum):
    MOINS_DE_500_METRES = "<=0.5"
    ENTRE_500_METRES_ET_1_KM = "Entre 0.5 et 1km"
    ENTRE_1_ET_3_KM = "Entre 1 et 3km"
    PLUS_DE_3_KM = ">=3"


class SchoolKind(str, Enum):
    Classique = 'Classique'
    Inclusif = 'Inclusif'
    Specialise = 'Spécialisé'
    Autres = 'Autres'
