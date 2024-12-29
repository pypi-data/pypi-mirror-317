from pydantic import BaseModel
from typing_extensions import Literal, Optional

from Schemas_ses.enumeration.enums import StudiesLevel
from Schemas_ses.models.model import AnnexeModel

Age = Literal[
    "Moins de 5 ans",
    "5 ans",
    "6 ans",
    "7 ans",
    "8 ans",
    "9 ans",
    "10 ans",
    "11 ans",
    "12 ans",
    "13 ans",
    "14 ans",
    "15 ans",
    "16 ans et plus"
]
Redoublant = Literal[
    "Total des redoublants",
    "Redoublants ayant 6 ans",
    "Redoublants ayant 11 ans",
]
Handicape = Literal[
    "Handicapés Moteur",
    "Handicapés Sensoriel",
    "Handicapés Psychique",
    "Handicapés Mental",
    "Handicapés Maladies Invalidantes"
]
ParticularCase = Literal[
    "Étrangers",
    "Orphelins ou enfants vulnérables",
    "Orphelins",
    "Élèves sans acte de naissance",
    "Nouveaux élèves venus d'une autre école",
    "Cas de grossesse",
    "Cas de mariage précoce",
    "Cas de viol",
    "Abandon pour cause d'abus sexuel"
]


class EffectifBySex(BaseModel):
    boys: Optional[int]
    girls: Optional[int]


class StudentEnrollmentByAge(AnnexeModel):
    years: dict[Age, EffectifBySex]


class RepeatersByAge(AnnexeModel):
    status: dict[Redoublant, EffectifBySex]


class DisabledByAge(AnnexeModel):
    kind: dict[Handicape, EffectifBySex]


class ParticularSituationByAge(AnnexeModel):
    situation: dict[ParticularCase, EffectifBySex]


class StudentsRecord(AnnexeModel):
    """
    """
    student_enrollment_by_age: dict[StudiesLevel, StudentEnrollmentByAge]
    repeaters_by_age: dict[StudiesLevel, RepeatersByAge]
    disabled_by_age: dict[StudiesLevel, DisabledByAge]
    particular_situation_by_age: dict[StudiesLevel, ParticularSituationByAge]
