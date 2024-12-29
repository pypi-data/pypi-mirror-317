from datetime import date

from pydantic import BaseModel, Field, EmailStr, constr
from typing_extensions import Annotated, Optional

from Schemas_ses.enumeration.enums import SchoolKind, SchoolStatus
from Schemas_ses.models.model import AnnexeModel
from Schemas_ses.type.types import Year


class ReferenceYear(AnnexeModel):
    """Contient les informations de référence de l'année scolaire"""

    creation_year: Optional[Year]
    creation_reference: Optional[str]
    creation_year_reference_date: Optional[date]

    extension_year: Optional[Year]
    extension_reference: Optional[str]
    extension_year_reference_date: Optional[date]


class LocaPeda(BaseModel):
    """Se réfère à la section Localisation dans le Réseau d'Animation Pédagogique"""
    circonscription_scolaire: Optional[str]
    zone_pedagogique: Optional[Annotated[int, Field(strict=True, ge=1, le=6)]]
    unite_pedagogique: Optional[str]


class LocaTerritoire(BaseModel):
    """Se réfère à la section Localisation dans l'Administration Territorialee"""
    departement: Optional[str]
    commune: Optional[str]
    arrondissement: Optional[str]
    village: Optional[str]
    adresse: Optional[str]
    postal_code: Optional[str]
    telephone: Optional[list[str]]
    email: Optional[EmailStr]


class IdAndLocation(BaseModel):
    """Se réfère à la section Identification et localisation de l'école"""
    school_status: Optional[SchoolStatus]
    school_kind: Optional[SchoolKind]
    reference_year: ReferenceYear
    loca_peda: LocaPeda
    loca_territoire: LocaTerritoire
