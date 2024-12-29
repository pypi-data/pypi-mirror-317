
from typing_extensions import Literal, Optional
from datetime import date

from Schemas_ses.enumeration.enums import StudiesLevel
from Schemas_ses.models.model import AnnexeModel
from Schemas_ses.type.types import Year, Sexe


class HighestDegree(AnnexeModel):
    academic: Optional[Literal["CEP", "BEPC", "BAC", "LICENCE", "MASTER"]]
    professional: Optional[Literal["CEAP", "CAP"]]


class Seniority(AnnexeModel):
    public: Optional[int]
    department: Optional[int]
    school: Optional[int]


class NumberOfVisit(AnnexeModel):
    inspector: Optional[int]
    director: Optional[int]
    cp: Optional[int]


class Personnel(AnnexeModel):
    matricule: str
    name: str
    surname: str
    sexe: Sexe
    birth_year: Optional[Year]
    highest_degree: HighestDegree
    grade: Optional[str]
    statut: Optional[Literal["ACPDE", "ACE", "AME", "Communautaire", "Fonctionnaire de l'état", "Privé", "Autre"]]
    fonction: Optional[Literal["Directeur", "Adjoint", "Enseignant"]]
    real_indice: Optional[int]
    teached_subjects: Optional[list[StudiesLevel]]
    seniority: Seniority
    last_formation_date: Optional[date]
    number_of_visit: NumberOfVisit
    up_participation: Optional[int]


class TeachingStaff(AnnexeModel):
    personnel: Optional[list[Personnel]]
